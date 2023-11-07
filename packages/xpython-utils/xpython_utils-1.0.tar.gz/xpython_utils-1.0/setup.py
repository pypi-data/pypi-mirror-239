import setuptools
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xpython_utils",  # 模块名称
    version="1.0",  # 当前版本
    author="zabida",  # 作者
    author_email="stcdaily@163.com",  # 作者邮箱
    description="常规用用的包",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'requests',
        'urllib3',
        'requests-toolbelt'
    ],
    python_requires='>=3.7',
)