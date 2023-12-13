from flask import Flask, request, jsonify
from flask_cors import CORS
#from classcq import *
#from chatbot_v2 import *
#from wikiq import *
#from model_2 import *
from model_pkl import *
import random
from dialochat import *
from keytrain import *
from dotenv import load_dotenv
import os

def prepro(s0):
    s = re.sub(r"[-–‐—]", ' ', s0)
    #remove non alpha numeric space chars
    ss = re.sub('[^0-9a-zA-Z\s]+', '', str(s))
    #remove extra spaces
    ss = re.sub("\s\s+" , " ", ss)
    return ss.lower()

#chat--------------------------------------
#from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch


#chat---------------------------------------------
app = Flask(__name__)
load_dotenv()
CORS(app)  # Enable CORS for all routes
@app.route('/chat', methods=['POST'])
def hello():
    data = request.get_json()
    request_promptt=data['message']
    request_prompt = prepro(request_promptt)
    #if(classify(request_prompt)):
    if not is_query_chitchat(request_prompt):#keytrain
        #query - traintry
        bot_reply, topic = query_reply(request_prompt)
    else:
        #chat - dialochat
        user_input = request_prompt
        # Generate and print the chatbot's response
        chatbot_response = chat_reply(user_input)
        bot_reply = chatbot_response
        #conversation_history += "Bot: "
        #conversation_history += bot_reply
        #conversation_history += "\n"
        topic = "chat"
        # Add chatbot response to the conversation history
    #topic_list = ['Health', 'Environment', 'Technology', 'Economy', 'Entertainment', 'Sports', 'Politics', 'Education', 'Travel', 'Food']
    #topic = random.choice(topic_list)
    #bot_reply=request_prompt+" bruh"
    response_data = {'message': bot_reply, 'topic':topic}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)