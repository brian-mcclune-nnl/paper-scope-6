"""Paper Scope 6 server setup script.

"""

import setuptools


setuptools.setup(
    name='paper-scope-6-api',
    version='0.0.1',
    author='Brian McClune',
    author_email='author@example.com',
    description='An API for finding documents by likeness',
    url='https://github.com/McClunatic/paper-scope-6-api',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'fastapi',
        'uvicorn[standard]',
        'python-jose[cryptography]',
        'httpx',
        'pydantic',
        'msal',
    ],
    package_data={'': ['matches.json']},
)
