# from distribute_setup import use_setuptools
from setuptools import setup, find_packages

#use_setuptools ()

setup (
        name="autobuild",
        version="0.1",
        packages=find_packages (),
        scripts=["autobuild.py", "config.py"],

        # entry
        entry_points = {
                "console_scripts": [
                        "autobuild = autobuild:main"
                    ]
            },

        # meta
        author="J.H.Mazis",
        author_email="recursiveowl@gmail.com",
        description="A tool for building c/c++ sources with minimal config",
        license="zlib",
        keywords="build c++ c make",
        url="",
    )
