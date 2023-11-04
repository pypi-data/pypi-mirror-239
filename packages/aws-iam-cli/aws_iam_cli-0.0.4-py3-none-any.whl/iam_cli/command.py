import csv
import yaml
from iam_cli.tools import print_figlet

print_figlet()

def process_csv(csvfile):
    # CSV 파일을 읽어 들임
    reader = csv.DictReader(csvfile)
    student_list = []

    for row in reader:
        ban = row['학번'][2]
        role = 'student'
        num = str(row['학번'])
        num_name = str(row['학번']) + str(row['이름'])

        student_info = {
            'ban': ban,
            'role': role,
            'num': num,
            'num_name': num_name
        }

        student_list.append(student_info)
    
    return student_list


def create_cloudformation_yaml(users, output_file='iam_users.yaml'):
    resources = {}
    groups = set()
    count = 0

    for user in users:
        ban = user['ban']
        role = user['role']
        num = user['num']
        num_name = user['num_name']
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
        