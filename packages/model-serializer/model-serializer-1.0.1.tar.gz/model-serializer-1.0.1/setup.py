from setuptools import setup, find_packages

setup(
    name='model-serializer',
    version='1.0.1',
    description='A simple Python package for serializing and deserializing Python objects to and from JSON.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Olger Chotza',
    author_email='olgerdev@icloud.com',
    url='https://github.com/ochotzas/',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.9',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
