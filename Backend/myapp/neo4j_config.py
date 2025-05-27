# myapp/neo4j_config.py

from neomodel import config
import os

def ensure_neo4j_connection():
    if not config.DATABASE_URL:
        config.DATABASE_URL = os.getenv("NEOMODEL_NEO4J_BOLT_URL")
        if not config.DATABASE_URL:
            raise ValueError("Neo4j connection not configured properly.")
