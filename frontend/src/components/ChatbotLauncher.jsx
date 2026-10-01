import React, { useState } from 'react';
import { Bus, MessageSquare, X } from 'lucide-react';

export default function ChatbotLauncher({ onOpenChat }) {
  const [isDismissed, setIsDismissed] = useState(false);

  return (
    <div className="chatbot-launcher-container" aria-label="Customer Support Launcher">
      {/* Welcome Speech Bubble */}
      {!isDismissed && (
        <div
          className="launcher-welcome-bubble"
          onClick={onOpenChat}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              onOpenChat();
            }
          }}
          aria-label="Need help with your journey? Chat with PinkBus Support"
        >
          <button
            type="button"
            className="bubble-dismiss-btn"
            onClick={(e) => {
              e.stopPropagation();
              setIsDismissed(true);
            }}
            title="Dismiss bubble"
            aria-label="Dismiss bubble"
          >
            <X size={13} />
          </button>

          <div className="bubble-body">
            <span className="bubble-icon" aria-hidden="true">👋</span>
            <div className="bubble-text">
              <div className="bubble-title">Need help with your journey?</div>
              <div className="bubble-sub">Chat with PinkBus Support</div>
            </div>
          </div>
          <div className="bubble-pointer" />
        </div>
      )}

      {/* Floating Action Button (FAB) */}
      <button
        type="button"
        className="chatbot-fab"
        onClick={onOpenChat}
        title="Open PinkBus Customer Support"
        aria-label="Open PinkBus Customer Support"
      >
        <span className="fab-pulse-ring" aria-hidden="true" />
        <div className="fab-icon">
          <Bus size={26} color="#ffffff" strokeWidth={2.3} />
        </div>
        <span className="fab-chat-badge" aria-hidden="true">
          <MessageSquare size={13} color="#ffffff" fill="#ffffff" />
        </span>
      </button>
    </div>
  );
}
