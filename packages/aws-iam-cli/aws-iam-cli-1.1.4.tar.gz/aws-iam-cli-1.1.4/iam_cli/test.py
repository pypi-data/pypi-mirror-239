import glob

# 특정 경로에 있는 모든 csv 파일의 리스트를 가져옵니다.
# 여기서 '*'는 '모든 것'을 의미합니다.
csv_files = glob.glob('*.csv')

# 파일 이름 출력
for file_name in csv_files:
    print(file_name)
