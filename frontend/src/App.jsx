import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import ChatbotLauncher from './components/ChatbotLauncher';
import ChatWindow from './components/ChatWindow';
import { sendMessage, resetChatSession } from './services/api';
import { speakText, stopSpeech, cleanTextForSpeech } from './services/speech';
import './App.css';

const INITIAL_WELCOME_TEXT = `Hi! 👋 Welcome to PinkBus Support.

I'm your virtual travel assistant. I can help you with bus availability, timings, fares, bookings, cancellations, refunds and more.

How can I help you today?`;

const INITIAL_QUICK_ACTIONS = [
  "Find a Bus",
  "Check Seat Availability",
  "Check Fare",
  "Booking Help",
  "Cancel Ticket",
  "Refund Information",
  "Reschedule Ticket",
  "FAQs",
  "Talk to Support"
];

function getCurrentTime() {
  const now = new Date();
  let hours = now.getHours();
  const minutes = now.getMinutes().toString().padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12 || 12;
  return `${hours}:${minutes} ${ampm}`;
}

export default function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isChatExpanded, setIsChatExpanded] = useState(false);

  const [sessionId, setSessionId] = useState(() => `session_${Date.now()}`);
  const [messages, setMessages] = useState([
    {
      id: 'welcome_msg',
      role: 'bot',
      text: INITIAL_WELCOME_TEXT,
      timestamp: getCurrentTime(),
      cards_type: null,
      data: null
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [quickActions, setQuickActions] = useState(INITIAL_QUICK_ACTIONS);
  const [activeSpeakingMessageId, setActiveSpeakingMessageId] = useState(null);

  // Send message to backend and receive response (used by typing, microphone, and quick actions)
  const handleSendMessage = async (text) => {
    if (!text || !text.trim()) return;

    const userMessageId = `user_${Date.now()}`;
    const userMessage = {
      id: userMessageId,
      role: 'user',
      text: text.trim(),
      timestamp: getCurrentTime()
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      const data = await sendMessage(text.trim(), sessionId);

      if (data.success && data.response) {
        const botMessage = {
          id: `bot_${Date.now()}`,
          role: 'bot',
          text: data.response.text,
          intent: data.intent,
          cards_type: data.response.cards_type,
          data: data.response.data,
          timestamp: data.timestamp || getCurrentTime()
        };

        // NOTE: The bot response is added to the chat as TEXT ONLY.
        // The bot NEVER speaks automatically per requirement.
        setMessages((prev) => [...prev, botMessage]);

        if (data.response.quick_actions && data.response.quick_actions.length > 0) {
          setQuickActions(data.response.quick_actions);
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: `bot_err_${Date.now()}`,
        role: 'bot',
        text: "I'm having trouble connecting to the PinkBus backend right now. Please verify that the Flask server is running on port 5000.",
        timestamp: getCurrentTime(),
        cards_type: null
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  // Toggle speaker speech for a bot message
  const handleToggleSpeak = (message) => {
    // If currently speaking this specific message, stop it
    if (activeSpeakingMessageId === message.id) {
      stopSpeech();
      setActiveSpeakingMessageId(null);
      return;
    }

    // Stop any previous message speech first
    stopSpeech();

    // Prepare clean natural English text for speech
    const spokenContent = cleanTextForSpeech(message.text, message);

    speakText(spokenContent, {
      onStart: () => {
        setActiveSpeakingMessageId(message.id);
      },
      onEnd: () => {
        setActiveSpeakingMessageId(null);
      },
      onError: () => {
        setActiveSpeakingMessageId(null);
      }
    });
  };

  // Reset / Clear Chat
  const handleResetChat = async () => {
    stopSpeech();
    setActiveSpeakingMessageId(null);

    try {
      await resetChatSession(sessionId);
    } catch (e) {
      console.warn('Could not reset remote session:', e);
    }

    const newSessionId = `session_${Date.now()}`;
    setSessionId(newSessionId);
    setMessages([
      {
        id: `welcome_${Date.now()}`,
        role: 'bot',
        text: INITIAL_WELCOME_TEXT,
        timestamp: getCurrentTime(),
        cards_type: null,
        data: null
      }
    ]);
    setQuickActions(INITIAL_QUICK_ACTIONS);
  };

  // Open Chatbot (optionally with an initial query)
  const handleOpenChat = (initialQuery = null) => {
    setIsChatOpen(true);
    if (initialQuery && typeof initialQuery === 'string') {
      handleSendMessage(initialQuery);
    }
  };

  // Close Chatbot Window
  const handleCloseChat = () => {
    stopSpeech();
    setActiveSpeakingMessageId(null);
    setIsChatOpen(false);
    setIsChatExpanded(false);
  };

  // Minimize Chatbot Window
  const handleMinimizeChat = () => {
    stopSpeech();
    setActiveSpeakingMessageId(null);
    setIsChatOpen(false);
  };

  // Toggle Expanded Full-Modal Mode
  const handleToggleExpand = () => {
    setIsChatExpanded((prev) => !prev);
  };

  const handleOpenFaqs = () => {
    handleSendMessage("FAQs");
  };

  const handleCancelTicket = (bookingId) => {
    handleSendMessage(`Cancel booking ${bookingId}`);
  };

  const handleRescheduleTicket = (bookingId) => {
    handleSendMessage(`Reschedule booking ${bookingId}`);
  };

  const handleAskSupport = (bookingId) => {
    handleSendMessage(`I need support for booking ${bookingId}`);
  };

  const handleTicketCreated = (ticket) => {
    const confirmationMsg = {
      id: `bot_sup_${Date.now()}`,
      role: 'bot',
      text: `Support request **${ticket.ticket_id}** is logged under your email **${ticket.email}**. An executive has been notified in demo mode.`,
      timestamp: getCurrentTime(),
      cards_type: null
    };
    setMessages((prev) => [...prev, confirmationMsg]);
  };

  return (
    <div className="pinkbus-app-root">
      {/* 1. PinkBus Landing Page */}
      <LandingPage onOpenChat={handleOpenChat} />

      {/* 2. Floating Chatbot Launcher (visible when chat is closed) */}
      {!isChatOpen && (
        <ChatbotLauncher onOpenChat={() => handleOpenChat()} />
      )}

      {/* 3. Floating Chatbot Window (visible when chat is open) */}
      {isChatOpen && (
        <div
          className={`chat-floating-window ${isChatExpanded ? 'expanded' : ''}`}
          role="dialog"
          aria-modal="false"
          aria-label="PinkBus Customer Support Assistant"
        >
          <ChatWindow
            messages={messages}
            isTyping={isTyping}
            quickActions={quickActions}
            activeSpeakingMessageId={activeSpeakingMessageId}
            onToggleSpeak={handleToggleSpeak}
            onSendMessage={handleSendMessage}
            onResetChat={handleResetChat}
            onOpenFaqs={handleOpenFaqs}
            onCancelTicket={handleCancelTicket}
            onRescheduleTicket={handleRescheduleTicket}
            onAskSupport={handleAskSupport}
            onTicketCreated={handleTicketCreated}
            isExpanded={isChatExpanded}
            onToggleExpand={handleToggleExpand}
            onMinimize={handleMinimizeChat}
            onClose={handleCloseChat}
          />
        </div>
      )}
    </div>
  );
}
