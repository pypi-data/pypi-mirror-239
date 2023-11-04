from setuptools import find_packages, setup

PACKAGE_NAME = "lcpf"

setup(
    name="lcpf",
    version="0.0.1",
    description="This package contains prompt flow tools for using LangChain Agents.",
    packages=find_packages(),
    install_requires=[
        'langchain'
    ],
    entry_points={
        "package_tools": ["query = lcpf.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)