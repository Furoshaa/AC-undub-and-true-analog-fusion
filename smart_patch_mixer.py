#!/usr/bin/env python3
"""
Smart Patch Mixer for ROM Files
Intelligently applies True Analog patches to undub version by finding correct offsets
using code context matching instead of assuming same offsets.
"""

import os
import logging
from datetime import datetime

def setup_logging():
    """Setup logging to both console and file"""
    # Create log folder if it doesn't exist
    log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_folder, exist_ok=True)
    
    log_filename = os.path.join(log_folder, f"patch_mixer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return log_filename

def find_file_in_folder(folder_path):
    """Find the first file in a folder and ensure only one file exists"""
    if not os.path.exists(folder_path):
        return None, None, "Folder does not exist"
    
    files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            files.append((item_path, item))
    
    if len(files) == 0:
        return None, None, "No files found"
    elif len(files) > 1:
        file_list = ", ".join([f[1] for f in files])
        return None, None, f"Multiple files found: {file_list}. Please ensure only one file per folder."
    else:
        return files[0][0], files[0][1], None

def find_context_match(original_data, undub_data, target_offset, context_size=16):
    """
    Find the corresponding location in undub by matching surrounding code context
    """
    # Extract context around the target offset in original
    start = max(0, target_offset - context_size)
    end = min(len(original_data), target_offset + context_size)
    original_context = original_data[start:end]
    
    # Search for this context in undub
    for i in range(len(undub_data) - len(original_context) + 1):
        if undub_data[i:i + len(original_context)] == original_context:
            # Found matching context, calculate the corresponding offset
            offset_diff = i - start
            new_offset = target_offset + offset_diff
            
            logging.info(f"Found context match: 0x{target_offset:06X} -> 0x{new_offset:06X} (diff: +{offset_diff})")
            return new_offset
    
    logging.warning(f"Could not find context match for offset 0x{target_offset:06X}")
    return None

def validate_patch_location(original_data, undub_data, true_analog_data, original_offset, undub_offset):
    """
    Validate that the patch location is correct by checking surrounding bytes
    """
    # Check a few bytes before and after the patch location
    check_size = 8
    start = max(0, original_offset - check_size)
    end = min(len(original_data), original_offset + check_size)
    
    original_section = original_data[start:end]
    undub_section = undub_data[undub_offset - (original_offset - start):undub_offset + (end - original_offset)]
    
    if len(undub_section) != len(original_section):
        logging.error(f"Section size mismatch at 0x{original_offset:06X}")
        return False
    
    # Check if the sections match (they should, since we found them by context)
    if undub_section != original_section:
        logging.error(f"Section content mismatch at 0x{original_offset:06X}")
        return False
    
    logging.info(f"OK: Validated patch location 0x{undub_offset:06X}")
    return True

def apply_smart_patch():
    """Main function to apply True Analog patches to undub with correct offsets"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    log_filename = setup_logging()
    
    logging.info("=== Smart Patch Mixer Started ===")
    logging.info(f"Log file: {log_filename}")
    
    # Check if mixed folder is empty
    mixed_folder = os.path.join(base_path, 'mixed')
    if os.path.exists(mixed_folder):
        mixed_files = [f for f in os.listdir(mixed_folder) if os.path.isfile(os.path.join(mixed_folder, f))]
        if mixed_files:
            logging.error(f"Mixed folder is not empty. Found files: {', '.join(mixed_files)}")
            logging.error("Please remove files from the mixed folder before running.")
            return False
    
    # Find files in each folder
    original_path, original_filename, error = find_file_in_folder(os.path.join(base_path, 'original'))
    if error:
        logging.error(f"Error in 'original' folder: {error}")
        return False
    
    true_analog_path, true_analog_filename, error = find_file_in_folder(os.path.join(base_path, 'true analog'))
    if error:
        logging.error(f"Error in 'true analog' folder: {error}")
        return False
    
    undub_path, undub_filename, error = find_file_in_folder(os.path.join(base_path, 'undub'))
    if error:
        logging.error(f"Error in 'undub' folder: {error}")
        return False
    
    logging.info(f"Found files:")
    logging.info(f"  Original: {original_filename}")
    logging.info(f"  True Analog: {true_analog_filename}")
    logging.info(f"  Undub: {undub_filename}")
    
    # Load files
    logging.info("Loading files...")
    try:
        with open(original_path, 'rb') as f:
            original_data = f.read()
        with open(true_analog_path, 'rb') as f:
            true_analog_data = f.read()
        with open(undub_path, 'rb') as f:
            undub_data = f.read()
        
        logging.info(f"Original: {len(original_data)} bytes")
        logging.info(f"True Analog: {len(true_analog_data)} bytes")
        logging.info(f"Undub: {len(undub_data)} bytes")
    except Exception as e:
        logging.error(f"Error loading files: {e}")
        return False
    
    # Find True Analog differences
    logging.info("Analyzing True Analog differences...")
    ta_diffs = []
    for i in range(min(len(original_data), len(true_analog_data))):
        if original_data[i] != true_analog_data[i]:
            ta_diffs.append((i, original_data[i], true_analog_data[i]))
    
    logging.info(f"Found {len(ta_diffs)} True Analog differences")
    
    # Create mixed file starting with undub
    logging.info("Creating mixed file from undub base...")
    mixed_data = bytearray(undub_data)
    
    # Apply True Analog patches with adjusted offsets
    successful_patches = 0
    failed_patches = 0
    
    for original_offset, original_byte, new_byte in ta_diffs:
        logging.info(f"Processing patch at 0x{original_offset:06X}: 0x{original_byte:02X} -> 0x{new_byte:02X}")
        
        # Find corresponding location in undub
        undub_offset = find_context_match(original_data, undub_data, original_offset)
        
        if undub_offset is None:
            logging.error(f"Failed to find location for patch at 0x{original_offset:06X}")
            failed_patches += 1
            continue
        
        # Validate the location
        if not validate_patch_location(original_data, undub_data, true_analog_data, original_offset, undub_offset):
            logging.error(f"Validation failed for patch at 0x{original_offset:06X}")
            failed_patches += 1
            continue
        
        # Apply the patch
        if undub_offset < len(mixed_data):
            mixed_data[undub_offset] = new_byte
            logging.info(f"APPLIED: Applied patch: 0x{original_offset:06X} -> 0x{undub_offset:06X}")
            successful_patches += 1
        else:
            logging.error(f"Offset 0x{undub_offset:06X} is out of bounds")
            failed_patches += 1
    
    # Save mixed file
    if not os.path.exists(mixed_folder):
        os.makedirs(mixed_folder)
    
    mixed_filename = undub_filename  # Use same name as undub
    mixed_path = os.path.join(mixed_folder, mixed_filename)
    
    try:
        with open(mixed_path, 'wb') as f:
            f.write(mixed_data)
        logging.info(f"SAVED: Mixed file saved: {mixed_path}")
    except Exception as e:
        logging.error(f"Error saving mixed file: {e}")
        return False
    
    # Summary
    logging.info("=== PATCH SUMMARY ===")
    logging.info(f"Total patches: {len(ta_diffs)}")
    logging.info(f"Successful patches: {successful_patches}")
    logging.info(f"Failed patches: {failed_patches}")
    logging.info(f"Success rate: {successful_patches/len(ta_diffs)*100:.1f}%")
    
    if failed_patches == 0:
        logging.info("SUCCESS: All patches applied successfully!")
    else:
        logging.warning(f"WARNING: {failed_patches} patches failed. Check log for details.")
    
    logging.info("=== Smart Patch Mixer Completed ===")
    return True

if __name__ == "__main__":
    apply_smart_patch()