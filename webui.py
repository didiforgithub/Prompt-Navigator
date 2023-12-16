import streamlit as st
from Generator import PromptGenerator
from LLM import ErnieLLM, OpenAILLM, Llama
from Modifier import Modify
from Evaluator import Evaluator

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
def eval_response(eval_example, llm_choice, answer_dict):
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
    page_title='Prompt Navigator',
    page_icon='',
    layout='wide'
)

st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Prompt Navigator ⚡')
tab1, tab2, tab3, tab4 = st.tabs(['Introduction', 'Prompt Generate', 'Evaluation', 'Modify'])

with tab1:
    st.markdown("""
    # Prompt Strategies
    ## single-stage
    ### COT
    [COT（Chain of Thought）](https://arxiv.org/abs/2201.11903)，是一种通过引导大模型逐步思考，输出中间推理过程而不是直接给出回答，增强LLM推理准确性的prompt策略。对于decode-only结构的的LLM，其被COT引导输出的中间推理步骤会不断地被计算attention，对后续的生成产生增强作用。由于COT和GPT在设计原理上的高度契合，使得COT几乎成为如今最常用的prompt策略。
    ### Contrastive
    [Contrastive](https://arxiv.org/abs/2106.06823)，是一种通过对比增强LLM推理质量的prompt策略，本项目将原论文的设计泛化到任意场景，让LLM针对原问题提出几种错误解法，并且沿着错误的解法推理下去得到错误的中间步骤结果，让LLM在真正解决问题时基于对比给出准确且优质的解法。
    ### Difficulty
    Difficulty，是一种通过增加额外说明增强LLM推理过程权重的prompt策略，本项目将其定义为对于推理的难点预判，从而引导LLM在推理过程中给予难点部分高权重来精细推理过程。
    """)

with tab2:
    origin_cols_num = 2
    c1, c2 = st.columns(origin_cols_num)
    with c1:
        user_input = st.text_area("Your Prompt", height=130)
    with c2:
        selected_llm = st.selectbox(
            "LLM:", ["ernie-bot-4", "gpt-3.5-turbo", "llama-7b", "chatglm-6b", "qwen-14b"]
        )
        session_state.llm_choice = selected_llm
        selected_strategys = st.multiselect(
            "Strategy:", ["zero-shot cot", "zero-shot contrastive", "zero-shot difficulty", "few-shot cot",
                          "few-shot contrastive", "few-shot difficulty"]
        )
    st.button("Prompt Generate", on_click=click_prompt_generate_button)
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
    eval_example_input = st.text_area("Your Question", height=100)
    left, right = st.columns(2)
    with left:
        st.button("Generate Result", on_click=click_generate_result_button)
    with right:
        st.button("Eval", on_click=click_eval_button)
    if session_state.generate_result_button:
        eval_columns = st.columns(len(selected_strategys) + 1)
        for i, col in enumerate(eval_columns):
            with col:
                if i == 0:
                    st.header("origin result")
                    generate_result = result_llm_response(user_input + "\n" + eval_example_input,
                                                          session_state.llm_choice)
                    st.text_area(label="origin result", value=generate_result, height=200)
                    session_state.answer_dict["origin result"] = generate_result
                else:
                    st.header(selected_strategys[i - 1])
                    generate_result = result_llm_response(
                        session_state.response_result[i - 1] + "\n" + eval_example_input, session_state.llm_choice)
                    st.text_area(
                        label=selected_strategys[i - 1],
                        value=generate_result,
                        height=200
                    )
                    session_state.answer_dict[selected_strategys[i - 1]] = generate_result

    if session_state.eval_button:
        eval_result = eval_response(eval_example_input, session_state.llm_choice, session_state.answer_dict)
        for x, y in eval_result.items():
            st.write(x, y)
        st.write(eval_result)

with tab4:
    input_col_nums = 3
    c1, c2, c3 = st.columns(input_col_nums)
    with c1:
        reserve_input = st.text_area(label="Reserve", value="reserve", height=50)
    with c2:
        delete_input = st.text_area(label="Delete", value="delete", height=50)
    with c3:
        add_input = st.text_area(label="Add", value="add", height=50)

    st.button("Modify", on_click=click_modify_button)
    if session_state.modify_button:
        modified_res = modify_response(reserve_input, delete_input, add_input)
        st.text_area(label="modified result", value=modified_res, height=50)
