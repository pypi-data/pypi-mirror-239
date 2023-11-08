from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
      return f.read()


setup(
    name='pealkoGPT',
    version='0.0.1',
    author='pealko',
    author_email='perelexa2.0@gmail.com',
    description='This is the simplest module for quick work with files.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/pealko/pealkoGPT',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
      'Programming Language :: Python :: 3.11',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent'
    ],
    keywords='gpt GPT chatGPT pealko',
    project_urls={
      'GitHub': 'https://github.com/pealko/pealkoGPT'
    },
    python_requires='>=3.11'
)