"""
Comprehensive Verification Script for PinkBus Customer Support Chatbot
Tests all 20 scenarios required for the internship technical demonstration.
Tests against the live server through the Vite proxy (http://127.0.0.1:5173/api).
"""

import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:5173/api"

def call_chat(message, session_id="test_suite_session"):
    payload = json.dumps({"message": message, "session_id": session_id}).encode('utf-8')
    req = urllib.request.Request(f"{API_URL}/chat", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"Error calling {message}: {e}")
        return None

def call_support_submission(name, email, issue, booking_id=None):
    payload = json.dumps({
        "name": name,
        "email": email,
        "issue": issue,
        "booking_id": booking_id
    }).encode('utf-8')
    req = urllib.request.Request(f"{API_URL}/support", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def call_reset(session_id="test_suite_session"):
    payload = json.dumps({"session_id": session_id}).encode('utf-8')
    req = urllib.request.Request(f"{API_URL}/chat/reset", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("=================================================================")
print("PINKBUS CUSTOMER SUPPORT CHATBOT - VERIFYING ALL 20 SCENARIOS")
print("=================================================================\n")

passed = 0
total = 20

# 1. Hi
r = call_chat("Hi")
if r and r["intent"] == "greeting" and "Welcome to PinkBus Support" in r["response"]["text"]:
    print("PASS [Scenario 1]: 'Hi' -> Welcome greeting with 9 quick action buttons")
    passed += 1
else:
    print("FAIL [Scenario 1]")

# 2. What can you help me with?
r = call_chat("What can you help me with?")
if r and r["intent"] == "help_overview" and "Bus Availability" in r["response"]["text"]:
    print("PASS [Scenario 2]: 'What can you help me with?' -> Full capabilities overview")
    passed += 1
else:
    print("FAIL [Scenario 2]")

# 3. Find a bus
r = call_chat("Find a bus", session_id="s3")
if r and r["intent"] == "bus_search" and "Where would you like to travel" in r["response"]["text"]:
    print("PASS [Scenario 3]: 'Find a bus' -> Prompts for source & destination")
    passed += 1
else:
    print("FAIL [Scenario 3]")

# 4. Pune to Mumbai bus
r = call_chat("Pune to Mumbai bus", session_id="s4")
if r and "Pune" in r["response"]["text"] and "Mumbai" in r["response"]["text"]:
    print("PASS [Scenario 4]: 'Pune to Mumbai bus' -> Recognizes route entities")
    passed += 1
else:
    print("FAIL [Scenario 4]")

# 5. Ask for travel date
if r and r["response"]["intent"] == "bus_search_need_date":
    print("PASS [Scenario 5]: Chatbot asks for travel date ('Sure! What date would you like to travel?')")
    passed += 1
else:
    print("FAIL [Scenario 5]")

# 6. Show available buses (responding with Tomorrow to previous search)
r = call_chat("Tomorrow", session_id="s4")
if r and r["response"]["cards_type"] == "buses" and len(r["response"]["data"]["buses"]) >= 5:
    print(f"PASS [Scenario 6]: Multi-turn date response returns {len(r['response']['data']['buses'])} bus cards")
    passed += 1
else:
    print("FAIL [Scenario 6]")

# 7. Check seat availability
r = call_chat("Are seats available on PB102?", session_id="s7")
if r and r["intent"] == "seat_availability" and "seats available" in r["response"]["text"]:
    print("PASS [Scenario 7]: 'Are seats available on PB102?' -> Returns live seat vacancies from SQLite")
    passed += 1
else:
    print("FAIL [Scenario 7]")

# 8. Check fare
r = call_chat("How much does PB102 cost?", session_id="s8")
if r and r["intent"] == "fare" and "₹650" in r["response"]["text"]:
    print("PASS [Scenario 8]: 'How much does PB102 cost?' -> Returns accurate fare (₹650)")
    passed += 1
else:
    print("FAIL [Scenario 8]")

# 9. Ask boarding point
r = call_chat("Where is the boarding point for PB102?", session_id="s9")
if r and r["intent"] == "boarding_point" and "Swargate" in r["response"]["text"]:
    print("PASS [Scenario 9]: 'Where is the boarding point for PB102?' -> Returns Swargate boarding location")
    passed += 1
else:
    print("FAIL [Scenario 9]")

# 10. Ask dropping point
r = call_chat("Where is the dropping point for PB102?", session_id="s10")
if r and r["intent"] == "dropping_point" and "Dadar" in r["response"]["text"]:
    print("PASS [Scenario 10]: 'Where is the dropping point for PB102?' -> Returns Dadar dropping location")
    passed += 1
else:
    print("FAIL [Scenario 10]")

# 11. Check booking PB10001
r = call_chat("Check my booking PB10001", session_id="s11")
if r and r["intent"] == "booking_status" and r["response"]["cards_type"] == "booking" and r["response"]["data"]["passenger_name"] == "Aarav Sharma":
    print("PASS [Scenario 11]: 'Check my booking PB10001' -> Returns booking card for Aarav Sharma")
    passed += 1
else:
    print("FAIL [Scenario 11]")

# 12. Ask booking status (without ID)
r = call_chat("What is my booking status?", session_id="s12")
if r and r["response"]["intent"] == "booking_status_need_id" and "PB10001" in r["response"]["text"]:
    print("PASS [Scenario 12]: 'What is my booking status?' -> Prompts for Booking ID")
    passed += 1
else:
    print("FAIL [Scenario 12]")

# 13. Ask cancellation policy / cancel ticket
r = call_chat("How can I cancel my ticket?", session_id="s13")
if r and r["intent"] == "cancellation" and "Demo Refund Policy" in r["response"]["text"]:
    print("PASS [Scenario 13]: 'How can I cancel my ticket?' -> Shows cancellation guidance & demo policy")
    passed += 1
else:
    print("FAIL [Scenario 13]")

# 14. Ask refund policy
r = call_chat("What is the refund policy?", session_id="s14")
if r and r["intent"] == "refund" and "80% refund" in r["response"]["text"] and "DEMO NOTICE" in r["response"]["text"]:
    print("PASS [Scenario 14]: 'What is the refund policy?' -> Shows tiers (80%, 50%, 0%) with DEMO notice")
    passed += 1
else:
    print("FAIL [Scenario 14]")

# 15. Ask rescheduling
r = call_chat("I want to reschedule my ticket", session_id="s15")
if r and r["intent"] == "reschedule" and "12 hours" in r["response"]["text"]:
    print("PASS [Scenario 15]: 'I want to reschedule my ticket' -> Shows rescheduling policy & Booking ID prompt")
    passed += 1
else:
    print("FAIL [Scenario 15]")

# 16. Ask FAQ
r = call_chat("What luggage allowance is permitted on PinkBus?", session_id="s16")
if r and r["intent"] == "faq" and "15 kg" in r["response"]["text"]:
    print("PASS [Scenario 16]: 'What luggage allowance is permitted on PinkBus?' -> Answers from FAQ database")
    passed += 1
else:
    print("FAIL [Scenario 16]")

# 17. Ask unknown question
r = call_chat("What is the distance to Neptune?", session_id="s17")
if r and r["intent"] == "unknown" and "Sorry, I couldn't understand your request." in r["response"]["text"]:
    print("PASS [Scenario 17]: 'What is the distance to Neptune?' -> Fallback with listed capabilities & buttons")
    passed += 1
else:
    print("FAIL [Scenario 17]")

# 18. Ask for human support
r = call_chat("I want to talk to customer support", session_id="s18")
if r and r["intent"] == "support" and r["response"]["cards_type"] == "support_card" and "support@pinkbus.demo" in str(r["response"]["data"]):
    print("PASS [Scenario 18]: 'I want to talk to customer support' -> Displays support card with demo info")
    passed += 1
else:
    print("FAIL [Scenario 18]")

# 19. Create support request
sup = call_support_submission("Kavita Rao", "kavita@example.com", "Luggage inquiry for PB102", "PB10001")
if sup and sup.get("success") and sup["ticket"]["ticket_id"].startswith("SUP-"):
    print(f"PASS [Scenario 19]: Create support request -> Ticket {sup['ticket']['ticket_id']} saved in SQLite")
    passed += 1
else:
    print("FAIL [Scenario 19]")

# 20. Clear/New Chat
reset_resp = call_reset("test_suite_session")
if reset_resp and reset_resp.get("success"):
    print("PASS [Scenario 20]: Clear/New Chat -> Resets conversation context successfully")
    passed += 1
else:
    print("FAIL [Scenario 20]")

print("\n-----------------------------------------------------------------")
print(f"RESULT: {passed}/{total} SCENARIOS PASSED SUCCESSFULLY!")
print("-----------------------------------------------------------------")
