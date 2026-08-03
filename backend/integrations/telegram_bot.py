"""
E.D.I.T.H. V8 — Telegram Bot
Remote control from your phone. Set TELEGRAM_ENABLED=True in config.
Get token from @BotFather on Telegram.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))
from config.config import TELEGRAM_ENABLED, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


async def start_bot(orchestrator):
    if not TELEGRAM_ENABLED or not TELEGRAM_TOKEN:
        print("  [Telegram] Disabled. Configure TELEGRAM_TOKEN in config.py")
        return

    # 🚨 SECURITY: Deny-by-default to prevent unauthorized global access
    if not TELEGRAM_CHAT_ID:
        print("  [Telegram] SECURITY WARNING: Bot enabled but TELEGRAM_CHAT_ID is missing.")
        print("  [Telegram] Refusing to start bot to prevent unauthorized remote access.")
        return

    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    except ImportError:
        print("  [Telegram] pip install python-telegram-bot")
        return

    def _guard(update) -> bool:
        return str(update.effective_chat.id) == str(TELEGRAM_CHAT_ID)

    async def start(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await u.message.reply_text("*E.D.I.T.H. V8 online.* Send any command.", parse_mode="Markdown")

    async def handle(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if not _guard(u): return
        q = u.message.text.strip()
        await u.message.reply_text("⚡ Processing…")
        try:
            r = await orchestrator.handle(q)
            await u.message.reply_text(f"🤖 {r}")
        except Exception as e:
            await u.message.reply_text(f"❌ {e}")

    async def status(u: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if not _guard(u): return
        await u.message.reply_text(f"`{orchestrator.sys.system_info()}`", parse_mode="Markdown")

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("  [Telegram] Bot running.")
    await app.run_polling()
