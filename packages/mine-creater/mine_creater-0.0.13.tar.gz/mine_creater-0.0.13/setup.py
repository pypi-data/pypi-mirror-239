from setuptools import setup, find_packages

VERSION = '0.0.13'
DESCRIPTION = 'Make Minecraft in Python easy'
LONG_DESCRIPTION = 'This allows you to create Minecraft in Python within minutes! And it\'s super easy!'

# Setting up
setup(
    name="mine_creater",
    version=VERSION,
    author="Bodie Sevcik",
    author_email="bodei11007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['minecraft', 'easy', 'mine', 'python', 'create', 'fast'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
