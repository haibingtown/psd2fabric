# PSD2Fabric

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/haibingtown/PSD2Fabric.svg)](https://github.com/haibingtown/PSD2Fabric/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/haibingtown/PSD2Fabric.svg)](https://github.com/haibingtown/PSD2Fabric/issues)
[![GitHub forks](https://img.shields.io/github/forks/haibingtown/PSD2Fabric.svg)](https://github.com/haibingtown/PSD2Fabric/network)
![GitHub contributors](https://img.shields.io/github/contributors/haibingtown/PSD2Fabric.svg)

# PSD2Fabric

PSD2Fabric is a Python tool designed to parse PSD files into the fabric.js format.

## Features

- **Parse PSD files:** Convert PSD files into fabric.js JSON format.
- **Support for the following features:**
  - PSD structure
  - Group
    - Children relative position
  - Font
    - Size
    - Text content
    - Color
    - Bold
    - Alignment
  - Effect
    - Stroke
  - Others to Image

## Usage

To use PSD2Fabric, follow these steps:

1. **Installation:**
   ```bash
   pip install psd2fabric

2. **Usage:**
   ```bash
    psd2fabric input.psd output.json

Replace input.psd with the path to your PSD file and output.json with the desired output JSON file.

## Preview Online

- Parse to JSON file and preview it on this online site: https://nihaojob.github.io/vue-fabric-editor/
- Alternatively, deploy locally using this forked repository: https://github.com/haibingtown/vue-fabric-editor

## Demo

[test.json](asserts%2Fjson%2Ftest.json)
![snapshot.jpeg](asserts%2Fimages%2Fsnapshot.jpeg)

## Contributing

We welcome and appreciate your contributions! Please refer to the contribution guidelines for more details.
