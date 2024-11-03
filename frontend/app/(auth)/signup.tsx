import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
import CustomButton from "@/components/CustomButton";

export default function SignUp() {
  const router = useRouter();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignUp = () => {
    // Handle sign-up logic here
    console.log("First Name:", firstName);
    console.log("Last Name:", lastName);
    console.log("Username:", username);
    console.log("Email:", email);
    console.log("Password:", password);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign up</Text>

      <TextInput
        style={styles.input}
        placeholder="First Name"
        value={firstName}
        onChangeText={setFirstName}
      />

      <TextInput
        style={styles.input}
        placeholder="Last Name"
        value={lastName}
        onChangeText={setLastName}
      />

      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        style={styles.input}
        placeholder="Password"
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
        color='#d1c9ec'
      />

      <Text style={styles.subTitle}> Already Have An Account?</Text>

      <CustomButton
        title="Back to Sign In"
        onPress={() => router.back()}
        style={styles.backButton}
        paddingVertical={10}
        paddingHorizontal={20}
        fontSize={16}
        fontWeight="normal"
        color='#add8e6'
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
    color: '#add8e6',
    fontSize: 15,
    marginBottom: 5,
    marginTop: 10,
  },
  input: {
    color: "#d1c9ec",
    width: "50%",
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
