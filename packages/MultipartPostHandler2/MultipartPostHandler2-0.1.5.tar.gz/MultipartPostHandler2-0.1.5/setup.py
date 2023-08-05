from setuptools import setup, find_packages
setup(
    name = "MultipartPostHandler2",
    py_modules = ['MultipartPostHandler'],
    version = "0.1.5",
    description = "A handler for urllib2 to enable multipart form uploading",
    license = "LGPLv2.1+",
    author = "Will Holcomb",
    author_email = "wholcomb@gmail.com",
    maintainer = "Sergio Basto",
    maintainer_email = "sergio@serjux.com", 
    url = "https://github.com/sergiomb2/MultipartPostHandler2/",
    keywords = ["http", "multipart", "post", "urllib2"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description = """\
Usage:
  Enables the use of multipart/form-data for posting forms
  add a fix for utf-8 systems.

Inspirations:
  Upload files in python:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
  urllib2_file:
    Fabien Seisen: <fabien@seisen.org>

Example:
  import MultipartPostHandler, urllib2

  opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
  params = { "username" : "bob", "password" : "riviera",
             "file" : open("filename", "rb") }
  opener.open("http://wwww.bobsite.com/upload/", params)

Further Example:
  The main function of this file is a sample which downloads a page and
  then uploads it to the W3C validator.
""",
    )

