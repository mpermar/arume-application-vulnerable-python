#!/usr/bin/env python3
"""
Secure Tar Archive Processor
"""

import tarfile
import sys
import os
import argparse
from pathlib import Path


class SecureTarProcessor:
    def __init__(self, max_extract_size=100_000_000, max_files=1000):
        """Initialize with security limits"""
        self.max_extract_size = max_extract_size  # 100MB default
        self.max_files = max_files
        
    def list_archive(self, tar_path):
        """Safely list contents of tar archive"""
        print(f"Listing contents of: {tar_path}")
        print("-" * 50)
        
        try:
            with tarfile.open(tar_path, 'r') as tar:
                file_count = 0
                total_size = 0
                
                for member in tar:
                    file_count += 1
                    
                    # Enforce file count limit
                    if file_count > self.max_files:
                        raise tarfile.ReadError(f"Too many files (>{self.max_files})")
                    
                    # Track total size
                    if member.isfile():
                        total_size += member.size
                        if total_size > self.max_extract_size:
                            raise tarfile.ReadError(f"Archive too large (>{self.max_extract_size} bytes)")
                    
                    # Display member info
                    type_char = self._get_type_char(member)
                    print(f"{type_char} {member.name:40} {member.size:>10} bytes")
                
                print("-" * 50)
                print(f"Total files: {file_count}")
                print(f"Total size: {total_size} bytes")
                
        except tarfile.ReadError as e:
            print(f"Error reading tar file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
            
        return True
    
    def extract_archive(self, tar_path, extract_to=None):
        """Safely extract tar archive"""
        if extract_to is None:
            extract_to = Path(tar_path).stem + "_extracted"
        
        extract_path = Path(extract_to)
        extract_path.mkdir(exist_ok=True)
        
        print(f"Extracting {tar_path} to {extract_path}")
        print("-" * 50)
        
        try:
            with tarfile.open(tar_path, 'r') as tar:
                file_count = 0
                total_size = 0
                
                for member in tar:
                    file_count += 1
                    
                    # Enforce limits
                    if file_count > self.max_files:
                        raise tarfile.ReadError(f"Too many files (>{self.max_files})")
                    
                    # Track size
                    if member.isfile():
                        total_size += member.size
                        if total_size > self.max_extract_size:
                            raise tarfile.ReadError(f"Archive too large (>{self.max_extract_size} bytes)")
                    
                    # Safe extraction
                    safe_path = extract_path / member.name
                    safe_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if member.isfile():
                        with tar.extractfile(member) as src:
                            with open(safe_path, 'wb') as dst:
                                dst.write(src.read())
                        print(f"Extracted: {member.name}")
                    elif member.isdir():
                        safe_path.mkdir(exist_ok=True)
                        print(f"Created directory: {member.name}")
                
                print("-" * 50)
                print(f"Extraction complete: {file_count} files, {total_size} bytes")
                
        except tarfile.ReadError as e:
            print(f"Error extracting tar file: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
            
        return True
    
    def _get_type_char(self, member):
        """Get character representing file type"""
        if member.isfile():
            return 'f'
        elif member.isdir():
            return 'd'
        elif member.islnk():
            return 'l'
        elif member.issym():
            return 's'
        else:
            return '?'


def main():
    parser = argparse.ArgumentParser(description='Secure Tar Archive Processor')
    parser.add_argument('archive', help='Path to tar archive')
    parser.add_argument('--extract', '-x', action='store_true', 
                       help='Extract archive (default: list only)')
    parser.add_argument('--output', '-o', help='Output directory for extraction')
    parser.add_argument('--max-size', type=int, default=100_000_000,
                       help='Maximum total extraction size in bytes')
    parser.add_argument('--max-files', type=int, default=1000,
                       help='Maximum number of files to process')
    
    args = parser.parse_args()
    
    # Check if archive exists
    if not os.path.exists(args.archive):
        print(f"Error: Archive '{args.archive}' not found")
        sys.exit(1)
    
    # Initialize processor with security limits
    processor = SecureTarProcessor(
        max_extract_size=args.max_size,
        max_files=args.max_files
    )
    
    # Process archive
    if args.extract:
        success = processor.extract_archive(args.archive, args.output)
    else:
        success = processor.list_archive(args.archive)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
