from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'A framework that makes discord bot programming easy'

with open("README.md", "r") as f:
    long_description = f.read()

# Setting up
setup(
    name="phonkd_bot",
    version=VERSION,
    author="Phonki",
    author_email="<phonkibusiness@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["discord", "asyncio"],
    keywords=['python', 'discord'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ]
)

"""
----- build commands -----

(delete all build files first)

python3 setup.py sdist bdist_wheel
twine upload dist/* --verbose
"""