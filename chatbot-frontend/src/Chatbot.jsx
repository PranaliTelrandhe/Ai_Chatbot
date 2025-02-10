import React, { useState } from "react";
import axios from "axios";
import { Container, TextField, Button, List, ListItem, Typography, Box } from "@mui/material";
import { lightGreen } from "@mui/material/colors";

const Chatbot = () => {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState([]);

  const handleQuery = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/query", { query });
      const botResponse = response.data.response;

      setHistory([...history, { query, response: botResponse }]);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>AI-Powered Chatbot</Typography>

      <TextField
        fullWidth
        label="Type your query..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        variant="outlined"
        sx={{ marginBottom: 2 }}
      />

      <Button 
        variant="contained" 
        onClick={handleQuery} 
        sx={{ backgroundColor: "#6200ea", color: "white", marginBottom: 2 }}
      >
        Submit
      </Button>

      <List>
        {history.map((item, index) => (
          <ListItem key={index} sx={{ flexDirection: "column", alignItems: "flex-start" }}>
              <Box sx={{ backgroundColor: "lightGreen", padding: 2, borderRadius: 2, marginTop: 1, width: "100%" }}>
            <Typography variant="body1" sx={{  fontWeight: "bold", color: "blue" }}>
              You: </Typography> {item.query}
           </Box>

            {/* Bot response styling */}
            <Box sx={{ backgroundColor: "#e3f2fd", padding: 2, borderRadius: 2, marginTop: 1, width: "100%" }}>
              <Typography variant="body1" sx={{ fontWeight: "bold", color: "#d32f2f" }}>
                Bot:
              </Typography>
              {Array.isArray(item.response) ? (
                <ul style={{ margin: 0, paddingLeft: 20 }}>
                  {item.response.map((product, i) => (
                    <li key={i} style={{ color: "#004d40" }}>
                      <strong>{product.name}</strong> - {product.brand} - ${product.price} ({product.category})
                    </li>
                  ))}
                </ul>
              ) : (
                <Typography sx={{ color: "#2e7d32" }}>{item.response}</Typography>
              )}
            </Box>
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default Chatbot;
