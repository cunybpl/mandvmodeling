# MandVModeling

**_NOTE:_** This project is actively developed. Expect frequent updates and changes.

## Overview

MandVModeling is an open-source Python project for modeling and visualizing changepoint models. It provides tools for analyzing trends in time series data. Uses research-driven findings to make modifications and additions to [CUNYBPL's `changepointmodel` Github repository](https://github.com/cunybpl/changepointmodel).

This package was developed in order to work with higher granularity data, as `cunybpl/changepointmodel` was designed and tested for only monthly granularity. This package was designed to support not only monthly but also daily granularity data with relevant tests applied. ASHRAE Guideline 14 points out that by using a daily granularity, data can be split up by weekdays and weekends, which results in separate models for the different daytimes. This allows for more fine-grained research and reporting.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Future Work](#future-work)
5. [License](#license)

## Installation

## Usage

## Features

- Supports various changepoint models (two-parameter, three-parameter, four-parameter, five-parameter)
- Generates changepoint coordinates
- Handles time series data analysis

## Future Work

- [] Ensure that pydantic v2 is being used and is compatible with the entire package
- [] Ensure PEP 484 compliancy. Make sure everything has a specified type.
- [] Put up some badges on this readme to show relevant information about this package.
- [] [Use Github Actions to develop a Python workflow](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README provides an overview of the MandVModeling project structure, installation instructions, usage examples, features, contribution guidelines, license information, and acknowledgments. It serves as a starting point for users and contributors alike, providing essential information about the project's purpose, functionality, and how to engage with it.