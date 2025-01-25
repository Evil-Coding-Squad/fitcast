import { ScrollView, Text, View, StyleSheet, Dimensions, Modal, TouchableOpacity, Image } from "react-native";
import { useState } from "react";
import * as ImagePicker from 'expo-image-picker';

export default function MyClothing() {
    const [modalVisible, setModalVisible] = useState(false); // State to control modal visibility
    const [image, setImage] = useState<string | null>(null);

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
        }
    }

    const uploadPicture = async () => {
        //send picture to server for analysis
        //store info in database
    }
  
  return (
    <ScrollView
    contentContainerStyle = {
        styles.container
    }
    >
        <View style = {styles.item}>
            <TouchableOpacity onPress={toggleModal}>
                <Text style={styles.itemText}>Add Clothing Item</Text>
            </TouchableOpacity>
        </View>

        <Modal
         visible={modalVisible}
         animationType="slide" // Makes the modal slide down from the top
         onRequestClose={toggleModal} // Close modal when pressing back button on Android
         style = {
            styles.container
         }
        >
            <View
                style = {
                    styles.modal_container
                }
            >
                <TouchableOpacity onPress={choosePicture}>
                    <Image source = {require('../../assets/images/icons8-camera-100.png')}/>
                </TouchableOpacity>
                {image && <Image source = {{uri: image}}/>}
                <TouchableOpacity onPress={toggleModal}>
                    <Text >Go Back</Text>
                </TouchableOpacity>
                {image &&
                    <TouchableOpacity onPress={uploadPicture}>
                        <Text >Upload</Text>
                    </TouchableOpacity>
                }
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
    padding: 20,
    width: ScreenWidth*0.7,
    height: 30,
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
