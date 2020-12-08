import telebot

from nlp_utils import get_item_for_search
from utils import krisa, by_popular, by_rating, generate_irec_markup, get_answer_from_top, Buffer
from utils import *
from parser import get_parsed_list, get_top_5
from config import token
from config import *
from _dialogflow import detect_intent_texts
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="newagent-gm9v-f9e2c39960b6.json"

bot = telebot.TeleBot(token, parse_mode=None)

user_dict = {}

intents_list = []
messages_list = []

small_talk_indicator = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id,
            'Привет, я помогаю найти варианты разных вещей по отзывам на Irecommend, ну или можем просто пообщаться. Что будем делать?'
                     )

@bot.message_handler(func=lambda message: message.text == by_popular and user_dict)
def echo_search_by_popular(message):
    global small_talk_indicator
    small_talk_indicator = False
    chat_id = message.chat.id
    item = user_dict[chat_id]
    to_find = item.saved
    result_list = get_parsed_list(to_find)
    top_results = get_top_5(result_list, 'feedback')
    answer = get_answer_from_top(top_results)
    bot.send_message(message.chat.id, answer, parse_mode='MarkdownV2')

@bot.message_handler(func=lambda message: message.text == small_talk)
def echo_small_talk(message):
    global small_talk_indicator
    small_talk_indicator=True
    bot.send_message(message.chat.id, 'Начинай!')


@bot.message_handler(func=lambda message: message.text == by_rating and user_dict)
def echo_search_by_rating(message):
    global  small_talk_indicator
    small_talk_indicator=False
    chat_id = message.chat.id
    item = user_dict[chat_id]
    to_find = item.saved
    result_list = get_parsed_list(to_find)
    top_results = get_top_5(result_list, 'rating')

    answer = get_answer_from_top(top_results)

    bot.send_message(message.chat.id, answer, parse_mode='MarkdownV2')

@bot.message_handler(func=lambda message: True)
def echo_get_intention(message):
    global small_talk_indicator
    answer, intent, action = detect_intent_texts(project_id, session_id, [message.text], language_code)
    if intent:
        bot.send_message(message.chat.id, intent)
    else:
        bot.send_message(message.chat.id, 'no intent')

    messages_list.append(message.text)
    intents_list.append(intent)
    if intent == 'my.make_order':
        small_talk_indicator = False
        bot.send_message(message.chat.id, answer)

    elif small_talk_indicator or intent=='my.lets_make_conversation' or action=='smalltalk.appraisal.thank_you':
        small_talk_indicator=True
        # answer, intent = detect_intent_texts(project_id, session_id, [message.text], language_code)
        bot.send_message(message.chat.id, answer)

    else:
        wish = get_item_for_search(message.text)

        if 'fail' not in wish:
            chat_id = message.chat.id

            markup = generate_irec_markup()

            user = Buffer(wish)

            user_dict[chat_id] = user

            bot.send_message(message.chat.id, 'Выбери способ подбора:', reply_markup=markup)
        else:
            negative = ''.join(['Много хочешь ', u'\U0001F5FF', '\n', 'Попробуй написать по-другому.'])
            bot.reply_to(message, negative)



# print(messages_list)
# print(intents_list)

bot.polling()