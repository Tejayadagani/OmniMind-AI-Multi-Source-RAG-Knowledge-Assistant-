import os
import streamlit as st

from llm.groq_client import get_response
from utils.pdf_export import generate_pdf
from rag.loader import load_documents
from rag.vector_store import create_index
from rag.query_engine import query_documents
from rag.study_engine import generate_study_material
from rag.load_index import load_index
import streamlit as st

# Load external CSS
with open("/Users/bhargavchowdaryyadagani/Desktop/ai-nexus-rag-system/.streamlit/.streamlit/style.css ") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from utils.youtube_utils import get_transcript
from utils.web_scraper import scrape_website
from utils.source_manager import add_text_to_kb
from utils.history_manager import (
    load_history,
    save_history,
    create_chat
)

st.set_page_config(
    page_title="OmniMind AI",
    page_icon="🧠",
    layout="wide"
)

# --------------------------
# Session State
# --------------------------
if "chats" not in st.session_state:
    st.session_state.chats = load_history()

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.title("🧠 OmniMind")

    if st.button("➕ New Chat", use_container_width=True):
        new_chat = create_chat("New Chat", "General Chat")
        st.session_state.chats.append(new_chat)
        save_history(st.session_state.chats)
        st.session_state.current_chat = new_chat
        st.session_state.messages = []

    st.divider()
    st.subheader("History")

    for chat in st.session_state.chats:
        icon = {
            "Document": "📄",
            "YouTube": "🎥",
            "Website": "🌐",
            "General Chat": "💬"
        }.get(chat["source"], "💬")

        if st.button(f"{icon} {chat['title']}",key=chat["id"],use_container_width=True):
            st.session_state.current_chat = chat
            st.session_state.messages = chat["messages"]

# --------------------------
# Header
# --------------------------
st.title("🧠 OmniMind AI")
st.caption("Documents • YouTube • Websites • Study Assistant")

# --------------------------
# Source Selector
# --------------------------
source = st.selectbox(
    "Select Source",
    ["General Chat", "Document", "YouTube", "Website"]
)

# --------------------------
# Document Upload
# --------------------------
if source == "Document":
    uploaded_file = st.file_uploader("Upload Document")

    if uploaded_file:
        os.makedirs("data/uploads", exist_ok=True)
        file_path = os.path.join("data/uploads", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Process Document"):
            docs = load_documents()
            create_index(docs, "documents")
            st.success("Document indexed successfully.")

# --------------------------
# YouTube
# --------------------------
elif source == "YouTube":
    youtube_url = st.text_input("YouTube URL")

    if st.button("Index Video"):
        transcript = get_transcript(youtube_url)
        add_text_to_kb(transcript, "youtube", youtube_url)
        st.success("Video indexed.")

# --------------------------
# Website
# --------------------------
elif source == "Website":
    website_url = st.text_input("Website URL")

    if st.button("Index Website"):
        text = scrape_website(website_url)
        add_text_to_kb(text, "website", website_url)
        st.success("Website indexed.")

# --------------------------
# Study Assistant
# --------------------------
st.divider()
st.subheader("📚 Quick Actions")

col1, col2, col3, col4 = st.columns(4)
study_mode = None

with col1:
    if st.button("📝 Notes"):
        study_mode = "Notes"

with col2:
    if st.button("🎯 MCQs"):
        study_mode = "MCQs"

with col3:
    if st.button("🧠 Flashcards"):
        study_mode = "Flashcards"

with col4:
    if st.button("💼 Interview"):
        study_mode = "Interview"

if study_mode:
    try:
        if source == "Document":
            index = load_index("documents")
        elif source == "YouTube":
            index = load_index("youtube")
        elif source == "Website":
            index = load_index("website")
        else:
            st.warning("Select a source first.")
            st.stop()

        result = generate_study_material(index, "entire source", study_mode)
        st.markdown(result)

        pdf_path = generate_pdf(result)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download PDF",
                data=f,
                file_name="study_material.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(str(e))

# --------------------------
# Chat History
# --------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --------------------------
# Chat Input
# --------------------------
prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    if (
        st.session_state.current_chat
        and st.session_state.current_chat["title"] == "New Chat"
    ):
        st.session_state.current_chat["title"] = prompt[:30]
        save_history(st.session_state.chats)

    with st.chat_message("user"):
        st.write(prompt)

    if source == "General Chat":
        answer = get_response(prompt)
    else:
        try:
            if source == "Document":
                index = load_index("documents")
            elif source == "YouTube":
                index = load_index("youtube")
            elif source == "Website":
                index = load_index("website")

            answer, nodes = query_documents(index, prompt)
        except:
            answer = "No indexed knowledge found."

    st.session_state.messages.append({"role": "assistant", "content": answer})

    if st.session_state.current_chat:
        st.session_state.current_chat["messages"] = st.session_state.messages
        save_history(st.session_state.chats)

    with st.chat_message("assistant"):
        st.write(answer)
