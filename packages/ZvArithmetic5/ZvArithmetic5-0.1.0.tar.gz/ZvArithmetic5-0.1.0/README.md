<!-- <p align="center">
  <img src="https://github.com/box/sdks/blob/master/images/box-dev-logo.png" alt= “box-dev-logo” width="30%" height="50%">
</p> -->

# Zv Python SDK

[![image](http://opensource.box.com/badges/active.svg)]
[![image](https://img.shields.io/pypi/v/boxsdk.svg)]
[![image](https://img.shields.io/pypi/dm/boxsdk.svg)]
[![image](https://coveralls.io/repos/github/box/box-python-sdk/badge.svg?branch=main)]


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Installing](#installing)
- [Getting Started](#getting-started)
- [Versions](#versions)
  - [Supported Version](#supported-version)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Installing

``` console
pip install ZvolvArithmetic 
```

The current version of the SDK is 0.1.0. --- With this release support for
Python 3.8 and earlier (including 2.x). if you're
looking for the code or documentation for v0.1.0

# Getting Started

To get started with the SDK, get a Developer Token from the
Configuration page of your app.

The SDK provides an interactive `arithmetic opertion` that makes it easy
to test out the SDK in a REPL. This client will automatically prompt for
a new Developer.

``` pycon
>>> from ZvolvArithmetic import arithmetic_opertion
>>> result = arithmetic_opertion.add_numbers(10,20)
>>> print(result)
>>> 20
>>> result = arithmetic_opertion.sub_numbers(10,20)
>>> print(result)
>>> -10

```
# Versions
We use a modified version of Semantic Versioning for all changes. See version strategy for details which is effective from 2 Nov 2023. 

## Project Statistics and Contributions
[![GitHub stars](https://img.shields.io/github/stars/username/repo.svg?style=social&label=Stars)](https://github.com/username/repo)

You can view statistics for this project on [Libraries.io](https://libraries.io/) or check out our [GitHub repository](https://github.com/your-username/your-repository) for more detailed insights. We welcome contributions, bug reports, and feature requests. Feel free to open issues or submit pull requests on GitHub!


## Supported Version

Only the current MAJOR version of SDK is supported. New features, functionality, bug fixes, and security updates will only be added to the current MAJOR version.

A current release is on the leading edge of our SDK development, and is intended for customers who are in active development and want the latest and greatest features.  Instead of stating a release date for a new feature, we set a fixed minor or patch release cadence of maximum 2-3 months (while we may release more often). At the same time, there is no schedule for major or breaking release. Instead, we will communicate one quarter in advance the upcoming breaking change to allow customers to plan for the upgrade. We always recommend that all users run the latest available minor release for whatever major version is in use. We highly recommend upgrading to the latest SDK major release at the earliest convenient time and before the EOL date.


# Copyright and License

    Copyright 2023 , Inc. All rights reserved.

    Licensed under the Apache License, Version 0.1.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at ---

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.