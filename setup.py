from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="myloginpath",
    license="MIT",
    version="0.0.3",
    description="MySQL login path file reader",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/PyMySQL/myloginpath/",
    keywords="MySQL",
    install_requires=["cryptography"],
    python_requires=">=3.4",
    py_modules=["myloginpath"],
)
