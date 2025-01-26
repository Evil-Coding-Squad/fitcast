package server

import (
	"net/http"
)

const baseUrl = "/api/"

const WeatherEndpoint = baseUrl + "weather"
const AiEndpoint = baseUrl + "ai"

func enableCors(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		next.ServeHTTP(w, r)
	})
}

func GetServerMux() *http.ServeMux {
	mux := http.NewServeMux()

	// Weather Handlers here
	mux.Handle(WeatherEndpoint, enableCors(&WeatherHandler{}))
	// AI Handlers here
	mux.Handle(SegmentEndpoint, enableCors(&SegmentHandler{}))
	return mux
}
