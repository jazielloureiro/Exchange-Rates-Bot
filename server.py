import telebot
from flask import Flask, request
from bot import bot

app = Flask(__name__)

@app.post('/')
def handle_webhook():
    updates = telebot.types.Update.de_json(request.json)
    bot.process_new_updates([updates])
    return ({}, 200)