from threading import Thread
from typing import Optional
from openai import OpenAI

import gradio as gr

# Currently only runs from a local install of the OpenAI Rest API endpoint (i.e. a local running LLM such as Mistral)
client = OpenAI(base_url="http://127.0.0.1:8000/v1/", api_key="Not-a-real-key")
system_prompt = "You are a helpful AI assistant named Tom.  You must always provide correct, complete, and concise responses to the user's requests.  Once you've answered the user's request, end your feedback.  If the user provides information rather than a question or a command, simply reply with OK."
username = ""

# Very simple username password that will be accepted by the application
users = {
    "Jack": "password",
    "Jill": "password"
}

# Add the username to the header for a person greeting, this is called once the block loads
# request : the request object populated once login has occured
def create_greeting(request: gr.Request):
    return {usermd : gr.Markdown(value=f"# Welcome, {request.username}")}

# Ensure the user is logged in with the correct password
# This is NOT intended to be a highly secure finished product!
# username: the login username
# password: the user's password 
def auth_user(username, password):
    if username in users and password == users[username]:
        print(f"Successful login for user {username}")
        return True
    else:
        print(f"Failed login for user {username}")
        return False

# Use the Gradio Blocks function to setup the user interface
with gr.Blocks() as app:
    with gr.Row():
       usermd = gr.Markdown(value="Not logged in")
    
    with gr.Row():
      with gr.Column(scale=2): 
         chatbot = gr.Chatbot(elem_id="chatbot", scale=1)
         clear = gr.Button("Clear Chat History", scale=0)
      with gr.Column():
          msg = gr.Textbox()
          submitBtn = gr.Button("Submit Prompt")
       
    # Update the user's history with new messages
    def user(user_message, history):
        return "", history + [[user_message, None]]

    # Update the chatbot text area with new input from the server API
    def bot(history):
        print("\n\nQuestion: ", history[-1][0])

        history_openai_format = []
        for human, assistant in history:
              history_openai_format.append({"role": "user", "content": human })
              history_openai_format.append({"role": "assistant", "content": assistant})

        # Make the call to the OpenAI RestAPI endpoint with all the existing chat history plus the new prompt
        stream = client.chat.completions.create(
           model="mistral",
           messages=history_openai_format,
           stream=True,
        )

        # Since we are streaming, update the chatbot window as each item is returned from the OpenAI Rest API endpoint
        history[-1][1] = ""
        for chunk in stream:
            print(chunk.choices[0].delta.content or "", end="")
            if chunk.choices[0].delta.content is not None:
                  history[-1][1] += chunk.choices[0].delta.content

            yield history
        
    # Setup actions on the user interface components
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    submitBtn.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

    # Once the application loads, ensure that the username is at the top of the screen 
    # This may be important later on if we want a user to have different sessions by clicking a button for "new chat"
    app.load(create_greeting, inputs=None, outputs=usermd)


app.queue()
app.launch(auth=auth_user)