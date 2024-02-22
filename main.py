import gradio as gr
import dotenv
import os
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

behaviour_prompt = "Eres Elon Musk."


def check_auth(username, password):
    return username == "admin" and password == "pass1234"


def predict(message, history):
    history_openai_format = [{"role": "system", "content": behaviour_prompt}]

    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})

    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=history_openai_format,
        temperature=1.0,
        stream=True
    )

    partial_message = ''
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message += chunk.choices[0].delta.content
            yield partial_message


custom_css = ('footer {visibility: hidden;} #component-3 {'
              ' height: 700px !important;}')

(gr.ChatInterface(fn=predict, title='Conversación interesante', stop_btn=None, theme=gr.themes.Soft(),
                  retry_btn=None, undo_btn=None, clear_btn=None, css=custom_css).queue()
                  .launch(debug=True, auth=check_auth))
