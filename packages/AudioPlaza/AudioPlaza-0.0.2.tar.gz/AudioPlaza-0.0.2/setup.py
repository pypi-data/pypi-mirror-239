import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

from AudioPlaza import __version__

with open("requirements.txt", "r") as f:
    required_packages = f.readlines()


setuptools.setup(
    name="AudioPlaza",
    version=__version__,
    license='Raondata Private',
    author="RAONDATA speech team",
    author_email="kojunseo@raondata.ai",
    description="AudioPlaza: RAONDATA speech team's Audio Preprocessing written by python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raondata/AudioPlaza",
    packages=setuptools.find_packages(),
    install_requires=required_packages,
    package_data={'AudioPlaza': [
        'src/*',
    ]},
    python_requires='>=3.6',
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)

print("AudioPlaza setup complete! Please install 1. wget / 2. ffmpeg package in your system.")