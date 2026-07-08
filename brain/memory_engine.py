"""
brain/memory_engine.py

Purpose:
Central memory controller for JARVIS.
"""

from brain.extractor import extract_memory
from brain.ai_extractor import ai_extract_memory
from brain.memory_filter import should_extract_memory


def process_memory(command):

    # Skip if sentence is not related to memory
    if not should_extract_memory(command):
        return None

    # Fast local extraction
    memory = extract_memory(command)

    if memory:
        return memory

    # AI fallback
    return ai_extract_memory(command)