from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ymdown',
    version='0.1.2',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'ymdown = ymdown.ymdown:main',
        ],
    },
    # Additional metadata about your package.
    author='Chan Yat Fu',
    author_email='chanyatfu0616@google.com',
    description='A utility build on top of ytmusicapi and yt-dlp for esay search-and-download in YouTube Music.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/chanyatfu/ymdown',
)
