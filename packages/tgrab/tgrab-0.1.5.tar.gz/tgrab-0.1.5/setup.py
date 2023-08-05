import platform
try: 
	from setuptools import setup
except ImportError: 
	from distutils.core import setup
setup(
    name="tgrab",
    version="0.1.5",
    description="Download Images form Tumblr Blogs",
    keywords=["Tumblr", "Image", "Download", "blog"],
    author="KaveenR",
    author_email="u.k.k.rodrigo@gmail.com",
    url="http://geeknirvana.org",
    scripts=['tgrab'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Utilities"]
)
