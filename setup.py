import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iputil",
    version="0.1.0",
    author="Robin Lu",
    description="Provide some useful util functions and a tool (ip2region) for ip processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4.0',
    entry_points={
        'console_scripts': [
            'ip2region = ip2region:main'
        ]
    },
    scripts=['iputil/ip2region.py'],
)
