"""
Intent Detector for PinkBus Customer Support Chatbot
Utilizes rule-based NLP, regex matching, and entity extraction to identify user intent
without relying on external paid APIs or internet access.
"""

import re
from typing import Dict, Any, Optional

CITIES = ["pune", "mumbai", "goa", "kolhapur", "nashik"]

CITY_CANONICAL = {
    "pune": "Pune",
    "mumbai": "Mumbai",
    "bombay": "Mumbai",
    "goa": "Goa",
    "panjim": "Goa",
    "kolhapur": "Kolhapur",
    "nashik": "Nashik",
    "nasik": "Nashik"
}

BUS_NUMBER_PATTERN = re.compile(r'\b(PB\d{3})\b', re.IGNORECASE)
BOOKING_ID_PATTERN = re.compile(r'\b(PB\d{5})\b', re.IGNORECASE)
TICKET_ID_PATTERN = re.compile(r'\b(SUP-\d{5})\b', re.IGNORECASE)
PRICE_PATTERN = re.compile(r'(?:under|below|less than|within|max(?:imum)?)\s*(?:₹|rs\.?|inr)?\s*(\d{3,4})', re.IGNORECASE)

DATE_KEYWORDS = [
    "today", "tomorrow", "day after tomorrow", "tonight",
    "next monday", "next tuesday", "next wednesday", "next thursday",
    "next friday", "next saturday", "next sunday",
    "this weekend", "next week"
]

def extract_entities(text: str) -> Dict[str, Any]:
    """Extracts cities, bus number, booking ID, dates, and fare constraints from text."""
    lower_text = text.lower().strip()
    entities = {
        "source": None,
        "destination": None,
        "bus_number": None,
        "booking_id": None,
        "max_fare": None,
        "travel_date": None
    }

    # Extract Bus Number (e.g. PB102)
    bus_match = BUS_NUMBER_PATTERN.search(text)
    if bus_match:
        entities["bus_number"] = bus_match.group(1).upper()

    # Extract Booking ID (e.g. PB10001)
    booking_match = BOOKING_ID_PATTERN.search(text)
    if booking_match:
        entities["booking_id"] = booking_match.group(1).upper()

    # Extract Max Fare constraint (e.g. "under 700")
    fare_match = PRICE_PATTERN.search(text)
    if fare_match:
        try:
            entities["max_fare"] = int(fare_match.group(1))
        except ValueError:
            pass

    # Extract Travel Date
    for kw in DATE_KEYWORDS:
        if kw in lower_text:
            entities["travel_date"] = kw.title()
            break
    
    # Check date patterns like "2026-10-05" or "10th Oct"
    if not entities["travel_date"]:
        iso_date = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', text)
        if iso_date:
            entities["travel_date"] = iso_date.group(1)
        else:
            word_date = re.search(r'\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*)\b', lower_text)
            if word_date:
                entities["travel_date"] = word_date.group(1).title()

    # Extract Route (Source and Destination)
    # Pattern 1: "from <city> to <city>"
    from_to = re.search(r'from\s+([a-zA-Z]+)\s+to\s+([a-zA-Z]+)', lower_text)
    if from_to:
        src = from_to.group(1)
        dst = from_to.group(2)
        if src in CITY_CANONICAL:
            entities["source"] = CITY_CANONICAL[src]
        if dst in CITY_CANONICAL:
            entities["destination"] = CITY_CANONICAL[dst]

    # Pattern 2: "<city> to <city>" or "<city> -> <city>" or "<city> - <city>"
    if not entities["source"] or not entities["destination"]:
        city_to_city = re.search(r'([a-zA-Z]+)\s*(?:to|->|—|-)\s*([a-zA-Z]+)', lower_text)
        if city_to_city:
            src = city_to_city.group(1)
            dst = city_to_city.group(2)
            if src in CITY_CANONICAL and dst in CITY_CANONICAL:
                entities["source"] = CITY_CANONICAL[src]
                entities["destination"] = CITY_CANONICAL[dst]

    # Pattern 3: Single city mentions like "buses to Goa" or "buses from Pune"
    if not entities["destination"]:
        to_city = re.search(r'(?:to|for)\s+([a-zA-Z]+)', lower_text)
        if to_city and to_city.group(1) in CITY_CANONICAL:
            entities["destination"] = CITY_CANONICAL[to_city.group(1)]

    if not entities["source"]:
        from_city = re.search(r'(?:from|departing|start(?:ing)?\s+at)\s+([a-zA-Z]+)', lower_text)
        if from_city and from_city.group(1) in CITY_CANONICAL:
            entities["source"] = CITY_CANONICAL[from_city.group(1)]

    return entities

def detect_intent(text: str, context: Optional[Dict[str, Any]] = None) -> tuple[str, Dict[str, Any]]:
    """
    Detects the primary intent and returns (intent_name, entities).
    Also consults active context to handle multi-turn dialogs (e.g. responding with date after bot prompt).
    """
    cleaned = text.strip()
    lower = cleaned.lower()
    entities = extract_entities(text)

    # 1. Check for Pending Context Intent first
    if context and context.get("pending_intent"):
        pending = context["pending_intent"]
        
        # If bot was waiting for travel date after bus search
        if pending == "bus_search_need_date":
            # If user provided a date (or anything plausible as date like "Tomorrow", "Next Monday", "Oct 5")
            if entities["travel_date"] or lower in DATE_KEYWORDS or any(w in lower for w in ["today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
                date_val = entities["travel_date"] or cleaned.title()
                entities["travel_date"] = date_val
                return "bus_search_date_provided", entities
            # If user asks a new question instead, fall through to general detection

        # If bot was waiting for booking ID
        if pending in ["need_booking_id_status", "need_booking_id_cancel", "need_booking_id_reschedule"]:
            if entities["booking_id"]:
                if pending == "need_booking_id_cancel":
                    return "cancellation", entities
                elif pending == "need_booking_id_reschedule":
                    return "reschedule", entities
                else:
                    return "booking_status", entities

    # 2. Clear / Reset Chat
    if any(k in lower for k in ["clear chat", "new chat", "reset chat", "restart chat", "start over"]):
        return "clear_chat", entities

    # 3. Human Support Escalation
    support_keywords = [
        "talk to a human", "talk to support", "customer support", "customer care",
        "human support", "talk to an agent", "contact agent", "call support",
        "speak to someone", "representative", "human agent", "talk to executive",
        "create support request", "support request", "raise ticket", "support ticket"
    ]
    if any(k in lower for k in support_keywords):
        return "support", entities

    # 4. Greeting
    if lower in ["hi", "hello", "hey", "hola", "namaste", "good morning", "good afternoon", "good evening", "greetings"]:
        return "greeting", entities

    # 5. Help / Overview
    if any(k in lower for k in ["what can you help me with", "what can you do", "help me", "how can you help", "features", "options"]):
        return "help_overview", entities

    # 6. Cancellation
    cancellation_patterns = [
        r'\bcancel', r'\bcancellation', r'\bdrop\s+booking\b', r'\bhow\s+to\s+cancel\b', r'\bcan\s+i\s+cancel\b'
    ]
    if any(re.search(p, lower) for p in cancellation_patterns):
        return "cancellation", entities

    # 7. Refund
    refund_patterns = [
        r'\brefund', r'\bmoney\s+back\b', r'\breturn\s+money\b', r'\breturn\s+fare\b'
    ]
    if any(re.search(p, lower) for p in refund_patterns):
        return "refund", entities

    # 8. Rescheduling
    reschedule_patterns = [
        r'\breschedul', r'\bchange\s+(?:my\s+|the\s+)?(?:travel\s+)?date\b',
        r'\bchange\s+(?:my\s+|the\s+)?bus\b', r'\bpostpone\b', r'\bprepone\b',
        r'\bmodif(?:y|ication)\b', r'\bchange\s+ticket\b'
    ]
    if any(re.search(p, lower) for p in reschedule_patterns):
        return "reschedule", entities

    # 9. Booking Status / Ticket Details
    booking_status_keywords = ["check my booking", "show ticket", "booking status", "track ticket", "view ticket", "my booking", "check booking", "ticket details", "status of booking"]
    if any(k in lower for k in booking_status_keywords) or (entities["booking_id"] and not any(k in lower for k in ["cancel", "refund", "reschedule"])):
        return "booking_status", entities

    # 10. Booking Help / Booking Procedure
    booking_help_keywords = ["how do i book a ticket", "how can i book a ticket", "how to book", "booking procedure", "ticket booking steps", "how to buy ticket", "booking help"]
    if any(k in lower for k in booking_help_keywords):
        return "booking_help", entities

    # 11. Seat Availability
    seat_keywords = ["seat availability", "available seats", "seats available", "is pb", "how many seats", "seat vacancy", "vacant seats", "are there seats", "check seat"]
    if any(k in lower for k in seat_keywords):
        return "seat_availability", entities

    # 12. Fare / Price
    fare_keywords = ["fare", "ticket price", "ticket cost", "how much is", "how much does", "buses under", "cost of ticket", "cheapest bus", "pricing", "rate"]
    if any(k in lower for k in fare_keywords) or entities["max_fare"] is not None:
        return "fare", entities

    # 13. Boarding Point
    boarding_keywords = ["boarding point", "pickup point", "pickup location", "where to board", "where is boarding", "boarding stop"]
    if any(k in lower for k in boarding_keywords):
        return "boarding_point", entities

    # 14. Dropping Point
    dropping_keywords = ["dropping point", "drop point", "drop location", "where does it drop", "destination stop", "arrival point"]
    if any(k in lower for k in dropping_keywords):
        return "dropping_point", entities

    # 15. Timings / Schedules
    timing_keywords = ["timing", "timings", "what time", "departure time", "bus timing", "schedule", "when does it leave", "arrival time", "bus schedule"]
    if any(k in lower for k in timing_keywords):
        return "timing", entities

    # 16. Bus Search (Route specific or general "find a bus")
    if any(k in lower for k in ["find a bus", "search bus", "find buses", "available buses", "book bus", "need a bus"]) or (entities["source"] and entities["destination"]) or (entities["source"] or entities["destination"]):
        return "bus_search", entities

    # 17. FAQs
    faq_keywords = ["faq", "frequently asked questions", "common questions", "luggage", "baggage", "delay", "passenger name", "reach boarding"]
    if any(k in lower for k in faq_keywords):
        return "faq", entities

    # 18. Fallback / Unknown
    return "unknown", entities
