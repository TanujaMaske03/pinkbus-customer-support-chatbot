import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'pinkbus.db')

def get_db():
    """Returns a SQLite connection with Row factory enabled."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes tables and seeds initial data if not already present."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    # Buses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL UNIQUE,
            bus_name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            duration TEXT NOT NULL,
            boarding_point TEXT NOT NULL,
            dropping_point TEXT NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL,
            fare INTEGER NOT NULL,
            bus_type TEXT NOT NULL
        )
    ''')

    # Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id TEXT NOT NULL UNIQUE,
            passenger_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            bus_number TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            travel_date TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            fare INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    # FAQs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL,
            keywords TEXT NOT NULL
        )
    ''')

    # Policies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_type TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')

    # Support requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            booking_id TEXT,
            issue TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()

    # Seed buses if empty
    cursor.execute('SELECT COUNT(*) FROM buses')
    if cursor.fetchone()[0] == 0:
        sample_buses = [
            ("PB101", "Pink Express", "Pune", "Mumbai", "06:00 AM", "09:30 AM", "3h 30m", "Swargate", "Dadar", 40, 14, 550, "AC Seater (2+2)"),
            ("PB102", "Pink Express", "Pune", "Mumbai", "08:30 AM", "12:00 PM", "3h 30m", "Swargate", "Dadar", 40, 18, 650, "AC Sleeper (2+1)"),
            ("PB103", "Shivshahi AC", "Pune", "Mumbai", "01:15 PM", "04:45 PM", "3h 30m", "Wakad Bypass", "Vashi", 45, 22, 500, "AC Semi-Sleeper"),
            ("PB104", "Pink Royal Cruiser", "Pune", "Mumbai", "05:30 PM", "09:00 PM", "3h 30m", "Hinjawadi Flyover", "Borivali", 36, 9, 750, "Multi-Axle Luxury AC"),
            ("PB105", "Pink Night Rider", "Pune", "Mumbai", "11:00 PM", "02:30 AM", "3h 30m", "Pune Station", "Dadar", 38, 25, 600, "AC Sleeper (2+1)"),
            ("PB201", "Pink Express", "Mumbai", "Pune", "06:30 AM", "10:00 AM", "3h 30m", "Dadar East", "Swargate", 40, 16, 550, "AC Seater (2+2)"),
            ("PB202", "Pink Royal Cruiser", "Mumbai", "Pune", "10:00 AM", "01:30 PM", "3h 30m", "Borivali", "Wakad Bypass", 36, 11, 750, "Multi-Axle Luxury AC"),
            ("PB203", "Shivshahi AC", "Mumbai", "Pune", "03:00 PM", "06:30 PM", "3h 30m", "Vashi Plaza", "Swargate", 45, 20, 500, "AC Semi-Sleeper"),
            ("PB204", "Pink Night Rider", "Mumbai", "Pune", "11:30 PM", "03:00 AM", "3h 30m", "Dadar", "Pune Station", 38, 30, 600, "AC Sleeper (2+1)"),
            ("PB301", "Goa Pink Wave", "Pune", "Goa", "07:00 PM", "06:00 AM", "11h 00m", "Swargate / Katraj", "Panjim KTC", 36, 12, 1100, "AC Sleeper (2+1)"),
            ("PB302", "Goa Sunset Express", "Pune", "Goa", "09:30 PM", "08:30 AM", "11h 00m", "Wakad / Chandani Chowk", "Mapusa", 32, 7, 1350, "Multi-Axle Sleeper"),
            ("PB303", "Pink Coastal Cruiser", "Pune", "Goa", "10:45 PM", "09:45 AM", "11h 00m", "Swargate", "Madgaon", 36, 15, 1200, "AC Sleeper (2+1)"),
            ("PB401", "Goa Pink Wave", "Goa", "Pune", "06:30 PM", "05:30 AM", "11h 00m", "Panjim KTC", "Swargate", 36, 14, 1100, "AC Sleeper (2+1)"),
            ("PB402", "Goa Sunrise Cruiser", "Goa", "Pune", "08:00 PM", "07:00 AM", "11h 00m", "Mapusa", "Wakad", 32, 9, 1350, "Multi-Axle Sleeper"),
            ("PB501", "Mahalaxmi Superfast", "Kolhapur", "Pune", "05:30 AM", "10:00 AM", "4h 30m", "CBS Kolhapur", "Swargate", 42, 28, 450, "Non-AC Pushback"),
            ("PB502", "Pink City Shuttle", "Kolhapur", "Pune", "11:00 AM", "03:30 PM", "4h 30m", "Kawala Naka", "Katraj", 40, 19, 550, "AC Seater (2+2)"),
            ("PB503", "Pink Star", "Kolhapur", "Pune", "06:00 PM", "10:30 PM", "4h 30m", "CBS Kolhapur", "Swargate", 36, 8, 650, "AC Sleeper (2+1)"),
            ("PB601", "Pink City Shuttle", "Pune", "Kolhapur", "07:00 AM", "11:30 AM", "4h 30m", "Swargate", "CBS Kolhapur", 40, 21, 550, "AC Seater (2+2)"),
            ("PB602", "Mahalaxmi Express", "Pune", "Kolhapur", "02:30 PM", "07:00 PM", "4h 30m", "Katraj", "Kawala Naka", 42, 17, 450, "Non-AC Pushback"),
            ("PB701", "Konkan Princess", "Mumbai", "Goa", "05:00 PM", "07:00 AM", "14h 00m", "Borivali / Dadar", "Panjim KTC", 32, 6, 1400, "Multi-Axle Luxury Sleeper"),
            ("PB702", "Goa Night Rider", "Mumbai", "Goa", "08:00 PM", "10:00 AM", "14h 00m", "Vashi / Sion", "Mapusa", 36, 13, 1250, "AC Sleeper (2+1)"),
            ("PB801", "Konkan Princess", "Goa", "Mumbai", "04:30 PM", "06:30 AM", "14h 00m", "Panjim KTC", "Borivali", 32, 8, 1400, "Multi-Axle Luxury Sleeper"),
            ("PB802", "Goa Night Rider", "Goa", "Mumbai", "07:30 PM", "09:30 AM", "14h 00m", "Mapusa", "Dadar", 36, 11, 1250, "AC Sleeper (2+1)"),
            ("PB901", "Panchavati Express", "Nashik", "Mumbai", "06:00 AM", "09:45 AM", "3h 45m", "CBS Nashik", "Dadar", 45, 31, 380, "AC Semi-Sleeper"),
            ("PB902", "Pink Grape City Link", "Nashik", "Mumbai", "02:00 PM", "05:45 PM", "3h 45m", "Dwarka Circle", "Thane / Dadar", 40, 22, 420, "AC Seater (2+2)"),
            ("PB951", "Panchavati Express", "Mumbai", "Nashik", "07:00 AM", "10:45 AM", "3h 45m", "Dadar", "CBS Nashik", 45, 27, 380, "AC Semi-Sleeper"),
            ("PB952", "Pink Grape City Link", "Mumbai", "Nashik", "04:30 PM", "08:15 PM", "3h 45m", "Thane", "Dwarka Circle", 40, 18, 420, "AC Seater (2+2)")
        ]
        cursor.executemany('''
            INSERT INTO buses (bus_number, bus_name, source, destination, departure_time, arrival_time, duration, boarding_point, dropping_point, total_seats, available_seats, fare, bus_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_buses)
        conn.commit()

    # Seed bookings if empty
    cursor.execute('SELECT COUNT(*) FROM bookings')
    if cursor.fetchone()[0] == 0:
        sample_bookings = [
            ("PB10001", "Aarav Sharma", "+91-9876543210", "PB102", "Pune", "Mumbai", "Tomorrow", "12A", 650, "Confirmed"),
            ("PB10002", "Pooja Patil", "+91-9823012345", "PB301", "Pune", "Goa", "2026-10-05", "07B (Sleeper)", 1100, "Cancelled"),
            ("PB10003", "Rohan Kulkarni", "+91-9765432109", "PB101", "Pune", "Mumbai", "2026-09-28", "15A", 550, "Completed"),
            ("PB10004", "Sneha Deshmukh", "+91-9988776655", "PB701", "Mumbai", "Goa", "2026-10-12", "04U (Upper Sleeper)", 1400, "Rescheduled"),
            ("PB10005", "Vikram Joshi", "+91-9811223344", "PB901", "Nashik", "Mumbai", "Tomorrow", "20B", 380, "Confirmed")
        ]
        cursor.executemany('''
            INSERT INTO bookings (booking_id, passenger_name, phone, bus_number, source, destination, travel_date, seat_number, fare, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_bookings)
        conn.commit()

    # Seed policies if empty
    cursor.execute('SELECT COUNT(*) FROM policies')
    if cursor.fetchone()[0] == 0:
        sample_policies = [
            ("cancellation_refund", "Demo Cancellation & Refund Policy", 
             "• More than 24 hours before departure: 80% refund\n• 12–24 hours before departure: 50% refund\n• Less than 12 hours before departure: No refund\n\n[DEMO NOTICE: This is a simulated demo policy for the internship project demonstration. No real payments or refunds are processed.]"),
            ("rescheduling", "Demo Rescheduling Policy",
             "• Rescheduling is allowed up to 12 hours before departure.\n• Fare difference applies if the new bus fare is higher.\n• Rescheduled tickets cannot be cancelled for a refund.\n\n[DEMO NOTICE: Rescheduling is simulated for demonstration purposes.]")
        ]
        cursor.executemany('''
            INSERT INTO policies (policy_type, title, content)
            VALUES (?, ?, ?)
        ''', sample_policies)
        conn.commit()

    # Seed FAQs if empty
    cursor.execute('SELECT COUNT(*) FROM faqs')
    if cursor.fetchone()[0] == 0:
        sample_faqs = [
            ("How do I book a ticket?", "To book a PinkBus ticket:\n1. Enter your source and destination.\n2. Select your travel date.\n3. Choose an available bus from the list.\n4. Select your preferred seat.\n5. Enter passenger details.\n6. Review the fare.\n7. Confirm your booking.\n\nNote: In this demo interface, you can search buses and view schedules directly through chat.", "Booking", "book ticket booking procedure steps how to book buy ticket"),
            ("How do I cancel my ticket?", "To cancel your ticket, simply type 'Cancel ticket' along with your booking ID (e.g., 'Cancel booking PB10001') or select 'Cancel Ticket' from quick actions. Please note our demo refund policy applies based on hours remaining before departure.", "Cancellation", "cancel ticket cancellation how to cancel drop booking"),
            ("How can I check my booking?", "You can check your booking status anytime by typing 'Check my booking' followed by your Booking ID (e.g., 'Check booking PB10001'). You will see your passenger details, bus number, travel date, seat number, and booking status.", "Booking", "check booking show ticket status booking details my booking"),
            ("How can I find available buses?", "Just type your travel route like 'Pune to Mumbai bus' or click [Find a Bus] in quick actions! We will show available buses, timings, fares, and open seats.", "Bus Search", "find bus search available buses route timings schedule"),
            ("How do I check seat availability?", "You can ask 'Are seats available on PB102?' or 'How many seats are available?' The chatbot will check our live mock database and show real-time seat counts.", "Seats", "seat availability available seats vacancies check seats"),
            ("Can I reschedule my ticket?", "Yes! Rescheduling is permitted up to 12 hours before departure. To reschedule, type 'Reschedule booking' with your booking ID or tap [Reschedule Ticket] to view demo options.", "Rescheduling", "reschedule change travel date change bus postpone advance ticket"),
            ("Where can I find my boarding point?", "Your boarding point is listed on your ticket and in the bus details card (e.g., Swargate, Dadar, CBS). You can also ask 'Where is the boarding point for PB102?'", "Boarding", "boarding point pickup location where to board stop departure point"),
            ("What happens if my bus is delayed?", "In case of unexpected delays, passengers receive SMS/WhatsApp updates with real-time GPS tracking. You can also connect with support for live status updates.", "Support", "bus delayed delay timing late bus tracking"),
            ("How can I check my refund?", "Demo refunds are calculated automatically upon cancellation: 80% if cancelled >24 hrs before departure, 50% if 12-24 hrs before, and 0% if under 12 hrs.", "Refund", "refund policy refund status money back return fare"),
            ("Can I change passenger details?", "Name and age modifications are allowed for minor corrections up to 6 hours before departure by contacting customer care.", "Modification", "change passenger name edit passenger details update passenger"),
            ("How early should I reach the boarding point?", "We recommend arriving at your designated boarding point at least 15 to 30 minutes before the scheduled departure time.", "Boarding", "reach boarding point arrival time when to reach pickup time"),
            ("Can I choose my seat?", "Yes! During ticket booking, you can choose window, aisle, or sleeper berths (lower or upper) from the bus layout.", "Seats", "choose seat select seat window seat sleeper berth"),
            ("How do I contact customer support?", "You can click [Talk to Support] or type 'Talk to human'. Our demo support team is available 9:00 AM – 9:00 PM at support@pinkbus.demo.", "Support", "contact customer support talk to agent human help call executive"),
            ("What should I do if I lose my ticket?", "Don't worry! You can retrieve your ticket anytime by asking 'Check my booking' with your Booking ID or registered mobile number.", "Booking", "lost ticket retrieve ticket find ticket forgot ticket"),
            ("How can I check my ticket details?", "Simply enter 'Check booking PB10001' or provide your Booking ID, and the chatbot will display full ticket details.", "Booking", "ticket details view ticket check ticket confirmation"),
            ("What luggage allowance is permitted on PinkBus?", "Each passenger is permitted up to 15 kg of personal luggage. Extra luggage may be accommodated in the luggage bay subject to space.", "Luggage", "luggage baggage bags weight limit allowance")
        ]
        cursor.executemany('''
            INSERT INTO faqs (question, answer, category, keywords)
            VALUES (?, ?, ?, ?)
        ''', sample_faqs)
        conn.commit()

    conn.close()

# Query helper functions

def get_all_buses():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buses ORDER BY departure_time ASC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def search_buses(source=None, destination=None, date=None, max_fare=None):
    conn = get_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM buses WHERE 1=1'
    params = []

    if source:
        query += ' AND LOWER(source) = LOWER(?)'
        params.append(source.strip())
    if destination:
        query += ' AND LOWER(destination) = LOWER(?)'
        params.append(destination.strip())
    if max_fare is not None:
        query += ' AND fare <= ?'
        params.append(int(max_fare))

    query += ' ORDER BY departure_time ASC'
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_bus_by_number(bus_number):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buses WHERE LOWER(bus_number) = LOWER(?)', (bus_number.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_bus_by_id(bus_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buses WHERE id = ?', (bus_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_booking(booking_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE LOWER(booking_id) = LOWER(?)', (booking_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def cancel_booking(booking_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE LOWER(booking_id) = LOWER(?)', (booking_id.strip(),))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    # Update status to Cancelled if not already
    booking = dict(row)
    if booking['status'] != 'Cancelled':
        cursor.execute('UPDATE bookings SET status = ? WHERE LOWER(booking_id) = LOWER(?)', ('Cancelled', booking_id.strip()))
        conn.commit()
        booking['status'] = 'Cancelled'
    
    conn.close()
    return booking

def get_all_faqs(category=None):
    conn = get_db()
    cursor = conn.cursor()
    if category:
        cursor.execute('SELECT * FROM faqs WHERE LOWER(category) = LOWER(?)', (category.strip(),))
    else:
        cursor.execute('SELECT * FROM faqs')
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def search_faqs(query_text):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faqs')
    rows = cursor.fetchall()
    conn.close()

    query_tokens = set(query_text.lower().split())
    best_match = None
    best_score = 0

    for r in rows:
        d = dict(r)
        q_tokens = set(d['question'].lower().split())
        kw_tokens = set(d['keywords'].lower().split())
        combined = q_tokens | kw_tokens

        # Score matching tokens
        overlap = query_tokens & combined
        score = len(overlap)
        if score > best_score:
            best_score = score
            best_match = d

    if best_score >= 1:
        return best_match
    return None

def get_policies():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM policies')
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_policy(policy_type):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM policies WHERE LOWER(policy_type) = LOWER(?)', (policy_type.strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_support_request(name, email, booking_id, issue):
    conn = get_db()
    cursor = conn.cursor()
    
    # Find next ticket id
    cursor.execute('SELECT COUNT(*) FROM support_requests')
    count = cursor.fetchone()[0] + 1
    ticket_id = f"SUP-{10000 + count}"
    
    from datetime import datetime
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO support_requests (ticket_id, name, email, booking_id, issue, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'Open', ?)
    ''', (ticket_id, name, email, booking_id or None, issue, created_at))
    conn.commit()

    cursor.execute('SELECT * FROM support_requests WHERE ticket_id = ?', (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)
