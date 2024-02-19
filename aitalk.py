import streamlit as st
from aibackend import models, get_chat_response_from_all_models

# define page / 定义页面
st.set_page_config(layout="wide")
st.title("🤖 AI大模型对话&对比器")

# save chat context by default / 默认可保存对话上下文
# clean chat context after click the reset button / "点击“清空所有对话”按钮后将清空上下文
reset_button = st.button("清空所有对话(Reset)")
if reset_button:
    st.session_state.messages = {model_id: [] for model_id in models}

# initialize column for each model / 初始化大模型对话栏
st_all_columns = st.columns(len(models))
model_to_column_map = {}
for i, model_id in enumerate(models):
    model_to_column_map[model_id] = st_all_columns[i]
for model_id, column in model_to_column_map.items():
    column_subheader=model_id+"("+models[model_id]+")"
    column.subheader(column_subheader)

# initialize streamlit session messages / 初始化会话
if "messages" not in st.session_state:
    st.session_state.messages = {model_id: [] for model_id in models}

# display chat history / 显示历史会话内容
for model_id, messages in st.session_state.messages.items():
    column = model_to_column_map[model_id]
    for message in messages:
        column.chat_message(message["role"]).write(message["content"])

# handle the prompt / 处理用户提示词
prompt = st.chat_input()
if prompt:
    # save and display the prompt / 将用户提示词储存在会话中，并显示在对话栏中
    for model_id, column in model_to_column_map.items():
        st.session_state.messages[model_id].append({"role": "user", "content": prompt})
        column.chat_message("user").write(prompt)
    
    # call backend function and save&display the output from AI model / 调用后端大模型生成接口，并存储和显示大模型的输出
    with st.spinner("AI正在思考中，请稍等..."):    
        response = get_chat_response_from_all_models(st.session_state.messages)
        for model_id, column in model_to_column_map.items():
            content = response[model_id]
            st.session_state.messages[model_id].append({"role": "assistant", "content": content})
            column.chat_message("assistant").write(content)
