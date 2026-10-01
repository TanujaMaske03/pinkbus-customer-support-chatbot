import React from 'react';
import {
  Bus,
  CheckCircle2,
  Tag,
  BookOpen,
  XCircle,
  RefreshCw,
  Calendar,
  HelpCircle,
  PhoneCall,
  Sparkles,
  FileText
} from 'lucide-react';

function getActionIcon(actionText) {
  const lower = actionText.toLowerCase();
  if (lower.includes('find a bus') || lower.includes('pune to') || lower.includes('mumbai to') || lower.includes('buses')) {
    return <Bus size={14} />;
  }
  if (lower.includes('seat')) {
    return <CheckCircle2 size={14} />;
  }
  if (lower.includes('fare') || lower.includes('cost') || lower.includes('price')) {
    return <Tag size={14} />;
  }
  if (lower.includes('booking help') || lower.includes('how to book')) {
    return <BookOpen size={14} />;
  }
  if (lower.includes('cancel')) {
    return <XCircle size={14} />;
  }
  if (lower.includes('refund')) {
    return <RefreshCw size={14} />;
  }
  if (lower.includes('reschedule') || lower.includes('date')) {
    return <Calendar size={14} />;
  }
  if (lower.includes('faq')) {
    return <HelpCircle size={14} />;
  }
  if (lower.includes('support request') || lower.includes('raise ticket')) {
    return <FileText size={14} />;
  }
  if (lower.includes('support') || lower.includes('human') || lower.includes('agent')) {
    return <PhoneCall size={14} />;
  }
  return <Sparkles size={14} />;
}

export default function QuickActions({ actions, onSelectAction, disabled }) {
  if (!actions || actions.length === 0) return null;

  return (
    <div className="quick-actions-bar" role="toolbar" aria-label="Quick Actions">
      {actions.map((action, idx) => (
        <button
          key={`${action}-${idx}`}
          type="button"
          className="quick-action-btn"
          disabled={disabled}
          onClick={() => onSelectAction(action)}
        >
          {getActionIcon(action)}
          <span>{action}</span>
        </button>
      ))}
    </div>
  );
}
