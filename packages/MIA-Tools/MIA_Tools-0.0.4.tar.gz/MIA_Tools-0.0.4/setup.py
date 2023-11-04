import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MIA_Tools",
    version="0.0.4",
    author="Jiameng Liu",
    author_email="JiamengLiu.PRC@gmail.com",
    description="Medical Image Analysis Tools",
    long_description=long_description,
    long_description_content_type="README.md",
    url="https://github.com/SaberPRC/MIA-Tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # exapmle
        'antspyx',
        'numpy',
        'SimpleITK',
        # 'Django >= 1.11, != 1.11.1, <= 2',
    ],
)