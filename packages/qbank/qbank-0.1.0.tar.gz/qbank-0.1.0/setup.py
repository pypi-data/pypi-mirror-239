from setuptools import find_packages, setup

# with open("README.md", "r", encoding="utf-8") as readme:
#     long_description = readme.read()


# def get_version():
#     top_dir = os.path.abspath(os.path.join(__file__, ".."))
#     with open(os.path.join(top_dir, "isqtools", "__init__.py"), "r") as f:
#         for line in f.readlines():
#             if line.startswith("__version__"):
#                 delim = '"' if '"' in line else "'"
#                 return line.split(delim)[1]
#     raise ValueError("Version not found.")


# version = get_version()

requirements = [
#     "autograd",

]

setup(
    name="qbank",
    version="0.1.0",
    description="qml",
    platforms="python 3.8+",
    python_requires=">=3.8",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    author="cgl",
    author_email="no",
    license="GNU GPLv3 ",
    packages=find_packages(where="src"),
    package_data={"": ["*.isq"]},
    install_requires=requirements,
)
