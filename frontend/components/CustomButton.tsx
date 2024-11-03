import React from 'react';
import { TouchableOpacity, Text, StyleSheet, GestureResponderEvent, ViewStyle, TextStyle } from 'react-native';

interface CustomButtonProps {
  title: string;
  onPress: (event: GestureResponderEvent) => void;
  style?: ViewStyle;
  paddingVertical?: number;    // Controls vertical padding
  paddingHorizontal?: number;  // Controls horizontal padding
  fontSize?: number;           // Controls font size
  fontWeight?: TextStyle['fontWeight']; // Controls font weight
  color?: string;              // Optional background color
}

export default function CustomButton({
  title,
  onPress,
  style,
  paddingVertical = 12,
  paddingHorizontal = 20,
  fontSize = 16,
  fontWeight = 'bold',
  color = '#d1c9ec',          // Default color (blue) if no color is specified
}: CustomButtonProps) {
  return (
    <TouchableOpacity
      style={[
        styles.button,
        style,
        { paddingVertical, paddingHorizontal, backgroundColor: color },
      ]}
      onPress={onPress}
    >
      <Text style={[styles.buttonText, { fontSize, fontWeight }]}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff', // Text color (white)
  },
});