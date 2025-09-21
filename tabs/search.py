import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import openai
import os
import faiss
import numpy as np
from dotenv import load_dotenv
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# .env 파일 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# OCR을 통해 PDF 페이지에서 텍스트 추출
def extract_text_with_ocr(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if not page_text:
                image = page.to_image().original
                page_text = pytesseract.image_to_string(Image.fromarray(image), lang='kor')
            text += page_text
    return text

# 텍스트를 청크로 나누기
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# OpenAI API를 사용해 텍스트 임베딩 생성
def get_openai_embeddings(texts):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )
    embeddings = [item['embedding'] for item in response['data']]
    return np.array(embeddings).astype('float32')

# PDF 파일을 열어 텍스트를 추출하고 벡터 데이터베이스 생성
def build_vectorstore(pdf_file):
    text = extract_text_with_ocr(pdf_file)
    chunks = chunk_text(text)
    embeddings = get_openai_embeddings(chunks)
    
    # FAISS 인덱스 생성
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    return index, chunks

# 가장 유사한 문서 검색
def search_documents(index, chunks, query, top_k=3):
    query_embedding = get_openai_embeddings([query])
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]

# RAG 체인 정의
def rag_chain(pdf_file, question):
    index, chunks = build_vectorstore(pdf_file)
    relevant_docs = search_documents(index, chunks, question)
    context = "\n\n".join(relevant_docs)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Check the pdf content and answer the question."},
        {"role": "user", "content": f"Question: {question}\n\nContext: {context}\n\nAnswer:"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# PDF 생성 함수
def create_pdf(question, answer):
    buffer = BytesIO()
    
    # 폰트 등록 (한글 지원)
    pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))
    
    # 스타일 정의
    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        name="Title",
        fontName='HYSMyeongJo-Medium',
        fontSize=18,
        leading=24,
        spaceAfter=10,
        alignment=1,  # center
        textColor=colors.HexColor("#2E4053")
    )
    style_body = ParagraphStyle(
        name="Body",
        fontName='HYSMyeongJo-Medium',
        fontSize=11,
        leading=18,
        spaceAfter=6
    )
    
    # PDF 파일 설정
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=20, rightMargin=20,
                            topMargin=20, bottomMargin=20)
    
    # 스토리 구성
    story = [
        Paragraph("질문과 답변", style_title),
        Spacer(1, 12),
        Paragraph(f"질문: {question}", style_body),
        Spacer(1, 12),
        HRFlowable(width="100%", thickness=1, color=colors.grey, spaceBefore=6, spaceAfter=10),
        Paragraph(f"답변: {answer}", style_body),
        Spacer(1, 12),
        HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceBefore=6)
    ]
    
    # 문서 생성
    doc.build(story)
    buffer.seek(0)
    return buffer

# Streamlit 탭에서 호출할 함수
def show_search():
    st.header("📒 매뉴얼 검색")
    st.subheader("📄 PDF 업로드")
    pdf_file = st.file_uploader("PDF 파일을 선택하세요", type=["pdf"])
    
    if pdf_file:
        st.success("PDF 업로드 완료!")
    
    st.subheader("🔍 자연어 질문")
    # 사용자 지정 예시 질문 사전
    SUGGESTIONS = {
        "🔵 간단한 요약을 제공해 줄 수 있나요?": "간단한 요약을 제공해 줄 수 있나요?",
        "🟢 이 장비의 안전 수칙은 무엇인가요?": "이 장비의 안전 수칙은 무엇인가요?",
        "🟠 자주 발생하는 오류 코드와 해결 방법은?": "자주 발생하는 오류 코드와 해결 방법은?",
        "🟣 작업 순서를 단계별로 알려 주세요.": "작업 순서를 단계별로 알려 주세요.",
    }
    
    # 세션 상태를 사용해 현재 입력된 질문을 저장
    if "current_query" not in st.session_state:
        st.session_state.current_query = ""
    
    # 예시 질문 버튼 생성
    st.write("예시 질문:")
    for label, question in SUGGESTIONS.items():
        if st.button(label):
            st.session_state.current_query = question
    
    # 질문 입력 필드 (세션 상태와 연동)
    query = st.text_input("질문 입력", value=st.session_state.current_query)
    
    # 세션 상태를 사용해 검색 결과를 저장
    if "search_result" not in st.session_state:
        st.session_state.search_result = None
    
    if st.button("검색 결과 불러오기"):
        if pdf_file and query:
            with st.spinner("검색 중..."):
                st.session_state.search_result = rag_chain(pdf_file, query)
        elif not pdf_file:
            st.warning("PDF 파일을 업로드해 주세요.")
        else:
            st.warning("질문을 입력해 주세요.")
    
    # 세션 상태에 저장된 검색 결과 표시
    if st.session_state.search_result:
        st.write(f"질문: {query}")
        st.write(f"답변: {st.session_state.search_result}")

        # PDF 다운로드 버튼
        pdf_buffer = create_pdf(query, st.session_state.search_result)
        st.download_button(
            label="📥 답변 PDF 다운로드",
            data=pdf_buffer,
            file_name="답변.pdf",
            mime="application/pdf"
        )