#!/usr/bin/env python3
"""
Generate Chirp 3 HD audio clips for ARIA demo conversations.
ARIA voice: en-US-Chirp3-HD-Aoede (warm, female)
Caller voice: en-US-Chirp3-HD-Fenrir (natural, male)
"""

import json
import base64
import urllib.request
import urllib.parse
import ssl
import os
import time

# Bypass SSL cert verification (same pattern as app.py)
_SSL_CTX = ssl.create_default_context()
_SSL_CTX.check_hostname = False
_SSL_CTX.verify_mode = ssl.CERT_NONE

API_KEY = "AIzaSyDu5Eljvc_NPfqiXppG3DNBWyF3tu-HIGI"
URL = f"https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={API_KEY}"

# Chirp 3 HD voices
ARIA_VOICE   = "en-US-Chirp3-HD-Aoede"   # warm female
CALLER_VOICE = "en-US-Chirp3-HD-Fenrir"  # natural male

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEMOS = {
    "dental": [
        ("aria",   "Thank you for calling Austin Dental! This is Jasmine. How are you doing today?"),
        ("caller", "Hi, yeah — I've been having some tooth pain and I need to get in to see someone."),
        ("aria",   "Oh I'm sorry to hear that — tooth pain is no fun. You called the right place. Dr. Martinez is wonderful with patients who are nervous about dental work, and we'll take great care of you. Are you a new patient with us?"),
        ("caller", "Yeah, first time. I'm honestly a little anxious about it."),
        ("aria",   "We hear that a lot — and I completely understand. We promise to take great care of you. Dr. Martinez has been doing this for 18 years and is incredibly gentle. Can I get your name and a couple time slots that work for you? We have some openings as early as tomorrow."),
        ("caller", "Oh wow, tomorrow works. I'm Marcus."),
        ("aria",   "Perfect, Marcus! We have 10am or 2:30pm tomorrow. Which works better? And I'll text you a confirmation with the address and what to bring."),
    ],
    "funeral": [
        ("aria",   "Thank you for reaching out to Riverside Memorial. This is Grace. I'm here to help — please take your time."),
        ("caller", "Hi... my father passed away this morning. I don't really know what to do."),
        ("aria",   "I'm so deeply sorry for your loss. I'm here. Please take all the time you need. You don't have to figure this out alone — we're going to guide you through every step."),
        ("caller", "Thank you. I just... I don't know where to start."),
        ("aria",   "That is completely understandable. Can I ask who I have the honor of speaking with today?"),
        ("caller", "I'm David. My father's name was Robert."),
        ("aria",   "David, I want to make sure Robert is cared for with the dignity and respect he deserves. I'm going to connect you directly with one of our directors right now — they'll walk alongside you through everything. Whatever you need, we're here."),
    ],
    "hvac": [
        ("aria",   "Lone Star HVAC, this is Riley. What can I help you with?"),
        ("caller", "My AC just stopped working. It's 96 degrees outside and I have two kids at home."),
        ("aria",   "Okay — I'm making this a priority right now. We handle emergency calls all day and we've got a tech in your area. Can you give me your address?"),
        ("caller", "6210 Barton Springs Road, Austin."),
        ("aria",   "Got it. And is it a complete shutdown — no cool air at all — or is it running but not cooling properly?"),
        ("caller", "Completely off. Nothing."),
        ("aria",   "Understood. I'm dispatching now. Someone will be at your door within 90 minutes. You'll get a text when the tech is on his way. In the meantime, keep the blinds closed and get the kids to the coolest room. We're on it."),
    ],
    "medspa": [
        ("aria",   "Thank you for calling Luminary Med Spa! This is Sophia. It's wonderful to hear from you — how can I help you today?"),
        ("caller", "Hi, I'm interested in Botox. I've never done it before and I'm not sure where to start."),
        ("aria",   "Oh you're going to love what we can do for you. First-time consultations are my favorite — there's something so exciting about that first visit. Can I ask what your main goal is? Are you looking to soften expression lines, prevent new ones from forming, or something else?"),
        ("caller", "Mostly around my eyes and forehead. I've been noticing them more."),
        ("aria",   "That's one of our most popular areas and the results are beautiful. Our provider will customize everything specifically for you during your consultation. Most clients describe it as looking in the mirror and seeing themselves, just refreshed. Can I get you on the calendar?"),
    ],
    "law": [
        ("aria",   "Thank you for calling Sterling Law Group. This is Victoria. How may I assist you today?"),
        ("caller", "Hi, I was just served with divorce papers and I'm honestly not sure what to do."),
        ("aria",   "I understand — this can feel very overwhelming. You've called the right place. Everything you share with our office is completely confidential."),
        ("caller", "I've never dealt with anything like this before."),
        ("aria",   "Our attorneys handle family law matters regularly, and they're very good at helping clients understand exactly where they stand and what their options are. Can I collect some initial information so our team can prepare before your call?"),
        ("caller", "Yes, please."),
        ("aria",   "Of course. Can I get your name? And do you have a preferred time for your consultation — we have availability this week."),
    ],
}

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
        with urllib.request.urlopen(req, timeout=30, context=_SSL_CTX) as resp:
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

total = 0
success = 0
for industry, lines in DEMOS.items():
    print(f"\n[{industry.upper()}]")
    for i, (role, text) in enumerate(lines):
        voice = ARIA_VOICE if role == "aria" else CALLER_VOICE
        filename = f"{industry}_{i:02d}_{role}.mp3"
        total += 1
        if synthesize(text, voice, filename):
            success += 1
        time.sleep(0.3)  # be gentle with the API

print(f"\n{'='*40}")
print(f"Done: {success}/{total} clips generated")
print(f"Output: {OUTPUT_DIR}")
