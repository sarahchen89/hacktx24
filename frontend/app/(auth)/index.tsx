import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import CustomButton from '@/components/CustomButton';

export default function SignIn() {
    const router = useRouter();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSignIn = () => {
        // handle sign in logic
        console.log('Username:', username);
        console.log('Password:', password);
    }

  return (
    <View style={styles.container}>
    <Text style={styles.title}>Sign In</Text>

    <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
    />

<TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        autoCapitalize="none"
    />

    <CustomButton title="Log In" onPress={handleSignIn} />

    <Text> </Text>

    <CustomButton title="Sign Up" onPress={handleSignIn} />
    </View>
  );
}

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#060631',
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    title: {
        color: '#d1c9ec',
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 15,
    },
    input: {
        color:'#d1c9ec',
        width: '50%',
        padding: 10,
        borderColor: '#d1c9ec',
        borderWidth: 1,
        borderRadius: 5,
        marginBottom: 15,
    },
})
