import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoBET",
    version="0.1.4",
    author="Jiameng Liu",
    author_email="JiamengLiu.PRC@gmail.com",
    description="Automatic Brain Extraction Tools",
    long_description=long_description,
    long_description_content_type="README.md",
    url="https://github.com/SaberPRC/Auto-BET",
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
        'pandas',
        'torch',
        'SimpleITK',
        'MIDP',
        # 'Django >= 1.11, != 1.11.1, <= 2',
    ],
    include_package_data=True,
)