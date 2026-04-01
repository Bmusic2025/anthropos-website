#!/usr/bin/env python3
"""
Generate Chirp 3 HD audio for the CHIEF OF STAFF website demo (3 scenarios).
Output: audio/cos_<scenario>_<index:02d>.mp3
Run once, commit, push to GitHub Pages.
"""

import json, base64, urllib.request, ssl, os, time

API_KEY = "AIzaSyDu5Eljvc_NPfqiXppG3DNBWyF3tu-HIGI"
URL = f"https://texttospeech.googleapis.com/v1beta1/text:synthesize?key={API_KEY}"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

_SSL = ssl.create_default_context()
_SSL.check_hostname = False
_SSL.verify_mode = ssl.CERT_NONE

COS_VOICE  = "en-US-Chirp3-HD-Leda"    # Chief of Staff — polished, premium female
EXEC_FENRIR = "en-US-Chirp3-HD-Fenrir" # Marcus Chen (hedge) — sharp male
EXEC_ORUS   = "en-US-Chirp3-HD-Orus"   # Jordan Davis (tech CEO) — deeper male
EXEC_AOEDE  = "en-US-Chirp3-HD-Aoede"  # Sandra Wright (broker) — confident female

SCRIPTS = {
    "hedge": [
        (EXEC_FENRIR, "Quick — where are we sitting on the Northfield position? Board call in 20 minutes."),
        (COS_VOICE,   "You're up 4.2% on Northfield since the August entry. Thesis is holding — their Q3 guidance revised upward last week, which you flagged as the trigger. One flag: sector volatility is elevated heading into the Fed decision Thursday. You mentioned last session you wanted to trim if it crossed 18% of the book. It's at 16.4 right now."),
        (EXEC_FENRIR, "Good. Remind me what I said about Chen after the last partners call."),
        (COS_VOICE,   "You said he's sharp but doesn't push back enough in rooms with senior partners — that you'd want to test him with a hard mandate before promoting. Your exact note was: talent, not yet conviction."),
        (EXEC_FENRIR, "That's exactly right. Pull that into the board deck notes."),
        (COS_VOICE,   "Done. Added to your board prep under Personnel — flagged for the Q4 review conversation. Anything else before the call?"),
    ],
    "tech": [
        (EXEC_ORUS,  "I need to think through the Series B timing. Talk me through where we are."),
        (COS_VOICE,  "Last time we talked about this you said you'd move when ARR crossed 4 million and churn dropped below 3%. You're at 3.7 million ARR and churn is sitting at 3.4 — close but not quite. The macro for B rounds has tightened, but your category is still getting funded. If you close the two enterprise deals in the pipeline, you hit both numbers inside 60 days and raise from strength instead of need."),
        (EXEC_ORUS,  "Which two deals are we talking?"),
        (COS_VOICE,  "Meridian Health and Coventry Group. Meridian has been warm for six weeks — you mentioned their procurement slows in Q4, so there's a window closing. Coventry is faster-moving. Their CTO wanted a pilot before committing. You were going to follow up on that last Friday."),
        (EXEC_ORUS,  "I didn't follow up. Help me draft the message."),
        (COS_VOICE,  "On it. Draft: Hi — following up on the pilot conversation. We've onboarded two similar-scale clients since we spoke and the ramp time came in under two weeks both times. Happy to walk you through the setup — do you have 20 minutes this week? Want me to adjust the tone or add anything specific?"),
    ],
    "realty": [
        (EXEC_AOEDE, "I've got a tough negotiation call with the Alderman Group tomorrow. Refresh me on where this stands."),
        (COS_VOICE,  "Alderman Group — 22,000 square feet commercial, East Austin. They came in 90 days ago expecting 28 dollars per square foot. Market has moved on them — comparables are closing at 24 to 25. Their timeline is firm — they need to be in by March or it affects their permit window. That's your leverage. They need a deal more than they need that number."),
        (EXEC_AOEDE, "What do I know about the broker on the other side?"),
        (COS_VOICE,  "First deal together. After your intro call you noted he's professional but relationship-new — meaning he'll follow his client's lead since there's no trust built yet. The deal has to speak for itself. Don't try to work him. Work the logic."),
        (EXEC_AOEDE, "What's my opening number and where do I land?"),
        (COS_VOICE,  "Open at 25.50 — close enough to market they can't call it unreasonable, but leaves you room to move. Your floor is 23.50 given the March constraint they're carrying. If they push hard on price, offer to absorb the first month's operating costs instead of moving the rate — protects your comp and gives them a win they can show their team."),
    ],
}

def synth(text, voice):
    body = json.dumps({
        "input": {"text": text},
        "voice": {"languageCode": voice[:5], "name": voice},
        "audioConfig": {"audioEncoding": "MP3"}
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=_SSL, timeout=20) as resp:
        return json.loads(resp.read())["audioContent"]

total = sum(len(v) for v in SCRIPTS.values())
done = 0

for scenario, lines in SCRIPTS.items():
    for i, (voice, text) in enumerate(lines):
        fname = f"cos_{scenario}_{i:02d}.mp3"
        out_path = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(out_path):
            print(f"  skip: {fname}")
            done += 1
            continue
        try:
            b64 = synth(text, voice)
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(b64))
            done += 1
            role = "COS" if "Leda" in voice else "exec"
            print(f"  [{done}/{total}] {fname} ({role}) — \"{text[:60]}...\"")
            time.sleep(0.15)
        except Exception as e:
            print(f"  ERROR {fname}: {e}")

print(f"\nDone. {done}/{total} files.")
