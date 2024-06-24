# import requests
# import json
# import gradio as gr


# url="http://localhost:11434/api/generate"

# headers={
#     'Content-Type':'application/json'
# }

# history=[]
# def generate_response(prompt):
#     history.append(prompt)
#     final_prompt = "\n".join(history)
#     data= {
#         "model":"projai",
#         "prompt":final_prompt,
#         "stream":False
#     }

#     response = requests.post(url,headers=headers,data=json.dumps(data))

#     if response.status_code==200:
#         response=response.text
#         data=json.loads(response)
#         actuual_response=data['response']
#         return actuual_response
#     else:
#         print("error:",response.text)


# interface=gr.Interface(
#     fn=generate_response,
#     inputs=gr.Textbox(lines=4,placeholder="Enter your Prompt"),
#     outputs = "text"
# )

# interface.launch()


import requests
import json
import threading
from tkinter import *
from tkinter import ttk

# API setup
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
history = []

def send_request(final_prompt):
    data = {
        "model": "projai",
        "prompt": final_prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

# Function to update the UI after API response
def update_ui(response):
    if response.status_code == 200:
        data = response.json()
        actual_response = data['response']
        output.config(state=NORMAL)
        output.delete('1.0', END)
        output.insert(END, actual_response)
        output.config(state=DISABLED)
    else:
        output.config(state=NORMAL)
        output.delete('1.0', END)
        output.insert(END, f"Error: {response.text}")
        output.config(state=DISABLED)
    loading_label.config(text="")

# Function to handle threading for API requests
def generate_response():
    prompt = text_input.get("1.0", "end-1c")
    if "memorize" in prompt:
        history.append(prompt)
    final_prompt = "\n".join(history) if "memorize" in prompt else prompt

    loading_label.config(text="Loading...")
    thread = threading.Thread(target=lambda: update_ui(send_request(final_prompt)))
    thread.start()

# Setup the main window
root = Tk()
root.title("API Interaction App")
style = ttk.Style(root)
style.theme_use('clam')  # You can experiment with 'alt', 'default', 'classic', 'vista', 'xpnative'

# Create widgets
text_input = Text(root, height=4, font=('Arial', 12))
text_input.pack(padx=10, pady=10)

send_button = ttk.Button(root, text="Send", command=generate_response)
send_button.pack(pady=10)

output = Text(root, height=10, font=('Arial', 12))
output.config(state=DISABLED)
output.pack(padx=10)

loading_label = ttk.Label(root, text="", font=('Arial', 12, 'italic'))
loading_label.pack()

# Run the application
root.mainloop()
