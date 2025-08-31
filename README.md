# pprof-decode

A Python tool to decode Protocol Buffers (protobuf) format pprof binary data into human-readable JSON format.

## Description

This project provides a decoder for pprof binary files, which are commonly used for profiling data in Go applications. It converts the binary protobuf format into a structured JSON format for easier analysis and processing.

## Features

- Decode pprof binary files (`.pb` format)
- Convert profiling data to JSON format
- Extract function calls, memory mappings, and sampling information
- Support for various pprof profile types

## Installation

```bash
# Clone the repository
git clone https://github.com/pakutoma/pprof-decode.git
cd pprof-decode

# Install dependencies using uv
uv sync

# Or using pip
pip install protobuf
```

## Usage

```python
python decode.py
```

The script reads `pprof.bin` from the current directory and outputs the decoded JSON data.

## Dependencies

- Python 3.12+
- protobuf library

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project uses Protocol Buffer definitions from [Google's pprof](https://github.com/google/pprof) project:
- `profile.proto` - The main pprof profile format definition
- The original pprof project is also licensed under Apache License 2.0

## Credits

- Google pprof team for the original protobuf definitions
- Protocol Buffers format specification