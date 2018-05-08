from setuptools import setup
import pathlib

readme = pathlib.Path("README.md").read_text("utf-8")

setup(
    name="myloginpath",
    license="MIT",
    version="0.0.1",
    description="MySQL login path file reader",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/PyMySQL/myloginpath/",
    keywords="MySQL",
    install_requires=["cryptography"],
    python_requires='>=3.4',
    py_modules=["myloginpath"],
)
