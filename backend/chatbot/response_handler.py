"""
Response Handler for PinkBus Customer Support Chatbot
Generates structured responses, interactive card payloads, and contextual quick actions.
"""

from typing import Dict, Any, List
import database
from chatbot.context_manager import context_store

DEFAULT_QUICK_ACTIONS = [
    "Find a Bus",
    "Check Seat Availability",
    "Check Fare",
    "Booking Help",
    "Cancel Ticket",
    "Refund Information",
    "Reschedule Ticket",
    "FAQs",
    "Talk to Support"
]

def handle_user_message(text: str, session_id: str, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
    """Processes user message, updates context, queries database, and constructs response."""
    context = context_store.get_session(session_id)

    # 1. Clear / Reset Chat
    if intent == "clear_chat":
        context_store.reset_session(session_id)
        return {
            "text": "Chat session has been cleared. How may I assist you today?",
            "intent": "clear_chat",
            "quick_actions": DEFAULT_QUICK_ACTIONS,
            "cards_type": None,
            "data": None
        }

    # 2. Greeting
    if intent == "greeting":
        context_store.clear_pending(session_id)
        return {
            "text": (
                "Hi! 👋 Welcome to PinkBus Support.\n\n"
                "I'm your virtual travel assistant. I can help you with bus availability, "
                "timings, fares, bookings, cancellations, refunds and more.\n\n"
                "How can I help you today?"
            ),
            "intent": "greeting",
            "quick_actions": DEFAULT_QUICK_ACTIONS,
            "cards_type": None,
            "data": None
        }

    # 3. Help Overview
    if intent == "help_overview":
        return {
            "text": (
                "Here are the travel support services I can assist you with:\n\n"
                "• **Bus Availability**: Search buses across major Maharashtra & Goa routes\n"
                "• **Schedules & Timings**: Check departure, arrival, and travel duration\n"
                "• **Boarding & Dropping**: Precise pickup and drop locations\n"
                "• **Seat Vacancies**: Real-time seat counts on any bus\n"
                "• **Fares & Pricing**: Fares from ₹380 and budget filters\n"
                "• **Booking Assistance**: Step-by-step booking guide & mock ticket lookups\n"
                "• **Cancellations & Refunds**: Instant demo ticket cancellations & refund calculations\n"
                "• **Ticket Rescheduling**: Rescheduling policy & date modifications\n"
                "• **FAQs & Support**: Instant answers to common questions and agent ticket creation"
            ),
            "intent": "help_overview",
            "quick_actions": ["Find a Bus", "Check Seat Availability", "Check Booking PB10001", "Talk to Support"],
            "cards_type": None,
            "data": None
        }

    # 4. Bus Search / Route Information
    if intent in ["bus_search", "bus_search_date_provided"]:
        src = entities.get("source") or context.get("source")
        dst = entities.get("destination") or context.get("destination")
        max_fare = entities.get("max_fare")
        travel_date = entities.get("travel_date") or context.get("travel_date")

        # Case A: Neither source nor destination provided (e.g. user clicked "Find a Bus")
        if not src and not dst:
            return {
                "text": "Where would you like to travel? Please mention your pickup and destination cities (e.g., *'Pune to Mumbai'* or *'Mumbai to Goa'*).",
                "intent": "bus_search",
                "quick_actions": ["Pune to Mumbai", "Mumbai to Pune", "Pune to Goa", "Kolhapur to Pune", "Nashik to Mumbai"],
                "cards_type": None,
                "data": None
            }

        # Case B: Only Source provided
        if src and not dst:
            context_store.update_session(session_id, source=src)
            return {
                "text": f"Great! Departing from **{src}**. What is your destination city? (e.g., Mumbai, Goa, Kolhapur)",
                "intent": "bus_search",
                "quick_actions": ["to Mumbai", "to Goa", "to Kolhapur"],
                "cards_type": None,
                "data": None
            }

        # Case C: Only Destination provided
        if dst and not src:
            context_store.update_session(session_id, destination=dst)
            return {
                "text": f"Heading to **{dst}**! What is your departure city? (e.g., Pune, Mumbai, Kolhapur, Nashik)",
                "intent": "bus_search",
                "quick_actions": ["from Pune", "from Mumbai", "from Kolhapur"],
                "cards_type": None,
                "data": None
            }

        # Case D: Both Source and Destination provided
        context_store.update_session(session_id, source=src, destination=dst)

        # If travel_date is missing, prompt for it
        if not travel_date and intent != "bus_search_date_provided":
            context_store.update_session(session_id, pending_intent="bus_search_need_date")
            return {
                "text": f"Sure! What date would you like to travel from **{src}** to **{dst}**?",
                "intent": "bus_search_need_date",
                "quick_actions": ["Today", "Tomorrow", "Day after tomorrow", "Next Monday"],
                "cards_type": None,
                "data": {
                    "source": src,
                    "destination": dst
                }
            }

        # Travel date is present (or default "Tomorrow")
        final_date = travel_date or "Tomorrow"
        context_store.update_session(session_id, travel_date=final_date, pending_intent=None)

        # Query database for matching buses
        buses = database.search_buses(source=src, destination=dst, max_fare=max_fare)

        if buses:
            # Set the first bus as last_bus_number for follow-ups
            context_store.update_session(session_id, last_bus_number=buses[0]["bus_number"])
            fare_msg = f" under ₹{max_fare}" if max_fare else ""
            return {
                "text": f"Found **{len(buses)}** PinkBus service(s) for **{src} → {dst}**{fare_msg} on **{final_date}**:",
                "intent": "bus_search_results",
                "quick_actions": ["Check Seat Availability", "How to book a ticket?", "Refund Policy", "Talk to Support"],
                "cards_type": "buses",
                "data": {
                    "source": src,
                    "destination": dst,
                    "travel_date": final_date,
                    "buses": buses
                }
            }
        else:
            return {
                "text": (
                    f"Sorry, we currently do not have direct PinkBus services between **{src}** and **{dst}**.\n\n"
                    "Our active serviced routes include:\n"
                    "• Pune ⇄ Mumbai\n"
                    "• Pune ⇄ Goa\n"
                    "• Kolhapur ⇄ Pune\n"
                    "• Mumbai ⇄ Goa\n"
                    "• Nashik ⇄ Mumbai"
                ),
                "intent": "bus_search_empty",
                "quick_actions": ["Pune to Mumbai", "Mumbai to Pune", "Pune to Goa", "Kolhapur to Pune"],
                "cards_type": None,
                "data": None
            }

    # 5. Seat Availability
    if intent == "seat_availability":
        bus_num = entities.get("bus_number") or context.get("last_bus_number")
        src = entities.get("source") or context.get("source")
        dst = entities.get("destination") or context.get("destination")

        if bus_num:
            bus = database.get_bus_by_number(bus_num)
            if bus:
                context_store.update_session(session_id, last_bus_number=bus["bus_number"])
                return {
                    "text": (
                        f"**{bus['bus_number']} ({bus['bus_name']})** on the **{bus['source']} → {bus['destination']}** route "
                        f"currently has **{bus['available_seats']} seats available** out of {bus['total_seats']}.\n\n"
                        f"• Bus Type: {bus['bus_type']}\n"
                        f"• Fare: ₹{bus['fare']}\n"
                        f"• Departure: {bus['departure_time']} ({bus['boarding_point']})"
                    ),
                    "intent": "seat_availability",
                    "quick_actions": [f"What is the fare for {bus['bus_number']}?", f"Boarding point for {bus['bus_number']}", "How to book a ticket?", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": [bus]}
                }

        if src and dst:
            buses = database.search_buses(source=src, destination=dst)
            if buses:
                avail_summary = "\n".join([f"• **{b['bus_number']}** ({b['bus_name']}): **{b['available_seats']} open seats** (Dep: {b['departure_time']})" for b in buses[:4]])
                return {
                    "text": f"Here is the current seat availability for **{src} → {dst}** buses:\n\n{avail_summary}",
                    "intent": "seat_availability",
                    "quick_actions": [f"Details of {buses[0]['bus_number']}", "How to book a ticket?", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": buses}
                }

        # Prompt user for bus number or route
        return {
            "text": "Which bus or route would you like to check seat availability for? (e.g., *'PB102'* or *'Pune to Mumbai'*).",
            "intent": "seat_availability_prompt",
            "quick_actions": ["Is PB102 available?", "Seats on Pune to Mumbai", "PB301 seat availability"],
            "cards_type": None,
            "data": None
        }

    # 6. Fare / Pricing
    if intent == "fare":
        bus_num = entities.get("bus_number") or context.get("last_bus_number")
        src = entities.get("source") or context.get("source")
        dst = entities.get("destination") or context.get("destination")
        max_fare = entities.get("max_fare")

        # If max_fare constraint given (e.g., "buses under 700")
        if max_fare is not None:
            buses = database.search_buses(source=src, destination=dst, max_fare=max_fare)
            if not buses and not src:
                # If no route was given, search all buses under max_fare
                all_b = database.get_all_buses()
                buses = [b for b in all_b if b["fare"] <= max_fare]
            
            if buses:
                return {
                    "text": f"Found **{len(buses)}** PinkBus option(s) with fares under **₹{max_fare}**:",
                    "intent": "fare_filtered",
                    "quick_actions": ["Check Seat Availability", "How to book a ticket?", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": buses}
                }
            else:
                return {
                    "text": f"No buses found with fare under ₹{max_fare}. Lowest fares start at ₹380 on routes like Nashik → Mumbai and ₹450 on Kolhapur → Pune.",
                    "intent": "fare_filtered_empty",
                    "quick_actions": ["Pune to Mumbai", "Kolhapur to Pune", "Nashik to Mumbai"],
                    "cards_type": None,
                    "data": None
                }

        if bus_num:
            bus = database.get_bus_by_number(bus_num)
            if bus:
                return {
                    "text": (
                        f"The fare for **{bus['bus_number']} ({bus['bus_name']})** from **{bus['source']} to {bus['destination']}** "
                        f"is **₹{bus['fare']}** per passenger.\n\n"
                        f"• Service Type: {bus['bus_type']}\n"
                        f"• Departure: {bus['departure_time']} ({bus['boarding_point']})\n"
                        f"• Available Seats: {bus['available_seats']}"
                    ),
                    "intent": "fare",
                    "quick_actions": [f"Available seats on {bus['bus_number']}", "How to book a ticket?", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": [bus]}
                }

        if src and dst:
            buses = database.search_buses(source=src, destination=dst)
            if buses:
                fares = [b["fare"] for b in buses]
                min_f, max_f = min(fares), max(fares)
                return {
                    "text": f"Fares for **{src} → {dst}** range between **₹{min_f}** and **₹{max_f}** depending on bus class (Seater, Semi-Sleeper, Luxury Sleeper):",
                    "intent": "fare",
                    "quick_actions": ["Check Seat Availability", "Show buses under ₹700", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": buses}
                }

        return {
            "text": "PinkBus fares start from ₹380 depending on the route and bus type (AC Seater, Semi-Sleeper, Multi-Axle Luxury Sleeper). Which route or bus would you like fare details for?",
            "intent": "fare_prompt",
            "quick_actions": ["How much is Pune to Mumbai?", "How much does PB102 cost?", "Show buses under ₹700"],
            "cards_type": None,
            "data": None
        }

    # 7. Timings / Schedules
    if intent == "timing":
        bus_num = entities.get("bus_number") or context.get("last_bus_number")
        src = entities.get("source") or context.get("source")
        dst = entities.get("destination") or context.get("destination")

        if bus_num:
            bus = database.get_bus_by_number(bus_num)
            if bus:
                return {
                    "text": (
                        f"⏰ **{bus['bus_number']} ({bus['bus_name']})** Schedule:\n\n"
                        f"• Route: {bus['source']} → {bus['destination']}\n"
                        f"• Departure Time: **{bus['departure_time']}** from {bus['boarding_point']}\n"
                        f"• Arrival Time: **{bus['arrival_time']}** at {bus['dropping_point']}\n"
                        f"• Duration: {bus['duration']}\n"
                        f"• Fare: ₹{bus['fare']} | Seats Open: {bus['available_seats']}"
                    ),
                    "intent": "timing",
                    "quick_actions": [f"Check seat availability for {bus['bus_number']}", "Boarding Point", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": [bus]}
                }

        if src and dst:
            buses = database.search_buses(source=src, destination=dst)
            if buses:
                return {
                    "text": f"Here are the scheduled departure & arrival timings for **{src} → {dst}**:",
                    "intent": "timing",
                    "quick_actions": ["Check Seat Availability", "Check Fare", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": buses}
                }

        return {
            "text": "Which bus or route schedule would you like to check? (e.g., *'PB102 timing'* or *'Pune to Mumbai buses'*).",
            "intent": "timing_prompt",
            "quick_actions": ["What time is PB102?", "Pune to Mumbai bus timing", "Next bus to Goa"],
            "cards_type": None,
            "data": None
        }

    # 8. Boarding Point
    if intent == "boarding_point":
        bus_num = entities.get("bus_number") or context.get("last_bus_number")
        if bus_num:
            bus = database.get_bus_by_number(bus_num)
            if bus:
                return {
                    "text": (
                        f"📍 The designated boarding point for **{bus['bus_number']} ({bus['bus_name']})** "
                        f"is **{bus['boarding_point']}**.\n\n"
                        f"• Departure Time: {bus['departure_time']}\n"
                        f"• Note: Please arrive at the pickup location at least 15–30 minutes before departure."
                    ),
                    "intent": "boarding_point",
                    "quick_actions": [f"Dropping point for {bus['bus_number']}", f"Check seat for {bus['bus_number']}", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": [bus]}
                }

        return {
            "text": "Which bus number would you like the boarding point for? (e.g., *'Where is the boarding point for PB102?'*). Boarding points are also shown on each bus card and your ticket.",
            "intent": "boarding_point_prompt",
            "quick_actions": ["Where is boarding point for PB102?", "PB101 boarding point", "Find a Bus"],
            "cards_type": None,
            "data": None
        }

    # 9. Dropping Point
    if intent == "dropping_point":
        bus_num = entities.get("bus_number") or context.get("last_bus_number")
        if bus_num:
            bus = database.get_bus_by_number(bus_num)
            if bus:
                return {
                    "text": (
                        f"🏁 The dropping point for **{bus['bus_number']} ({bus['bus_name']})** "
                        f"is **{bus['dropping_point']}**.\n\n"
                        f"• Estimated Arrival Time: {bus['arrival_time']}\n"
                        f"• Duration: {bus['duration']}"
                    ),
                    "intent": "dropping_point",
                    "quick_actions": [f"Boarding point for {bus['bus_number']}", f"Check fare for {bus['bus_number']}", "Talk to Support"],
                    "cards_type": "buses",
                    "data": {"buses": [bus]}
                }

        return {
            "text": "Which bus number would you like the dropping point for? (e.g., *'Dropping point for PB102'*).",
            "intent": "dropping_point_prompt",
            "quick_actions": ["Dropping point for PB102", "Dropping point for PB301", "Find a Bus"],
            "cards_type": None,
            "data": None
        }

    # 10. Booking Status & Ticket Information
    if intent == "booking_status":
        b_id = entities.get("booking_id") or context.get("last_booking_id")

        if b_id:
            booking = database.get_booking(b_id)
            if booking:
                context_store.update_session(session_id, last_booking_id=booking["booking_id"], pending_intent=None)
                return {
                    "text": f"Here are the details for Booking ID **{booking['booking_id']}**:",
                    "intent": "booking_status",
                    "quick_actions": ["Cancel Ticket", "Reschedule Ticket", "FAQs", "Talk to Support"],
                    "cards_type": "booking",
                    "data": booking
                }
            else:
                return {
                    "text": f"We could not find any booking matching ID **{b_id}**.\n\nPlease check your ticket number. Demo booking IDs in this system include: **PB10001**, **PB10002**, **PB10003**, **PB10004**, **PB10005**.",
                    "intent": "booking_not_found",
                    "quick_actions": ["Check booking PB10001", "Check booking PB10002", "Talk to Support"],
                    "cards_type": None,
                    "data": None
                }

        # No booking ID provided -> prompt for it
        context_store.update_session(session_id, pending_intent="need_booking_id_status")
        return {
            "text": "Please provide your 7-character Booking ID (e.g., **PB10001**) to check your booking status.",
            "intent": "booking_status_need_id",
            "quick_actions": ["PB10001", "PB10002", "PB10005"],
            "cards_type": None,
            "data": None
        }

    # 11. Booking Help (Required exact text)
    if intent == "booking_help":
        return {
            "text": (
                "To book a PinkBus ticket:\n\n"
                "1. Enter your source and destination.\n"
                "2. Select your travel date.\n"
                "3. Choose an available bus.\n"
                "4. Select your seat.\n"
                "5. Enter passenger details.\n"
                "6. Review the fare.\n"
                "7. Confirm your booking.\n\n"
                "For this demo, I can help you find available buses."
            ),
            "intent": "booking_help",
            "quick_actions": ["Find a Bus", "Check Seat Availability", "Check Fare", "Talk to Support"],
            "cards_type": None,
            "data": None
        }

    # 12. Cancellation
    if intent == "cancellation":
        b_id = entities.get("booking_id") or context.get("last_booking_id")

        if b_id:
            booking = database.get_booking(b_id)
            if booking:
                if booking["status"] == "Cancelled":
                    return {
                        "text": f"Booking **{booking['booking_id']}** is already marked as **Cancelled**.\n\nRefund status: 80% refund processed in demo mode.",
                        "intent": "cancellation_already",
                        "quick_actions": ["Refund Information", "Find a Bus", "Talk to Support"],
                        "cards_type": "booking",
                        "data": booking
                    }
                if booking["status"] == "Completed":
                    return {
                        "text": f"Booking **{booking['booking_id']}** has already been completed and cannot be cancelled.",
                        "intent": "cancellation_completed",
                        "quick_actions": ["Find a Bus", "Talk to Support"],
                        "cards_type": "booking",
                        "data": booking
                    }

                # Perform demo cancellation in database
                updated_booking = database.cancel_booking(b_id)
                refund_amt = int(round(updated_booking["fare"] * 0.8))
                return {
                    "text": (
                        f"✅ Booking **{updated_booking['booking_id']}** has been successfully cancelled in demo mode.\n\n"
                        f"💰 **Demo Refund Calculation:**\n"
                        f"• Ticket Fare: ₹{updated_booking['fare']}\n"
                        f"• Refund Eligible: 80% (>24h cancellation tier)\n"
                        f"• Refund Amount: **₹{refund_amt}**\n\n"
                        f"⚠️ *[DEMO NOTICE: This is a simulated cancellation. No real funds were charged or refunded.]*"
                    ),
                    "intent": "cancellation_success",
                    "quick_actions": ["Refund Policy", "Find a Bus", "Talk to Support"],
                    "cards_type": "booking",
                    "data": updated_booking
                }
            else:
                return {
                    "text": f"Could not find booking **{b_id}** to cancel. Please verify your booking reference.",
                    "intent": "cancellation_not_found",
                    "quick_actions": ["Cancel booking PB10001", "Talk to Support"],
                    "cards_type": None,
                    "data": None
                }

        # If booking ID not provided
        context_store.update_session(session_id, pending_intent="need_booking_id_cancel")
        return {
            "text": (
                "To cancel your ticket, please provide your Booking ID (e.g., **PB10001**).\n\n"
                "**Demo Refund Policy:**\n"
                "• More than 24 hours before departure: 80% refund\n"
                "• 12–24 hours before departure: 50% refund\n"
                "• Less than 12 hours before departure: No refund\n\n"
                "*[DEMO NOTICE: This is a simulated demo policy for the internship project demonstration. No real payments or refunds are processed.]*"
            ),
            "intent": "cancellation_need_id",
            "quick_actions": ["Cancel booking PB10001", "Cancel booking PB10005", "Refund Policy"],
            "cards_type": "policy",
            "data": {
                "title": "Demo Cancellation & Refund Policy",
                "policy_type": "cancellation_refund"
            }
        }

    # 13. Refund Information
    if intent == "refund":
        return {
            "text": (
                "**Demo Refund Policy:**\n\n"
                "• More than 24 hours before departure: **80% refund**\n"
                "• 12–24 hours before departure: **50% refund**\n"
                "• Less than 12 hours before departure: **No refund**\n\n"
                "[DEMO NOTICE: This is a simulated demo policy for the internship project demonstration. No real payments or refunds are processed.]"
            ),
            "intent": "refund",
            "quick_actions": ["Cancel Ticket", "Check Booking PB10001", "Talk to Support"],
            "cards_type": "policy",
            "data": {
                "title": "Demo Cancellation & Refund Policy",
                "policy_type": "cancellation_refund"
            }
        }

    # 14. Rescheduling
    if intent == "reschedule":
        b_id = entities.get("booking_id") or context.get("last_booking_id")

        if b_id:
            booking = database.get_booking(b_id)
            if booking:
                return {
                    "text": (
                        f"Rescheduling details for Booking ID **{booking['booking_id']}** ({booking['source']} → {booking['destination']}):\n\n"
                        f"**Demo Rescheduling Policy:**\n"
                        f"• Rescheduling is permitted up to 12 hours before departure.\n"
                        f"• Free date change on the same route.\n"
                        f"• Fare difference applies if you choose a higher fare bus class.\n"
                        f"• Rescheduled tickets cannot be cancelled for a refund.\n\n"
                        f"*[DEMO NOTICE: Rescheduling is simulated for demonstration purposes.]*"
                    ),
                    "intent": "reschedule_details",
                    "quick_actions": ["Find a Bus", "Talk to Support"],
                    "cards_type": "booking",
                    "data": booking
                }

        context_store.update_session(session_id, pending_intent="need_booking_id_reschedule")
        return {
            "text": (
                "Yes, you can reschedule your ticket up to 12 hours before departure!\n\n"
                "Please provide your Booking ID (e.g., **PB10001**) to proceed with demo rescheduling.\n\n"
                "**Demo Rescheduling Policy:**\n"
                "• Free date alteration for the same route.\n"
                "• Subject to seat availability.\n"
                "• Difference in fare is payable if upgrading bus category.\n\n"
                "*[DEMO NOTICE: Rescheduling is simulated for demonstration purposes.]*"
            ),
            "intent": "reschedule_need_id",
            "quick_actions": ["Check booking PB10001", "Check booking PB10004", "Talk to Support"],
            "cards_type": "policy",
            "data": {
                "title": "Demo Rescheduling Policy",
                "policy_type": "rescheduling"
            }
        }

    # 15. Human Support Escalation
    if intent == "support":
        return {
            "text": "Sure! I can help you connect with customer support.",
            "intent": "support",
            "quick_actions": ["Create Support Request", "FAQs", "Find a Bus"],
            "cards_type": "support_card",
            "data": {
                "phone": "+91-XXXXXXXXXX",
                "email": "support@pinkbus.demo",
                "hours": "9:00 AM – 9:00 PM",
                "demo_notice": "DEMO NOTICE: These are simulated support contact details for technical evaluation."
            }
        }

    # 16. FAQs
    if intent == "faq":
        matched_faq = database.search_faqs(text)
        if matched_faq:
            return {
                "text": f"**Q: {matched_faq['question']}**\n\n{matched_faq['answer']}",
                "intent": "faq_answer",
                "quick_actions": ["More FAQs", "Booking Help", "Talk to Support"],
                "cards_type": "faq_item",
                "data": matched_faq
            }
        else:
            faqs = database.get_all_faqs()
            return {
                "text": "Here are our most frequently asked questions. Click any question to see the answer, or type your query:",
                "intent": "faqs_list",
                "quick_actions": [f["question"] for f in faqs[:4]],
                "cards_type": "faqs",
                "data": {"faqs": faqs}
            }

    # 17. Unknown / Fallback (Required exact text)
    return {
        "text": (
            "Sorry, I couldn't understand your request.\n\n"
            "I can help you with:\n\n"
            "• Bus availability\n"
            "• Timings\n"
            "• Seat availability\n"
            "• Fare\n"
            "• Booking\n"
            "• Cancellation\n"
            "• Refund\n"
            "• Rescheduling\n"
            "• FAQs\n"
            "• Customer support"
        ),
        "intent": "unknown",
        "quick_actions": DEFAULT_QUICK_ACTIONS,
        "cards_type": None,
        "data": None
    }
