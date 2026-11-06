"""
Alliance University - Utility Helpers
Formatting, Image Encoding, Audio Synthesizer & Common Helpers
"""

import os
import base64
import datetime
from typing import Optional


def get_image_base64(filepath: str) -> Optional[str]:
    """Encodes a local image file into a Base64 string for zero-latency HTML embedding."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            return None
    return None


def format_timestamp(dt_str: Optional[str] = None) -> str:
    """Formats a datetime string into a readable student-facing timestamp."""
    if not dt_str:
        return datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    try:
        dt = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return str(dt_str)


def generate_audio_siren_html() -> str:
    """Generates an embedded Web Audio API oscillating emergency siren tone."""
    return """
    <audio autoplay style="display:none;">
        <script>
            (function() {
                try {
                    const AudioCtx = window.AudioContext || window.webkitAudioContext;
                    if (!AudioCtx) return;
                    const ctx = new AudioCtx();
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(650, ctx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(950, ctx.currentTime + 0.3);
                    osc.frequency.exponentialRampToValueAtTime(650, ctx.currentTime + 0.6);
                    gain.gain.setValueAtTime(0.2, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 1.2);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + 1.3);
                } catch(e) {}
            })();
        </script>
    </audio>
    """

