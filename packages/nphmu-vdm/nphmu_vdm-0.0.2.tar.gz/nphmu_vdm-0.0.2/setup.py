import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


requirements = [
    'matplotlib',
    'scipy',
    'ipykernel',
]

test_requirements = [
    'pytest',
    # 'pytest-pep8',
    # 'pytest-cov',
]


setuptools.setup(
    name="nphmu_vdm", # Replace with your own username
    version="0.0.2",
    author="N. Papadakis",
    author_email="npapnet@gmail.com",
    description="A package for Vibrations and Machine Dynamics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    tests_require=test_requirements,
    python_requires='>=3.6',
)