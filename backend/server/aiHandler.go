package server

import (
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
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

	// some processing here

	//removeFile(sourceImg.FullPath)

	w.Header().Set("Content-Type", sourceImg.MimeType)
	w.Header().Set("Content-Disposition", `inline; filename="`+removeExtension(sourceImg.Name)+`.jpg"`)
	w.Header().Set("Predicted-Label", "Hello")
	w.Write(sourceImg.Bytes)

	/* _, err = fmt.Fprintln(w, "Image processing not yet implemented")
	if err != nil {
		log.Fatal(err)
	} */
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
