import React from 'react';
import {
  Ticket,
  XCircle,
  RotateCcw,
  AlertCircle
} from 'lucide-react';

export default function BookingCard({ booking, onCancelTicket, onRescheduleTicket, onAskSupport }) {
  if (!booking) return null;

  const statusClass = {
    Confirmed: 'status-confirmed',
    Cancelled: 'status-cancelled',
    Completed: 'status-completed',
    Rescheduled: 'status-rescheduled'
  }[booking.status] || 'status-confirmed';

  return (
    <div className="booking-card">
      <div className="booking-header">
        <div className="booking-id-tag">
          <Ticket size={18} />
          <span>Ticket: {booking.booking_id}</span>
        </div>
        <span className={`booking-status-badge ${statusClass}`}>
          {booking.status}
        </span>
      </div>

      <div className="booking-grid">
        <div>
          <div className="booking-field-label">Passenger Name</div>
          <div className="booking-field-value">{booking.passenger_name}</div>
        </div>

        <div>
          <div className="booking-field-label">Contact Phone</div>
          <div className="booking-field-value">{booking.phone}</div>
        </div>

        <div>
          <div className="booking-field-label">Bus Number</div>
          <div className="booking-field-value">{booking.bus_number}</div>
        </div>

        <div>
          <div className="booking-field-label">Seat Assigned</div>
          <div className="booking-field-value">{booking.seat_number}</div>
        </div>

        <div>
          <div className="booking-field-label">Route Journey</div>
          <div className="booking-field-value">
            {booking.source} → {booking.destination}
          </div>
        </div>

        <div>
          <div className="booking-field-label">Travel Date</div>
          <div className="booking-field-value">{booking.travel_date}</div>
        </div>

        <div>
          <div className="booking-field-label">Fare Paid</div>
          <div className="booking-field-value" style={{ color: 'var(--pink-700)', fontSize: '0.95rem' }}>
            ₹{booking.fare}
          </div>
        </div>

        <div>
          <div className="booking-field-label">Demo Status</div>
          <div className="booking-field-value" style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Simulated Booking
          </div>
        </div>
      </div>

      {booking.status === 'Cancelled' && (
        <div className="demo-notice-alert" style={{ background: '#fef2f2', borderColor: '#fecaca', color: '#991b1b', marginBottom: '8px' }}>
          <AlertCircle size={14} />
          <span>This ticket was cancelled. Demo refund of 80% (₹{Math.round(booking.fare * 0.8)}) has been calculated.</span>
        </div>
      )}

      {/* Action buttons */}
      <div className="booking-actions-row">
        {booking.status === 'Confirmed' && onCancelTicket && (
          <button
            type="button"
            className="booking-btn booking-btn-danger"
            onClick={() => onCancelTicket(booking.booking_id)}
          >
            <XCircle size={13} />
            Cancel Ticket
          </button>
        )}

        {booking.status === 'Confirmed' && onRescheduleTicket && (
          <button
            type="button"
            className="booking-btn booking-btn-secondary"
            onClick={() => onRescheduleTicket(booking.booking_id)}
          >
            <RotateCcw size={13} />
            Reschedule Ticket
          </button>
        )}

        {onAskSupport && (
          <button
            type="button"
            className="booking-btn booking-btn-secondary"
            onClick={() => onAskSupport(booking.booking_id)}
          >
            Need Help with This Ticket?
          </button>
        )}
      </div>
    </div>
  );
}
