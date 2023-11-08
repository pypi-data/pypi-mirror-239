from setuptools import setup, find_packages

setup(
    name='aws_library',
    version='0.1',
    packages=find_packages(),
    description='A simple AWS utility library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='gokul',
    author_email='gokulmarwal@outlook.com',
    url='',
    license='MIT',
    install_requires=[
        'boto3',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires='>=3.7',
)
