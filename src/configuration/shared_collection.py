import collections
import threading

from src.data_classes.peer import Peer


class SharedPeerCollection:
    def __init__(self):
        self._lock = threading.Lock()  # Lock for thread safety
        self._collection = collections.deque()  # Efficient collection for adding/removing

    def add(self, peer: Peer):
        with self._lock:  # Acquire the lock to ensure exclusive access
            if peer not in self._collection:
                self._collection.append(peer)  # Add the string only if it's unique

    def get_all(self):
        with self._lock:  # Acquire the lock for consistent retrieval
            return list(self._collection)  # Return a copy of the collection
