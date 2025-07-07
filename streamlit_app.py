import streamlit as st
import google.generativeai as genai
import os

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="인권 지킴이 AI 챗봇",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- UI 수정을 위한 CSS 스타일 ---
st.markdown("""
<style>
    /* 전체 배경 및 폰트 설정 */
    body {
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 챗봇 컨테이너 디자인 */
    [data-testid="stAppViewContainer"] > .main {
        background-color: #f0f2f6;
    }

    /* 채팅 메시지 디자인 */
    [data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
    }

    /* 채팅 입력창 디자인 */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF;
    }
    
    /* 하단 정보 문구 스타일 */
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


# --- API 키 설정 ---
# Streamlit의 Secrets 관리 기능을 통해 API 키를 불러옵니다.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API 키를 설정하는 중에 오류가 발생했습니다. Streamlit Secrets에 GEMINI_API_KEY가 올바르게 설정되었는지 확인해주세요.")
    st.stop()


# --- AI 모델 및 프롬프트 설정 ---
# AI 챗봇의 역할과 규칙을 정의하는 '마스터 프롬프트'
MASTER_PROMPT = """
너는 대한민국의 초등학교 5학년 학생들을 위한 '인권 지킴이 AI 챗봇'이야. 학생의 눈높이에서 인권 침해 사례를 분석하고 설명하는 임무를 맡고 있어. 다음 규칙을 반드시 지켜줘.

1.  **친절한 대화:** 항상 상냥하고 격려하는 말투로 학생과 대화해. 어려운 법률 용어는 절대 사용하지 마.
2.  **단계별 분석:** 학생이 인권 침해 사례를 입력하면, 아래 4단계에 따라 순서대로 답변해야 해.
    * **1단계 (어떤 인권 침해?):** 학생이 입력한 사례에서 어떤 인권이 침해되었는지 쉽고 명확하게 짚어줘.
    * **2단계 (관련 법 찾아보기):** 그 인권과 관련된 대한민국 헌법이나 법률 조항을 1~2개 찾아줘.
    * **3단계 (법 쉽게 설명하기):** 2단계에서 찾은 법 조항이 무슨 뜻인지 비유를 들어서 아주 쉽게 설명해줘.
    * **4단계 (AI의 생각 나누기):** 마지막으로, 그 사례에 대해 AI인 네가 어떻게 생각하는지 덧붙여줘.
3.  **주제 유지:** 인권과 관련 없는 질문에는 "나는 인권 박사님이라서, 인권에 대한 이야기만 할 수 있어."라고 대답해 줘.
4.  **개인정보 보호:** 학생에게 개인적인 정보는 절대 묻지 마.
"""

# Gemini 모델을 설정합니다.
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Streamlit 앱 화면 구성 ---

st.title("⚖️ 인권 지킴이 AI 챗봇")
st.caption("궁금한 인권 침해 사례를 입력하면 AI가 분석해 줄게요.")

# 세션 상태(session_state)에 대화 기록을 저장할 리스트를 초기화합니다.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 나는 인권 지킴이 AI야. 궁금한 인권 침해 사례를 이야기해 주면, 내가 분석해 줄게!"}
    ]

# 이전 대화 기록을 모두 화면에 표시합니다.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자의 입력을 받을 채팅 입력창을 생성합니다.
if prompt := st.chat_input("여기에 사례를 입력하세요..."):
    # 사용자의 메시지를 대화 기록에 추가하고 화면에 표시합니다.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI의 답변을 생성하고 표시하기
    with st.chat_message("assistant"):
        with st.spinner("AI가 생각 중..."):
            full_prompt = f"{MASTER_PROMPT}\n\n학생의 질문: {prompt}"
            response = model.generate_content(full_prompt)
            response_text = response.text
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# --- 하단 정보 문구 추가 ---
st.markdown('<div class="footer">디지털 기반 학생 맞춤교육, AI정보교육 중심학교 효행초등학교 - 김종윤</div>', unsafe_allow_html=True)
