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

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    root = tk.Tk()
    root.title("Chat Client")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)  

    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=10)

    message_entry.bind("<Return>", lambda event: send_message(client, message_entry, text_area))

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client, message_entry, text_area))
    send_button.pack(pady=10)

    threading.Thread(target=receive_messages, args=(client, text_area), daemon=True).start()

    root.mainloop()

start_client()  