from setuptools import setup, find_packages
# import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding = "utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'The framework for algorithms engineering with Python.'
LONG_DESCRIPTION = 'C4Dynamics (read Tsipor (bird) Dynamics) is the open-source framework of algorithms development for objects in space and time.'

# Setting up
setup(
    name                          = "C4dynamics",
    version                       =  VERSION,
    author                        = "C4dynamics",
    author_email                  = "zivmeri@gmail.com",
    description                   =  DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description              = LONG_DESCRIPTION,   # long_description  
    packages                      = find_packages(),
    install_requires              = ['numpy', 'scipy', 'matplotlib', 'opencv-python'],
    keywords                      = ['python', 'dynamics', 'physics', 'algorithms', 'computer vision', 'navigation'],
    classifiers                   = [
                                      "Development Status :: 5 - Production/Stable",
                                      "Intended Audience :: Developers",
                                      "Programming Language :: Python :: 3",
                                      "Operating System :: Unix",
                                      "Operating System :: MacOS :: MacOS X",
                                      "Operating System :: Microsoft :: Windows",
                                        ])