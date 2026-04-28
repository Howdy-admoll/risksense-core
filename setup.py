from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="risksense-core",
    version="1.0.0",
    author="Ademola Adefemi",
    author_email="hello@admoll.dev",
    description="Production-grade Mamdani fuzzy inference system for credit risk scoring in fintech lending",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Howdy-admoll/risksense-core",
    project_urls={
        "Bug Tracker": "https://github.com/Howdy-admoll/risksense-core/issues",
        "Documentation": "https://github.com/Howdy-admoll/risksense-core#readme",
        "Source Code": "https://github.com/Howdy-admoll/risksense-core",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy==1.26.4",
        "scikit-fuzzy==0.4.2",
        "matplotlib==3.8.3",
        "flask==3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.4",
            "pytest-cov==4.1.0",
            "black==24.1.1",
            "flake8==7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "risksense=risksense.cli:main",
        ],
    },
    keywords="fuzzy-logic credit-risk fintech scoring african-fintech",
    zip_safe=False,
)