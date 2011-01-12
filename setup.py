from setuptools import setup, find_packages

setup(
    name="fdfgen",
    version="0.9.2",
    author="Anders Pearson",
    author_email="anders@columbia.edu",
    url="http://github.com/ccnmtl/fdfgen/",
    description="library for creating FDF files",
    long_description="Python port of the PHP forge_fdf library for creating FDF files",
    scripts = [],
    license = "BSD",
    platforms = ["any"],
    zip_safe=False,
    packages=find_packages()
    )
    
