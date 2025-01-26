import { ScrollView, Text, View, Image, StyleSheet } from "react-native";
import React, { useEffect, useState } from 'react';
import * as Location from 'expo-location';
import axios from "axios";

export default function Index() {
  const [weatherData, setWeatherData] = useState<any | null>(null);
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  async function getCurrentLocation() {
    try {
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
            console.log('Failed to fetch user location')
            return;
        }
        let coords = await Location.getCurrentPositionAsync({

        });
        setLocation(coords);
        console.log(location)
        return coords;
    }catch (e){
        console.log(e)
    }
  }

  const fetchData = async () => {

    //Fetch weather data with axios from backend
    try {
        let loc = await getCurrentLocation();
        const data = {
            lon: loc?.coords.longitude.toFixed(3),
            lat: loc?.coords.latitude.toFixed(3),
        };
        const endpoint = `http://143.198.31.74:8080/api/weather?lon=${data.lon}&lat=${data.lat}`
        console.log(endpoint)
        const response = await axios.get(endpoint);
        console.log(response.data)
        setWeatherData(response.data);
    } catch (error) {
      console.error('Error posting data:', error);
    }
      setIsRefreshing(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const onRefresh = () => {
    setIsRefreshing(true);
    fetchData();
  };

  return (
    <ScrollView>
      <View
        style={{
          flex: 1,
          flexDirection: 'column',
          justifyContent: "center",
          alignItems: "center",
          height: 200,
          padding: 50,
          margin: 50,
        }}
      >
      <Text style={styles.heavyText}>{weatherData?.weather[0].description}</Text>
      <View
        style={{
          flex: 1,
          flexDirection: 'row',
          justifyContent: "center",
          alignItems: "center",
          gap: 40,
        }}
      >
          {weatherData && <Text style={styles.heavyText}>{(weatherData?.main.temp).toFixed(2)}</Text>}
        <Image
          source={require('../../assets/images/icons8-cloud-50.png')}
          style={{
            height: 60,
            width: 60,
            tintColor: 'tomato'
          }}
        />
      </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  heavyText: {
    fontSize: 24,
    fontWeight: '800', // Makes the font heavier
  },
});