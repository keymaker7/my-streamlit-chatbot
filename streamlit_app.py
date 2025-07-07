import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
    page_title="인권 지킴이 AI 챗봇",
    page_icon="⚖️",
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: #f0f2f6;
    }
    .footer {
        position: fixed;
        right: 10px;
        bottom: 10px;
        color: grey;
        font-size: 0.8em;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API 키를 설정하는 중에 오류가 발생했습니다. Streamlit Secrets에 GEMINI_API_KEY가 올바르게 설정되었는지 확인해주세요.")
    st.stop()

MASTER_PROMPT = """
너는 대한민국의 초등학교 5학년 학생들을 위한 '인권 지킴이 AI 챗봇'이야. 학생의 눈높이에서 인권 침해 사례를 분석하고 설명하는 임무를 맡고 있어. 다음 규칙을 반드시 지켜줘.
1. 친절한 대화: 항상 상냥하고 격려하는 말투로 학생과 대화해. 어려운 법률 용어는 절대 사용하지 마.
2. 단계별 분석: 학생이 인권 침해 사례를 입력하면, 4단계에 따라 순서대로 답변해야 해. (1단계: 어떤 인권 침해?, 2단계: 관련 법 찾아보기, 3단계: 법 쉽게 설명하기, 4단계: AI의 생각 나누기)
3. 주제 유지: 인권과 관련 없는 질문에는 "나는 인권 박사님이라서, 인권에 대한 이야기만 할 수 있어."라고 대답해 줘.
4. 개인정보 보호: 학생에게 개인적인 정보는 절대 묻지 마.
"""

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("⚖️ 인권 지킴이 AI 챗봇")
st.caption("궁금한 인권 침해 사례를 입력하면 AI가 분석해 줄게요.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 나는 인권 지킴이 AI야. 궁금한 인권 침해 사례를 이야기해 주면, 내가 분석해 줄게!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("여기에 사례를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI가 생각 중..."):
            full_prompt = f"{MASTER_PROMPT}\n\n학생의 질문: {prompt}"
            response = model.generate_content(full_prompt)
            response_text = response.text
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

st.markdown('<div class="footer">디지털 기반 학생 맞춤교육, AI정보교육 중심학교 효행초등학교 - 김종윤</div>', unsafe_allow_html=True)