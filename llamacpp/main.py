from threading import Thread
from typing import Optional
from openai import OpenAI

import gradio as gr

client = OpenAI(base_url="http://127.0.0.1:8000/v1/", api_key="Not-a-real-key")
system_prompt = "You are a helpful AI assistant named Tom.  You must always provide correct, complete, and concise responses to the user's requests.  Once you've answered the user's request, end your feedback.  If the user provides information rather than a question or a command, simply reply with OK."
username = ""

CSS ="""
.contain { display: flex; flex-direction: column; }
.gradio-container { height: 100vh !important; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; overflow: auto;}
"""

users = {
    "Jack": "password",
    "Jill": "password"
}

def create_greeting(request: gr.Request):
    return {usermd : gr.Markdown(value=f"# Welcome, {request.username}")}

def updateUser(request : gr.Request):
    username = request.username
    usermd = gr.Markdown(value="TEST")
    print("Username : " + username)


def auth_user(username, password):
    if username in users and password == users[username]:
        print(f"Successful login for user {username}")
        return True
    else:
        print(f"Failed login for user {username}")
        return False


with gr.Blocks(css=CSS) as app:
    with gr.Row():
       usermd = gr.Markdown(value="Not logged in")
    
    with gr.Row():
      with gr.Column(scale=2): 
         chatbot = gr.Chatbot(elem_id="chatbot", scale=1)
         clear = gr.Button("Clear Chat History", scale=0)
      with gr.Column():
          msg = gr.Textbox()
          submitBtn = gr.Button("Submit Prompt")
       

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        print("\n\n" + username + " Question: ", history[-1][0])

        history_openai_format = []
        for human, assistant in history:
              history_openai_format.append({"role": "user", "content": human })
              history_openai_format.append({"role": "assistant", "content": assistant})

        stream = client.chat.completions.create(
           model="mistral",
           messages=history_openai_format,
           stream=True,
        )

        history[-1][1] = ""
        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")
            if chunk.choices[0].delta.content is not None:
                  history[-1][1] += chunk.choices[0].delta.content

            yield history
        

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    submitBtn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

    app.load(create_greeting, inputs=None, outputs=usermd)

app.queue()
app.launch(auth=auth_user)