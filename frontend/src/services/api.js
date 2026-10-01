/**
 * PinkBus Chatbot API Service
 * Centralizes all communication with the Flask backend.
 */

const API_BASE = '/api';

export async function sendMessage(message, sessionId = 'pinkbus_session') {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId })
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Failed to send message to support chatbot.');
  }

  return await response.json();
}

export async function resetChatSession(sessionId = 'pinkbus_session') {
  const response = await fetch(`${API_BASE}/chat/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId })
  });
  return await response.json();
}

export async function getBuses(params = {}) {
  const query = new URLSearchParams(params).toString();
  const response = await fetch(`${API_BASE}/buses?${query}`);
  if (!response.ok) throw new Error('Failed to fetch buses.');
  return await response.json();
}

export async function searchBuses(source, destination, date = null, maxFare = null) {
  const params = new URLSearchParams();
  if (source) params.append('source', source);
  if (destination) params.append('destination', destination);
  if (date) params.append('date', date);
  if (maxFare) params.append('max_fare', maxFare);

  const response = await fetch(`${API_BASE}/buses/search?${params.toString()}`);
  if (!response.ok) throw new Error('Failed to search buses.');
  return await response.json();
}

export async function getBusDetail(identifier) {
  const response = await fetch(`${API_BASE}/buses/${identifier}`);
  if (!response.ok) throw new Error(`Failed to fetch details for bus ${identifier}`);
  return await response.json();
}

export async function getBooking(bookingId) {
  const response = await fetch(`${API_BASE}/bookings/${bookingId}`);
  if (!response.ok) throw new Error(`Failed to fetch booking ${bookingId}`);
  return await response.json();
}

export async function cancelBooking(bookingId) {
  const response = await fetch(`${API_BASE}/bookings/${bookingId}/cancel`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!response.ok) throw new Error(`Failed to cancel booking ${bookingId}`);
  return await response.json();
}

export async function getFaqs(category = null, q = null) {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (q) params.append('q', q);

  const response = await fetch(`${API_BASE}/faqs?${params.toString()}`);
  if (!response.ok) throw new Error('Failed to load FAQs.');
  return await response.json();
}

export async function getPolicies() {
  const response = await fetch(`${API_BASE}/policies`);
  if (!response.ok) throw new Error('Failed to load policies.');
  return await response.json();
}

export async function submitSupportRequest(data) {
  const response = await fetch(`${API_BASE}/support`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Failed to submit support request.');
  }

  return await response.json();
}
