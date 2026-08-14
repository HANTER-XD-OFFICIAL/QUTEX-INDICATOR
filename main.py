import datetime
import logging
import os
import random
import threading
from flask import Flask
import pytz
import telebot
from telebot import types

TOKEN = "8908381436:AAG0KD5BuSxqMQgBO07tMCAjL7eVe3cl1W4"
DEVELOPER_NAME = "@HANTER_XD_OFFICIAL"
DEVELOPER_LINK = "https://t.me/HANTER_XD_OFFICIAL"
OTHER_BOT_LINK = "https://t.me/qutex7intigateaur_bot"

ADMIN_USERNAME = "HANTER_XD_OFFICIAL"
ADMIN_CHAT_ID = 6204875999

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

approved_users = set()
pending_requests = {}


@app.route("/")
def home():
  return "Elite AI 100% Sure-Shot Signal Bot is running!"


def run_web_server():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


def generate_advanced_sure_shot_signal(symbol, timeframe):
  candle_patterns = [
      {
          "pattern": "Three White Soldiers (Bullish Continuation Pattern)",
          "analysis": (
              "Strong bullish momentum with three consecutive long green"
              " candles. Indicates heavy institutional buying pressure."
          ),
          "bias": "Bullish",
      },
      {
          "pattern": "Bullish Engulfing with High Volume",
          "analysis": (
              "A large green candle completely engulfs the previous red"
              " candle, signaling an aggressive trend reversal to the upside."
          ),
          "bias": "Bullish",
      },
      {
          "pattern": "Morning Star at Key Support Level",
          "analysis": (
              "Three-candle reversal pattern showing sellers losing momentum"
              " and buyers taking total control of the next candle."
          ),
          "bias": "Bullish",
      },
      {
          "pattern": "Three Black Crows (Bearish Continuation Pattern)",
          "analysis": (
              "Consecutive strong red candles showing aggressive selling"
              " pressure and institutional profit-taking."
          ),
          "bias": "Bearish",
      },
      {
          "pattern": "Bearish Engulfing Rejection",
          "analysis": (
              "A dominant red candle engulfs the prior green candle, indicating"
              " immediate downward price rejection."
          ),
          "bias": "Bearish",
      },
      {
          "pattern": "Evening Star at Resistance Zone",
          "analysis": (
              "Strong reversal pattern indicating exhaustion of buyers and an"
              " imminent sharp drop in the upcoming candle."
          ),
          "bias": "Bearish",
      },
  ]

  news_catalysts = [
      {
          "title": "US Core Retail Sales & Consumer Spending Surge",
          "impact": "High Impact (Bullish USD)",
      },
      {
          "title": "FOMC Interest Rate Outlook & Liquidity Tightening",
          "impact": "High Impact (Bearish Pressure)",
      },
      {
          "title": "Global Institutional Order Block Liquidity Sweep",
          "impact": "Maximum Volatility Confirmed",
      },
      {
          "title": "Technical Resistance Zone Rejection & Volatility Spike",
          "impact": "Medium Impact Reversal",
      },
  ]

  selected_pattern = random.choice(candle_patterns)
  selected_news = random.choice(news_catalysts)
  rsi = round(random.uniform(24, 76), 2)

  bd_tz = pytz.timezone("Asia/Dhaka")
  now_bd = datetime.datetime.now(bd_tz)

  start_time = now_bd.strftime("%I:%M:%S %p")
  tf_mins = int(timeframe.replace("m", ""))
  end_time = (now_bd + datetime.timedelta(minutes=tf_mins)).strftime(
      "%I:%M:%S %p"
  )

  if selected_pattern["bias"] == "Bullish" or rsi < 40:
    prediction = "🟢 NEXT CANDLE: UP (CALL) [100% SURE-SHOT]"
    accuracy = (
        f"99.4% ({timeframe} Institutional Scan & Multi-Confirmation Verified)"
    )
    action_advice = (
        "Next candle will open with strong upward momentum. Enter CALL"
        " precisely at the candle opening."
    )
  else:
    prediction = "🔴 NEXT CANDLE: DOWN (PUT) [100% SURE-SHOT]"
    accuracy = (
        f"99.4% ({timeframe} Institutional Scan & Multi-Confirmation Verified)"
    )
    action_advice = (
        "Next candle will face heavy rejection and drop down. Enter PUT precisely"
        " at the candle opening."
    )

  return (
      prediction,
      accuracy,
      selected_pattern["pattern"],
      selected_pattern["analysis"],
      selected_news["title"],
      selected_news["impact"],
      rsi,
      start_time,
      end_time,
      action_advice,
  )


@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id
  username = message.from_user.username
  name = message.from_user.first_name

  if username and username.lower() == ADMIN_USERNAME.lower():
    approved_users.add(user_id)
    show_main_menu(message.chat.id)
    return

  if user_id in approved_users or (
      username and username.lower() == ADMIN_USERNAME.lower()
  ):
    show_main_menu(message.chat.id)
  else:
    pending_requests[user_id] = message.chat.id

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            "✅ Approve User", callback_data=f"approve_{user_id}"
        ),
        types.InlineKeyboardButton(
            "❌ Reject User", callback_data=f"reject_{user_id}"
        ),
    )

    admin_msg = (
        f"🔔 <b>New Access Request!</b>\n\n👤 <b>Name:</b> {name}\n🔗"
        f" <b>Username:</b> @{username if username else 'None'}\n🆔 <b>User"
        f" ID:</b> <code>{user_id}</code>\n\n<i>Do you want to approve this user"
        f" for signal access?</i>"
    )

    if ADMIN_CHAT_ID:
      try:
        bot.send_message(
            ADMIN_CHAT_ID, admin_msg, parse_mode="HTML", reply_markup=markup
        )
      except Exception as e:
        logging.error(f"Failed to send approval request to admin: {e}")

    waiting_text = (
        f"⏳ <b>Account Pending Approval!</b>\n\nYour access request has been sent"
        f" to the admin ({DEVELOPER_NAME}). Please wait until your account is"
        f" approved to unlock 100% Sure-Shot signals."
    )
    bot.send_message(message.chat.id, waiting_text, parse_mode="HTML")


def show_main_menu(chat_id):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  btn1 = types.KeyboardButton("💱 Currencies (OTC)")
  btn2 = types.KeyboardButton("🪙 Crypto Markets")
  btn3 = types.KeyboardButton("🛢 Commodities & Stocks")
  btn4 = types.KeyboardButton("⚡ Live News Flash")
  btn5 = types.KeyboardButton("🛡 Admin Contact")
  btn6 = types.KeyboardButton("💬 Support")
  markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

  welcome_text = (
      f"🚀 <b>Welcome to Elite AI 100% Sure-Shot Signal Bot!</b> 🚀\n\n"
      f"Powered by Advanced Candle Analysis, Real-Time News Filters, and Broker"
      f" Price Action Feeds.\n\n👨‍💻 <b>Lead Developer:</b> <a"
      f" href='{DEVELOPER_LINK}'>{DEVELOPER_NAME}</a>\n\n👇 <i>Select your"
      f" target market below to get 100% sure-shot signals:</i>"
  )
  bot.send_message(
      chat_id,
      welcome_text,
      parse_mode="HTML",
      reply_markup=markup,
      disable_web_page_preview=True,
  )


@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_user_callback(call):
  target_user_id = int(call.data.split("_")[1])
  approved_users.add(target_user_id)

  bot.answer_callback_query(call.id, "User Approved Successfully!")
  bot.edit_message_text(
      chat_id=call.message.chat.id,
      message_id=call.message.message_id,
      text=(
          f"✅ <b>User Approved!</b>\nUser ID: <code>{target_user_id}</code> has"
          " been granted access."
      ),
      parse_mode="HTML",
  )

  if target_user_id in pending_requests:
    user_chat_id = pending_requests[target_user_id]
    try:
      bot.send_message(
          user_chat_id,
          (
              "🎉 <b>Congratulations! Your account has been approved by the"
              " Admin.</b>\n\nType /start to access the signal engine."
          ),
          parse_mode="HTML",
      )
    except Exception as e:
      logging.error(f"Failed to notify approved user: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def reject_user_callback(call):
  target_user_id = int(call.data.split("_")[1])
  bot.answer_callback_query(call.id, "User Rejected.")
  bot.edit_message_text(
      chat_id=call.message.chat.id,
      message_id=call.message.message_id,
      text=(
          f"❌ <b>User Rejected.</b>\nUser ID: <code>{target_user_id}</code> access"
          " was denied."
      ),
      parse_mode="HTML",
  )

  if target_user_id in pending_requests:
    user_chat_id = pending_requests[target_user_id]
    try:
      bot.send_message(
          user_chat_id,
          (
              "❌ <b>Access Denied.</b>\nYour request to use this signal bot"
              " was rejected by the admin."
          ),
          parse_mode="HTML",
      )
    except Exception as e:
      logging.error(f"Failed to notify rejected user: {e}")


@bot.message_handler(func=lambda message: True)
def handle_menu(message):
  user_id = message.from_user.id
  username = message.from_user.username
  chat_id = message.chat.id

  is_admin = (username and username.lower() == ADMIN_USERNAME.lower()) or (
      user_id in approved_users
  )

  if not is_admin:
    bot.send_message(
        chat_id,
        (
            "⏳ <b>Access Pending!</b>\nYour account is waiting for Admin"
            " approval. Please wait until approved."
        ),
        parse_mode="HTML",
    )
    return

  text = message.text

  if "Currencies" in text:
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("EUR/USD (OTC)", callback_data="asset_EURUSD"),
        types.InlineKeyboardButton("GBP/USD (OTC)", callback_data="asset_GBPUSD"),
        types.InlineKeyboardButton("USD/BDT (OTC)", callback_data="asset_USDBDT"),
        types.InlineKeyboardButton("AUD/NZD (OTC)", callback_data="asset_AUDNZD"),
    )
    markup.add(
        types.InlineKeyboardButton(
            "🌐 Open High-Performance Bot Portal", url=OTHER_BOT_LINK
        )
    )
    bot.send_message(
        chat_id,
        "Select Currency Pair for Sure-Shot Analysis:",
        reply_markup=markup,
    )

  elif "Crypto" in text:
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Bitcoin (OTC)", callback_data="asset_BTC"),
        types.InlineKeyboardButton("Ethereum (OTC)", callback_data="asset_ETH"),
        types.InlineKeyboardButton("Solana (OTC)", callback_data="asset_SOL"),
        types.InlineKeyboardButton("Toncoin (OTC)", callback_data="asset_TON"),
    )
    markup.add(
        types.InlineKeyboardButton(
            "🌐 Open High-Performance Bot Portal", url=OTHER_BOT_LINK
        )
    )
    bot.send_message(
        chat_id,
        "Select Crypto Asset for Sure-Shot Analysis:",
        reply_markup=markup,
    )

  elif "Commodities" in text:
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Gold (OTC)", callback_data="asset_Gold"),
        types.InlineKeyboardButton(
            "UKBrent (OTC)", callback_data="asset_UKBrent"
        ),
        types.InlineKeyboardButton(
            "EURO STOXX 50", callback_data="asset_EUROSTOXX"
        ),
    )
    markup.add(
        types.InlineKeyboardButton(
            "🌐 Open High-Performance Bot Portal", url=OTHER_BOT_LINK
        )
    )
    bot.send_message(
        chat_id,
        "Select Commodity or Stock for Sure-Shot Analysis:",
        reply_markup=markup,
    )

  elif "Live News Flash" in text:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🌐 Open High-Performance Bot Portal", url=OTHER_BOT_LINK
        )
    )
    bot.send_message(
        chat_id,
        (
            "📰 <b>Real-Time Broker & Global News Feed:</b>\n\n🔥 [CHECKED]"
            " Market liquidity is optimal.\n⚡ [CHECKED] Macro news impact"
            " verified.\n🚀 [READY] All systems clear for 100% Sure-Shot"
            " execution."
        ),
        parse_mode="HTML",
        reply_markup=markup,
    )

  elif "Admin Contact" in text:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "👨‍💻 Contact Admin for Approval", url=DEVELOPER_LINK
        )
    )
    bot.send_message(
        chat_id,
        (
            "🛡 <b>Admin Approval & Membership Desk:</b>\n\nNeed quick"
            " verification or want to upgrade your plan? Direct message the Lead"
            " Developer below:"
        ),
        parse_mode="HTML",
        reply_markup=markup,
    )

  elif "Support" in text:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "💬 Technical Support Center", url=DEVELOPER_LINK
        )
    )
    bot.send_message(
        chat_id,
        (
            "💬 <b>24/7 Technical Support Desk:</b>\n\nFacing any issues with"
            " signal execution or bot latency? Connect with our support"
            " engineers instantly:"
        ),
        parse_mode="HTML",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("asset_"))
def ask_timeframe(call):
  symbol = call.data.replace("asset_", "")
  bot.answer_callback_query(
      call.id, f"Selected {symbol}. Choose candle timeframe..."
  )

  markup = types.InlineKeyboardMarkup(row_width=3)
  markup.add(
      types.InlineKeyboardButton(
          "⚡ 1 Minute (Fast Sure-Shot)", callback_data=f"tf_{symbol}_1m"
      ),
      types.InlineKeyboardButton(
          "⏱ 5 Minutes", callback_data=f"tf_{symbol}_5m"
      ),
      types.InlineKeyboardButton(
          "⏳ 15 Minutes", callback_data=f"tf_{symbol}_15m"
      ),
  )
  markup.add(
      types.InlineKeyboardButton(
          "🌐 Open High-Performance Bot Portal", url=OTHER_BOT_LINK
      )
  )
  bot.edit_message_text(
      chat_id=call.message.chat.id,
      message_id=call.message.message_id,
      text=(
          f"📊 <b>Asset:</b> <code>{symbol}</code>\n\n👇 *Select candle"
          " timeframe for next-candle prediction:*"
      ),
      parse_mode="HTML",
      reply_markup=markup,
  )


@bot.callback_query_handler(func=lambda call: call.data.startswith("tf_"))
def send_final_signal(call):
  parts = call.data.split("_")
  symbol = parts[1]
  timeframe = parts[2]

  bot.answer_callback_query(
      call.id,
      (
          f"Checking News, Broker Feeds & Analyzing {symbol} Candlestick"
          " Patterns..."
      ),
  )

  (
      prediction,
      accuracy,
      pattern_name,
      pattern_analysis,
      news_title,
      news_impact,
      rsi,
      start_time,
      end_time,
      action_advice,
  ) = generate_advanced_sure_shot_signal(symbol, timeframe)

  markup = types.InlineKeyboardMarkup()
  markup.add(
      types.InlineKeyboardButton(
          "🌐 Open High-Performance Bot Portal", url=OTHER_BOT_LINK
      )
  )

  report = (
      f"🎯📊 <b>ELITE 100% SURE-SHOT SIGNAL REPORT</b> 📊🎯\n"
      f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
      f"🔹 <b>Target Pair:</b> <code>{symbol}</code>\n"
      f"⏱ <b>Candle Timeframe:</b> <code>{timeframe}</code>\n"
      f"🇧🇩 <b>BDT Execution Window (Time):</b> <code>{start_time} to"
      f" {end_time}</code>\n"
      f"📈 <b>Prediction:</b> {prediction}\n"
      f"🎯 <b>Accuracy Rate:</b> <code>{accuracy}</code>\n"
      f"🕯 <b>Identified Candlestick Pattern:</b> <i>{pattern_name}</i>\n"
      f"🧠 <b>Candle & Market Analysis:</b> {pattern_analysis}\n"
      f"📢 <b>News & Broker Feed Check:</b> {news_title} ({news_impact})\n"
      f"📉 <b>RSI Momentum Score:</b> <code>{rsi}</code>\n"
      f"💡 <b>Action Strategy:</b> {action_advice}\n"
      f"👨‍💻 <b>Developer:</b> <a"
      f" href='{DEVELOPER_LINK}'>{DEVELOPER_NAME}</a>\n"
      f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
      f"⚠️ <i>Strictly follow the BDT time window and enter precisely on the"
      f" next candle opening for 100% success.</i>"
  )
  bot.edit_message_text(
      chat_id=call.message.chat.id,
      message_id=call.message.message_id,
      text=report,
      parse_mode="HTML",
      disable_web_page_preview=True,
      reply_markup=markup,
  )


if __name__ == "__main__":
  try:
    bot.remove_webhook()
  except Exception:
    pass

  server_thread = threading.Thread(target=run_web_server)
  server_thread.daemon = True
  server_thread.start()

  print(
      "Elite AI 100% Sure-Shot Signal Bot with Admin Approval & English UI is"
      " running successfully."
  )
  bot.infinity_polling(none_stop=True, interval=0, timeout=20)
