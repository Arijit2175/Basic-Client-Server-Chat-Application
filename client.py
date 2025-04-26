import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client, text_area, client_listbox):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith("CLIENT_LIST:"):
                update_client_list(message.split(":")[1], client_listbox)
            else:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message + '\n')
                text_area.yview(tk.END)
                text_area.config(state=tk.DISABLED)
        except:
            break

def update_client_list(client_list, client_listbox):
    """Update the client list in the GUI."""
    client_listbox.delete(0, tk.END) 
    for client_name in client_list.split(','):
        client_listbox.insert(tk.END, client_name)

def send_message(client, message_entry, text_area, selected_client):
    message = message_entry.get()
    if message and selected_client:
        client.send(f"PRIVATE:{selected_client} {message}".encode('utf-8'))
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, "You: " + message + '\n')
        text_area.yview(tk.END)
        text_area.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    root = tk.Tk()
    root.title("Chat Client")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)

    client_listbox = tk.Listbox(root, height=10, width=20)
    client_listbox.pack(padx=10, pady=10)

    selected_client = None
    def on_client_select(event):
        nonlocal selected_client
        selected_client = client_listbox.get(client_listbox.curselection())
    
    client_listbox.bind('<<ListboxSelect>>', on_client_select)

    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=10)

    message_entry.bind("<Return>", lambda event: send_message(client, message_entry, text_area, selected_client))

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client, message_entry, text_area, selected_client))
    send_button.pack(pady=10)

    threading.Thread(target=receive_messages, args=(client, text_area, client_listbox), daemon=True).start()

    root.mainloop()

start_client()
