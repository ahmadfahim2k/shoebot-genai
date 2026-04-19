from pathlib import Path
import streamlit as st
from router import router
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from smalltalk import small_talk_interaction

st.set_page_config(
    page_title="ShoeBot",
    page_icon="\U0001F45F",
    layout="centered",
)

FAQ_PATH = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(FAQ_PATH)


def ask(query):
    route = router(query).name
    if route == "faq":
        return faq_chain(query)
    elif route == "sql":
        return sql_chain(query)
    elif route == 'small_talk':
        return small_talk_interaction(query)
    else:
        return f"Route {route} not implemented yet"


st.markdown("""
<style>
    .stAppDeployButton {display: none;}
    .block-container {padding-top: 1rem;}
    [data-testid="stSidebar"] > div:first-child {padding-top: 1rem;}
    .stChatMessage div[data-testid="stMarkdownContainer"] {
        word-wrap: break-word;
        overflow-wrap: break-word;
        word-break: break-all;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header(":athletic_shoe: ShoeBot")
    st.caption("Your AI-powered shoe shopping assistant")
    st.divider()
    st.markdown(
        "**I can help you with:**\n"
        "- :mag: Finding shoes by brand, price & rating\n"
        "- :question: FAQs about orders, returns & payments\n"
        "- :speech_balloon: General questions"
    )
    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# --- Main chat area ---
st.title(":athletic_shoe: ShoeBot")
st.caption("Ask me anything about shoes — search products, check policies, or just say hi!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Welcome message when chat is empty
if not st.session_state["messages"]:
    with st.chat_message("assistant", avatar="\U0001F45F"):
        st.markdown(
            "Hey there! I'm **ShoeBot** — your personal shoe shopping assistant. "
            "Try asking me something like:\n\n"
            '- *"Nike shoes under 5000"*\n'
            '- *"What is your return policy?"*\n'
            '- *"Best rated Puma shoes"*'
        )

for message in st.session_state.messages:
    kwargs = {"avatar": "\U0001F45F"} if message["role"] == "assistant" else {}
    with st.chat_message(message["role"], **kwargs):
        st.markdown(message["content"])

if query := st.chat_input("Ask about shoes, prices, policies..."):
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant", avatar="\U0001F45F"):
        with st.spinner("Thinking..."):
            response = ask(query)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
        