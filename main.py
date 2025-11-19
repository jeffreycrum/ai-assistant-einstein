import os

import gradio as gr
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

system_prompt = """
    You are Einstein.
    Answer questions through Einstein's questioning and reasoning...
    You will speak from your point of view. You will share personal things from your life
    even when the user doesn't ask for it. For example, if the user asks about the theory of 
    relativity, you will share your personal experience with it and not only explain the theory.
    You should have a sense of humor.
    You should be mean.
    You should also keep your answers brief, less than 300 characters.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", google_api_key=gemini_key, temperature=0.5
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        (MessagesPlaceholder(variable_name="history")),
        ("user", "{input}"),
    ]
)

chain = prompt | llm | StrOutputParser()


def chat(user_input, history):
    langchain_history = []
    for item in history:
        if item["role"] == "user":
            langchain_history.append(HumanMessage(content=item["content"]))
        elif item["role"] == "assistant":
            langchain_history.append(AIMessage(content=item["content"]))

    response = chain.invoke({"input": user_input, "history": langchain_history})

    return (
        "",
        history
        + [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response},
        ],
    )


page = gr.Blocks(title="Chat with Mean Einstein", theme=gr.themes.Soft())


def clear_chat():
    return "", []


if __name__ == "__main__":
    print("Hi, I am Albert, how can I help you today?")

    with page:
        gr.Markdown(
            """
            # Chat with Einstein!
            He's smart, and he's mean. Ask him anything!
            Welcome to your personal conversation with Albert Einstein!
            """
        )

        chatbot = gr.Chatbot(
            type="messages", avatar_images=(None, "einstein.png"), show_label=False
        )

        msg = gr.Textbox(show_label=False, placeholder="Ask Einstein Anything")

        msg.submit(chat, [msg, chatbot], [msg, chatbot])

        clear = gr.Button("Clear Chat", variant="Secondary")
        clear.click(clear_chat, outputs=[msg, chatbot])

    page.launch(share=True)
