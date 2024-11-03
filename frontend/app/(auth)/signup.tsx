import React, { useState } from "react";
import { View, Text, TextInput, Alert, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import CustomButton from "@/components/CustomButton";

export default function SignUp() {
  const router = useRouter();
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignUp = async () => {
    const signUpData = {
      first_name,
      last_name,
      username,
      email,
      password,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/api/create_user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(signUpData),
      });

      const data = await response.json();

      if (response.ok) {
        Alert.alert("Success", "Account created successfully!");
        router.back(); // Redirect to login after successful signup
      } else {
        Alert.alert("Signup Failed", data.message || "Please check your information.");
      }
    } catch (error) {
      Alert.alert("Signup Failed", "An error occurred. Please try again.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign up</Text>

      <TextInput
        style={styles.input}
        placeholder="First Name"
        placeholderTextColor="#d1c9ec"
        value={first_name}
        onChangeText={setFirstName}
      />

      <TextInput
        style={styles.input}
        placeholder="Last Name"
        placeholderTextColor="#d1c9ec"
        value={last_name}
        onChangeText={setLastName}
      />

      <TextInput
        style={styles.input}
        placeholder="Username"
        placeholderTextColor="#d1c9ec"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Email"
        placeholderTextColor="#d1c9ec"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
        placeholderTextColor="#d1c9ec"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />

      <CustomButton
        title="Sign Up"
        onPress={handleSignUp}
        paddingVertical={15}
        fontSize={18}
        fontWeight="bold"
        color="#d1c9ec"
      />

      <Text style={styles.subTitle}>Already Have An Account?</Text>

      <CustomButton
        title="Back to Sign In"
        onPress={() => router.back()}
        style={styles.backButton}
        paddingVertical={10}
        paddingHorizontal={20}
        fontSize={16}
        fontWeight="normal"
        color="#add8e6"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#060631",
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    color: "#d1c9ec",
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 15,
  },
  subTitle: {
    color: "#add8e6",
    fontSize: 15,
    marginBottom: 5,
    marginTop: 10,
  },
  input: {
    color: "#d1c9ec",
    width: "80%",
    padding: 10,
    borderColor: "#d1c9ec",
    borderWidth: 1,
    borderRadius: 5,
    marginBottom: 15,
  },
  backButton: {
    marginTop: 10,
  },
});