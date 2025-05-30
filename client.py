import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages(client, text_area):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            #Enable the text area to insert messages
            text_area.config(state=tk.NORMAL)  
            text_area.insert(tk.END, message + '\n')  
            text_area.yview(tk.END)  
            text_area.config(state=tk.DISABLED)  
        except:
            break #Exit the loop if an error occurs

def send_message(client, message_entry, text_area):
    message = message_entry.get()
    if message:
        #Send the message to the server
        client.send(message.encode('utf-8'))
        #Show the message in the text area
        text_area.config(state=tk.NORMAL)  
        text_area.insert(tk.END, "You: " + message + '\n')  
        text_area.yview(tk.END)  
        text_area.config(state=tk.DISABLED)  
        message_entry.delete(0, tk.END) #Clear the entry field

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555)) # Connect to the server

    # Create the GUI
    root = tk.Tk()
    root.title("Chat Client")
    
    # Create a scrolled text area for displaying messages
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.config(state=tk.DISABLED)  # Make the text area read-only initially

    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=10)

    message_entry.bind("<Return>", lambda event: send_message(client, message_entry, text_area))

    send_button = tk.Button(root, text="Send", command=lambda: send_message(client, message_entry, text_area))
    send_button.pack(pady=10)

    threading.Thread(target=receive_messages, args=(client, text_area), daemon=True).start()

    root.mainloop()

# Start the client
start_client()
