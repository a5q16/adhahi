import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

TELEGRAM_TOKEN = "8784742099:AAFjyHzHOR1G8BmcTN3erNrlHI9PVhMSBdk"
CHAT_ID = "1935101763"
URL_BOUIRA = "https://adhahi.dz/api/v1/locations/wilayas/10/communes"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}

# متغير لحفظ الحالة
commune_states = {}

def send_msg(text):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text}
    )

@app.get("/api/cron")
def check_adhahi():
    global commune_states
    try:
        resp = requests.get(URL_BOUIRA, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            changes = []
            
            for commune in data:
                c_id = commune["id"]
                c_name = commune["name"]
                is_active = commune["isActive"]

                if c_id not in commune_states:
                    commune_states[c_id] = is_active
                
                # توفر حجز
                if is_active and not commune_states[c_id]:
                    send_msg(f"✅ عاجل: فتح الحجز!\n📍البويرة - {c_name}\n🔗 adhahi.dz")
                    commune_states[c_id] = True
                    changes.append(f"{c_name}: Opened")
                
                # انتهاء حجز
                elif not is_active and commune_states[c_id]:
                    send_msg(f"❌ انتهى الحجز.\n📍البويرة - {c_name}")
                    commune_states[c_id] = False
                    changes.append(f"{c_name}: Closed")
            
            return JSONResponse({"status": "Checked successfully", "changes": changes})
        return JSONResponse({"error": f"Site returned {resp.status_code}"})
    except Exception as e:
        return JSONResponse({"error": str(e)})
