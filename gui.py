import socket 
import threading 
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client, text_area):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            text_area.insert(tk.END, message + '\n')
            text_area.yview(tk.END)  # Auto-scroll to the latest message
        except:
            break