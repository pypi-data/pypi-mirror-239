import csv
import yaml
import glob
from inquirer import List, prompt
from datetime import datetime

from iam_cli.tools import print_figlet

class Command:
    csv_files_list = []
    choose_csv_file = None
    student_list = []
    now = datetime.now()

    def __init__(self):
        print_figlet()
        self.get_csv_files()
        self.choose_csv_files()
        self.process_csv()
        self.create_cloudformation_yaml()

    def get_csv_files(self):
        csv_files = glob.glob('*.csv')

        # 파일 이름 출력
        for file_name in csv_files:
            self.csv_files_list.append(file_name)

    def choose_csv_files(self):
        questions = [
            List(
                name='csv_files',
                message='Choose csv file',
                choices=self.csv_files_list
            )
        ]

        answer = prompt(questions=questions, raise_keyboard_interrupt=True)
        self.choose_csv_file = answer.get('csv_files')

    def process_csv(self):
        # CSV 파일을 읽어 들임
        with open(self.choose_csv_file, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                ban = row['학번'][2]
                role = 'student'
                num = str(row['학번'])
                num_name = str(row['학번']) + str(row['이름'])
                created_date = self.now.strftime("%Y-%m-%d")

                student_info = {
                    'ban': ban,
                    'role': role,
                    'num': num,
                    'num_name': num_name,
                    'created_date': created_date
                }

                self.student_list.append(student_info)

    def create_cloudformation_yaml(self, output_file='iam_users.yaml'):
        resources = {}
        groups = set()
        count = 0

        for user in self.student_list:
            ban = user['ban']
            role = user['role']
            num = user['num']
            num_name = user['num_name']
            created_date = user['created_date']
            groups.add(role)  # 그룹 이름을 집합에 추가하여 중복을 제거

            initial_password = 'smc@' + str(num) + '!'
            count += 1

            # 여기서 추가적인 속성을 사용자 정의 필드로 추가할 수 있습니다.
            resources['User' + str(count)] = {
                'Type': 'AWS::IAM::User',
                'Properties': {
                    'UserName': num,
                    'Groups': [role],
                    'LoginProfile': {
                        'Password': initial_password, # 초기 비밀번호 설정
                        'PasswordResetRequired': True      # 첫 로그인 시 비밀번호 변경 요구
                    },
                    'Tags': [
                        {
                            'Key': 'Ban',
                            'Value': ban
                        },
                        {
                            'Key': 'Role',
                            'Value': role
                        },
                        {
                            'Key': 'Name',
                            'Value': num_name
                        },
                        {
                            'Key': 'Created Date',
                            'Value': created_date
                        }
                    ]
                }
            }
        
        cloudformation_template = {
            'AWSTemplateFormatVersion': '2010-09-09',
            'Resources': resources
        }

        with open(output_file, 'w') as file:
            yaml.dump(cloudformation_template, file, allow_unicode=True, default_flow_style=False)

        print("aws cloudformation deploy --stack-name aws-student-iam-cf --template-file ./iam_users.yaml --capabilities CAPABILITY_NAMED_IAM")
        