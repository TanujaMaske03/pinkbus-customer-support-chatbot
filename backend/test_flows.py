import sys
import json
sys.stdout.reconfigure(encoding='utf-8')
from app import app

client = app.test_client()

def test_chat(msg, session_id='test1'):
    res = client.post('/api/chat', data=json.dumps({'message': msg, 'session_id': session_id}), content_type='application/json')
    d = res.get_json()
    print(f"USER: {msg}")
    print(f"INTENT: {d.get('intent')}")
    print(f"BOT: {d['response']['text'][:100]}...")
    if d['response']['cards_type']:
        print(f"CARDS: {d['response']['cards_type']}")
    print("-" * 50)

print("=== RUNNING SCENARIO TESTS ===")
test_chat("Hi")
test_chat("I need a bus from Pune to Mumbai")
test_chat("Tomorrow")
test_chat("Are seats available?")
test_chat("What is the fare?")
test_chat("Where is the boarding point?")
test_chat("Check my booking PB10001")
test_chat("What is the refund policy?")
test_chat("I want to talk to customer support")
test_chat("What is the capital of Mars?")

print("=== TESTING ALL REMAINING SCENARIOS ===")
test_chat("What can you help me with?")
test_chat("Find a bus")
test_chat("Show available buses")
test_chat("Where is the dropping point for PB102?")
test_chat("What is my booking status?")
test_chat("Cancel booking PB10001")
test_chat("Can I change my travel date?")
test_chat("How do I book a ticket?")
test_chat("What luggage allowance is permitted on PinkBus?")
test_chat("Clear chat")

