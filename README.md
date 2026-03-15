# K Intelligence 해커톤 2025 
> Track2 본선 - SOTA K 기반의 프롬프트 엔지니어링 <br>
> 바이브 코딩 기반 서비스 개발

## 대회 설명
프롬프트 엔지니어링을 기반으로 바이브 코딩(Vibe Coding)을 수행하며, 이를 통해 서비스 개발 전 과정을 완성해야 합니다.
- 프롬프트 엔지니어링 → 기획서 도출 → 바이브 코딩 → 서비스 개발 및 완성

## 주최 및 주관
주최/주관: KT
운영: 데이콘


[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)](https://streamlit.io)
[![GPT-4o](https://img.shields.io/badge/GPT--4o-OpenAI-412991?logo=openai)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green)](https://langchain.com)
[![FAISS](https://img.shields.io/badge/FAISS-VectorDB-blue)](https://faiss.ai)

---

# 📌 서비스 소개

제조 현장의 긴 매뉴얼 탐색, 신입 교육 부담, 노하우 단절, 불량 대응 지연 문제를 LLM + RAG로 해결합니다.

- PDF 업로드 → 핵심 절차·안전 수칙·FAQ 자동 요약
- 자연어 질문 → FAISS 기반 매뉴얼 정밀 검색
- 작업자 노하우 게시판 → AI 자동 분류·연관 문서 링크
- CSV 센서 로그 분석 → 이상 감지 & 이메일 알림

---

# 🔧 기술 스택

| 분류 | 기술 |
|------|------|
| LLM | GPT-4o (KT SOTA K) |
| RAG | LangChain + FAISS |
| Frontend | Streamlit |
| Backend | Flask API |

---

# 🧠 프롬프트 전략

Instruction / Context / Input Data / Output Indicator 4요소 구조화로 LLM 출력 일관성 확보.
페르소나(현장 작업자·엔지니어·신입)별 응답 최적화, Few-shot + CoT 기법 적용.

---

# 🚀 실행 방법
```bash
git clone https://github.com/YOUR_USERNAME/manupilot.git
cd manupilot
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

---

> 한계: 실제 제조 데이터 검증 필요 / 추후 MES·PLC 연동 및 다국어 지원 예정
