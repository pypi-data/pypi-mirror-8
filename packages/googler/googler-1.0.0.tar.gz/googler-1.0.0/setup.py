##
# Googler - Google API Library for Python
#
# Copyright (C) 2014 Christian Jurk <commx@commx.ws>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

from setuptools import setup, find_packages

setup(
    name='googler',
    version='1.0.0',
    author='Christian Jurk',
    author_email='commx@commx.ws',
    description=('Google API Library for Python',),
    license='Apache',
    keywords='google api recaptcha geocode geocoding',
    url='https://github.com/commx/googler',
    packages=find_packages(),
    install_requires=[
        'pycrypto',
        'requests'
    ],
    long_description='README.md',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries'
    ],
)