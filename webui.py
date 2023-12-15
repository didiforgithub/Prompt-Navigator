import streamlit as st
from Generator import PromptGenerator
from ErnieLLM import ErnieLLM
from Modifier import Modify
from streamlit_chat import message

# 设置全局属性
st.set_page_config(
    page_title='Streamlit Demo',
    page_icon='',
    layout='wide'
)

st.title('Streamlit Demo ⚡')
session_state = st.session_state
if 'response_result' not in session_state:
    session_state.response_result= []
tab1, tab2, tab3 = st.tabs(['Introduction', 'Prompt Generate', 'Evaluation'])



with tab1:
    '''
    ```text
    项目介绍与各种策略介绍
    ```
    '''

with tab2:
    origin_cols_num = 2
    c1, c2 = st.columns(origin_cols_num)
    with c1:
        user_input = st.text_area("Your Prompt", height=100)
    with c2:
        selected_strategys = st.multiselect(
            "Strategy:", ["zero-shot cot", "few-shot cot", "zero-shot contrastive"]
        )
        st.write('num:', len(selected_strategys))

    if st.button("生成响应"):
        prompt_generator = PromptGenerator()
        for strategy in selected_strategys:
            response = prompt_generator.generate(user_input, strategy)
            st.session_state.response_result.append(response)
        columns = st.columns(len(selected_strategys) + 1)
        for i, col in enumerate(columns):
            with col:
                if i == 0:
                    st.header("origin input")
                    st.text_area(label="origin input", value=user_input, height=200, disabled=True)
                else:
                    st.header(selected_strategys[i - 1])
                    st.text_area(label=selected_strategys[i - 1], value=session_state.response_result[i-1], height=200, disabled=True)

    # TODO 如何避免Reload需要再看一下
    reserve_input = st.text_area(label="reserve", value="reserve", height=50)
    delete_input = st.text_area(label="delete", value="delete", height=50)
    add_input = st.text_area(label="add", value="add", height=50)

    if st.button("生成修改结果"):
        modify_block = Modify()
        modified_result = modify_block.GetModifyResult(
            reserve=reserve_input,
            delete=delete_input,
            add=add_input
        )
        st.text_area(label="modified result", value=modified_result, height=50)


with tab3:
    st.title('Evaluation Different prompt generation strategies')
    eval_example_input = st.text_area("Example", height=100)
    if st.button("Generate Result"):
        eval_llm = ErnieLLM()
        eval_columns = st.columns(len(selected_strategys) + 1 )
        for i, col in enumerate(eval_columns):
            with col:
                if i == 0:
                    st.header("origin result")
                    eval_result = eval_llm.response(user_input + eval_example_input)
                    st.text_area(label="origin result", value=eval_result, height=200)
                else:
                    st.header(selected_strategys[i - 1])
                    eval_result = eval_llm.response(session_state.response_result[i-1] + eval_example_input)
                    st.text_area(
                        label=selected_strategys[i - 1],
                        value=eval_result,
                        height=200
                    )

    # message("Hello, I'm a chatbot!")  # 显示聊天消息
    # message("How can I help you?", is_user=True)  # 将消息对齐到右侧
    # placeholder = st.empty()  # 创建一个空白容器
    # input_ = st.text_input("你：")  # 接收用户输入
    # with placeholder.container():
    #     message("我收到了你的消息：" + input_)