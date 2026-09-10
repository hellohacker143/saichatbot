```python
import os

import streamlit as st
import google.generativeai as genai


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            color: #777;
            font-size: 17px;
            margin-bottom: 30px;
        }

        .response-box {
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #ddd;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# GET API KEY
# ---------------------------------------------------------
def get_api_key():
    """
    Get GOOGLE_API_KEY from Streamlit Secrets.
    For local development, .env / environment variable
    can also be used.
    """

    # Streamlit Cloud
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        if api_key:
            return api_key
    except Exception:
        pass

    # Local environment variable
    api_key = os.getenv("GOOGLE_API_KEY")

    return api_key


# ---------------------------------------------------------
# CONFIGURE GEMINI
# ---------------------------------------------------------
api_key = get_api_key()

if not api_key:
    st.error("❌ GOOGLE_API_KEY is not configured.")

    st.info(
        """
        ### Streamlit Cloud Setup

        Go to:

        **Manage app → Settings → Secrets**

        Add:

        `GOOGLE_API_KEY = "YOUR_API_KEY"`
        """
    )

    st.stop()


try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("❌ Failed to configure Gemini API.")
    st.exception(e)
    st.stop()


# ---------------------------------------------------------
# GEMINI MODEL
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    """
    Load the Gemini model once and reuse it.
    """
    return genai.GenerativeModel("gemini-pro")


try:
    model = load_model()
except Exception as e:
    st.error("❌ Unable to load Gemini model.")
    st.exception(e)
    st.stop()


# ---------------------------------------------------------
# GEMINI RESPONSE FUNCTION
# ---------------------------------------------------------
def get_gemini_response(question):
    """
    Send the user's question to Gemini
    and return the generated response.
    """

    if not question or not question.strip():
        return "Please enter a question."

    try:
        response = model.generate_content(question)

        if response and hasattr(response, "text"):
            return response.text

        return "Sorry, Gemini did not return a response."

    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="main-title">🤖 Gemini AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask anything and get an AI-powered answer.</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------
question = st.text_input(
    "💬 Enter your question",
    placeholder="Example: Explain machine learning in simple words...",
    key="question"
)


# ---------------------------------------------------------
# BUTTONS
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    ask_button = st.button(
        "🚀 Ask Gemini",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    )


# ---------------------------------------------------------
# CLEAR CHAT
# ---------------------------------------------------------
if clear_button:
    st.session_state.chat_history = []
    st.rerun()


# ---------------------------------------------------------
# ASK GEMINI
# ---------------------------------------------------------
if ask_button:

    if not question.strip():
        st.warning("⚠️ Please enter a question first.")

    else:

        with st.spinner("🤔 Gemini is thinking..."):

            answer = get_gemini_response(question)

        # Save conversation
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------
if st.session_state.chat_history:

    st.subheader("💬 Conversation")

    for chat in reversed(st.session_state.chat_history):

        st.markdown("### 👤 You")
        st.write(chat["question"])

        st.markdown("### 🤖 Gemini")

        st.markdown(
            f"""
            <div class="response-box">
                {chat["answer"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")

st.caption("Powered by Google Gemini + Streamlit")
```
