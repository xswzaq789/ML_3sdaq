from setuptools import setup, find_packages

setup(
    name='samsdaq', # 패키지 명

    version='1.0.1.11',

    description='Test Package',

    author='yourms',

    author_email='yourms73@gmail.com',

    url='https://github.com/yourms',

    license='MIT', # MIT에서 정한 표준 라이센스 따른다

    #py_modules=['samsdaq/model_test'], # 패키지에 포함되는 모듈

    python_requires='>=3',

    install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

    packages=find_packages(),#['samsdaq']# 패키지가 들어있는 폴더들

    include_package_data=True,

    package_data={'': ['X_train.csv', 'ml_model.h5','konlpy.sh']},

)