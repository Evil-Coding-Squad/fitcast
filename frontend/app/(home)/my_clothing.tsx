import { ScrollView, Text, View, StyleSheet, Dimensions, Modal, TouchableOpacity, Button, Pressable} from "react-native";
import { useState, useEffect } from "react";
import {Image} from 'expo-image'
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system'
import * as SQLite from 'expo-sqlite';
import axios from "axios";
import { SafeAreaView } from 'react-native-safe-area-context';
import { blue, ColorProperties } from "react-native-reanimated/lib/typescript/Colors";
//const db = SQLite.openDatabaseSync('fitCast.db');

export default function MyClothing() {
    const [modalVisible, setModalVisible] = useState(false); // State to control modal visibility
    const [image, setImage] = useState<string | null>(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [loadedImages, setloadedImages] = useState([]);  // Store the data from SQLite

    const fetchData = async () => {
        // db.withTransactionAsync(async () => {
        //     await db.execAsync('CREATE TABLE IF NOT EXISTS processedImages (id INTEGER PRIMARY KEY NOT NULL, uri TEXT NOT NULL, intValue INTEGER);')
        //     setloadedImages(await db.getAllAsync('SELECT * FROM processedImages'));
        // })
    };

    useEffect(() => {
        fetchData();
      }, []);

    // Function to toggle the modal visibility
    const toggleModal = () => {
      setModalVisible(!modalVisible);
    };

    const choosePicture = async () => {
        // No permissions request is necessary for launching the image library
        let result = await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ['images'],
          allowsEditing: true,
          aspect: [4, 3],
          quality: 1,
        });

        if (!result.canceled) {
            setImage(result.assets[0].uri);
            console.log(result)
        }
    }

    const uploadPicture = async () => {
        // try {
        //     if (!image) {
        //         setUploadStatus('Please pick an image first!');
        //         return;
        //     }
        //     const fileInfo = await FileSystem.getInfoAsync(image);
        //     const fileExtension = fileInfo.uri.split('.').pop();
        //     const mimeType = `image/${fileExtension === 'jpg' ? 'jpeg' : fileExtension}`;
        //     const imageBlob = await fetch(image).then((res) => res.blob());
      
        //     const formData = new FormData();
        //     formData.append('file', imageBlob, `image.${fileExtension}`);
        //   const response = await axios.post('https://localhost:8080/processClothingImage', formData, {
        //     headers: {
        //       'Content-Type': 'multipart/form-data', // Ensure this header is set for file uploads
        //     },
        //   });
    
        //   if (response.status === 200) {
        //     setUploadStatus('Upload Successful!');
        //     //store image info to sql database and then 
        //     //reset modal
        //     await db.execAsync(`
        //         PRAGMA journal_mode = WAL;
        //         CREATE TABLE IF NOT EXISTS processedImages (id INTEGER PRIMARY KEY NOT NULL, uri TEXT NOT NULL, intValue INTEGER);
        //         INSERT INTO processedImages (uri) VALUES ('${"sdfsdf"}');
        //         `);
        //     setUploadStatus('');
        //     setImage(null);
        //     setModalVisible(false);
        //     fetchData();
        //   } else {
        //     setUploadStatus('Upload Failed.');
        //   }
        // } catch (error) {
        //   setUploadStatus('Error uploading image.');
        //   console.error(error);
        // }
      };

    //   {
    //     loadedImages.map((item) => (
    //         <View key={"item.id"} style={styles.item}>
    //             <Text style={styles.itemText}>{""}</Text>
    //         </View>
    //     ))
    // }
  
  return (
    <ScrollView
    contentContainerStyle = {
        styles.container
    }
    >
        <SafeAreaView>

        </SafeAreaView>
            <Pressable onPress={toggleModal} style={styles.item}>
                <Text style = {{
                    color: 'white'
                }}
                >
                    Add New Clothing
                </Text>
            </Pressable>
        <Modal
         visible={modalVisible}
         animationType="slide" // Makes the modal slide down from the top
         onRequestClose={toggleModal} // Close modal when pressing back button on Android
        >
            <View
                style = {
                    styles.modal_container
                }
            >
                <TouchableOpacity onPress={choosePicture}>
                    <Text>Choose Image</Text>
                </TouchableOpacity>

                {image && <Image source = {{uri: image || ""}}/>}

                <Button title="Cancel" onPress={toggleModal} color={"blue"}/>

                {image &&
                    <Button title="Upload" onPress={uploadPicture} color={'blue'}/>
                }

                {uploadStatus &&<Text > {uploadStatus}</Text>}

            </View>
        </Modal>
    </ScrollView>

  );
}

const ScreenWidth = Dimensions.get('window').width;

const styles = StyleSheet.create({
  container:{
    flexDirection: 'column',
    justifyContent: 'flex-start',
    alignItems: 'center',
    padding: 20,
  },
  modal_container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  item: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'blue',
      color: 'white',
    padding: 20,
    width: ScreenWidth*0.7,
    height: 40,
    borderRadius: 10,
  },
  heavyText: {
    fontSize: 24,
    fontWeight: '800', // Makes the font heavier
  },
  itemText: {
    color: 'white', // White text
    fontSize: 18,
  },
});
