import setuptools

name = "cloud-ranges"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

version_file = "cloud_ranges/version.py"
with open(version_file) as fi:
    vs = {}
    exec(fi.read(), vs)
    __version__ = vs["__version__"]

setuptools.setup(
    name=name,
    version=__version__,
    author="zer1t0ps@protonmail.com",
    description="Discover if IP belongs cloud providers ranges",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "{name} = cloud_ranges.__main__:main".format(name=name),
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
