"""Memory management for the Agent"""
from typing import Dict, List

class Memory:
    """Memory management for the Agent"""

    def __init__(self):
        self._memory: List[Dict] = []

    def add_to_memory(self, memory) -> None:
        """Store a value in memory"""
        self._memory.append(memory)

    def get_memory(self) -> List[Dict]:
        """Retrieve memory"""
        return self._memory

    def clear_memory(self) -> None:
        """Clear all memory"""
        self._memory = []

    def __repr__(self):
        return f"Memory(memory={self._memory})"
