import { ScrollView, Text, View, Image, StyleSheet } from "react-native";
import React, { useEffect, useState } from 'react';
import * as Location from 'expo-location';
import axios from "axios";

export default function Index() {
  const [weatherData, setWeatherData] = useState(null);
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  async function getCurrentLocation() {
      
    let { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      console.log('Failed to fetch user location')
      return;
    }

    let location = await Location.getCurrentPositionAsync({});
    setLocation(location);
    console.log(location)
  }

  const fetchData = async () => {
    await getCurrentLocation();
    //Fetch weather data with axios from backend
    try {
      const data = {
        longitude: location?.coords.longitude,
        latitude: location?.coords.latitude,
      };
  
      const response = await axios.get('https://localhost:8080/api/weather', {
        params: data
      }); 
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
      <Text style={styles.heavyText}>Day of Week</Text>
      <View
        style={{
          flex: 1,
          flexDirection: 'row',
          justifyContent: "center",
          alignItems: "center",
          gap: 40,
        }}
      >
        <Text style={styles.heavyText}>-15 C</Text>
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