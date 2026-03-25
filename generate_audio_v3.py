#!/usr/bin/env python3
"""
Generate Chirp 3 HD clips for 3 new ARIA demos:
- Construction / Remodeling
- Real Estate
- Luxury Auto Dealership
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

NEW_DEMOS = {
    "construction": [
        ("aria",   "Pinnacle Construction, this is Jordan. How can I help you today?"),
        ("caller", "Hey, I'm looking to do a full kitchen remodel. I've been getting some estimates and a friend recommended you guys."),
        ("aria",   "You came to the right place — kitchens are actually our specialty. We've done over 200 of them in the Austin area. Are you looking at a full gut and remodel, or more of an upgrade — new cabinets, countertops, that kind of thing?"),
        ("caller", "Full gut. We want to take it down to the studs and start fresh. New layout, the whole thing."),
        ("aria",   "I love it — that's where you really get to make it yours. Our project manager David does a free in-home consultation where he walks the space with you, talks through the vision, and gives you a detailed scope and number. No pressure, no obligation. What does your timeline look like?"),
        ("caller", "We're hoping to start in the next 60 days or so."),
        ("aria",   "That's actually great timing — we have availability opening up. Can I get your first and last name to get you scheduled?"),
        ("caller", "It's Brian Torres."),
        ("aria",   "Brian Torres. And the best email to send you some project examples and confirm the appointment time?"),
        ("caller", "brian.torres at gmail dot com."),
        ("aria",   "Perfect — Brian Torres, brian dot torres at gmail dot com. David is going to take great care of you. I'll have someone reach out within the hour to lock in a time. You're going to love what we can do with that kitchen, Brian."),
    ],
    "realestate": [
        ("aria",   "Thank you for calling Premier Realty! This is Morgan. How can I help you today?"),
        ("caller", "Hi, I'm looking to buy a home. Probably in the 600 to 700 thousand range, in the north Austin area. Just getting started."),
        ("aria",   "That's an exciting step — and north Austin is a great market right now. A few pockets up there are still moving really well. Are you working with a lender yet, or are you still in the early stages of figuring out financing?"),
        ("caller", "Still early. I know I want to buy, I just don't know all the steps yet."),
        ("aria",   "That is completely fine — honestly, that's the best time to call. Our agents walk you through everything from pre-approval to close. There's zero pressure, and the first conversation is really just about understanding what you want. Can I set you up with one of our buyer's agents for a quick intro call?"),
        ("caller", "Yeah, that sounds good actually."),
        ("aria",   "Wonderful. Can I get your first and last name?"),
        ("caller", "James Holloway."),
        ("aria",   "James Holloway. And the best email to send you a few current listings in that north Austin range while you wait?"),
        ("caller", "james.holloway at icloud dot com."),
        ("aria",   "Got it — James Holloway, james dot holloway at icloud dot com. I'm sending those listings right now and one of our agents will be in touch within the hour. This is going to be a great process, James. We find our buyers the right home — not just any home. Talk soon."),
    ],
    "auto": [
        ("aria",   "Good afternoon, thank you for calling Mercedes-Benz of Austin. This is Devon. How may I assist you today?"),
        ("caller", "Hi, I'm interested in the GLE 53 AMG. I saw one on your website — the Obsidian Black one with the Macchiato Beige interior."),
        ("aria",   "Excellent taste — the GLE 53 is a stunning vehicle, especially in that combination. That particular one just came in last week. Are you looking to come in for a drive today, or would you like me to hold it while we get some details sorted out first?"),
        ("caller", "I'd love to come in for a drive. I've been driving a BMW X5 for the last few years and I think it's time for something different."),
        ("aria",   "The 53 is going to feel like a completely different world — the AMG-tuned inline six, the air suspension, the way it responds. Once you drive it I think you'll know. Let me get you with one of our AMG specialists. Can I get your name?"),
        ("caller", "It's Marcus Reed."),
        ("aria",   "Marcus Reed. And the best email so I can send you the full spec sheet and have your paperwork ready before you arrive?"),
        ("caller", "marcus.reed at outlook dot com."),
        ("aria",   "Perfect — Marcus Reed, marcus dot reed at outlook dot com. I'll have the GLE 53 pulled up front and ready for you. What time works today? We have availability this afternoon, and I want to make sure we give you the full experience you deserve, Marcus. This is a big decision and we take that seriously."),
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
for industry, lines in NEW_DEMOS.items():
    print(f"\n[{industry.upper()}]")
    for i, (role, text) in enumerate(lines):
        voice = ARIA_VOICE if role == "aria" else CALLER_VOICE
        filename = f"{industry}_{i:02d}_{role}.mp3"
        total += 1
        if synthesize(text, voice, filename):
            success += 1
        time.sleep(0.3)

print(f"\n{'='*40}")
print(f"Done: {success}/{total} clips generated")
