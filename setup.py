from setuptools import setup, find_packages

setup(
    name='github-resume-builder',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask==3.0.0',
        'requests==2.31.0',
        'python-dotenv==1.0.0',
        'PyGithub==2.1.1',
        'markdown2==2.4.10',
        'pdfkit==1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'github-resume=src.app:main',
        ],
    },
    author='Daniel Corbett',
    description='GitHub Resume Builder',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
