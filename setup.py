from setuptools import setup

setup(
    name='li-analyzer',
    version='0.1.0',
    py_modules=['li_analyzer'],
    install_requires=[
        'pandas',
        'click',
    ],
    entry_points='''
        [console_scripts]
        li-analyzer=li_analyzer:analyze
    ''',
    author='Your Name',
    description='CLI tool to analyze LinkedIn profile data from CSV',
    license='MIT',
)
