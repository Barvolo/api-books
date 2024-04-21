
# Book Management System

## Overview

This Flask-based Book Management System is designed to manage a collection of books for a book club application. It allows users to create, retrieve, update, and delete book entries, as well as rate books and retrieve ratings. The system integrates with external APIs to enrich book data and generate summaries using a Large Language Model (LLM).

## Features

- **CRUD Operations**: Manage books through Create, Read, Update, and Delete operations.
- **External API Integration**: Fetch additional book details from Google Books API.
- **LLM Integration**: Generate book summaries using an AI-based text summarization model.
- **Ratings Management**: Allow users to rate books and retrieve average ratings.
- **Top Books Listing**: Retrieve a list of top-rated books based on average ratings.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask
- Requests library
- Docker (for containerization)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd book-management-system
   ```

2. **Set up a Python virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

- **Environment Variables**:
  - `API_KEY`: Set this environment variable with your Google Books or LLM API key.
  - Flask and other configurations are managed in `config/settings.py`.

### Running the Application

1. **Start the Flask server**:
   ```bash
   flask run --port=8000
   ```
   This will start the application on `localhost:8000`.

2. **Using Docker**:
   - Build the Docker image:
     ```bash
     docker build -t book-management-system .
     ```
   - Run the Docker container:
     ```bash
     docker run -p 8000:8000 book-management-system
     ```
   This maps port 8000 of the container to port 8000 on your host, allowing you to access the API at `localhost:8000`.

## API Documentation

### Endpoints

- `POST /books`: Create a new book entry.
- `GET /books`: Retrieve all books.
- `GET /books/{id}`: Retrieve a specific book by ID.
- `PUT /books/{id}`: Update a specific book by ID.
- `DELETE /books/{id}`: Delete a specific book by ID.
- `GET /ratings`: Retrieve all ratings.
- `GET /ratings/{id}`: Retrieve ratings for a specific book by ID.
- `GET /top`: Retrieve the top-rated books.

### Usage

- **Create a Book**:
  - Endpoint: `POST /books`
  - Payload example:
    ```json
    {
      "title": "Sample Book",
      "ISBN": "1234567890123",
      "genre": "Fiction"
    }
    ```
  - The server will enrich the book data from Google Books and generate a summary using the LLM.

- **Get a Book**:
  - Endpoint: `GET /books/{id}`
  - Returns detailed information including the enriched data.

## Testing

- **Manual Testing**:
  - Use tools like Postman or curl to manually test the API endpoints.

- **Automated Testing**:
  - Run unit tests:
    ```bash
    python -m pytest
    ```

## Deployment

- The application is containerized using Docker, which simplifies deployment on any system supporting Docker.

## Contributing

Contributions are welcome. Please fork the repository and submit pull requests for any enhancements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any further queries, please reach out to the repository maintainer or open an issue in the project repository.
