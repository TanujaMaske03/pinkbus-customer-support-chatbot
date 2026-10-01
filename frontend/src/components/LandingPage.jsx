import React from 'react';
import { Bus, Headphones, MessageSquare } from 'lucide-react';

const SUPPORT_OPTIONS = [
  {
    id: 'buses',
    emoji: '🚌',
    title: 'Find Buses',
    desc: 'Routes, timings & availability',
    query: 'Find a Bus'
  },
  {
    id: 'booking',
    emoji: '🎫',
    title: 'Booking Support',
    desc: 'Bookings & tickets',
    query: 'Booking Help'
  },
  {
    id: 'refunds',
    emoji: '💰',
    title: 'Fare & Refunds',
    desc: 'Fare, cancellation & refunds',
    query: 'Refund Information'
  },
  {
    id: 'support',
    emoji: '💬',
    title: '24/7 Support',
    desc: 'Quick virtual assistance',
    query: 'Talk to Support'
  }
];

export default function LandingPage({ onOpenChat }) {
  return (
    <div className="landing-page-container">
      {/* ================= COMPACT HEADER ================= */}
      <header className="landing-header">
        <div className="landing-header-inner">
          <div className="landing-brand">
            <div className="landing-brand-icon">
              <Bus size={18} color="#ffffff" strokeWidth={2.4} />
            </div>
            <span className="brand-name">PinkBus</span>
          </div>

          <button
            type="button"
            className="landing-support-header-btn"
            onClick={() => onOpenChat()}
            aria-label="Open Customer Support Chat"
          >
            <Headphones size={15} />
            <span>Customer Support</span>
          </button>
        </div>
      </header>

      {/* ================= MAIN CONTENT ================= */}
      <main className="landing-main">
        {/* HERO SECTION */}
        <section className="landing-hero-section">
          <div className="hero-left">
            <h1 className="hero-title">
              Travel Easy with <span className="highlight-pink">PinkBus</span>
            </h1>

            <p className="hero-tagline">
              Your journey starts here.
            </p>

            <p className="hero-description">
              Get quick help with buses, bookings, fares, cancellations and more.
            </p>

            <button
              type="button"
              className="hero-primary-btn"
              onClick={() => onOpenChat()}
              aria-label="Chat with PinkBus Support"
            >
              <MessageSquare size={17} />
              <span>Chat with PinkBus Support</span>
            </button>
          </div>

          {/* COMPACT, SOFT BUS ILLUSTRATION */}
          <div className="hero-right">
            <div className="hero-visual-card">
              <svg
                viewBox="0 0 460 250"
                className="bus-illustration-svg"
                xmlns="http://www.w3.org/2000/svg"
                aria-label="PinkBus Coach Illustration"
              >
                <defs>
                  <linearGradient id="softBusGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#f43f5e" />
                    <stop offset="100%" stopColor="#e11d48" />
                  </linearGradient>
                  <linearGradient id="windowGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#f0f9ff" stopOpacity="0.95" />
                    <stop offset="100%" stopColor="#e0f2fe" stopOpacity="0.85" />
                  </linearGradient>
                  <linearGradient id="softBg" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#fff1f2" />
                    <stop offset="100%" stopColor="#ffe4e6" stopOpacity="0.5" />
                  </linearGradient>
                </defs>

                {/* Subtle Backdrop Glow */}
                <rect x="10" y="10" width="440" height="230" rx="20" fill="url(#softBg)" />
                <ellipse cx="230" cy="195" rx="170" ry="12" fill="#e2e8f0" opacity="0.6" />

                {/* Road Line */}
                <path
                  d="M 30 196 C 140 188, 320 188, 430 196"
                  stroke="#cbd5e1"
                  strokeWidth="2.5"
                  strokeDasharray="10 8"
                  strokeLinecap="round"
                />

                {/* Minimalist Clouds */}
                <path d="M 60 55 Q 75 45 90 50 Q 105 42 120 52 Q 130 48 135 60 Z" fill="#ffffff" opacity="0.8" />
                <path d="M 340 45 Q 352 36 366 40 Q 380 34 394 42 Q 402 38 408 48 Z" fill="#ffffff" opacity="0.75" />

                {/* Sleek Bus Body */}
                <g>
                  {/* Underbody shadow */}
                  <ellipse cx="232" cy="186" rx="145" ry="8" fill="#94a3b8" opacity="0.35" />

                  {/* Main Bus Shell */}
                  <path
                    d="M 95 174 L 95 98 C 95 86, 110 78, 140 78 L 335 78 C 360 78, 378 90, 382 110 L 386 156 C 387 168, 378 174, 365 174 Z"
                    fill="url(#softBusGrad)"
                  />

                  {/* Windows Ribbon */}
                  <path
                    d="M 108 126 L 108 102 C 108 94, 116 89, 128 89 L 362 89 C 370 89, 375 95, 374 105 L 370 126 Z"
                    fill="url(#windowGrad)"
                  />

                  {/* Window Dividers */}
                  <line x1="156" y1="89" x2="156" y2="126" stroke="#be123c" strokeWidth="2.5" />
                  <line x1="206" y1="89" x2="206" y2="126" stroke="#be123c" strokeWidth="2.5" />
                  <line x1="256" y1="89" x2="256" y2="126" stroke="#be123c" strokeWidth="2.5" />
                  <line x1="306" y1="89" x2="306" y2="126" stroke="#be123c" strokeWidth="2.5" />
                  <line x1="350" y1="89" x2="350" y2="126" stroke="#be123c" strokeWidth="2.5" />

                  {/* Passenger silhouettes */}
                  <circle cx="132" cy="108" r="5" fill="#64748b" opacity="0.4" />
                  <circle cx="181" cy="108" r="5" fill="#64748b" opacity="0.4" />
                  <circle cx="231" cy="108" r="5" fill="#64748b" opacity="0.4" />
                  <circle cx="281" cy="108" r="5" fill="#64748b" opacity="0.4" />
                  <circle cx="331" cy="108" r="5" fill="#64748b" opacity="0.4" />

                  {/* PinkBus Branding */}
                  <text
                    x="170"
                    y="157"
                    fill="#ffffff"
                    fontFamily="Plus Jakarta Sans, sans-serif"
                    fontWeight="800"
                    fontSize="18"
                    letterSpacing="0.03em"
                  >
                    PinkBus
                  </text>

                  {/* White accent line */}
                  <line x1="105" y1="137" x2="370" y2="137" stroke="#ffffff" strokeWidth="1.8" opacity="0.8" />

                  {/* Headlight */}
                  <ellipse cx="382" cy="158" rx="4" ry="7" fill="#fef08a" />

                  {/* Wheels */}
                  <circle cx="330" cy="176" r="16" fill="#1e293b" />
                  <circle cx="330" cy="176" r="10" fill="#64748b" />
                  <circle cx="330" cy="176" r="5" fill="#f8fafc" />

                  <circle cx="145" cy="176" r="16" fill="#1e293b" />
                  <circle cx="145" cy="176" r="10" fill="#64748b" />
                  <circle cx="145" cy="176" r="5" fill="#f8fafc" />
                </g>
              </svg>
            </div>
          </div>
        </section>

        {/* FOUR COMPACT SUPPORT CARDS */}
        <section className="landing-cards-section" aria-label="Customer Support Services">
          <div className="support-cards-grid">
            {SUPPORT_OPTIONS.map((opt) => (
              <div
                key={opt.id}
                className="compact-support-card"
                onClick={() => onOpenChat(opt.query)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    onOpenChat(opt.query);
                  }
                }}
                aria-label={`${opt.title}: ${opt.desc}. Click to open chat.`}
              >
                <div className="card-icon-bubble">
                  <span className="card-emoji" aria-hidden="true">{opt.emoji}</span>
                </div>
                <div className="card-info">
                  <h3 className="card-title">{opt.title}</h3>
                  <p className="card-desc">{opt.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* ================= MINIMAL FOOTER ================= */}
      <footer className="landing-footer-minimal">
        <p>© 2026 PinkBus • Customer Support Assistant Demo</p>
      </footer>
    </div>
  );
}
