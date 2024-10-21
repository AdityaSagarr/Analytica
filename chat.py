import streamlit as st

def chat_display(messages):
    """Display chat messages in the Streamlit app."""
    for message in messages:
        role = "user" if message['role'] == 'user' else 'assistant'
        color = "blue" if role == "user" else "green"
        content = message['content'] if isinstance(message['content'], str) else message['content'].get('answer', 'No answer found.')
        st.markdown(f"<div style='text-align: {'right' if role == 'user' else 'left'}; color: {color}; font-size: 18px; font-family: \"Segoe UI\", Tahoma, Geneva, Verdana, sans-serif;'><b>🤵🏻</b> {content}</div>", unsafe_allow_html=True)
