import numpy as np
import torch
import time
import gradio as gr
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM

class ChatBot():
    def __init__(self):
        self.chat_history_ids = None
        self.bot_input_ids = None
        self.end_chat = False
        self.welcome()
        
    def welcome(self):
        print("Initializing ChatBot ...")
        time.sleep(2)
        print('Type "bye" or "quit" or "exit" to end chat \n')
        time.sleep(3)
        greeting = np.random.choice([
            "Welcome, I am ChatBot, here for your kind service",
            "Hey, Great day! I am your virtual assistant",
            "Hello, it's my pleasure meeting you",
            "Hi, I am a ChatBot. Let's chat!"
        ])
        print("ChatBot >>  " + greeting)
        
    def user_input(self):
        text = input("User    >> ")
        if text.lower().strip() in ['bye', 'quit', 'exit']:
            self.end_chat=True
            print('ChatBot >>  See you soon! Bye!')
            time.sleep(1)
            print('\nQuitting ChatBot ...')
        else:
            self.new_user_input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt').to(device)

    def bot_response(self):
        if self.chat_history_ids is not None:
            self.bot_input_ids = torch.cat([self.chat_history_ids, self.new_user_input_ids], dim=-1).to(device)
        else:
            self.bot_input_ids = self.new_user_input_ids.to(device)
        
        self.chat_history_ids = model.generate(self.bot_input_ids, max_length=1031, pad_token_id=tokenizer.eos_token_id).to(device)
        response = tokenizer.decode(self.chat_history_ids[:, self.bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        if response == "":
            response = self.random_response()
        print('ChatBot >>  '+ response)
        
    def random_response(self):
        i = -1
        response = tokenizer.decode(self.chat_history_ids[:, self.bot_input_ids.shape[i]:][0], skip_special_tokens=True)
        while response == '':
            i = i-1
            response = tokenizer.decode(self.chat_history_ids[:, self.bot_input_ids.shape[i]:][0], skip_special_tokens=True)
        if response.strip() == '?':
            reply = np.random.choice(["I don't know", "I am not sure"])
        else:
            reply = np.random.choice(["Great", "Fine. What's up?", "Okay"])
        return reply

# Load tokenizer and model
access_token = ""
tokenizer = AutoTokenizer.from_pretrained("epfl-llm/meditron-7b", token=access_token)
model = AutoModelForCausalLM.from_pretrained("epfl-llm/meditron-7b", token=access_token)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Build a ChatBot object
bot = ChatBot()

# Start chatting
while True:
    bot.user_input()
    if bot.end_chat:
        break
    bot.bot_response()