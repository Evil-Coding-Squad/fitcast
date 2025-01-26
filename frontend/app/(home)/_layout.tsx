import { Tabs } from 'expo-router';
import { Image } from 'react-native';

export default function TabLayout() {
  return (
    <Tabs 
    screenOptions={{
        tabBarActiveTintColor: 'tomato', // Active tab icon color
        tabBarInactiveTintColor: 'gray', // Inactive tab icon color
        tabBarStyle: { height: 60 }, // Tab bar height for better spacing
      }}
      >
      <Tabs.Screen name="index" options={{
          title: 'Weather',
          headerShown: false,
          tabBarIcon: ({ color, size}) => (<Image 
            source={require('../../assets/images/icons8-cloud-50.png')}
            style={{
                width: size,
                height: size,
                tintColor: color, // Ensures the icon matches the color theme
              }}
          />) 
        }}/>
      <Tabs.Screen name="my_clothing" options={{
          title: 'Clothing',
          headerShown: false,
          tabBarIcon: ({ color, size}) => (<Image 
            source={require('../../assets/images/icons8-outfit-48.png')}
            style={{
                width: size,
                height: size,
                tintColor: color, // Ensures the icon matches the color theme
              }}
          />) 
        }}/>
      <Tabs.Screen name="settings" options={{
          title: 'Settings',
          headerShown: false,
          tabBarIcon: ({ color, size}) => (<Image 
            source={require('../../assets/images/icons8-settings-38.png')}
            style={{
                width: size,
                height: size,
                tintColor: color, // Ensures the icon matches the color theme
              }}
          />) 
        }}/>
    </Tabs>
  );
}