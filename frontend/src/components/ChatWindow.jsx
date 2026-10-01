import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, AlertCircle } from 'lucide-react';
import ChatHeader from './ChatHeader';
import MessageBubble from './MessageBubble';
import QuickActions from './QuickActions';
import { createSpeechRecognition, isSpeechRecognitionSupported } from '../services/speech';

export default function ChatWindow({
  messages,
  isTyping,
  quickActions,
  activeSpeakingMessageId,
  onToggleSpeak,
  onSendMessage,
  onResetChat,
  onOpenFaqs,
  onCancelTicket,
  onRescheduleTicket,
  onAskSupport,
  onTicketCreated,
  isExpanded,
  onToggleExpand,
  onMinimize,
  onClose
}) {
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [voiceNotice, setVoiceNotice] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const recognitionRef = useRef(null);

  // Auto-scroll to bottom on new messages or typing state change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping, isListening]);

  // Clean up speech recognition on unmount
  useEffect(() => {
    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
        } catch {
          // ignore
        }
      }
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = inputText.trim();
    if (!trimmed || isTyping || isListening) return;

    onSendMessage(trimmed);
    setInputText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Toggle Microphone / Voice Input
  const handleToggleMic = () => {
    // If currently listening, stop it
    if (isListening) {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch {
          // ignore
        }
      }
      setIsListening(false);
      setVoiceNotice(null);
      return;
    }

    // Check browser support
    if (!isSpeechRecognitionSupported()) {
      setVoiceNotice("Voice input is not supported in this browser. Please use Google Chrome or another supported browser.");
      setTimeout(() => setVoiceNotice(null), 6000);
      return;
    }

    // Initialize speech recognition
    const recognition = createSpeechRecognition({
      onStart: () => {
        setIsListening(true);
        setVoiceNotice("🔴 Listening... Speak now in English");
      },
      onResult: (transcript) => {
        setIsListening(false);
        setVoiceNotice(null);
        if (transcript && transcript.trim()) {
          setInputText(transcript.trim());
          // Automatically send the recognized voice message using existing chatbot logic
          onSendMessage(transcript.trim());
        }
      },
      onError: (errorType) => {
        setIsListening(false);
        if (errorType === 'not-allowed') {
          setVoiceNotice("Microphone permission is required to use voice input. Please enable microphone access in your browser.");
        } else if (errorType === 'no-speech') {
          setVoiceNotice("Sorry, I couldn't hear that. Please try again.");
        } else {
          setVoiceNotice("Voice recognition encountered an issue. Please try again or type your message.");
        }
        setTimeout(() => setVoiceNotice(null), 5000);
      },
      onEnd: () => {
        setIsListening(false);
      }
    });

    if (recognition) {
      recognitionRef.current = recognition;
      try {
        recognition.start();
      } catch (err) {
        console.warn('Failed to start speech recognition:', err);
        setIsListening(false);
      }
    }
  };

  return (
    <div className="chat-app-container" role="main" aria-label="PinkBus Customer Support Chatbot">
      {/* Fixed Chat Header */}
      <ChatHeader
        onResetChat={onResetChat}
        onOpenFaqs={onOpenFaqs}
        isExpanded={isExpanded}
        onToggleExpand={onToggleExpand}
        onMinimize={onMinimize}
        onClose={onClose}
      />

      {/* Messages Scroll Area */}
      <div className="chat-messages-container" aria-live="polite">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            message={msg}
            isSpeaking={activeSpeakingMessageId === msg.id}
            onToggleSpeak={onToggleSpeak}
            onSelectQuery={onSendMessage}
            onCancelTicket={onCancelTicket}
            onRescheduleTicket={onRescheduleTicket}
            onAskSupport={onAskSupport}
            onTicketCreated={onTicketCreated}
          />
        ))}

        {/* Animated Typing Indicator */}
        {isTyping && (
          <div className="message-wrapper bot">
            <div className="typing-indicator" aria-label="PinkBus Support is typing">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-label">PinkBus Support is typing...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Contextual Quick Action Buttons */}
      <QuickActions
        actions={quickActions}
        onSelectAction={onSendMessage}
        disabled={isTyping || isListening}
      />

      {/* Voice Status / Error Banner */}
      {voiceNotice && (
        <div className={`voice-status-banner ${isListening ? '' : 'info'}`}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {isListening ? (
              <span className="voice-status-pulse"></span>
            ) : (
              <AlertCircle size={15} />
            )}
            <span>{voiceNotice}</span>
          </div>
          <button
            type="button"
            style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '0.85rem', color: 'inherit' }}
            onClick={() => setVoiceNotice(null)}
          >
            ✕
          </button>
        </div>
      )}

      {/* Message Input Footer with Microphone and Send buttons */}
      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          className="chat-input-field"
          placeholder={isListening ? "Listening... Speak in English" : "Type your message..."}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isTyping}
          aria-label="Type your message"
          autoFocus
        />

        {/* Microphone / Voice Input Button */}
        <button
          type="button"
          className={`mic-btn ${isListening ? 'listening' : ''}`}
          onClick={handleToggleMic}
          disabled={isTyping}
          title={isListening ? "Stop listening" : "Speak your message"}
          aria-label="Speak your message"
        >
          {isListening ? <MicOff size={18} /> : <Mic size={18} />}
        </button>

        {/* Send Button */}
        <button
          type="submit"
          className="send-btn"
          disabled={!inputText.trim() || isTyping || isListening}
          aria-label="Send message"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
