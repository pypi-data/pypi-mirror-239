from setuptools import setup, find_packages

setup(
    name='DependMLOps',
    version='0.0.1',
    author='Nullzero',
    author_email='p4rlx-news@pm.me',
    packages=find_packages(),
    license='LICENSE.txt',
    description='An MLOps and LLMOps Toolkit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)