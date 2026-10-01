"""
Context Manager for PinkBus Chatbot
Maintains lightweight conversational memory across multi-turn interactions.
"""

import time
from typing import Dict, Any

class ContextManager:
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Retrieve session context, creating a new session if not present."""
        if not session_id:
            session_id = "default_session"
            
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "session_id": session_id,
                "source": None,
                "destination": None,
                "travel_date": None,
                "pending_intent": None,
                "last_bus_number": None,
                "last_booking_id": None,
                "last_route": None,
                "last_intent": None,
                "last_updated": time.time()
            }
        return self._sessions[session_id]

    def update_session(self, session_id: str, **kwargs) -> Dict[str, Any]:
        """Update fields in the session context."""
        session = self.get_session(session_id)
        for key, val in kwargs.items():
            session[key] = val
        session["last_updated"] = time.time()
        return session

    def clear_pending(self, session_id: str):
        """Clears any pending followup intent."""
        session = self.get_session(session_id)
        session["pending_intent"] = None

    def reset_session(self, session_id: str):
        """Resets the entire session state."""
        if session_id in self._sessions:
            del self._sessions[session_id]
        return self.get_session(session_id)

# Global context manager instance
context_store = ContextManager()
