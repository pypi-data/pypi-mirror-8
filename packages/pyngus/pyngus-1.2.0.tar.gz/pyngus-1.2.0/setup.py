#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from setuptools import setup

_VERSION = "1.2.0"   # NOTE: update __init__.py too!

setup(name="pyngus",
      version=_VERSION,
      author="kgiusti",
      author_email="kgiusti@apache.org",
      packages=["pyngus"],
      package_dir={"pyngus": "python/pyngus"},
      description="Callback API implemented over Proton",
      url="https://github.com/kgiusti/pyngus",
      license="Apache Software License",
      # install_requires=['python-qpid-proton>=0.7,<0.8'],
      classifiers=["License :: OSI Approved :: Apache Software License",
                   "Intended Audience :: Developers",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python"])
