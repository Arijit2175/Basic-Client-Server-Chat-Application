import socket 
import threading 
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client, text_area):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            text_area.insert(tk.END, message + '\n')
            text_area.yview(tk.END)  
        except:
            break

def send_message(client, message_entry, text_area):
    message = message_entry.get()
    if message:
        client.send(message.encode('utf-8'))
        text_area.insert(tk.END, "You: " + message + '\n') 
        text_area.yview(tk.END)  
        message_entry.delete(0, tk.END)  