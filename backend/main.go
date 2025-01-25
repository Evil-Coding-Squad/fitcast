package main

import (
	"fitcast/server"
	"fmt"
	"github.com/joho/godotenv"
	"log"
	"net/http"
)

const port = ":8080"

func main() {
	fmt.Println("Starting server...")
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	mux := server.GetServerMux()
	fmt.Printf("Server listening on %s\n", port)
	err = http.ListenAndServe(port, mux)
	if err != nil {
		log.Fatal(err)
	}
}
