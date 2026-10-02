# PinkBus Customer Support Chatbot

## Project Overview

PinkBus Customer Support Chatbot is a first-level virtual customer support system designed to assist users with common bus booking related queries.

The chatbot provides information and support related to bus availability, routes, timings, boarding and dropping points, seat availability, fares, booking, cancellation, refunds, rescheduling and frequently asked questions.

## Features

- Bus availability and route queries
- Source and destination information
- Bus timings
- Boarding and dropping point information
- Seat availability
- Fare information
- Booking support
- Cancellation and refund support
- Rescheduling support
- Frequently asked questions
- Human support/escalation
- Voice input using Speech Recognition
- Manual voice output using Speech Synthesis
- Clean and responsive React chatbot interface

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- Flask

### Database

- SQLite

### Voice Features

- Web Speech API
- Speech Recognition
- Speech Synthesis

## System Architecture

User  
↓  
React Frontend  
↓  
Flask API  
↓  
Chatbot Logic  
↓  
SQLite Database  
↓  
Response  
↓  
React Frontend  
↓  
User

## Chatbot Working

The user enters a question through the chatbot interface.

The React frontend sends the request to the Flask backend through an API.

The backend processes the request using intent-based chatbot logic and retrieves relevant information from the database where required.

The generated response is then returned to the React frontend and displayed to the user.

## Voice Input

The chatbot supports voice input using the browser's Speech Recognition API.

Flow:

Microphone → Speech Recognition → Text → Chatbot → Response

The user can click the microphone button and speak a query in English.

## Voice Output

The chatbot supports manual voice output using the browser's Speech Synthesis API.

Each chatbot response has a speaker button. The response is spoken only when the user clicks the speaker button.

The chatbot does not automatically speak.

## Database

The project uses SQLite for sample/demo bus and booking data.

The database contains information such as:

- Bus name/number
- Source
- Destination
- Departure time
- Arrival time
- Boarding point
- Dropping point
- Available seats
- Fare
- Sample booking information

The current project uses sample/mock data for demonstration and is not connected to the PinkBus production database.

## How to Run

### Backend

Open a terminal:

```bash
cd backend
py app.py
````

The Flask backend runs locally on:

```text
http://127.0.0.1:5000
```

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on the Vite development server.

Open the URL shown in the terminal, normally:

```text
http://localhost:5173
```

## Sample Queries

Examples:

* Show buses from Pune to Mumbai
* What are the bus timings?
* What is the fare?
* Are seats available?
* Where is the boarding point?
* How can I cancel my booking?
* What is the refund process?
* Can I reschedule my ticket?
* I want to talk to customer support

## Current Limitations

* The project uses sample/mock data.
* It is not connected to the real-time PinkBus production database.
* It does not process real payments.
* Booking and cancellation flows are demonstration/support flows.
* The chatbot currently uses controlled intent-based logic and may not understand every possible natural-language query.

## Future Scope

* Real-time bus APIs
* Live seat availability
* Real booking and payment integration
* Real cancellation and refund processing
* User authentication
* Generative AI
* RAG-based customer support
* Improved natural language understanding
* Human support ticket integration
* Multilingual support

## Project Purpose

The main goal of this project is to provide quick first-level customer support and reduce repetitive customer queries related to bus booking services.


