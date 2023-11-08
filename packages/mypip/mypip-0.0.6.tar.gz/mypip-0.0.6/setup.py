from setuptools import setup

setup(
    name="mypip",
    version="0.0.6",
    description="My pip installer",
    author="Tomy",
    author_email="tom@gmail.com",
    packages=[],  # Replace with the actual list of packages
    install_requires=[
        "codefast"
    ],
    extras_require={
        "dev": [
            "pytest>=5.2",
        ]
    },
    entry_points={
        "console_scripts": [
            "mpip=mypip:pip_install",
        ]
    }
)
