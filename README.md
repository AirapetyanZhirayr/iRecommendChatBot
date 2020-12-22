# iRecommendChatBot
ChatBot for small talks and ordering things from irecommend.

bot.py - handles the users queries and sends them to telegram chat using
telegram api from  telebot library. 

In _dialogwlof.py there is only one function that takes the query as an input and by using dialogflow_v2 API outputs the response of the small talk model, 
the action and the intent of the input. 

config.py - some variables to acces the right agent in dialogflow (nothing interesting) 

newagent-...b6.json - settings for the used agent (nothing interesting) 

