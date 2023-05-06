import openai
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import json
import ctypes
from tkinter import messagebox, simpledialog
import os.path
import time
openai.api_key = ''
# Define the file name for the API key
API_KEY_FILE = "api_key.txt"

# Load the API key from the file if it exists
if os.path.isfile(API_KEY_FILE):
    with open(API_KEY_FILE, "r") as f:
        openai.api_key = f.read().strip()
        print(openai.api_key)

# Define the function that saves the API key to a file
def save_api_key(api_key):
    with open(API_KEY_FILE, "w") as f:
        f.write(api_key)

# Define the function that handles the "Set API Key" command
def set_api_key():
    api_key = simpledialog.askstring("Set API Key", "Enter your API key:")
    if api_key:
        openai.api_key = api_key
        save_api_key(api_key)
        messagebox.showinfo("API Key Set", "API key has been set.")

 
ctypes.windll.shcore.SetProcessDpiAwareness(1)



# Define the function that handles the user's input and generates a response
# Define the function that handles the user's input and generates a response
def generate_response(input_text):
    if not openai.api_key:
        return "Please enter API key in the options menu to use."

    # Show loading message
    content = "Thinking..."
    chat_box.configure(state="normal")
    image_id = chat_box.image_create("end", image=gpt)
    chat_box.insert("end", " : " + content + "\n", ("ai", "bg_ai"))
    chat_box.configure(state="disabled")
    root.update()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_text}]
    )

    json_object = json.loads(json.dumps(response))

    # Extract the content field from the choices dictionary
    content = json_object['choices'][0]['message']['content']

    # Remove any occurrence of "Thinking..." in the generated text
    content = content.replace("Thinking...", "")

    # Delete the loading message
    chat_box.configure(state="normal")
    chat_box.delete(image_id, "end")
    if chat_box.compare("end-1c", "!=", "1.0"):
        chat_box.insert("end", "\n")
    chat_box.configure(state="disabled")


    # Return the generated text
    return content





# Define the function that handles the "Send" button click event
def send_message():
    input_text = input_box.get()
    response_text = generate_response(input_text)
    response_text = response_text.replace("Thinking...", "")
    chat_box.configure(state="normal")
    chat_box.image_create("end", image=user)
    chat_box.insert("end", " : " + input_text + "\n", ("user", "bg_user"))
    chat_box.image_create("end", image=gpt)
    chat_box.insert("end", " : " + response_text + "\n", ("ai", "bg_ai"))
    chat_box.configure(state="disabled")



# Set up the Tkinter GUI
root = tk.Tk()
root.title("ChatGPT")
root.geometry("675x455")
user = PhotoImage(file="UserIcon.png").subsample(7, 7)
gpt = PhotoImage(file="GPTIcon.png").subsample(7, 7)
root.configure(bg="#333333")
root.iconbitmap("GPTIcon.ico")

# Create a menu bar
menu_bar = tk.Menu(root)

# Add an "Options" menu to the menu bar
options_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=options_menu)

# Add a "Set API Key" option to the "Options" menu
options_menu.add_command(label="Set API Key", command=set_api_key)

# Set the menu bar
root.config(menu=menu_bar)

# Define the input and chat boxes
chat_box = tk.Text(root, height=15, state="disabled", wrap="word")
chat_box.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
chat_box.configure(background='#333333', highlightthickness=0)


# Define the style for the send button
send_button_style = ttk.Style()
send_button_style.configure("Custom.TButton", padding=4, width=5, font=('Helvetica', 10), foreground="#000000", borderwidth=0, bordercolor="#ffffff")

# Define the input style
input_style = ttk.Style()
input_style.configure("Custom.TEntry", padding=10, relief="flat", font=("Helvetica", 12), background="#ffffff", height=send_button_style.lookup("Custom.TButton", "padding"))

# Define the input box and send button using the custom styles
input_box = ttk.Entry(root, width=50, style="Custom.TEntry")
input_box.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

send_button = ttk.Button(root, text="Send", image=gpt, compound=tk.LEFT, style="Custom.TButton", command=send_message)
send_button.grid(row=1, column=1, sticky="e", padx=10, pady=10)

# Configure the column widths to make the input box stretch to fill the window
root.columnconfigure(0, weight=1)
root.columnconfigure(1, minsize=100)

# Define the tag configurations for the background colors
chat_box.tag_configure("user", background="#333333", foreground="#ffffff")
chat_box.tag_configure("ai", background="#444444", foreground="#ffffff")
chat_box.tag_configure("bg_user", background="#333333")
chat_box.tag_configure("bg_ai", background="#444444")

# Start the GUI main loop
root.mainloop()
