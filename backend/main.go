package main

import (
	"fitcast/server"
	"fmt"
	"log"
	"net/http"
)

const port = ":8080"

func main() {
	fmt.Println("Starting server...")

	mux := server.GetServerMux()
	fmt.Printf("Server listening on %s\n", port)
	err := http.ListenAndServe(port, mux)
	if err != nil {
		log.Fatal(err)
	}
}
