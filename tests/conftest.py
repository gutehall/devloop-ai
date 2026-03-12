"""Pytest configuration. Add ai/ to path so tests can import modules."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ai"))
