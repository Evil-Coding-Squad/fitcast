package server

import (
	"net/http"
)

const baseUrl = "/api/"

const WeatherEndpoint = baseUrl + "weather"
const AiEndpoint = baseUrl + "ai"

func GetServerMux() *http.ServeMux {
	mux := http.NewServeMux()

	// AI Handlers here
	mux.Handle(SegmentEndpoint, &SegmentHandler{})
	return mux
}
