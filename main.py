import streamlit as st
from tabs.home import show_home
from tabs.search import show_search
from tabs.wiki import show_wiki
from tabs.pattern import show_pattern

# 페이지 기본 설정
st.set_page_config(page_title="Manupilot", layout="wide")

# 탭 구성
tabs = st.tabs(["홈", "매뉴얼 검색", "협업 게시판", "이상 패턴 분석"])

# 각 탭 호출
with tabs[0]:
    show_home()
with tabs[1]:
    show_search()
with tabs[2]:
    show_wiki()
with tabs[3]:
    show_pattern()