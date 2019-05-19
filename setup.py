import setuptools

setuptools.setup(
    name="dclua",
    version="1.1",
    description="Library for word declensions",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/syntpump/declensor",
    license="MIT License",
    author="Syntpump",
    author_email="lynnporu@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License"
    ],
    keywords="nlp",
    packages=setuptools.find_packages(),
    python_requires=">3",
    project_urls={
        "Syntpump on GitHub": "https://github.com/syntpump"
    }
)
