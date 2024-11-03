import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { useRouter } from "expo-router";
import CustomButton from "@/components/CustomButton";

interface Receipt {
  id: number;
  uploader: { username: string };
  items: { name: string; price: number }[];
}

export default function ReceiptsScreen() {
  const [uploadedReceipts, setUploadedReceipts] = useState<Receipt[]>([]);
  const [assignedReceipts, setAssignedReceipts] = useState<Receipt[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const username = "replace_with_logged_in_username"; // You may need to manage user sessions

  useEffect(() => {
    const fetchReceipts = async () => {
      try {
        // Fetch uploaded receipts
        const uploaded = await fetch(`http://127.0.0.1:5000/api/${username}/get_uploaded_receipts`);
        const uploadedData = await uploaded.json();
        if (uploaded.ok) {
          setUploadedReceipts(uploadedData.uploaded_receipts || []);
        } else {
          console.error("Error fetching uploaded receipts:", uploadedData.error);
        }

        // Fetch assigned receipts
        const assigned = await fetch(`http://127.0.0.1:5000/api/${username}/get_assigned_receipts`);
        const assignedData = await assigned.json();
        if (assigned.ok) {
          setAssignedReceipts(assignedData.assigned_receipts || []);
        } else {
          console.error("Error fetching assigned receipts:", assignedData.error);
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchReceipts();
  }, [username]);

  const renderReceipt = ({ item }: { item: Receipt }) => (
    <View style={styles.receiptContainer}>
      <Text style={styles.receiptText}>Receipt ID: {item.id}</Text>
      <Text style={styles.receiptText}>Uploader: {item.uploader.username}</Text>
      <Text style={styles.receiptText}>Items:</Text>
      {item.items.map((receiptItem, index) => (
        <Text key={index} style={styles.itemText}>
          {receiptItem.name} - ${receiptItem.price.toFixed(2)}
        </Text>
      ))}
    </View>
  );

  if (loading) {
    return <ActivityIndicator size="large" color="#0000ff" style={styles.loader} />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your Uploaded Receipts</Text>
      <FlatList
        data={uploadedReceipts}
        renderItem={renderReceipt}
        keyExtractor={(item) => item.id.toString()}
        ListEmptyComponent={<Text style={styles.noReceiptsText}>No uploaded receipts found.</Text>}
      />

      <Text style={styles.title}>Receipts Assigned to You</Text>
      <FlatList
        data={assignedReceipts}
        renderItem={renderReceipt}
        keyExtractor={(item) => item.id.toString()}
        ListEmptyComponent={<Text style={styles.noReceiptsText}>No assigned receipts found.</Text>}
      />

  
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "#060631",
    flex: 1,
    padding: 20,
  },
  title: {
    color: "#d1c9ec",
    fontSize: 24,
    fontWeight: "bold",
    textAlign: "center",
    marginBottom: 20,
  },
  receiptContainer: {
    backgroundColor: "#2E2E2E",
    padding: 15,
    borderRadius: 8,
    marginBottom: 15,
  },
  receiptText: {
    color: "#d1c9ec",
    fontSize: 16,
  },
  itemText: {
    color: "#d1c9ec",
    fontSize: 14,
    marginLeft: 10,
  },
  noReceiptsText: {
    color: "#d1c9ec",
    textAlign: "center",
    marginTop: 20,
  },
  loader: {
    flex: 1,
    justifyContent: "center",
  },
  addButton: {
    marginTop: 20,
    alignSelf: "center",
  },
});
