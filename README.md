# iRecommendChatBot
ChatBot for small talks and ordering things from irecommend.

bot.py - handles the users queries and sends them to telegram chat using
telegram api from  telebot library. 

nlp_utils.py contains functions for extracting 'wish' from user's query. Algorithm:
      1. Incoming query is preprocessed with Natasha Morph Tagger and Syntax parser;
      2. Looking for first inanimate noun;
      3. After found, looks for its dependent words;
Example: input: 'Я хочу плюшевого медведя;
         output: 'плюшевого медведя';
Then output is used to look for results on site.
With functions in parser.py obtained page is parsed.
utils.py provides different functions for bot 'buttons' and selecting options of sorting found data: by rating or by popularity.

config.py - some variables to acces the right agent in dialogflow

In _dialogwlof.py there is only one function that takes the query as an input and by using dialogflow_v2 API outputs the response of the small talk model, 
the action and the intent of the input. 

config.py - some variables to acces the right agent in dialogflow (nothing interesting) 

newagent-...b6.json - settings for the used agent (nothing interesting) 

