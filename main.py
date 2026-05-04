import requests
import time

TELEGRAM_TOKEN = "8784742099:AAFjyHzHOR1G8BmcTN3erNrlHI9PVhMSBdk"
CHAT_ID = "1935101763"
URL_BOUIRA = "https://adhahi.dz/api/v1/locations/wilayas/10/communes"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text})

# قاموس لتخزين حالة كل بلدية
commune_states = {}

print("بدأ البوت في العمل والمراقبة...")
send_msg("🤖 تم تشغيل البوت وهو الآن يراقب ولاية البويرة...")

while True:
    try:
        resp = requests.get(URL_BOUIRA, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for commune in data:
                c_id = commune["id"]
                c_name = commune["name"]
                is_active = commune["isActive"]

                # تسجيل البلدية لأول مرة كـ "مغلقة" افتراضياً
                if c_id not in commune_states:
                    commune_states[c_id] = is_active

                # إذا تغيرت الحالة إلى True (فتح الحجز)
                if is_active and not commune_states[c_id]:
                    send_msg(f"✅ عاجل: فتح الحجز في البويرة!\n📍البلدية: {c_name}\n🔗 الرابط: https://adhahi.dz/")
                    commune_states[c_id] = True
                
                # إذا تغيرت الحالة إلى False (انتهاء الحجز)
                elif not is_active and commune_states[c_id]:
                    send_msg(f"❌ انتهى الحجز في البويرة.\n📍البلدية: {c_name}")
                    commune_states[c_id] = False

    except Exception as e:
        pass # تجاهل أعطال الاتصال المؤقتة كي لا يتوقف السكربت

    # فحص كل 15 ثانية لتجنب حظر الـ IP من خوادم الموقع
    time.sleep(15)
