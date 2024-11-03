import React, { useState } from "react";
import { View, Text, TextInput, Alert, StyleSheet } from "react-native";
import { useRouter } from "expo-router";

import CustomButton from "@/components/CustomButton";

export default function SignIn() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSignIn = async () => {
    // handle sign in logic
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/${username}/validate_user/${password}`, {
          method: "GET",
        });
  
        if (response.ok) {
            console.log("Successful Navigating with username:", username);
          // Navigate to the receipts page if the login is successful
          router.push({ pathname:"./(tabs)/index", params: {username}});
        } else {
          const data = await response.json();
          Alert.alert("Sign In Failed", data.error || "Invalid credentials.");
        }
      } catch (error) {
        Alert.alert("Error", "An error occurred during sign-in.");
      }
    };

  return (
    <View style={styles.container}>
      <Text style={styles.mainTitle}>ReSplit</Text>
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

      <CustomButton
        title="Sign In"
        onPress={handleSignIn}
        paddingVertical={15}
        fontSize={18}
        fontWeight="bold"
      />

      <CustomButton
        title="Don't Have an Account? Sign Up Here"
        onPress={() => router.push("/signup")}
        style={styles.signupButton}
        paddingVertical={10}
        paddingHorizontal={25}
        fontSize={16}
        fontWeight="500"
        color='#ADD8E6'
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
  mainTitle: {
    color: "#d1c9ec",
    fontSize: 40,
    fontWeight: "bold",
    marginBottom: 15,
  },
  title: {
    color: "#d1c9ec",
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 15,
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
  signupButton: {
    marginTop: 10,
  },
});
