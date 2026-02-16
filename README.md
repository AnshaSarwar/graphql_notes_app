# FastAPI Notes App (GraphQL)

A modern, type-safe GraphQL backend for managing user notes, built with FastAPI and [Strawberry GraphQL](https://strawberry.rocks/).

## Features

- **GraphQL API**: Single endpoint `/graphql` for all operations.
- **Strongly Typed**: Full schema validation using Strawberry Types.
- **JWT Authentication**: Secure authentication handled via GraphQL mutations and context.
- **Relational Queries**: Fetch users and their notes in a single request.
- **Interactive Playground**: Built-in GraphiQL tool for testing queries and mutations.

## Tech Stack

- **Framework**: FastAPI
- **GraphQL**: Strawberry
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Security**: Argon2, PyJWT

## Getting Started

### Prerequisites

1.  **PostgreSQL**: Ensure you have a database named `notes_app`.
2.  **Environment**: Configure `.env` in the `app/` directory with `DATABASE_URL`, `SECRET_KEY`, etc.

### Setup & Run

1.  **Install dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
2.  **Start the server**:
    ```powershell
    uvicorn main:app --reload
    ```
3.  **Explore the API**:
    Visit [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql)

## GraphQL Examples

### Register a User
```graphql
mutation {
  register(
    email: "test@example.com",
    username: "testuser",
    password: "password123"
  ) {
    id
    username
  }
}
```

### Login
```graphql
mutation {
  login(username: "testuser", password: "password123") {
    accessToken
    tokenType
  }
}
```

### Fetch My Notes
*Note: Set "Authorization: Bearer <token>" in headers.*
```graphql
query {
  me {
    username
    notes {
      title
      content
    }
  }
}
```

### Create a Note
```graphql
mutation {
  createNote(title: "GraphQL Note", content: "Practicing GraphQL is fun!") {
    id
    title
  }
}
```
