"""
Proxy module exposing SupabaseManager from root directory.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from supabase_client import SupabaseManager, _ensure_local_db, _save_local_db

__all__ = ["SupabaseManager", "_ensure_local_db", "_save_local_db"]

