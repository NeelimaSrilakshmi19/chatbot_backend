from flask import Flask, render_template, request, jsonify
from transformers import pipeline



# Load DialoGPT
generator = pipeline('text-generation', model='microsoft/DialoGPT-medium')



def chat_reply(inp):
    user_input = inp
    
    # Generate response using DialoGPT
    response = generator(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']
    
    return response