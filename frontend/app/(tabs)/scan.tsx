import React, { useState } from 'react';
import { Alert, Button, Image, View, StyleSheet } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';

export default function ImagePickerExample() {
  const [image, setImage] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const username = localStorage.getItem('username'); // Replace with actual username or a variable holding the username

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      const imageUri = result.assets[0].uri;
      setImage(imageUri);
      await uploadImage(imageUri); // Upload the image after picking
    }
  };

  const uploadImage = async (uri: string) => {
    setIsUploading(true);

    // Prepare the image as form data
    const formData = new FormData();
    formData.append('receipt', {
      uri,
      name: uri.split('/').pop() || 'receipt.jpg', // Get image name from URI or use default name
      type: 'image/jpeg',
    } as any);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/${username}/add_receipt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        Alert.alert('Success', 'Receipt added successfully');
      } else {
        const errorData = await response.json();
        Alert.alert('Error', errorData.error || 'Failed to add receipt');
      }
    } catch (error) {
      console.error('Upload error:', error);
      Alert.alert('Error', 'An error occurred while uploading the receipt');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Button title={isUploading ? 'Uploading...' : 'Pick an image from camera roll'} onPress={pickImage} disabled={isUploading} />
      {image && <Image source={{ uri: image }} style={styles.image} />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    width: 200,
    height: 200,
    marginTop: 10,
  },
});
