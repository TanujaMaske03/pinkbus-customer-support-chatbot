import React from 'react';
import { Bus, User, Volume2, VolumeX } from 'lucide-react';
import BusCard from './BusCard';
import BookingCard from './BookingCard';
import SupportForm from './SupportForm';
import PolicyCard from './PolicyCard';
import FaqCard from './FaqCard';

/**
 * Formats plain text containing basic markdown (**bold**, *italics*, lists) into React elements.
 */
function renderFormattedText(text) {
  if (!text) return null;

  const lines = text.split('\n');
  return lines.map((line, lineIdx) => {
    // Check for bold syntax **bold**
    const parts = line.split(/(\*\*.*?\*\*|\*.*?\*)/g);

    const formattedLine = parts.map((part, partIdx) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={partIdx}>{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith('*') && part.endsWith('*')) {
        return <em key={partIdx}>{part.slice(1, -1)}</em>;
      }
      return part;
    });

    return (
      <React.Fragment key={lineIdx}>
        {formattedLine}
        {lineIdx < lines.length - 1 && <br />}
      </React.Fragment>
    );
  });
}

export default function MessageBubble({
  message,
  isSpeaking,
  onToggleSpeak,
  onSelectQuery,
  onCancelTicket,
  onRescheduleTicket,
  onAskSupport,
  onTicketCreated
}) {
  const isBot = message.role === 'bot';

  // Extract buses list if present
  let busesList = [];
  if (message.cards_type === 'buses') {
    if (message.data && Array.isArray(message.data.buses)) {
      busesList = message.data.buses;
    } else if (Array.isArray(message.data)) {
      busesList = message.data;
    }
  }

  return (
    <div className={`message-wrapper ${isBot ? 'bot' : 'user'}`}>
      <div className="avatar-wrapper">
        {isBot ? (
          <div className="bot-avatar-icon" aria-label="PinkBus Assistant">
            <Bus size={18} strokeWidth={2.4} />
          </div>
        ) : (
          <div className="user-avatar-icon" aria-label="User">
            <User size={18} />
          </div>
        )}
      </div>

      <div className="message-content-wrapper">
        <div className="message-bubble">
          <div className="message-text">
            {renderFormattedText(message.text)}
          </div>

          {/* Bus Cards List */}
          {isBot && message.cards_type === 'buses' && busesList.length > 0 && (
            <div className="cards-scroll-container">
              {busesList.map((bus) => (
                <BusCard
                  key={bus.id || bus.bus_number}
                  bus={bus}
                  onSelectQuery={onSelectQuery}
                />
              ))}
            </div>
          )}

          {/* Booking Card */}
          {isBot && message.cards_type === 'booking' && message.data && (
            <BookingCard
              booking={message.data}
              onCancelTicket={onCancelTicket}
              onRescheduleTicket={onRescheduleTicket}
              onAskSupport={onAskSupport}
            />
          )}

          {/* Support Form Card */}
          {isBot && (message.cards_type === 'support_card' || message.cards_type === 'support_form') && (
            <SupportForm
              _data={message.data}
              defaultBookingId={message.data?.booking_id}
              onTicketCreated={onTicketCreated}
            />
          )}

          {/* Policy Card */}
          {isBot && message.cards_type === 'policy' && (
            <PolicyCard data={message.data} />
          )}

          {/* FAQs List or FAQ Item */}
          {isBot && (message.cards_type === 'faqs' || message.cards_type === 'faq_item') && (
            <FaqCard
              data={message.data}
              onSelectQuestion={onSelectQuery}
            />
          )}
        </div>

        <div className="message-meta">
          <span>{message.timestamp}</span>

          {/* Speaker Button - ONLY on bot messages */}
          {isBot && onToggleSpeak && (
            <button
              type="button"
              className={`speaker-btn ${isSpeaking ? 'speaking' : ''}`}
              onClick={() => onToggleSpeak(message)}
              title={isSpeaking ? 'Stop speaking' : 'Listen to this message'}
              aria-label="Listen to this message"
            >
              {isSpeaking ? (
                <>
                  <VolumeX size={13} />
                  <span>Speaking...</span>
                </>
              ) : (
                <>
                  <Volume2 size={13} />
                  <span>Listen</span>
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
