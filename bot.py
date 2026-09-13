import os
import time
import schedule
import requests
from groq import Groq
import google.generativeai as genai

# ============ تنظیمات ============
BOT_TOKEN = os.environ.get("8280504730:AAFFtWnrodJp8Ia8Yz8AyDp7IJRiy_5LTJc")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@NAVA_Life_ir")
GROQ_API_KEY = os.environ.get("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")
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6JrFynOHjKKCAV7qJJC25KWrPLwzX4TKn_DVSKCBG_e3g")

# کلاینت‌ها
groq_client = Groq(api_key=GROQ_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


# ============ توابع تولید محتوا ============

def ask_groq(prompt):
    try:
        r = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        return r.choices[0].message.content.strip()
    except Exception as e:
        print("Groq error:", e)
        return None


def ask_gemini(prompt):
    try:
        r = gemini_model.generate_content(prompt)
        return r.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return None


def send(text):
    if not text:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML"
        }, timeout=20)
        print("Sent:", text[:50])
    except Exception as e:
        print("Send error:", e)


# ============ پست‌ها ============

def post_english_words_am():
    p = ("۵ کلمه انگلیسی امروز رو با معنی و یه مثال کوتاه بنویس. "
         "فرمت: هر کلمه در یک خط، بعدش معنی فارسی و یه مثال انگلیسی کوتاه. "
         "با ایموجی‌های مناسب. حداکثر ۱۵۰ کلمه.")
    send(ask_groq(p))

def post_morning_motivation():
    p = ("یه جمله انگیزشی کوتاه و قشنگ برای شروع روز بنویس. "
         "حداکثر ۲۰ کلمه، با ۲ ایموجی. فقط جمله، نه توضیح.")
    send(ask_gemini(p))

def post_idiom():
    p = ("یه اصطلاح پرکاربرد انگلیسی رو با معنی فارسی و یه مثال توضیح بده. "
         "فرمت: اصطلاح + معنی + مثال. با ایموجی. حداکثر ۸۰ کلمه.")
    send(ask_groq(p))

def post_book_morning():
    p = ("یه پاراگراف کوتاه و زیبا از یه کتاب معروف (ایرانی یا خارجی) بنویس. "
         "اسم کتاب و نویسنده رو هم ذکر کن. با ایموجی 📖. حداکثر ۱۰۰ کلمه.")
    send(ask_gemini(p))

def post_love_quote():
    p = ("یه جمله عاشقانه کوتاه و قشنگ بنویس. "
         "حداکثر ۲۰ کلمه، با ۲ ایموجی. فقط جمله.")
    send(ask_gemini(p))

def post_fact():
    p = ("یه دانستنی جالب و واقعی بگو (علمی، تاریخی یا جغرافیایی). "
         "با ایموجی 🌍. حداکثر ۸۰ کلمه. واقعی باشه، الکی نساز.")
    send(ask_gemini(p))

def post_english_words_pm():
    p = ("۵ کلمه انگلیسی جدید (سطح متوسط) با معنی فارسی و یه مثال کوتاه بنویس. "
         "با ایموجی. حداکثر ۱۵۰ کلمه.")
    send(ask_groq(p))

def post_book_evening():
    p = ("یه پاراگراف کوتاه و الهام‌بخش از یه کتاب معروف بنویس. "
         "اسم کتاب و نویسنده رو ذکر کن. با ایموجی 📖. حداکثر ۱۰۰ کلمه.")
    send(ask_gemini(p))

def post_night_motivation():
    p = ("یه جمله انگیزشی کوتاه برای شب بنویس. "
         "حداکثر ۲۰ کلمه، با ۲ ایموجی.")
    send(ask_gemini(p))

def post_calm():
    p = ("یه جمله آرامش‌بخش و دلنشین برای پایان روز بنویس. "
         "حداکثر ۲۰ کلمه، با ایموجی 🌙.")
    send(ask_gemini(p))


# ============ زمان‌بندی ============
schedule.every().day.at("07:00").do(post_english_words_am)
schedule.every().day.at("09:00").do(post_morning_motivation)
schedule.every().day.at("11:00").do(post_idiom)
schedule.every().day.at("13:00").do(post_book_morning)
schedule.every().day.at("15:00").do(post_love_quote)
schedule.every().day.at("17:00").do(post_fact)
schedule.every().day.at("19:00").do(post_english_words_pm)
schedule.every().day.at("21:00").do(post_book_evening)
schedule.every().day.at("22:00").do(post_night_motivation)
schedule.every().day.at("23:00").do(post_calm)


# ============ اجرا ============
if __name__ == "__main__":
    print("Nava bot started...")
    # تست: یه پست همین الان بفرست که ببینی کار می‌کنه
    post_morning_motivation()
    while True:
        schedule.run_pending()
        time.sleep(30)
