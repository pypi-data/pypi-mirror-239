from setuptools import setup, find_packages
import pathlib

base = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (base / "README.md").read_text(encoding="utf-8")

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  "Topic :: Software Development :: Libraries :: Python Modules",
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
]
 
setup(
  name='py_simple_email',
  version='1.0.0',
  description='Python Simple Fast Email Sending without External Libs',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/sannjayy/py-simple-email',  
  author='Sanjay Sikdar',
  author_email='me@sanjaysikdar.dev',
  license='MIT', 
  classifiers=classifiers,
  keywords='python, smtp, email send, python send email', 
  packages=find_packages(where="src"),
  python_requires=">=3.8, <4",   
  package_dir={'':'src'},
  install_requires=[],
  project_urls={
    "Bug Reports": "https://github.com/sannjayy/py-simple-email/issues",
    "Funding": "https://www.paypal.com/paypalme/znasofficial",
    "Say Thanks!": "https://saythanks.io/to/sannjayy",
    "Source": "https://github.com/sannjayy/py-simple-email/",
  },
)