import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ضع توكن البوت هنا
TOKEN = "7527297788:AAFmpBRr_fO4RoP-VNmes2Fkd9lnewxhwYE"

# دالة تحميل الفيديو
async def download_video(url: str) -> str:
    """تحميل الفيديو وإرجاع مساره."""
    output_path = "downloads/%(title)s.%(ext)s"
    ydl_opts = {
        "outtmpl": output_path,
        "format": "best",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

# دالة استقبال الرابط من المستخدم
async def handle_message(update: Update, context: CallbackContext) -> None:
    """استقبال الرابط وتحميل الفيديو."""
    url = update.message.text.strip()
    chat_id = update.message.chat_id

    if "http" not in url:
        await update.message.reply_text("🚫 الرجاء إرسال رابط صالح للفيديو.")
        return

    await update.message.reply_text("⏳ جاري تحميل الفيديو، انتظر قليلًا...")

    try:
        video_path = await download_video(url)
        await update.message.reply_video(video=open(video_path, "rb"))
        os.remove(video_path)  # حذف الفيديو بعد الإرسال
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل: {e}")

# دالة بدء البوت
async def start(update: Update, context: CallbackContext) -> None:
    """إرسال رسالة ترحيبية عند بدء البوت."""
    await update.message.reply_text("👋 ما تحمل سكس يا كسم انتا.")

# إعداد البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)  # إنشاء مجلد التخزين إذا لم يكن موجودًا
    main()
