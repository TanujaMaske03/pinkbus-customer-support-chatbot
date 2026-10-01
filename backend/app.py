"""
PinkBus Customer Support Chatbot - Flask Backend API
Provides REST endpoints for chat interaction, bus lookups, booking retrieval,
demo cancellation, FAQs, policies, and support ticket creation.
"""

from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

import database
from chatbot.intent_detector import detect_intent
from chatbot.response_handler import handle_user_message
from chatbot.context_manager import context_store

app = Flask(__name__)
# Enable CORS for frontend development server
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ensure database tables and seed rows are initialized on startup
database.init_db()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "PinkBus Customer Support Chatbot API",
        "demo_mode": True,
        "language": "English",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Main chat processing endpoint."""
    data = request.get_json(force=True, silent=True) or {}
    message = (data.get("message") or "").strip()
    session_id = data.get("session_id") or "session_default"

    if not message:
        return jsonify({
            "success": False,
            "error": "Empty message provided."
        }), 400

    # Retrieve current conversational context
    context = context_store.get_session(session_id)

    # Detect user intent and extract entities
    intent, entities = detect_intent(message, context)

    # Generate chatbot response
    response_payload = handle_user_message(message, session_id, intent, entities)

    return jsonify({
        "success": True,
        "session_id": session_id,
        "intent": intent,
        "entities": entities,
        "response": response_payload,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })

@app.route('/api/chat/reset', methods=['POST'])
def reset_chat_endpoint():
    """Resets session context for clear/new chat."""
    data = request.get_json(force=True, silent=True) or {}
    session_id = data.get("session_id") or "session_default"
    context_store.reset_session(session_id)
    return jsonify({
        "success": True,
        "message": "Chat session reset successfully.",
        "session_id": session_id
    })

@app.route('/api/buses', methods=['GET'])
def get_buses_endpoint():
    """Retrieve all buses or filter by source/destination."""
    source = request.args.get("source")
    destination = request.args.get("destination")
    max_fare = request.args.get("max_fare")

    if source or destination or max_fare:
        buses = database.search_buses(source=source, destination=destination, max_fare=max_fare)
    else:
        buses = database.get_all_buses()
    return jsonify({
        "success": True,
        "count": len(buses),
        "buses": buses
    })

@app.route('/api/buses/search', methods=['GET'])
def search_buses_endpoint():
    """Search buses with query parameters."""
    source = request.args.get("source")
    destination = request.args.get("destination")
    date = request.args.get("date")
    max_fare = request.args.get("max_fare")

    buses = database.search_buses(source=source, destination=destination, date=date, max_fare=max_fare)
    return jsonify({
        "success": True,
        "count": len(buses),
        "source": source,
        "destination": destination,
        "travel_date": date or "Tomorrow",
        "buses": buses
    })

@app.route('/api/buses/<identifier>', methods=['GET'])
def get_bus_detail_endpoint(identifier):
    """Retrieve single bus details by bus_number (e.g. PB102) or numeric ID."""
    if identifier.isdigit():
        bus = database.get_bus_by_id(int(identifier))
    else:
        bus = database.get_bus_by_number(identifier)

    if not bus:
        return jsonify({"success": False, "error": f"Bus {identifier} not found"}), 404
    return jsonify({"success": True, "bus": bus})

@app.route('/api/bookings/<booking_id>', methods=['GET'])
def get_booking_endpoint(booking_id):
    """Retrieve booking details by booking ID (e.g. PB10001)."""
    booking = database.get_booking(booking_id)
    if not booking:
        return jsonify({"success": False, "error": f"Booking {booking_id} not found"}), 404
    return jsonify({"success": True, "booking": booking})

@app.route('/api/bookings/<booking_id>/cancel', methods=['POST'])
def cancel_booking_endpoint(booking_id):
    """Simulates ticket cancellation in demo mode."""
    booking = database.cancel_booking(booking_id)
    if not booking:
        return jsonify({"success": False, "error": f"Booking {booking_id} not found"}), 404
    
    refund_amt = int(round(booking["fare"] * 0.8))
    return jsonify({
        "success": True,
        "message": f"Booking {booking_id} has been cancelled in demo mode.",
        "booking": booking,
        "refund_amount": refund_amt,
        "refund_percentage": "80%",
        "demo_mode": True
    })

@app.route('/api/faqs', methods=['GET'])
def get_faqs_endpoint():
    """Retrieve FAQs or search by query."""
    q = request.args.get("q")
    category = request.args.get("category")
    if q:
        faq = database.search_faqs(q)
        return jsonify({"success": True, "faq": faq})
    faqs = database.get_all_faqs(category=category)
    return jsonify({"success": True, "count": len(faqs), "faqs": faqs})

@app.route('/api/policies', methods=['GET'])
def get_policies_endpoint():
    """Retrieve demo policies."""
    policies = database.get_policies()
    return jsonify({"success": True, "policies": policies})

@app.route('/api/support', methods=['POST'])
def create_support_endpoint():
    """Submits a demo support ticket and records it in SQLite."""
    data = request.get_json(force=True, silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    issue = (data.get("issue") or "").strip()
    booking_id = (data.get("booking_id") or "").strip()

    if not name or not email or not issue:
        return jsonify({
            "success": False,
            "error": "Name, email, and issue description are required."
        }), 400

    ticket = database.create_support_request(name, email, booking_id, issue)
    return jsonify({
        "success": True,
        "message": "Your support request has been created successfully.",
        "ticket": ticket
    }), 201

if __name__ == '__main__':
    print("Starting PinkBus Chatbot API on port 5000...")
    app.run(host='127.0.0.1', port=5000, debug=True)
