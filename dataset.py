import pandas as pd
import numpy as np

# 설정
num_records = 10000
num_equipment = 5
equipment_ids = [f'EQP{i+1:03d}' for i in range(num_equipment)]
start_time = pd.Timestamp('2024-11-01 00:00:00')

# 데이터 생성
np.random.seed(42)  # 재현 가능한 난수 생성
data = []

for i in range(num_records):
    equipment_id = np.random.choice(equipment_ids)
    timestamp = start_time + pd.Timedelta(seconds=i)
    sensor_value1 = np.random.uniform(20, 100)  # 예: 온도 (20 ~ 100 사이)
    sensor_value2 = np.random.uniform(0, 1)     # 예: 진동 (0 ~ 1 사이)
    status_code = 'NORMAL' if sensor_value1 < 80 else 'ALERT'
    is_anomaly = 1 if sensor_value1 >= 80 else 0  # 이상 여부를 0 또는 1로 표시
    
    data.append({
        '설비ID': equipment_id,
        '시간': timestamp,
        '센서값1': sensor_value1,
        '센서값2': sensor_value2,
        '상태코드': status_code,
        '이상 여부': is_anomaly,
        '주기': 1,
        '작업ID': f'JOB{i//2000 + 1:05d}',  # 2000개 단위로 작업ID 변경
        '운영자': f'operator_{i % 3 + 1:02d}'  # 3명의 운영자 가정
    })

# 데이터프레임 생성
df = pd.DataFrame(data)

# CSV 파일로 저장 (파일 경로는 필요에 따라 조정)
df.to_csv('mock_equipment_data.csv', index=False, encoding='utf-8-sig')