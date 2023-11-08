import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyssword",
    version="0.2.3",
    author="Vitor Assis",
    author_email="vitor.assis.dev@gmail.com",
    description="A Python password generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/vassis/pyssword",
    download_url="https://pypi.org/project/pyssword",
    packages=setuptools.find_packages(),
    install_requires=[
        'colorama',
        'click',
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Environment :: Console",
        "Natural Language :: Portuguese (Brazilian)",
        "Natural Language :: English",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points='''
        [console_scripts]
        pyssword=pyssword.pyssword:run
    ''',
)
