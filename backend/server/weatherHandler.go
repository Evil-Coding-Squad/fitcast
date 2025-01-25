package server

import (
	"fmt"
	"net/http"
)

type WeatherHandler struct{}

func (handler *WeatherHandler) getWeatherHandler(w http.ResponseWriter, r *http.Request) {
	// TODO: Make the actual API call to get the real weather info
	query := r.URL.Query()
	lon, lat := query.Get("lon"), query.Get("lat")
	_, err := fmt.Fprintf(w, "lon: %s, lat: %s\n", lon, lat)
	if err != nil {
		fmt.Println(err.Error())
	}
}

func (handler *WeatherHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		fmt.Printf("GET called on %s\n", r.URL.Path)
		handler.getWeatherHandler(w, r)
	}
}
