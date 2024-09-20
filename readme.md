# Memory-Efficient Folder Compression Script

This Python script provides a memory-efficient way to compress entire folders using the zstandard (zstd) compression algorithm. It's designed to handle large folders by processing files in chunks, making it suitable for systems with limited RAM.

## Features

- Compresses entire folders, including all subfolders and files
- Uses zstandard compression for efficient compression ratios
- Memory-efficient: processes files in chunks to avoid loading entire files into memory
- Multiprocessing support for faster compression on multi-core systems
- Progress bar to show compression status
- Detailed error reporting

## Requirements

- Python 3.6 or higher
- zstandard library
- tqdm library (for progress bar)

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Install the required libraries using pip:

   ```
   pip install zstandard tqdm
   ```


## Customization

You can modify the following parameters in the script to adjust its behavior:

- `compression_level`: Change the compression level (1-22, default is 3) in the `compress_folder` function call.
- `chunk_size`: Adjust the chunk size (default is 1MB) in the `compress_folder` function call to balance between memory usage and compression speed.

## Output Format

The script produces a single `.zst` file containing all compressed files. The format is as follows:

- For each file:
  - 2 bytes: Length of the file path
  - Variable bytes: File path (UTF-8 encoded)
  - For each chunk of the file:
    - 4 bytes: Length of the compressed chunk
    - Variable bytes: Compressed chunk data

## Decompression

To decompress the files, you'll need to write a custom script that understands this format. The script should:

1. Read the file path length
2. Read and decode the file path
3. Read chunk lengths and decompress chunks until the next file is encountered
4. Repeat for all files in the archive

## Troubleshooting

If you encounter memory errors:

1. Reduce the `chunk_size` in the `compress_folder` function call.
2. Limit the number of parallel processes by modifying the `multiprocessing.Pool()` call.

For any other issues, the script will print detailed error messages, including Python and zstandard library versions.

## License

This script is provided "as is", without warranty of any kind. You are free to use, modify, and distribute it as needed.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or encounter any problems.