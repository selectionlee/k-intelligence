import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# 목업 데이터 생성
def create_mock_data():
    num_records = 10000
    num_equipment = 5
    equipment_ids = [f'EQP{i+1:03d}' for i in range(num_equipment)]
    start_time = pd.Timestamp('2024-11-01 00:00:00')
    
    np.random.seed(42)
    data = []
    for i in range(num_records):
        equipment_id = np.random.choice(equipment_ids)
        timestamp = start_time + pd.Timedelta(seconds=i)
        sensor_values = {
            '온도': np.random.uniform(20, 100),
            '진동': np.random.uniform(0, 1),
            '압력': np.random.uniform(0, 50),
            '유량': np.random.uniform(0, 5),
            '전력': np.random.uniform(0, 500)
        }
        status_code = 'NORMAL' if sensor_values['온도'] < 80 else 'ALERT'
        is_anomaly = 1 if sensor_values['온도'] >= 80 else 0
        data.append({
            '설비ID': equipment_id,
            '시간': timestamp,
            **sensor_values,
            '상태코드': status_code,
            '이상 여부': is_anomaly
        })
    return pd.DataFrame(data)

# 세션 상태 초기화
if 'data' not in st.session_state:
    st.session_state['data'] = create_mock_data()

if 'saved_records' not in st.session_state:
    st.session_state['saved_records'] = []

# Streamlit 앱
def show_pattern():
    st.header("📊 이상 패턴 분석")
    
    # 데이터 미리보기
    st.subheader("데이터 미리보기")
    st.dataframe(st.session_state['data'].head())
    
    # 설비 ID와 센서 선택
    st.subheader("설비 및 센서 선택")
    selected_equipment = st.selectbox("설비 ID", st.session_state['data']['설비ID'].unique())
    selected_sensor = st.selectbox("센서값 선택", ['온도', '진동', '압력', '유량', '전력'])
    
    # 선택한 설비와 센서 데이터 필터링
    filtered_data = st.session_state['data'][st.session_state['data']['설비ID'] == selected_equipment]
    
    # 센서별 색상 지정
    sensor_colors = {
        '온도': '#ff7f0e',
        '진동': '#2ca02c',
        '압력': '#1f77b4',
        '유량': '#d62728',
        '전력': '#9467bd'
    }
    
    # 시각화
    st.subheader(f"{selected_equipment}의 {selected_sensor} 시계열 그래프")
    chart = alt.Chart(filtered_data).mark_line(color=sensor_colors[selected_sensor]).encode(
        x='시간:T',
        y=alt.Y(selected_sensor, title=selected_sensor),
        tooltip=['시간:T', selected_sensor]
    ).properties(width=800, height=400).interactive()
    st.altair_chart(chart, use_container_width=True)
    
    # --- 2. 공정 지원 기능 ---
    st.subheader("유사 불량 패턴 탐색 및 공정 지원")
    
    # 조건 입력
    threshold = st.number_input(f"{selected_sensor} 임계치", value=80.0)
    receiver_email = st.text_input("알림 수신 이메일", "receiver@example.com")
    
    # 유사 불량 패턴 탐색
    st.subheader("유사 불량 패턴 탐색 결과")
    if pd.api.types.is_numeric_dtype(st.session_state['data'][selected_sensor]):
        anomalies = filtered_data[filtered_data[selected_sensor] > threshold]
        if not anomalies.empty:
            st.write(f"임계치를 벗어난 구간이 {len(anomalies)}건 발견되었습니다.")
            st.dataframe(anomalies[['시간', selected_sensor]])
            
            # 이메일 발송 버튼 (실제 발송은 하지 않음)
            if st.button("이상 알림 이메일 발송"):
                st.info("📧 이메일 발송 시도 (실제 발송되지 않습니다)")
        else:
            st.write("임계치를 벗어난 구간이 없습니다.")
    else:
        st.write("선택한 센서는 범주형 데이터이므로 임계치 비교를 수행할 수 없습니다.")
    
    # 점검 순서·원인 후보·조치안 제안
    st.subheader("제안된 점검 순서·원인 후보·조치안")
    suggestions = {
        "점검 순서": [
            ("설비 전원 상태 확인", "설비가 정상적으로 전원이 공급되고 있는지 확인합니다."),
            ("센서 연결 상태 점검", "센서 케이블 및 커넥터가 제대로 연결되어 있는지 확인합니다."),
            ("최근 교체 부품 확인", "최근 교체된 부품이 제대로 장착되었는지 확인합니다."),
            ("설비 주변 환경(온도·습도) 확인", "설비가 설치된 환경의 온도·습도가 적정 범위인지 확인합니다.")
        ],
        "원인 후보": [
            ("센서 오작동", "센서 자체의 고장 또는 오작동일 가능성이 있습니다."),
            ("부품 마모", "설비 내부 부품이 마모되어 이상이 발생했을 수 있습니다."),
            ("전원 불안정", "전원 공급이 불안정하여 센서 값이 이상하게 측정될 수 있습니다."),
            ("환경 조건(온도·습도) 변화", "주변 환경 변화로 인해 센서 값이 변동했을 가능성이 있습니다.")
        ],
        "조치안": [
            ("센서 재연결 및 교체", "센서를 다시 연결하거나 필요 시 교체합니다."),
            ("마모된 부품 교체", "마모된 부품을 새 부품으로 교체합니다."),
            ("전원 안정화 장치 점검", "전원 공급 장치를 점검하고 필요한 경우 안정화 장치를 설치합니다."),
            ("환경 조건 조정", "설비 주변의 온도·습도를 적정 범위로 조정합니다.")
        ]
    }
    
    # 선택 항목 저장용 리스트
    selected_steps = []
    selected_causes = []
    selected_actions = []
    
    # 점검 순서
    st.markdown("**점검 순서**")
    for step, desc in suggestions["점검 순서"]:
        if st.checkbox(f"{step} - {desc}", key=f"check_step_{step}"):
            selected_steps.append(step)
    
    # 원인 후보
    st.markdown("**원인 후보**")
    for cause, desc in suggestions["원인 후보"]:
        if st.checkbox(f"{cause} - {desc}", key=f"check_cause_{cause}"):
            selected_causes.append(cause)
    
    # 조치안
    st.markdown("**조치안**")
    for action, desc in suggestions["조치안"]:
        if st.checkbox(f"{action} - {desc}", key=f"check_action_{action}"):
            selected_actions.append(action)
    
    # 선택 항목 저장 버튼
    if st.button("선택 항목 저장"):
        st.session_state['saved_records'].append({
            '설비ID': selected_equipment,
            '센서': selected_sensor,
            '시간': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '점검 순서': selected_steps.copy(),
            '원인 후보': selected_causes.copy(),
            '조치안': selected_actions.copy()
        })
        st.success("선택한 항목이 저장되었습니다.")
    
    # 저장된 항목 리스트업
    if st.session_state['saved_records']:
        st.subheader("최근 저장한 선택 항목")
        for idx, record in enumerate(reversed(st.session_state['saved_records'])):
            st.markdown(f"**{idx+1}. [{record['설비ID']}] {record['센서']} 데이터를 보고 선택한 항목 (저장 시각: {record['시간']})**")
            if record['점검 순서']:
                st.write("· 점검 순서: " + ", ".join(record['점검 순서']))
            if record['원인 후보']:
                st.write("· 원인 후보: " + ", ".join(record['원인 후보']))
            if record['조치안']:
                st.write("· 조치안: " + ", ".join(record['조치안']))
            st.markdown("---")