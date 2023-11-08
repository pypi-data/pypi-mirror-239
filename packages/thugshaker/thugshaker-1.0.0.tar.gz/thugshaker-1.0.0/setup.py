from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="thugshaker",
    version="1.0.0",
    author="Niggeshwar Faggotlal",
    author_email="thugcentral@gmail.com",
    description="You can't stop the Thug Shaker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://knowyourmeme.com/editorials/guides/what-is-a-thug-shaker-the-meme-explained",
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