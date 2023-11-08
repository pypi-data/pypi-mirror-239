from setuptools import setup, find_packages

VERSION = '1.3'
DESCRIPTION = 'Yantu tools for python'

setup(
    name="fdfd-test",
    version=VERSION,
    author="yantu-tech",
    author_email="wu466687121@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),
    include_package_data=True,
    package_data={'fourth_dimension': ['config/question_regex.txt', 'cache/faiss_cache/temp.index']},
    install_requires=[],
    keywords=["python", "yantu", "中文"],
    license="MIT",
    url="https://gitee.com/hustai/Fourth-Dimension",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)
