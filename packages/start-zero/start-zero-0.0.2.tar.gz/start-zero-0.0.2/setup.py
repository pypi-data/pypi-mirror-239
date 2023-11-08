from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(name='start-zero',
      version='0.0.2',
      description='DeepLearningFramework',
      long_description=long_description,
      author='he bin',
      author_email='hebingaa@126.com',
      url='https://gitee.com/tank2140896/start-zero',
      install_requires=[],
      license='Apache License 2.0',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3'
      ],
      )

