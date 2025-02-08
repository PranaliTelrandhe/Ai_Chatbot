# AI Chatbot

## AI-Powered Chatbot for Supplier and Product Information

This project is an AI-powered chatbot that allows users to query a product and supplier database using natural language. The chatbot interacts with a MySQL database to fetch relevant information and uses an open-source LLM (GPT-2) for summarizing supplier data.

## Features

- Query products and suppliers using natural language.
- Summarize supplier information using GPT-2.
- User-friendly interface built with React.
- FastAPI backend for handling requests.
- MySQL database for storing supplier and product details.

## Tech Stack

### Frontend

- **React**: JavaScript library for building the user interface.
- **Material-UI**: Component library for styling the UI.
- **Axios**: For making HTTP requests to the backend.

### Backend

- **FastAPI**: Python framework for building the backend API.
- **SQLAlchemy**: ORM for interacting with the MySQL database.
- **Hugging Face Transformers**: For using the GPT-2 model for summarization.

### Database

- **MySQL**: Relational database for storing product and supplier data.
- **PyMySQL**: MySQL driver for Python.

### Other Tools

- **CORS Middleware**: For enabling cross-origin requests between the frontend and backend.

## Installation

### Prerequisites

Make sure you have the following installed:

- Python (>=3.8)
- Node.js (>=14.x)
- MySQL Server

### Setting up the Environment

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows

# Install backend dependencies
pip install -r requirements.txt
```

### Setting Up MySQL Database

1. Start your MySQL server.

2. Create a database:

   ```sql
   CREATE DATABASE chatbot_db;
   ```

3. Configure your 

   ```
   .env
   ```

    file with MySQL credentials:

   ```ini
   DB_USER=username
   DB_PASSWORD=password
   DB_HOST=localhost
   DB_NAME=chatbot_db
   ```

4. Run database migrations:

   ```bash
   python migrate.py  # (If using Alembic or a similar tool)
   ```

### Running the Backend

```bash
uvicorn main:app --reload
```

### Running the Frontend

```bash
cd frontend
npm install
npm start
```

## Example Queries

- **"Show me all products under brand X."**
- **"Which suppliers provide laptops?"**
- **"Give me details of product ABC."**
