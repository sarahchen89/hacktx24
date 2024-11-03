import React, { useEffect, useState } from 'react';
import { View, Text, Button, ActivityIndicator, Alert, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';

interface UserProfile {
  first_name: string;
  last_name: string;
  email: string;
  username: string;
}

const Profile: React.FC = () => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Fetch user profile data
    const fetchUserData = async () => {
      const username = await AsyncStorage.getItem('username'); // Assumes username is stored on login
      if (username) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/users/${username}`);
          if (!response.ok) {
            throw new Error('Failed to fetch user data');
          }
          const data = await response.json();
          setUser(data.user);
        } catch (error) {
          console.error('Error fetching user data:', error);
          Alert.alert('Error', 'Failed to load user data');
        } finally {
          setLoading(false);
        }
      } else {
        router.replace('./profile'); // Redirect if no username is stored
      }
    };

    fetchUserData();
  }, [router]);

  const handleLogout = async () => {
    await AsyncStorage.removeItem('username'); // Clear stored user info
    router.replace('./profile'); // Redirect to sign-in page
  };

  if (loading) {
    return <ActivityIndicator size="large" color="#0000ff" />;
  }

  if (!user) {
    return <Text style={styles.errorText}>User data not available</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>User Profile</Text>
      <Text style={styles.label}>
        <Text style={styles.bold}>First Name: </Text> {user.first_name}
      </Text>
      <Text style={styles.label}>
        <Text style={styles.bold}>Last Name: </Text> {user.last_name}
      </Text>
      <Text style={styles.label}>
        <Text style={styles.bold}>Email: </Text> {user.email}
      </Text>
      <Text style={styles.label}>
        <Text style={styles.bold}>Username: </Text> {user.username}
      </Text>
      <Button title="Logout" onPress={handleLogout} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    marginBottom: 10,
  },
  bold: {
    fontWeight: 'bold',
  },
  errorText: {
    fontSize: 18,
    color: 'red',
  },
});

export default Profile;
