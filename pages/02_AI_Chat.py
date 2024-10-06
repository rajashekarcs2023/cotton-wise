import streamlit as st
from utils.openai_chat import get_ai_response

st.title("💬 AI Advisor Chat")
st.markdown("Ask our AI advisor any questions about cotton farming!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI advisor for cotton farmers in Maharashtra, India. Provide helpful, concise advice on cotton farming practices, pest control, irrigation, and market trends."}
    ]

# Display chat messages from history on rerun
for message in st.session_state.messages[1:]:  # Skip the system message
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What's your question about cotton farming?"):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    response = get_ai_response(st.session_state.messages)

    # Add assistant response to chat history and display it
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = [st.session_state.messages[0]]  # Keep only the system message
    st.experimental_rerun()