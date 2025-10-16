from setuptools import setup, find_packages



setup(
    name="picoscript",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pico=picoscript.__main__:main",
        ],
    },
)

