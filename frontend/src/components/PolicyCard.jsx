import React from 'react';
import { ShieldCheck, AlertCircle } from 'lucide-react';

export default function PolicyCard({ data }) {
  const isReschedule = data?.policy_type === 'rescheduling';
  const title = data?.title || (isReschedule ? 'Demo Rescheduling Policy' : 'Demo Cancellation & Refund Policy');

  return (
    <div className="policy-card">
      <div className="policy-title">
        <ShieldCheck size={18} color="var(--primary-pink)" />
        <span>{title}</span>
      </div>

      <div className="policy-content">
        {isReschedule ? (
          <>
            <div>• <strong>Timing:</strong> Rescheduling is allowed up to 12 hours before departure time.</div>
            <div>• <strong>Fare Adjustment:</strong> Fare difference applies if you choose a higher bus class.</div>
            <div>• <strong>Conditions:</strong> Rescheduled tickets cannot be cancelled for a cash refund.</div>
            <div>• <strong>Seat Availability:</strong> Subject to available seats on the requested travel date.</div>
          </>
        ) : (
          <>
            <div>• <strong>&gt; 24 hours before departure:</strong> 80% refund</div>
            <div>• <strong>12 – 24 hours before departure:</strong> 50% refund</div>
            <div>• <strong>&lt; 12 hours before departure:</strong> No refund</div>
          </>
        )}
      </div>

      <div className="demo-notice-alert">
        <AlertCircle size={15} style={{ flexShrink: 0 }} />
        <span>
          <strong>DEMO NOTICE:</strong> This is a simulated demo policy for the internship technical demonstration. No real payments, cards, or bank refunds are processed.
        </span>
      </div>
    </div>
  );
}
