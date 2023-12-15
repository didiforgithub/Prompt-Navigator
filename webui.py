import streamlit as st

# 设置全局属性
st.set_page_config(
    page_title='Stratey Choose Agent',
    page_icon=' ',
    layout='wide'
)


## st.sidebar 下的内容会被渲染到侧边栏
with st.sidebar:
    st.title('欢迎来到我的应用')
    st.markdown('---')
    st.markdown('这是它的特性：\n- feature 1\n- feature 2\n- feature 3')

## 默认渲染到主界面
st.title('这是主界面')
st.info('这是主界面内容')