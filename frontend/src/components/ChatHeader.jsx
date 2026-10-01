import React from 'react';
import { Bus, RotateCcw, HelpCircle, Minus, Maximize2, Minimize2, X } from 'lucide-react';

export default function ChatHeader({
  onResetChat,
  onOpenFaqs,
  isExpanded = false,
  onToggleExpand,
  onMinimize,
  onClose
}) {
  return (
    <header className="chat-header">
      <div className="header-left">
        <div className="header-avatar" aria-label="PinkBus Support Avatar">
          <Bus size={22} color="#ffffff" strokeWidth={2.2} />
        </div>
        <div className="header-title-group">
          <h1>PinkBus Support</h1>
          <div className="header-subtitle">
            <span className="status-dot" aria-hidden="true"></span>
            <span>Online • Virtual Assistant</span>
          </div>
        </div>
      </div>

      <div className="header-right">
        <span className="demo-badge" title="Running with simulated sample data for internship technical demonstration">
          Demo Mode
        </span>

        {onOpenFaqs && (
          <button
            type="button"
            className="header-btn"
            onClick={onOpenFaqs}
            title="Browse FAQs"
            aria-label="Frequently Asked Questions"
          >
            <HelpCircle size={17} />
          </button>
        )}

        {onResetChat && (
          <button
            type="button"
            className="header-btn"
            onClick={onResetChat}
            title="Clear and start new chat session"
            aria-label="Clear chat"
          >
            <RotateCcw size={17} />
          </button>
        )}

        {onMinimize && (
          <button
            type="button"
            className="header-btn minimize-btn"
            onClick={onMinimize}
            title="Minimize chat"
            aria-label="Minimize chat"
          >
            <Minus size={17} />
          </button>
        )}

        {onToggleExpand && (
          <button
            type="button"
            className="header-btn expand-btn"
            onClick={onToggleExpand}
            title={isExpanded ? "Restore standard size" : "Expand chat window"}
            aria-label={isExpanded ? "Restore standard size" : "Expand chat window"}
          >
            {isExpanded ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
          </button>
        )}

        {onClose && (
          <button
            type="button"
            className="header-btn close-header-btn"
            onClick={onClose}
            title="Close chat window"
            aria-label="Close chat window"
          >
            <X size={18} />
          </button>
        )}
      </div>
    </header>
  );
}
