from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="thugshaker",
    version="1.0.2",
    author="Niggeshwar Faggotlal",
    description="you've got an ass on you alright",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/thugshaker/",
    packages=find_packages(),
    install_requires=["pygame", "opencv-python", "keyboard"],
    entry_points={
        "console_scripts": [
            "thugshaker=thugshaker.player:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'thugshaker': ['assets/*.mp3', 'assets/*.mp4']},
    include_package_data=True,
    license="MIT"
)