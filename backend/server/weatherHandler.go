package server

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
)

const weather_api_url = "https://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s"

func parseLonAndLat(lonStr string, latStr string) (float64, float64, error) {
	lon, err := strconv.ParseFloat(lonStr, 64)
	if err != nil {
		return 0, 0, err
	}

	lat, err := strconv.ParseFloat(latStr, 64)
	if err != nil {
		return 0, 0, err
	}

	return lon, lat, nil
}

type WeatherHandler struct{}

func (handler *WeatherHandler) getWeatherHandler(w http.ResponseWriter, r *http.Request) {
	// TODO: Make the actual API call to get the real weather info
	query := r.URL.Query()
	lonQuery, latQuery := query.Get("lon"), query.Get("lat")

	lon, lat, err := parseLonAndLat(lonQuery, latQuery)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		_, _ = fmt.Fprintln(w, "Error parsing longitude and/or latitude. Please check your query parameters.")
		return
	}

	apiKey := os.Getenv("WEATHER_API_KEY")
	res, err := http.Get(fmt.Sprintf(weather_api_url, lon, lat, apiKey))

	defer func() {
		if err := res.Body.Close(); err != nil {
			log.Println("error closing response body")
		}
	}()
	_, err = io.Copy(w, res.Body)
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
