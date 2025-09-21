import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="Manupilot", layout="wide")

# 상단 로고(또는 제목)와 중제목
st.markdown(
    '''
    <div style="text-align: center; padding: 20px;">
        <h1 style="margin-bottom: 0; color: #D84315;">Manupilot</h1>
        <h3 style="margin-top: 5px; color: #6D4C41;">매뉴얼은 짧게, 지식은 함께, 문제는 빠르게</h3>
    </div>
    ''',
    unsafe_allow_html=True
)
with st.sidebar:
    st.subheader("🔐 로그인")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")  # 비밀번호 입력란 (숨김 처리)
    if st.button("로그인"):
        if username and password:
            st.session_state['logged_in_user'] = username  # 로그인한 사용자 이름 저장
            st.success(f"환영합니다, {username}님!")
        else:
            st.warning("사용자 이름과 비밀번호를 모두 입력하세요.")

            
with st.sidebar:
    # 검색창
    st.subheader("🔎 검색")
    sidebar_query = st.text_input("검색어를 입력하세요")
    if sidebar_query:
        st.write(f"사이드바 검색어: {sidebar_query} (검색 결과는 여기에 표시됩니다)")
    
    # 여백
    st.write("\n\n\n")
    
    # 버그 개선 및 도움 요청
    st.subheader("🐞 버그·도움 요청")
    st.markdown(
        """
        - 버그가 발생했거나 도움이 필요하시면 아래 메일로 연락해 주세요.
        """
    )
    
    # 메일 주소
    st.markdown(
        """
        
            📧 support@manupilot.com
        
        """,
        unsafe_allow_html=True
    )
    
    # 여백
    st.write("\n\n\n")
    
    # 푸터
    st.markdown(
        '''
        
        
            © 2025 Manupilot
        
        ''',
        unsafe_allow_html=True
    )


st.markdown(
    """
    <style>
    .custom-card {
        background-color: #FFF8F1;
        border: 1px solid #FF7043;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .custom-card strong {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 카드 컴포넌트 함수 (둥근 직사각형 스타일 적용)
def card(title, content, image_path=None, icon=None):
    icon_html = f'{icon} ' if icon else ''
    st.markdown(
        f'''
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <strong>{icon_html}{title}</strong>
            <div style="margin-top: 10px;">{content}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )
    if image_path:
        st.image(image_path, use_column_width=True)

def show_home():
    # 서비스 소개 카드
    card(
        "✅ 서비스 소개",
        "Manupilot은 제조 현장에서의 정보 공유 어려움을 해소하고, 작업자 간 지식 교류를 촉진하여 불량 및 이상 상황을 빠르게 파악할 수 있도록 돕는 서비스입니다. "
        "긴 매뉴얼을 핵심 절차·안전수칙·FAQ로 자동 요약해 PDF 형태로 제공하며, 자연어 기반 질문에 즉시 필요한 절차와 근거를 찾아드립니다. "
        "또한, 작업자들이 축적한 노하우를 태그·글·사진과 함께 손쉽게 등록하고 자동으로 분류·연결해 줌으로써, 그동안 어려웠던 도메인 특화 정보의 공유를 한층 수월하게 만듭니다. "
        "공정 지원 기능을 통해 증상·설비·조건을 입력하면 유사 사례와 대응 절차를 즉시 제시하여 문제 해결 시간을 획기적으로 단축할 수 있습니다. "
        "Manupilot과 함께라면 제조 현장에서 더욱 효율적으로 업무를 수행할 수 있습니다.",
    )
    
    # 데모 영상 카드
    card(
        "📹 사용자 영상",
        "영상은 준비 중입니다. 업로드 예정!"
    )
    
    # 구분선 추가
    st.markdown("---")
    
    # 사용 방법을 표 형태로 정리
    st.header("📋 사용 방법")
    
    # 사용 방법 데이터
    usage_data = {
        "단계": ["1. PDF 매뉴얼 업로드", "2. 자연어 질문 입력", "3. 협업 위키 활용", "4. 이상 패턴 분석"],
        "설명": [
            "상단의 매뉴얼 검색 탭에서 PDF 파일을 업로드합니다.",
            "원하는 질문을 자연어로 입력하면 AI가 매뉴얼을 요약해 답변을 제공합니다.",
            "위키 게시판 탭에서 작업 노하우와 자주 발생하는 문제를 등록하고 공유하세요.",
            "이상 패턴 분석 탭에서 설비 로그 데이터를 시각화해 이상 패턴을 빠르게 감지합니다."
        ]
    }
    
    # 데이터프레임 생성
    usage_df = pd.DataFrame(usage_data)
    usage_df.index = [""] * len(usage_df)
    
    # 표 출력
    st.table(usage_df)
    
    # 구분선 추가
    st.markdown("---")
    
    # FAQ 섹션
    st.header("🔍 FAQ")
    with st.expander("Manupilot는 어떤 서비스인가요?"):
        st.write("제조 매뉴얼 요약, 자연어 검색, 협업 위키, 불량 문제 해결을 한 번에 제공합니다.")
    with st.expander("어떤 파일 형식을 지원하나요?"):
        st.write("PDF 및 텍스트 파일을 지원합니다.")
    with st.expander("데이터는 안전한가요?"):
        st.write("데이터는 암호화되어 안전하게 저장됩니다.")
    with st.expander("무료로 사용할 수 있나요?"):
        st.write("기본 기능은 무료로 제공되며, 프리미엄 플랜도 준비되어 있습니다.")
    with st.expander("어떤 AI 모델을 사용하나요?"):
        st.write("Manupilot은 최신 자연어 처리 모델을 사용해 빠르고 정확한 답변을 제공합니다.")
    with st.expander("검색 결과가 정확하지 않으면 어떻게 하나요?"):
        st.write("질문을 조금 더 구체적으로 입력하거나, 위키 게시판에서 추가 정보를 확인해 보세요.")