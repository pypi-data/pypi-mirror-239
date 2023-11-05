from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='cust_logger',
    version='v0.0.4',
    author='dimka4621',
    author_email='mismartconfig@gmail.com',
    description='This is my custom logger',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/DIMKA4621',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='cust logger',
    project_urls={
        'GitHub': 'https://github.com/DIMKA4621'
    },
    python_requires='>=3.8'
)
