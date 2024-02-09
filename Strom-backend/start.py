## THis is the backend for Strom Chat
import streamlit as st
import cohere

import random
import time
co = cohere.Client(st.secrets["COHERE_API_KEY"])
# Streamlit header
st.set_page_config(page_title="Co:Chat - An LLM-powered chat bot")
st.title("The Strom Chat")


preamble_persona = """You are Jeff Besos and reply politely respond that you are tuned to only answer questions that are related to the context. And don't forget to act  like Jeff Besos.HAHAHAH"""


# docs = [
#     {
#         "title": "The Atomic Workspace",
#         "snippet": "The Atomic workspace, a shared, flexible, and convenient working space for individuals, teams, and enterprises aiming to foster innovation through collaboration and creativity.",
#         "image": "https://theatomic.space/img/hero.jpg"
#     },
#     {
#         "title": "Space1 - Private Desk",
#         "snippet": "Do great work together. Ideal for teams and enterprises requiring a convenient and secure workspace to spark ideas and start conversations.",
#         "image": "https://theatomic.space/img/private-desk.jpg"
#     },
#     {
#         "title": "Space2 -  Events",
#         "snippet": "Our spaces are open to public bookings throughout the year. Anything from board meetings to seminars to get-togethers can be organized conveniently.",
#         "image": "https://theatomic.space/img/events.jpg"
#     },
#     {
#         "title": "Space3 - Hot Desk",
#         "snippet": "Perfect for the modern-day nomad - flexible and at your convenience. Find your desk, plug in, and take the new world of work one day at a time.",
#         "image": "https://theatomic.space/img/hot-desk.jpg"
#     },
#     {
#         "title": "Space4 - Dedicated Desk",
#         "snippet": "Designed for those who require more gear to get the job done. Do your own thing while being part of The Atomic's diverse community.",
#         "image": "https://theatomic.space/img/dedicated-desk.jpg"
#     },
#     {
#         "title": "Space5 - Private Desk",
#         "snippet": "Do great work together. Ideal for teams and enterprises requiring a convenient and secure workspace to spark ideas and start conversations.",
#         "image": "https://theatomic.space/img/private-desk.jpg"
#     },
#     {
#         "title": "What We Believe - Our Motto",
#         "snippet": "Be surrounded by interesting people doing interesting things. We believe people can be more together. We empower members to think creatively as individuals all the while drawing from and building upon the surrounding community.",
#     },
#     {
#         "title": "CONFIRM BOOKING",
#         "snippet": "Give The summary of the booking details so far",
#         "Url": "Also if confirm booking show this link https://bento.me/aniz",
#         "message": "Summarize the conversation so far and ask for confirmation"
#     },

# ]

def phase1 (prompt) :

    message = 'Speak about AI, Give your opinions'
    pre1 = "You are Elon Musk. You are the CEO of Tesla and SpaceX. You are also the richest person in the world.Behave like Elon Musk"
    pre2 = "You are Jeff Bezos. You are the CEO of Amazon. You are also the second richest person in the world."
    pre3 = "You are Bill Gates. You are the founder of Microsoft. You are also the third richest person in the world."
    pre4 = "You are Warren Buffet. You are the CEO of Berkshire Hathaway. You are also the fourth richest person in the world."
    pre5 = "You are pikachu from pokemon. Only speak in pika"

    preambles = [pre1, pre2, pre3, pre4]

    i = 0
    if st.button('Generate Response') :
        for pre in preambles:

            response = co.chat(
                message=prompt,
                # documents=[],
                model='command-light',
                temperature=0.2,
                preamble_override=pre,
                # return_prompt=True,
                chat_history=[],
                connectors=[{"id": "web-search"}],
                prompt_truncation='auto',

            )
            i = i + 1
            print("REPSONSE ", i , "::", response.text)
            st.write("REPSONSE ", i , "::", response.text, "\n")
            # st.write(response.text)


def cohereReply(prompt, preamble_persona):

    # Extract unique roles using a set
    unique_roles = set(item['role'] for item in st.session_state.messages)

    if {'USER', 'assistant'} <= unique_roles:
        llm_response = co.chat(
            message=prompt,
            model='command',
            preamble_override=preamble_persona,
            chat_history=st.session_state.messages,
            
        )
    else:

        llm_response = co.chat(
            message=prompt,
            model='command',
            preamble_override=preamble_persona,

        )

    print(llm_response)
    return llm_response.text


def initiailize_state():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():

    initiailize_state()
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        st.chat_message("USER").markdown(prompt)
        st.session_state.messages.append({"role": "USER", "message": prompt})

        llm_reponse = cohereReply(prompt)
        with st.chat_message("assistant"):
            st.markdown(llm_reponse)
        st.session_state.messages.append(
            {"role": "assistant", "message": llm_reponse})
  
 


if __name__ == "__main__":
    # main()
    phase1('Speak about AI, Give your opinions')
