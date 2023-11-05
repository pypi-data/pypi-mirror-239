from setuptools import setup

setup(
    name='rfch',
    version='2.0.1',
    description='serial库rfid模块整合库',
    author='Liu YUchen',
    author_email='liuyuchen032901@outlook.com',
    url='',
    py_modules=['test', 'setup', 'main'],
    REQUIRES_PYTHON = '>=3.9.0',
    REQUIRED=[
            'serial', 'time', 'sys','test'
    ]
)
# What packages are required for this module to be executed?
