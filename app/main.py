# Main entry point for the FastAPI application.
from fastapi import FastAPI
from db.database import engine, Base
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from graphql_api.schema import schema
from graphql_api.context import get_context

# Create tables in database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="FastAPI Notes App (GraphQL)", version="2.0.0")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL Router
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def root():
    return {"message": "Welcome to the Notes App GraphQL API", "docs": "/graphql"}
