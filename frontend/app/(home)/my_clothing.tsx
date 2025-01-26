import { ScrollView, Text, View, StyleSheet, Dimensions, Modal, TouchableOpacity, Button, Pressable} from "react-native";
import { useState, useEffect } from "react";
import {Image} from 'expo-image'
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system'
import * as SQLite from 'expo-sqlite';
import axios from "axios";
import { SafeAreaView } from 'react-native-safe-area-context';
import {blue, ColorProperties, green} from "react-native-reanimated/lib/typescript/Colors";
import {API_URL} from "@/app/idfk/constants";

const db = SQLite.openDatabaseSync('fitCast.db');

export default function MyClothing() {
    const [modalVisible, setModalVisible] = useState(false); // State to control modal visibility
    const [image, setImage] = useState<string | null>(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [loadedImages, setloadedImages] = useState<any[]>([]);  // Store the data from SQLite

    const fetchData = async () => {
        db.withTransactionAsync(async () => {
            await db.execAsync('CREATE TABLE IF NOT EXISTS processedImages (id INTEGER PRIMARY KEY NOT NULL, uri TEXT NOT NULL, intValue INTEGER);')
            setloadedImages(await db.getAllAsync('SELECT * FROM processedImages'));
        })
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
        try {
            if (!image) {
                setUploadStatus('Please pick an image first!');
                return;
            }
            const fileInfo = await FileSystem.getInfoAsync(image);
            const fileExtension = fileInfo.uri.split('.').pop();
            const mimeType = `image/${fileExtension === 'jpg' ? 'jpeg' : fileExtension}`;
            //const imageBlob = await fetch(image).then((res) => res.blob());
      
            const formData = new FormData();
            formData.append('image',
                {
                    uri: image,
                    name: `testfile.${fileExtension}`
                } as any);

            const config = {
                method: 'post',
                maxBodyLength: Infinity,
                url: `${API_URL}/api/ai/segment`,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                data: formData,
            };

          const response = await axios.request(config);

          const getRandomInt = (min: number, max: number) => {
              return Math.floor(Math.random() * (max - min + 1)) + min;
          }

          const saveImage = async (binaryData: string) => {
              const filePath = `${FileSystem.documentDirectory}image${getRandomInt(0, 100000000)}.png`
              try {
                  await FileSystem.writeAsStringAsync(filePath, binaryData, {encoding: FileSystem.EncodingType.Base64})
                  return Promise.resolve(filePath)
              } catch (e) {
                  console.error(e)
              }
          };

          if (response.status === 200) {
            console.log('Successful upload')
            //setUploadStatus('Upload Successful!');
            //store image info to sql database and then
            //reset modal
              console.log(response.headers)
              console.log(response.data)
              const imageFilePath = saveImage(response.data)
            await db.execAsync(`
                PRAGMA journal_mode = WAL;
                CREATE TABLE IF NOT EXISTS processedImages (id INTEGER PRIMARY KEY NOT NULL, uri TEXT NOT NULL, intValue INTEGER);
                INSERT INTO processedImages (uri) VALUES ('${imageFilePath}');
                `);
            setUploadStatus('');
            setImage(null);
            setModalVisible(false);
            fetchData();
          } else {
            setUploadStatus('Upload Failed.');
          }
        } catch (error) {
          setUploadStatus('Error uploading image.');
          console.error(error);
        }
      };

    const deleteImageById = async (id: string) => {
        db.execSync(
            `DELETE FROM processedImages WHERE id=${id}`
        )
        await fetchData()
    }
    function getImageCard(id: string, uri: string) {
        const deleteImage = () => {
        console.log(`image id: ${id}, uri: ${uri}`)
        }
        return (
            <View key={id} style={styles.image_card}>
                <Image source={{uri: uri}} style={styles.image_card_image}/>
                <Pressable onPress={() => deleteImageById(id)}>
                    <Text style={{color:"red"}}>DELETE</Text>
                </Pressable>
            </View>
        )
    }
  
  return (
    <ScrollView
    contentContainerStyle = {
        styles.container
    }
    >
        <SafeAreaView>

        </SafeAreaView>
        <View style={styles.image_card_container}>
            <Pressable onPress={toggleModal} style={styles.item}>
                <Text style = {{
                    color: 'white'
                }}
                >
                    Add New Clothing
                </Text>
            </Pressable>
            {
              loadedImages.map(item => getImageCard(item.id, item.uri))
            }
        </View>
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

                <Image source = {{uri: image ?? ""}} style={styles.image}/>

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
    image_card: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        padding: 10,
        height: 80,
        width: ScreenWidth * 0.7,
        backgroundColor: "lightblue",
        borderRadius: 15,
    },
    image_card_image: {
        height: 60,
        width: 60,
        borderRadius: 10,
    },
    image: {
        width: 200, // Adjust width
        height: 150, // Adjust height
        marginTop: 20, // Add some spacing
        borderRadius: 10, // Optional: Makes the image corners rounded
    },
  modal_container: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
    image_card_container: {
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        gap: 20,
    },
  item: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'blue',
      color: 'white',
    padding: 20,
    width: ScreenWidth*0.7,
    height: 80,
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
