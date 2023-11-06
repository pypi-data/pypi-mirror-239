from setuptools import setup, find_packages
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nonebot_plugin_BiliMedalWall",
    version="0.1.1",
    author="Shadow403",
    author_email="admin@shadow403.cn",
    description="Show BiliUsers MedalWall(info)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shadow403/nonebot_plugin_BiliMedalWall",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "nonebot2 >= 2.1.2",
        "nonebot-adapter-onebot >= 2.3.1",
        "requests >= 2.31.0",
        "jsonpath >= 0.82.2",
        "matplotlib >= 3.8.1",
        "pathlib >= 1.0.1"
        ],
    python_requires='>=3.10',
)