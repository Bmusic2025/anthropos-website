#!/usr/bin/env python3
"""
Generate additional Chirp 3 HD clips for intake/booking completion lines.
These extend each demo conversation with name collection, email, and confirmation.
"""

import json, base64, urllib.request, ssl, os, time

API_KEY = "AIzaSyDu5Eljvc_NPfqiXppG3DNBWyF3tu-HIGI"
URL = f"https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={API_KEY}"
ARIA_VOICE   = "en-US-Chirp3-HD-Aoede"
CALLER_VOICE = "en-US-Chirp3-HD-Fenrir"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

_SSL = ssl.create_default_context()
_SSL.check_hostname = False
_SSL.verify_mode = ssl.CERT_NONE

NEW_LINES = {
    "dental": [
        # index continues from 07
        ("caller", "2:30 works perfectly."),
        ("aria",   "Wonderful! And can I grab your last name, Marcus?"),
        ("caller", "It's Johnson. Marcus Johnson."),
        ("aria",   "Perfect. And the best email for your appointment confirmation?"),
        ("caller", "marcus.johnson at gmail dot com."),
        ("aria",   "Got it — Marcus Johnson, marcus dot johnson at gmail dot com, 2:30 tomorrow. You're all set! Dr. Martinez is genuinely great and I think you're going to feel really good about this. We'll send your confirmation right now. See you tomorrow!"),
    ],
    "funeral": [
        # index continues from 07
        ("aria",   "David, I also want to make sure we have the best way to reach you. Can I confirm your phone number and a good email address?"),
        ("caller", "Of course. 512-555-0147. Email is david.chen at gmail dot com."),
        ("aria",   "Thank you, David. 512-555-0147, and david dot chen at gmail dot com. Director Williams will be reaching out to you personally within the next few minutes. You are not alone in this. We will take care of everything — for Robert, and for your family."),
    ],
    "hvac": [
        # index continues from 07
        ("caller", "Thank you so much. What's the tech's name?"),
        ("aria",   "That'll be Carlos — he's fantastic. Can I confirm your name and a good number to text when he's 15 minutes out?"),
        ("caller", "Sarah Mitchell. Best number is 512-555-0293."),
        ("aria",   "Got it, Sarah. And a good email for your service invoice after the visit?"),
        ("caller", "sarah.mitchell at yahoo dot com."),
        ("aria",   "Perfect — Sarah Mitchell, 512-555-0293, sarah dot mitchell at yahoo dot com. Carlos is dispatched. You'll get a text when he's on the way. Stay cool in the meantime — you've got this handled."),
    ],
    "medspa": [
        # index continues from 05
        ("caller", "Yes, absolutely. I'd love to come in."),
        ("aria",   "You are going to love it. Can I get your first and last name to get you in our system?"),
        ("caller", "It's Nicole Williams."),
        ("aria",   "Beautiful name. And the best email for your consultation confirmation, Nicole?"),
        ("caller", "nicole.williams at icloud dot com."),
        ("aria",   "Perfect — Nicole Williams, nicole dot williams at icloud dot com. You are officially on the calendar. Our provider is going to love working with you, Nicole. You'll receive your confirmation shortly. We absolutely cannot wait to meet you."),
    ],
    "law": [
        # index continues from 07
        ("caller", "My name is Robert Chen."),
        ("aria",   "Thank you, Robert. And the best email address so we can send you some preliminary information before your consultation?"),
        ("caller", "robert.chen at outlook dot com."),
        ("aria",   "Robert Chen, robert dot chen at outlook dot com. You are in excellent hands. One of our attorneys will be reaching out to you within the hour. Everything you share with us is completely confidential. You made the right call today, Robert. We've got you."),
    ],
}

# Starting indices for each industry
START_IDX = {"dental": 7, "funeral": 7, "hvac": 7, "medspa": 5, "law": 7}

def synthesize(text, voice_name, filename):
    payload = json.dumps({
        "input": {"text": text},
        "voice": {"languageCode": "en-US", "name": voice_name},
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": 0.95,
            "pitch": 0.0,
            "effectsProfileId": ["headphone-class-device"]
        }
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=_SSL) as resp:
            data = json.loads(resp.read())
            audio = base64.b64decode(data["audioContent"])
            path = os.path.join(OUTPUT_DIR, filename)
            with open(path, "wb") as f:
                f.write(audio)
            print(f"  ✓ {filename} ({len(audio):,} bytes)")
            return True
    except Exception as e:
        print(f"  ✗ {filename} — {e}")
        return False

total = success = 0
for industry, lines in NEW_LINES.items():
    print(f"\n[{industry.upper()}]")
    start = START_IDX[industry]
    for i, (role, text) in enumerate(lines):
        voice = ARIA_VOICE if role == "aria" else CALLER_VOICE
        filename = f"{industry}_{start+i:02d}_{role}.mp3"
        total += 1
        if synthesize(text, voice, filename):
            success += 1
        time.sleep(0.3)

print(f"\n{'='*40}")
print(f"Done: {success}/{total} new clips generated")
