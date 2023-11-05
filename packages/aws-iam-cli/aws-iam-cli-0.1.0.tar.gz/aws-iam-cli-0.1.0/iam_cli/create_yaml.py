import yaml


class CreateYAML:
    resources = {}
    groups = set()
    count = 0
    student_list = []

    def __init__(self, student_list):
        self.student_list = student_list
        self.create_iam_user(student_list=self.student_list)
        self.create_yaml()

    def create_iam_user(self, student_list):

        for user in student_list:
            ban = user['ban']
            role = user['role']
            num = user['num']
            num_name = user['num_name']
            created_date = user['created_date']
            self.groups.add(role)  # 그룹 이름을 집합에 추가하여 중복을 제거

            initial_password = 'smc@' + str(num) + '!'
            self.count += 1

            # 여기서 추가적인 속성을 사용자 정의 필드로 추가할 수 있습니다.
            self.resources['User' + str(self.count)] = {
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

    def create_yaml(self):
        template = {
            'AWSTemplateFormatVersion': '2010-09-09',
            'Description': 'VPC Stack Generator CLI',
            'Resources': self.resources
        }

        try:
            with open('iam_users.yaml', 'w') as f:
                yaml.dump(template, f)

        except Exception as e:
            print(e)
