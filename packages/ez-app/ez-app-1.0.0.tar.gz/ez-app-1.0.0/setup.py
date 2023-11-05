from setuptools import setup

data = {
    "name": "ez-app",
    "version": "1.0.0",
    "author": "TunaFish2K",
    "author_email": "tunafish2k@163.com",
    "description": "app toolkits",
    "long_description": "serveral toolkits with documents that are useful for building an app.",
    "keywords": "app",
    "packages": ["ez-app"],
    "python_requires": ">=2.7, <=3"
}

setup(
    **data
)