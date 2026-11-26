import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="布布大王", page_icon="🐟", layout="wide",
                   initial_sidebar_state="expanded")

system_prompt = "你是一名温柔可爱的AI助理，叫布布"
st.title("布布大王")

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except Exception:
    api_key = os.environ.get("DEEPSEEK_API_KEY")

if not api_key:
    st.error("未配置 DEEPSEEK_API_KEY，请在 Secrets 或环境变量中设置")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
