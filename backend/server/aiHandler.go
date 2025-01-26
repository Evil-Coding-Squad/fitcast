package server

import (
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

const SegmentEndpoint = AiEndpoint + "/segment"

type SegmentHandler struct{}

type ImageFile struct {
	Name     string
	FullPath string
	MimeType string
	Bytes    []byte
}

var (
	_, b, _, _     = runtime.Caller(0)
	RootPath       = filepath.Join(filepath.Dir(b), "../")
	tempFolderPath = filepath.Join(RootPath, "/temp-files")
)

func (handler *SegmentHandler) handlePost(w http.ResponseWriter, r *http.Request) {
	// TODO: implement image processing
	//fmt.Println(r)

	// Limit the size of the image to 10 MB
	maxFileSize := int64(10 << 20) // 10 MB
	err := r.ParseMultipartForm(maxFileSize)
	if err != nil {
		http.Error(w, "Cannot upload images larger than 10 MB", http.StatusBadRequest)
		return
	}

	// Get the file from the form data
	file, header, err := r.FormFile("image")
	if err != nil {
		fmt.Println("Error reading file of 'image' form data. Reason: ", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Save file to server device
	sourceImg, err := saveFile(file, header)
	if err != nil {
		fmt.Println("Error saving file. Reason: ", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	sendNormalResponse := true
	// Process the image
	predictedLabel, err := processClothingImage(sourceImg)
	if err != nil {
		fmt.Println("Error processing the image. Reason: ", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		sendNormalResponse = false
	}

	outputImage, err := getFile(filepath.Join(tempFolderPath, "output_img.png"))
	if err != nil {
		fmt.Println("Error getting the output image. Reason: ", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		sendNormalResponse = false
	}

	if sendNormalResponse {
		w.Header().Set("Content-Type", "image/png")
		w.Header().Set("Content-Disposition", `inline; filename="output_img.png"`)
		w.Header().Set("Predicted-Label", predictedLabel)
		w.Write(outputImage.Bytes)
	}

	// Remove the temp files
	if removed := removeFile(sourceImg.FullPath); !removed {
		fmt.Println("Error removing the received image")
	}
	if removed := removeFile(outputImage.FullPath); !removed {
		fmt.Println("Error removing the output image")
	}
}

func processClothingImage(img ImageFile) (string, error) {
	// Run the machine learning model
	cmd := exec.Command("python3", "../ml/segmentation_and_classification.py", img.FullPath, "./output_img.png")
	cmd.Dir = tempFolderPath
	out, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("Error in getting stdout pipe. Reason: ", err)
		return "", err
	}
	if err := cmd.Start(); err != nil {
		fmt.Println("Error in starting the command. Reason: ", err)
		return "", err
	}
	outputBytes, err := io.ReadAll(out)
	if err != nil {
		fmt.Println("Error in reading the output bytes. Reason: ", err)
		return "", err
	}
	if err := cmd.Wait(); err != nil {
		fmt.Println("Error in waiting for the command to finish. Reason: ", err)
		return "", err
	}

	return string(outputBytes), nil
}

func getFile(filePath string) (ImageFile, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return ImageFile{}, err
	}
	defer file.Close()

	filebytes, err := io.ReadAll(file)
	if err != nil {
		return ImageFile{}, err
	}

	image := ImageFile{
		Name:     removeExtension(filePath),
		FullPath: filePath,
		MimeType: "image/png",
		Bytes:    filebytes,
	}
	return image, nil
}

func removeExtension(filePath string) string {
	return strings.TrimSuffix(filePath, filepath.Ext(filePath))
}

func saveFile(file multipart.File, header *multipart.FileHeader) (ImageFile, error) {
	defer file.Close()

	tempFileName := fmt.Sprintf("uploaded-%s-*%s", removeExtension(header.Filename), filepath.Ext(header.Filename))

	tempFile, err := os.CreateTemp(tempFolderPath, tempFileName)
	if err != nil {
		fmt.Println("Error in creating the file. Reason: ", err)
		return ImageFile{}, err
	}

	defer tempFile.Close()

	filebytes, err := io.ReadAll(file)
	if err != nil {
		fmt.Println("Error in reading the file buffer. Reason: ", err)
		return ImageFile{}, err
	}

	tempFile.Write(filebytes)

	_, tFilename := filepath.Split(tempFile.Name())

	imgFile := ImageFile{
		Name:     tFilename,
		FullPath: tempFile.Name(),
		MimeType: header.Header.Get("Content-Type"),
		Bytes:    filebytes,
	}

	return imgFile, nil
}

func removeFile(path string) bool {
	//fmt.Print("Removing file: ", path)
	err := os.Remove(path)
	if err != nil {
		fmt.Println("\nCannot remove file. Reason: ", err)
		return false
	}
	return true
}

func (handler *SegmentHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		fmt.Printf("POST called on %s\n", r.URL.Path)
		handler.handlePost(w, r)
	}
}
