import streamlit as st
from Generator import PromptGenerator
from LLM import ErnieLLM,OpenAILLM,Llama
from Modifier import Modify
from Evaluator import Evaluator
from streamlit_chat import message

# 定义相关Session State
session_state = st.session_state
if 'response_result' not in session_state:
    session_state.response_result = []
if 'answer_dict' not in session_state:
    session_state.answer_dict = {}
if 'llm_choice' not in session_state:
    session_state.llm_choice = "ernie-bot-4"
if "prompt_generate_button" not in session_state:
    session_state.prompt_generate_button = False
if "generate_result_button" not in session_state:
    session_state.generate_result_button = False
if "eval_button" not in session_state:
    session_state.eval_button = False
if "modify_button" not in session_state:
    session_state.modify_button = False


def click_prompt_generate_button():
    session_state.prompt_generate_button = True


def click_generate_result_button():
    session_state.generate_result_button = True


def click_eval_button():
    session_state.eval_button = True


def click_modify_button():
    session_state.modify_button = True

@st.cache(suppress_st_warning=True)
def prompt_generate(user_in, selected_strategies):
    prompt_generator = PromptGenerator(session_state.llm_choice)
    for strategy in selected_strategies:
        response = prompt_generator.generate(user_in, strategy)
        session_state.response_result.append(response)

@st.cache(suppress_st_warning=True)
def generate_result(user_in, selected_strategies):
    prompt_generator = PromptGenerator(session_state.llm_choice)
    for strategy in selected_strategies:
        response = prompt_generator.generate(user_in, strategy)
        session_state.response_result.append(response)


@st.cache(suppress_st_warning=True)
def result_llm_response(input_text, llm_choice):
    if llm_choice == "ernie-bot-4":
        eval_llm = ErnieLLM()
    elif llm_choice == "gpt-3.5-turbo":
        eval_llm = OpenAILLM()
    elif llm_choice == "llama-7b":
        eval_llm = Llama()
    else:
        eval_llm = ErnieLLM()
    return eval_llm.response(input_text)


@st.cache(suppress_st_warning=True)
def eval_response(eval_example,llm_choice,answer_dict):
    evaluator = Evaluator(llm_choice)
    eval_result = evaluator.evaluate(eval_example, answer_dict)
    return eval_result


@st.cache(suppress_st_warning=True)
def modify_response(reserve_in, delete_in, add_in):
    modify_block = Modify()
    modified_result = modify_block.GetModifyResult(
        reserve=reserve_in,
        delete=delete_in,
        add=add_in
    )
    return modified_result



# 设置全局属性
st.set_page_config(
    page_title='Streamlit Demo',
    page_icon='',
    layout='wide'
)

st.title('Streamlit Demo ⚡')
tab1, tab2, tab3, tab4 = st.tabs(['Introduction', 'Prompt Generate', 'Evaluation', 'Modify'])

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
        user_input = st.text_area("Your Prompt", height=130)
    with c2:
        selected_llm = st.selectbox(
            "LLM:", ["ernie-bot-4", "gpt-3.5-turbo", "llama-7b"]
        )
        session_state.llm_choice = selected_llm
        selected_strategys = st.multiselect(
            "Strategy:", ["zero-shot cot", "zero-shot contrastive", "zero-shot difficulty", "few-shot cot",
                          "few-shot contrastive", "few-shot difficulty"]
        )
    st.button("生成响应", on_click=click_prompt_generate_button)
    if session_state.prompt_generate_button:
        prompt_generate(user_input, selected_strategys)
        columns = st.columns(len(selected_strategys) + 1)
        for i, col in enumerate(columns):
            with col:
                if i == 0:
                    st.header("origin input")
                    st.text_area(label="origin input", value=user_input, height=200)
                else:
                    st.header(selected_strategys[i - 1])
                    st.text_area(label=selected_strategys[i - 1], value=session_state.response_result[i - 1],
                                 height=200)

with tab3:
    st.title('Evaluation Different prompt generation strategies')
    eval_example_input = st.text_area("Example", height=100)
    st.button("Generate Result", on_click=click_generate_result_button)
    if session_state.generate_result_button:
        eval_columns = st.columns(len(selected_strategys) + 1)
        for i, col in enumerate(eval_columns):
            with col:
                if i == 0:
                    st.header("origin result")
                    generate_result = result_llm_response(user_input + "\n" + eval_example_input, session_state.llm_choice )
                    st.text_area(label="origin result", value=generate_result, height=200)
                    session_state.answer_dict["origin result"] = generate_result
                else:
                    st.header(selected_strategys[i - 1])
                    generate_result = result_llm_response(
                        session_state.response_result[i - 1] + "\n" + eval_example_input, session_state.llm_choice )
                    st.text_area(
                        label=selected_strategys[i - 1],
                        value=generate_result,
                        height=200
                    )
                    session_state.answer_dict[selected_strategys[i - 1]] = generate_result

    st.button("Eval", on_click=click_eval_button)
    if session_state.eval_button:
        eval_result = eval_response(eval_example_input, session_state.llm_choice, session_state.answer_dict)
        for x, y in eval_result.items():
            st.write(x, y)
        st.write(eval_result)

with tab4:
    input_col_nums = 3
    c1, c2, c3 = st.columns(input_col_nums)
    with c1:
        reserve_input = st.text_area(label="reserve", value="reserve", height=50)
    with c2:
        delete_input = st.text_area(label="delete", value="delete", height=50)
    with c3:
        add_input = st.text_area(label="add", value="add", height=50)

    st.button("生成修改结果", on_click=click_modify_button)
    if session_state.modify_button:
        modified_res = modify_response(reserve_input, delete_input, add_input)
        st.text_area(label="modified result", value=modified_res, height=50)

    # message("Hello, I'm a chatbot!")  # 显示聊天消息
    # message("How can I help you?", is_user=True)  # 将消息对齐到右侧
    # placeholder = st.empty()  # 创建一个空白容器
    # input_ = st.text_input("你：")  # 接收用户输入
    # with placeholder.container():
    #     message("我收到了你的消息：" + input_)
