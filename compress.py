import zstandard as zstd
import os
import multiprocessing
from tqdm import tqdm
import sys

def compress_file_chunk(args):
    file_path, arcname, chunk_size, chunk_number, compression_level = args
    cctx = zstd.ZstdCompressor(level=compression_level)
    
    try:
        with open(file_path, 'rb') as f:
            f.seek(chunk_size * chunk_number)
            data = f.read(chunk_size)
        
        compressed_data = cctx.compress(data)
        return arcname, chunk_number, compressed_data, len(data)
    except Exception as e:
        return arcname, chunk_number, str(e), 0

def compress_folder(input_folder, output_file, compression_level=3, chunk_size=1024*1024):  # 1MB chunks
    try:
        input_folder = os.path.normpath(input_folder)
        
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"The input folder '{input_folder}' does not exist.")
        
        files_to_compress = []
        for root, _, files in os.walk(input_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, input_folder)
                file_size = os.path.getsize(file_path)
                chunks = (file_size + chunk_size - 1) // chunk_size
                for i in range(chunks):
                    files_to_compress.append((file_path, arcname, chunk_size, i, compression_level))
        
        if not files_to_compress:
            raise ValueError(f"The input folder '{input_folder}' is empty.")
        
        total_original_size = 0
        total_compressed_size = 0
        
        with open(output_file, 'wb') as out_f:
            with multiprocessing.Pool() as pool:
                with tqdm(total=len(files_to_compress), unit='chunk') as pbar:
                    for arcname, chunk_number, result, original_size in pool.imap_unordered(compress_file_chunk, files_to_compress):
                        if isinstance(result, str):  # This is an error message
                            print(f"Error processing {arcname} (chunk {chunk_number}): {result}")
                            continue
                        
                        compressed_data = result
                        total_original_size += original_size
                        total_compressed_size += len(compressed_data)
                        
                        if chunk_number == 0:
                            out_f.write(len(arcname).to_bytes(2, byteorder='big'))
                            out_f.write(arcname.encode('utf-8'))
                        
                        out_f.write(len(compressed_data).to_bytes(4, byteorder='big'))
                        out_f.write(compressed_data)
                        
                        pbar.update(1)
                        pbar.set_description(f"Processed {arcname} (chunk {chunk_number})")
        
        print(f"\nCompressed {input_folder} to {output_file}")
        print(f"Original size: {total_original_size} bytes")
        print(f"Compressed size: {total_compressed_size} bytes")
        print(f"Compression ratio: {total_original_size / total_compressed_size:.2f}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Python version:", sys.version)
        print("zstandard version:", zstd.__version__)

if __name__ == '__main__':
    try:
        input_folder = input("Enter the path of the folder to compress: ").strip().strip("\"'")
        output_file = input("Enter the name of the output file (e.g., output.zst): ").strip()
        
        if not output_file.endswith('.zst'):
            output_file += '.zst'
        
        compress_folder(input_folder, output_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Python version:", sys.version)
        print("zstandard version:", zstd.__version__)