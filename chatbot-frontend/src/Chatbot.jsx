import React, { useState } from "react";
import axios from "axios";
import { 
  Container, TextField, Button, List, ListItem, Typography, Paper, Stack 
} from "@mui/material";

const Chatbot = () => {
  const [query, setQuery] = useState("");  // User input state
  const [history, setHistory] = useState([]);  // Chat history state
  const [loading, setLoading] = useState(false);  // Loading state
  const [error, setError] = useState(null);  // Error state

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page refresh
    if (!query.trim()) return; // Ignore empty queries

    setLoading(true);
    setError(null); // Reset error state

    try {
      const response = await axios.post("http://localhost:8000/query", { query });
      setHistory([...history, { query, response: response.data.response }]); // Update chat history
      setQuery(""); // Clear input after submission
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Failed to connect to chatbot. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom align="center">AI Powered Chatbot</Typography>

      {/* Form Submission */}
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <TextField
          fullWidth
          label="Type your query..."
          variant="outlined"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button 
          type="submit" 
          variant="contained" 
          style={{ marginTop: "10px" }} 
          disabled={loading}
        >
          {loading ? "Loading..." : "Sumbit"}
        </Button>
      </form>

      {/* Error Message */}
      {error && <Typography color="error">{error}</Typography>}

      {/* Chat History */}
      <List>
        {history.map((item, index) => (
          <Stack key={index} spacing={1}>

            {/* User Message */}
            <ListItem>
              <Paper 
                style={{
                  padding: "10px",
                  backgroundColor: "lightgreen", 
                  width: "fit-content",
                  maxWidth: "80%"
                }}
              >
                <Typography variant="body1"><strong>You:</strong> {item.query}</Typography>
              </Paper>
            </ListItem>

            {/* Bot Response */}
            <ListItem>
              <Paper 
                style={{
                  padding: "10px",
                  backgroundColor: "lightyellow", 
                  width: "fit-content",
                  maxWidth: "80%"
                }}
              >
                <Typography variant="body1"><strong>Bot:</strong> {item.response}</Typography>
              </Paper>
            </ListItem>

          </Stack>
        ))}
      </List>
    </Container>
  );
};

export default Chatbot;
