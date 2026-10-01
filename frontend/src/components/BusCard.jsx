import React, { useState } from 'react';
import {
  Bus,
  ChevronDown,
  ChevronUp,
  CheckCircle2
} from 'lucide-react';

export default function BusCard({ bus, onSelectQuery }) {
  const [showDetails, setShowDetails] = useState(false);

  if (!bus) return null;

  const seatsClass =
    bus.available_seats > 15
      ? 'seats-high'
      : bus.available_seats > 7
      ? 'seats-medium'
      : 'seats-low';

  return (
    <div className="bus-card">
      {/* Top Header */}
      <div className="bus-card-header">
        <div className="bus-name-badge">
          <span className="bus-name">{bus.bus_name}</span>
          <span className="bus-number-pill">{bus.bus_number}</span>
        </div>
        <span className="bus-type-tag">{bus.bus_type}</span>
      </div>

      {/* Route & Times */}
      <div className="bus-card-route-row">
        <div className="route-stop">
          <span className="route-time">{bus.departure_time}</span>
          <span className="route-city">{bus.source}</span>
          <span className="route-point" title={`Boarding: ${bus.boarding_point}`}>
            📍 {bus.boarding_point}
          </span>
        </div>

        <div className="route-duration-center">
          <span className="route-duration-text">{bus.duration}</span>
          <div className="route-line">
            <span className="route-line-bar"></span>
            <Bus size={14} />
            <span className="route-line-bar"></span>
          </div>
        </div>

        <div className="route-stop" style={{ textAlign: 'right' }}>
          <span className="route-time">{bus.arrival_time}</span>
          <span className="route-city">{bus.destination}</span>
          <span className="route-point" title={`Dropping: ${bus.dropping_point}`}>
            🏁 {bus.dropping_point}
          </span>
        </div>
      </div>

      {/* Footer Info & Actions */}
      <div className="bus-card-footer">
        <div className="bus-seats-fare">
          <span className={`seats-badge ${seatsClass}`}>
            <CheckCircle2 size={13} />
            {bus.available_seats} Seats Available
          </span>
          <span className="bus-fare">₹{bus.fare}</span>
        </div>

        <button
          type="button"
          className="bus-details-btn"
          onClick={() => setShowDetails(!showDetails)}
          aria-expanded={showDetails}
        >
          <span>{showDetails ? 'Hide Details' : 'View Details'}</span>
          {showDetails ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
      </div>

      {/* Collapsible Details */}
      {showDetails && (
        <div className="bus-expanded-details">
          <div>
            <strong>Boarding Point:</strong> {bus.boarding_point} (Report 15m prior)
          </div>
          <div>
            <strong>Dropping Point:</strong> {bus.dropping_point}
          </div>
          <div>
            <strong>Total Capacity:</strong> {bus.total_seats} passenger berths/seats
          </div>
          <div>
            <strong>Included Amenities:</strong>
            <div className="amenities-row">
              <span className="amenity-pill">❄️ Air Conditioned</span>
              <span className="amenity-pill">🔌 Mobile Charging</span>
              <span className="amenity-pill">💡 Reading Light</span>
              <span className="amenity-pill">🧳 15 kg Luggage</span>
              <span className="amenity-pill">📍 Live GPS</span>
            </div>
          </div>
          <div style={{ marginTop: '6px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {onSelectQuery && (
              <>
                <button
                  type="button"
                  className="quick-action-btn"
                  style={{ fontSize: '0.72rem', padding: '3px 10px' }}
                  onClick={() => onSelectQuery(`Is ${bus.bus_number} available?`)}
                >
                  Check Seat Vacancy
                </button>
                <button
                  type="button"
                  className="quick-action-btn"
                  style={{ fontSize: '0.72rem', padding: '3px 10px' }}
                  onClick={() => onSelectQuery(`How much does ${bus.bus_number} cost?`)}
                >
                  Fare Details
                </button>
                <button
                  type="button"
                  className="quick-action-btn"
                  style={{ fontSize: '0.72rem', padding: '3px 10px' }}
                  onClick={() => onSelectQuery(`Where is the boarding point for ${bus.bus_number}?`)}
                >
                  Boarding Point Info
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
