from setuptools import setup, find_packages

requires = [
    'PyYAML>=6.0.1',
    'pyfiglet>=1.0.2'
]

setup(
    name='aws-iam-cli',
    version='0.0.1',
    author='JaeMin',
    description='AWS IAM CloudFormation Stack Generator',
    author_email='tuiab25906370@gmail.com',
    license='MIT',
    entry_points={
        'console_scripts': [
            'iam-cli=iam_cli.main:main'
        ]
    },
    install_requires=requires,
    # packages=find_packages(),
    python_requires='>=3.10',
    url='https://github.com/rlawoals2590/aws-iam-cli',
    project_urls={
        'Source': 'https://github.com/rlawoals2590/aws-iam-cli'
    },
    include_package_data=True
)