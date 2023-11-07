from setuptools import setup, find_packages

with open('avala/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='avala-sdk',
    version='0.0.17',
    description='Avala Client SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Avala Developer',
    author_email='developer@avala.ai',
    url='https://github.com/avala-ai/avala-python',
    python_requires='>=3, <=3.9',
    packages=find_packages(),
    py_modules=['entry'],
    package_data={'': ['config.json', 'LICENSE', 'README.md', 'CONTRIB.md']},
    entry_points={
        'console_scripts': [
            'avala = entry:main',
        ]
    },
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)

