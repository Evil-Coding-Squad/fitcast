package server

import (
	"fmt"
	"log"
	"net/http"
)

const SegmentEndpoint = AiEndpoint + "/segment"

type SegmentHandler struct{}

func (handler *SegmentHandler) handlePost(w http.ResponseWriter, r *http.Request) {
	// TODO: implement image processing
	_, err := fmt.Fprintln(w, "Image processing not yet implemented")
	if err != nil {
		log.Fatal(err)
	}
}

func (handler *SegmentHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		fmt.Printf("POST called on %s\n", r.URL.Path)
		handler.handlePost(w, r)
	}
}
