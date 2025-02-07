# Ai_Chatbot
AI-Powered Chatbot for Supplier and Product Information

This project is an AI-powered chatbot that allows users to query a product and supplier database using natural language. The chatbot interacts with a MySQL database to fetch relevant information and uses an open-source LLM (GPT-2) for summarizing supplier data. The system consists of:
A React frontend for user interaction.
A FastAPI backend for handling queries and interacting with the database.
A MySQL database for storing product and supplier information.
The chatbot can handle queries like:
"Show me all products under brand X."
"Which suppliers provide laptops?"
"Give me details of product ABC."

Tools and Technologies Used
Frontend
React: JavaScript library for building the user interface.
Material-UI: Component library for styling the UI.
Axios: For making HTTP requests to the backend.

Backend
FastAPI: Python framework for building the backend API.
SQLAlchemy: ORM for interacting with the MySQL database.
LangGraph: For creating and managing chatbot workflows.
Hugging Face Transformers: For using the GPT-2 model for summarization.

Database
MySQL: Relational database for storing product and supplier data.

Other Tools
PyMySQL: MySQL driver for Python.

CORS Middleware: For enabling cross-origin requests between the frontend and backend.

