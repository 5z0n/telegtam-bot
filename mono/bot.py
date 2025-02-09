import telebot
import yt_dlp
import os

# قراءة التوكن من متغير البيئة
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# رسالة الترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أرسل لي رابط الفيديو لتحميله 🎥")

# معالجة الروابط وتحميل الفيديو
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.reply_to(message, "جاري تحميل الفيديو، يرجى الانتظار ⏳...")
    try:
        # إعدادات yt-dlp
        ydl_opts = {
            'outtmpl': 'videos/%(title)s.%(ext)s',  # حفظ الفيديو في مجلد videos
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            video_path = f"videos/{video_title}.mp4"

        # إرسال الفيديو إلى المستخدم
        with open(video_path, 'rb') as video:
            bot.send_video(message.chat.id, video)

    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء تحميل الفيديو: {e}")

# تشغيل البوت
bot.polling()
