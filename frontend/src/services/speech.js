/**
 * Speech Utility for PinkBus Chatbot
 * Uses native Web Speech API (SpeechSynthesis & SpeechRecognition).
 * 100% local, no paid APIs, English only (en-IN / en-US).
 */

// Voice cache
let cachedVoices = [];

function loadVoices() {
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    cachedVoices = window.speechSynthesis.getVoices();
  }
}

if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
  loadVoices();
  if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }
}

/**
 * Finds best available English voice (en-IN preferred, then en-US, then any English).
 */
export function getEnglishVoice() {
  if (!cachedVoices || cachedVoices.length === 0) {
    loadVoices();
  }

  // 1. Try Indian English
  const enIN = cachedVoices.find((v) => v.lang === 'en-IN' || v.lang.replace('_', '-') === 'en-IN');
  if (enIN) return enIN;

  // 2. Try US English
  const enUS = cachedVoices.find((v) => v.lang === 'en-US' || v.lang.replace('_', '-') === 'en-US');
  if (enUS) return enUS;

  // 3. Any English voice
  const anyEn = cachedVoices.find((v) => v.lang.toLowerCase().startsWith('en'));
  if (anyEn) return anyEn;

  return null;
}

/**
 * Cleans text and formats rich message data into natural spoken English.
 * Strips markdown, technical markers, emojis, and creates natural descriptions for cards.
 */
export function cleanTextForSpeech(text, message = null) {
  let speechText = text || '';

  // 1. If Booking Card is present, produce a natural booking summary
  if (message && message.cards_type === 'booking' && message.data) {
    const b = message.data;
    const busName = b.bus_name || b.bus_number;
    speechText = `Your booking ${b.booking_id} is ${b.status.toLowerCase()}. Passenger is ${b.passenger_name}. Traveling from ${b.source} to ${b.destination} on ${b.travel_date}. Bus is ${busName}, seat number ${b.seat_number}, and the fare is ${b.fare} rupees.`;
  }
  // 2. If Bus Cards are present, produce a natural bus result summary
  else if (message && message.cards_type === 'buses' && message.data) {
    const buses = Array.isArray(message.data.buses)
      ? message.data.buses
      : Array.isArray(message.data)
      ? message.data
      : [];

    if (buses.length > 0) {
      const b0 = buses[0];
      const countWord = buses.length === 1 ? 'one bus' : `${buses.length} buses`;
      const src = message.data.source || b0.source;
      const dst = message.data.destination || b0.destination;

      speechText = `I found ${countWord} from ${src} to ${dst}. ${b0.bus_name} departs at ${b0.departure_time} from ${b0.boarding_point}. It has ${b0.available_seats} seats available and the fare is ${b0.fare} rupees.`;
    }
  }

  // 3. Clean markdown, technical symbols, and naturalize phrasing
  speechText = speechText
    .replace(/\*\*(.*?)\*\*/g, '$1') // Bold **text** -> text
    .replace(/\*(.*?)\*/g, '$1')     // Italics *text* -> text
    .replace(/\[DEMO NOTICE:.*?\]/gi, '') // Strip demo notice blocks from spoken voice
    .replace(/⚠️/g, '')
    .replace(/•\s*Departure(?:\s+Time)?:\s*([0-9:]+\s*[APM]+)/gi, 'Departure is $1.')
    .replace(/•\s*Arrival(?:\s+Time)?:\s*([0-9:]+\s*[APM]+)/gi, 'Arrival is $1.')
    .replace(/•\s*Fare:\s*₹?\s*(\d+)/gi, 'The fare is $1 rupees.')
    .replace(/•\s*Duration:\s*(\d+h\s*\d*m?)/gi, 'Duration is $1.')
    .replace(/•\s*/g, '. ')          // Other bullets become clear sentence pauses
    .replace(/₹\s*(\d+)/g, '$1 rupees') // ₹650 -> 650 rupees
    .replace(/Rs\.?\s*(\d+)/gi, '$1 rupees')
    .replace(/(\d+)\s*hrs?\b/gi, '$1 hours')
    .replace(/(\d+)\s*m\b/gi, '$1 minutes')
    .replace(/→/g, ' to ')
    .replace(/⇄/g, ' to and from ')
    .replace(/->/g, ' to ')
    .replace(/[\uFE00-\uFE0F]/g, '') // Variation selectors
    .replace(/[👋🚌📍🏁⏰💰🔌❄💡🧳✨🔴🎤🔊]/gu, '') // Emojis
    .replace(/:\s*\./g, '.')
    .replace(/\.{2,}/g, '.')
    .replace(/\s+/g, ' ')
    .trim();

  return speechText;
}

/**
 * Stops any ongoing speech synthesis.
 */
export function stopSpeech() {
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
}

/**
 * Speaks given text using browser SpeechSynthesis.
 * Calls onStart, onEnd, onError callbacks.
 */
export function speakText(text, { onStart, onEnd, onError } = {}) {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
    if (onError) onError(new Error('Speech synthesis not supported.'));
    return null;
  }

  // Always cancel any prior speech
  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  const voice = getEnglishVoice();

  if (voice) {
    utterance.voice = voice;
    utterance.lang = voice.lang;
  } else {
    utterance.lang = 'en-IN';
  }

  // Natural speech settings per prompt requirements
  utterance.rate = 0.95;
  utterance.pitch = 1.0;
  utterance.volume = 1.0;

  utterance.onstart = () => {
    if (onStart) onStart();
  };

  utterance.onend = () => {
    if (onEnd) onEnd();
  };

  utterance.onerror = (e) => {
    // If canceled manually, do not treat as error
    if (e.error === 'canceled' || e.error === 'interrupted') {
      if (onEnd) onEnd();
      return;
    }
    console.warn('SpeechSynthesis error:', e);
    if (onError) onError(e);
    if (onEnd) onEnd();
  };

  window.speechSynthesis.speak(utterance);
  return utterance;
}

/**
 * Checks if browser supports Speech Recognition.
 */
export function isSpeechRecognitionSupported() {
  if (typeof window === 'undefined') return false;
  return Boolean(window.SpeechRecognition || window.webkitSpeechRecognition);
}

/**
 * Creates and initializes a SpeechRecognition instance.
 */
export function createSpeechRecognition({ onResult, onError, onEnd, onStart }) {
  if (!isSpeechRecognitionSupported()) {
    return null;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  // Settings
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  // Prefer en-IN, fallback en-US
  recognition.lang = 'en-IN';

  recognition.onstart = () => {
    if (onStart) onStart();
  };

  recognition.onresult = (event) => {
    if (event.results && event.results.length > 0) {
      const transcript = event.results[0][0].transcript;
      if (onResult) onResult(transcript);
    }
  };

  recognition.onerror = (event) => {
    console.warn('SpeechRecognition error:', event.error);
    if (onError) onError(event.error);
  };

  recognition.onend = () => {
    if (onEnd) onEnd();
  };

  return recognition;
}
