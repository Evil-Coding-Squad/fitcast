package server

import (
	"net/http"
)

const baseUrl = "/api/"

const WeatherEndpoint = baseUrl + "weather/"

func GetServerMux() *http.ServeMux {
	mux := http.NewServeMux()
	return mux
}
