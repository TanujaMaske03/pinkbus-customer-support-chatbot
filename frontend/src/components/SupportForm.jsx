import React, { useState } from 'react';
import {
  PhoneCall,
  Mail,
  Clock,
  AlertTriangle,
  Send,
  CheckCircle,
  FileText
} from 'lucide-react';
import { submitSupportRequest } from '../services/api';

export default function SupportForm({ _data, defaultBookingId, onTicketCreated }) {
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [bookingId, setBookingId] = useState(defaultBookingId || '');
  const [issue, setIssue] = useState('');
  const [loading, setLoading] = useState(false);
  const [createdTicket, setCreatedTicket] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim() || !email.trim() || !issue.trim()) {
      setErrorMessage('Please fill in your name, email, and description of your issue.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    try {
      const response = await submitSupportRequest({
        name: name.trim(),
        email: email.trim(),
        booking_id: bookingId.trim() || null,
        issue: issue.trim()
      });

      if (response.success && response.ticket) {
        setCreatedTicket(response.ticket);
        if (onTicketCreated) {
          onTicketCreated(response.ticket);
        }
      }
    } catch (err) {
      setErrorMessage(err.message || 'Could not submit support ticket.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="support-card">
      {/* Support Info */}
      <div className="support-header-info">
        <div className="support-row">
          <PhoneCall size={16} color="var(--primary-pink)" />
          <strong>Phone:</strong>
          <span>+91-XXXXXXXXXX (Demo)</span>
        </div>
        <div className="support-row">
          <Mail size={16} color="var(--primary-pink)" />
          <strong>Email:</strong>
          <span>support@pinkbus.demo</span>
        </div>
        <div className="support-row">
          <Clock size={16} color="var(--primary-pink)" />
          <strong>Hours:</strong>
          <span>9:00 AM – 9:00 PM</span>
        </div>
      </div>

      {/* Demo Warning Notice */}
      <div className="demo-notice-alert">
        <AlertTriangle size={15} style={{ flexShrink: 0 }} />
        <span>
          <strong>DEMO NOTICE:</strong> These are simulated contact details for the internship evaluation. No real calls or emails are routed.
        </span>
      </div>

      {/* Toggle button if ticket not created and form not open */}
      {!showForm && !createdTicket && (
        <button
          type="button"
          className="form-submit-btn"
          style={{ marginTop: '12px', width: '100%' }}
          onClick={() => setShowForm(true)}
        >
          <FileText size={16} />
          <span>Create Support Request</span>
        </button>
      )}

      {/* Support Request Form */}
      {showForm && !createdTicket && (
        <form className="support-form-wrapper" onSubmit={handleSubmit}>
          <div style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-main)', marginBottom: '2px' }}>
            Submit Customer Support Request
          </div>

          {errorMessage && (
            <div style={{ color: '#b91c1c', background: '#fee2e2', padding: '6px 10px', borderRadius: '6px', fontSize: '0.78rem' }}>
              {errorMessage}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="sup-name">Full Name *</label>
            <input
              id="sup-name"
              type="text"
              className="form-input"
              placeholder="e.g. Aarav Sharma"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="sup-email">Email Address *</label>
            <input
              id="sup-email"
              type="email"
              className="form-input"
              placeholder="e.g. aarav@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="sup-bid">Booking ID (Optional)</label>
            <input
              id="sup-bid"
              type="text"
              className="form-input"
              placeholder="e.g. PB10001"
              value={bookingId}
              onChange={(e) => setBookingId(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="sup-issue">Describe your issue / question *</label>
            <textarea
              id="sup-issue"
              className="form-textarea"
              placeholder="Please describe how we can assist you..."
              value={issue}
              onChange={(e) => setIssue(e.target.value)}
              required
            />
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              type="submit"
              className="form-submit-btn"
              style={{ flex: 1 }}
              disabled={loading}
            >
              <Send size={15} />
              <span>{loading ? 'Submitting...' : 'Submit Support Ticket'}</span>
            </button>
            <button
              type="button"
              className="bus-details-btn"
              onClick={() => setShowForm(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Success View */}
      {createdTicket && (
        <div className="ticket-success-box" style={{ marginTop: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 700 }}>
            <CheckCircle size={18} color="#059669" />
            <span>Your support request has been created successfully.</span>
          </div>
          <div>Ticket Reference Number:</div>
          <div className="ticket-id-highlight">{createdTicket.ticket_id}</div>
          <div style={{ fontSize: '0.78rem', color: '#047857', marginTop: '4px' }}>
            A virtual customer support executive will review your ticket (Status: <strong>{createdTicket.status}</strong>). Recorded in demo database.
          </div>
        </div>
      )}
    </div>
  );
}
