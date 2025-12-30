from setuptools import setup

setup(name="liarsDice",
    version="0.6.1",
    packages=["LiarsDice"],
    install_requires=[],
    author="Yusuf739",
    author_email="yusuf265820@gmail.com",
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description="Simple Liar's Dice game. Inspired by RDR1 minigame",
    long_description=open('readme.txt').read(),
    long_description_content_type="text/plain",
    url="https://github.com/YusufA442/liarsDice",
    entry_points={
        "console_scripts": [
            "liarsDice=LiarsDice.liarsDice:run",
        ]
    })