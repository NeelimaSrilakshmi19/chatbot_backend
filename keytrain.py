import re

def is_query_chitchat(query):
    greeting_words = set(['hi', 'hello', 'you', 'how', 'good', 'fine', 'hey', 'are', 'what', 'im', 'am', 'ive', 'whats', 'up', 'hows', 'your', 'me', 'i', 'thanks', 'awesome', 'ha', 'haha', ' hahaha', 'nice', 'thats', 'glad', 'awesome','welcome', 'doing', 'well'])

    greeting_word_count = sum(1 for word in query.split() if word in greeting_words)
    #print("debug:----------------------------------------------")
    #print(word for word in query.split() if word in greeting_words)
    #print("greeting wc: ", greeting_word_count)
    #print("debug:----------------------------------------------")
    ischatbig = greeting_word_count >= 2 and len(query.split()) < 15
    #print(ischatbig)
    ischatone = greeting_word_count == 1 and len(query.split()) == 1
    #print(ischatone)
    #print(len(query.split()))
    return ischatbig or ischatone #true is chat, false is query