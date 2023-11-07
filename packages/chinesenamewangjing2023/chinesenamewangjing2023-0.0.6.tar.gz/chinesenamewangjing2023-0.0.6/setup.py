from setuptools import setup, find_packages

setup(
    name='chinesenamewangjing2023',
    version='0.0.6',
    # keywords = ('chinesename',),
    description='get a chinesename by random',
    license='MIT License',
    install_requires=[],
    packages=['chinesenamewangjing2023'],  # 要打包的项目文件夹
    include_package_data=True,  # 自动打包文件夹内所有数据
    author='wj',
    author_email='120551025@qq.com',
    url='https://github.com/mouday/chinesename',
    # packages = find_packages(include=("*"),),
)

