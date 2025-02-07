import React, { useState } from "react";
import axios from "axios";
import { Container, TextField, Button, List, ListItem, Typography } from "@mui/material";

const Chatbot = () => {
  const [query, setQuery] = useState("");  // State to hold user input
  const [history, setHistory] = useState([]);  // State to hold chat history
  const [loading, setLoading] = useState(false);  // Loading state

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent page refresh
    if (!query.trim()) return; // Prevent empty queries

    setLoading(true);  // Show loading indicator

    try {
      const response = await axios.post("http://localhost:8000/query", { query });
      setHistory([...history, { query, response: response.data.response }]); // Update chat history
      setQuery(""); // Clear input after submission
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);  // Hide loading indicator
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>AI-Powered Chatbot</Typography>

      {/* Form Submission */}
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="Enter your query"
          value={query}
          onChange={(e) => setQuery(e.target.value)} // Update query state
        />
        <Button type="submit" variant="contained" style={{ marginTop: "10px" }} disabled={loading}>
          {loading ? "Loading..." : "Submit"} {/* Show loading state */}
        </Button>
      </form>

      {/* Chat History */}
      <List>
        {history.map((item, index) => (
          <ListItem key={index}>
            <Typography><strong>You:</strong> {item.query}</Typography>
            <Typography><strong>Bot:</strong> {JSON.stringify(item.response)}</Typography>
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default Chatbot;
