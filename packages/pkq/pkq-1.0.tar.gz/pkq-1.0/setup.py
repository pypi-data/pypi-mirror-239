import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

    setuptools.setup(
        name="pkq",# 模块名称
    version="1.0",# 当前版本
    author="ngw",# 作者
    author_email="821512128@qq.com",# 作者邮箱
    description="一个很NB的包",    # 模块简介
                long_description=long_description,# 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
                                  url="",# 模块github地址
    packages=setuptools.find_packages(),# 自动找到项目中导入的模块
    # 模块相关的元数据（更多的描述）
    classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License"                ],
                # 依赖模块
                install_requires=[

                                 ],
    # python版本
    python_requires=">=3",
    )