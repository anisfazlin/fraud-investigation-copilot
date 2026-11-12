"""MongoDB connection helper.

One MongoClient per process: it holds a connection pool and is thread-safe, so
creating a new client per request would waste connections (Atlas Free clusters
cap these) and add TLS handshake latency to every call.
"""
from functools import lru_cache

import certifi
from pymongo import MongoClient
from pymongo.database import Database

from backend.app.config import get_settings


@lru_cache
def get_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(
        settings.mongodb_uri,
        tlsCAFile=certifi.where(),      # avoids "CERTIFICATE_VERIFY_FAILED" on Windows/macOS
        serverSelectionTimeoutMS=10_000,  # fail fast with a clear error instead of hanging
        maxPoolSize=10,                  # small pool: Free tier, single small API instance
        appname="fraud-investigation-copilot",
    )


def get_db() -> Database:
    return get_client()[get_settings().mongodb_db]
