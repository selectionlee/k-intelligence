import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def show_wiki():
    st.header("📚 협업 게시판")
    
    # 세션 상태에 초기 태그 목록이 없으면 빈 리스트로 초기화
    if 'all_tags' not in st.session_state:
        st.session_state.all_tags = []
    
    # 태그 추천 (빈도 기반)
    tag_frequencies = {tag: 0 for tag in st.session_state.all_tags}
    for entry in st.session_state.get('wiki', []):
        for tag in entry['tags']:
            if tag in tag_frequencies:
                tag_frequencies[tag] += 1
    recommended_tags = sorted(tag_frequencies, key=tag_frequencies.get, reverse=True)[:5]
    
    # 새 태그 입력 필드
    st.subheader("🔖 새 태그 입력")
    new_tag = st.text_input("새 태그 입력 (Enter 키로 추가)")
    if new_tag:
        if new_tag not in st.session_state.all_tags:
            st.session_state.all_tags.append(new_tag)
            st.success(f"태그 '{new_tag}' 추가 완료")
        else:
            st.warning("이미 존재하는 태그입니다.")
        st.session_state['new_tag'] = ''
    
    # 추천 태그 버튼
    if recommended_tags:
        st.write("추천 태그:")
        for tag in recommended_tags:
            if st.button(tag):
                if tag not in st.session_state.all_tags:
                    st.session_state.all_tags.append(tag)
    
    st.markdown("---")
    
    # 새 위키 항목 등록
    st.subheader("✍ 새 항목 등록")
    author = st.text_input("작성자 이름")
    
    # 태그 입력
    tags = st.multiselect(
        "태그 (기존 태그 선택 또는 새 태그 입력 후 Enter)",
        options=st.session_state.all_tags,
        default=[],
        help="기존 태그를 선택하거나 새 태그를 입력한 뒤 Enter를 눌러 추가하세요."
    )
    
    # 위키 내용 입력 (예시 템플릿 제공)
    example_template = (
        "## 제목\n\n"
        "### 개요\n\n"
        "- 핵심 요약\n"
        "- 주요 포인트\n\n"
        "### 상세 내용\n\n"
        "1. 첫 번째 항목\n"
        "2. 두 번째 항목\n\n"
        "### 참고 자료\n\n"
        "- 링크 1\n"
        "- 링크 2\n"
    )
    content = st.text_area("위키 내용", value=example_template, height=200)
    
    # 위키 저장
    if st.button("저장"):
        if author and tags and content:
            new_entry = {'author': author, 'tags': tags, 'content': content}
            st.session_state.setdefault('wiki', []).append(new_entry)
            st.success("위키 저장 완료")
        else:
            st.warning("작성자 이름, 태그, 내용을 모두 입력하세요.")
    
    st.markdown("---")
    
    # 게시판 내 검색 기능
    st.subheader("🔍 게시판 검색")
    search_query = st.text_input("검색어 입력")
    
    # 필터 태그
    filter_tags = st.multiselect("필터 태그", options=st.session_state.all_tags)
    
    # 검색 및 필터 적용
    wiki_data = st.session_state.get('wiki', [])
    if search_query:
        wiki_data = [w for w in wiki_data if search_query.lower() in w['content'].lower() or search_query.lower() in w['author'].lower()]
    if filter_tags:
        wiki_data = [w for w in wiki_data if any(tag in w['tags'] for tag in filter_tags)]
    
    # 유사 항목 병합 제안
    if len(wiki_data) > 1:
        contents = [entry['content'] for entry in wiki_data]
        vectorizer = TfidfVectorizer().fit_transform(contents)
        similarities = cosine_similarity(vectorizer)
        np.fill_diagonal(similarities, 0)
        similar_pairs = np.argwhere(similarities > 0.8)
        
        if similar_pairs.size > 0:
            st.warning("유사도가 높은 항목이 있습니다. 병합을 고려해 보세요.")
            for i, j in similar_pairs:
                st.write(f"유사 항목: [{wiki_data[i]['author']}]와 [{wiki_data[j]['author']}] (유사도: {similarities[i, j]:.2f})")
    
    # 게시판 표시
    st.subheader("📂 게시판 목록")
    if wiki_data:
        for entry in wiki_data:
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                    <strong>작성자</strong>: {entry['author']}<br />
                    <strong>태그</strong>: {', '.join(entry['tags'])}<br />
                    <strong>내용</strong>:<br />{entry['content']}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("등록된 항목이 없습니다.")