import React, { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, Sparkles } from 'lucide-react';

export default function FaqCard({ data, onSelectQuestion }) {
  const [expandedId, setExpandedId] = useState(null);

  if (!data) return null;

  // Single FAQ item
  if (data.question && data.answer) {
    return (
      <div className="faq-item-card" style={{ marginTop: '8px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--pink-700)', fontSize: '0.75rem', fontWeight: 700, marginBottom: '4px' }}>
          <HelpCircle size={14} />
          <span>Category: {data.category || 'General Help'}</span>
        </div>
        <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-main)', marginBottom: '6px' }}>
          {data.question}
        </div>
        <div className="faq-answer" style={{ borderTop: 'none', paddingTop: 0 }}>
          {data.answer}
        </div>
      </div>
    );
  }

  // List of FAQs
  const faqs = data.faqs || [];
  if (faqs.length === 0) return null;

  return (
    <div className="faq-list-container">
      {faqs.map((faq) => {
        const isOpen = expandedId === faq.id;
        return (
          <div
            key={faq.id}
            className="faq-item-card"
            onClick={() => setExpandedId(isOpen ? null : faq.id)}
          >
            <div className="faq-question-row">
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span style={{ color: 'var(--primary-pink)', fontSize: '0.75rem', fontWeight: 700 }}>
                  [{faq.category}]
                </span>
                <span>{faq.question}</span>
              </span>
              {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </div>

            {isOpen && (
              <div className="faq-answer">
                <p>{faq.answer}</p>
                {onSelectQuestion && (
                  <button
                    type="button"
                    className="quick-action-btn"
                    style={{ marginTop: '8px', fontSize: '0.72rem' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectQuestion(faq.question);
                    }}
                  >
                    <Sparkles size={12} />
                    <span>Ask this in chat</span>
                  </button>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
