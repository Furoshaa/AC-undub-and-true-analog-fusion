#!/usr/bin/env python3
"""
FDAT.T File Comparison Tool for Armored Core PSX
Simple comparison to identify patch conflicts and generate diff files
"""

import os

def compare_files():
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # File paths
    original_path = os.path.join(base_path, 'original', 'FDAT.T')
    true_analog_path = os.path.join(base_path, 'true analog', 'FDAT.T')
    undub_path = os.path.join(base_path, 'undub', 'FDAT.T')
    
    # Load files
    print("Loading files...")
    try:
        with open(original_path, 'rb') as f:
            original = f.read()
        with open(true_analog_path, 'rb') as f:
            true_analog = f.read()
        with open(undub_path, 'rb') as f:
            undub = f.read()
        print(f"Original: {len(original)} bytes")
        print(f"True Analog: {len(true_analog)} bytes")
        print(f"Undub: {len(undub)} bytes")
    except Exception as e:
        print(f"Error loading files: {e}")
        return
    
    # Find differences
    print("\nAnalyzing differences...")
    
    max_len = max(len(original), len(true_analog), len(undub))
    
    # Pad files to same length
    original += b'\x00' * (max_len - len(original))
    true_analog += b'\x00' * (max_len - len(true_analog))
    undub += b'\x00' * (max_len - len(undub))
    
    # Find True Analog differences
    ta_diffs = []
    for i in range(max_len):
        if original[i] != true_analog[i]:
            ta_diffs.append((i, original[i], true_analog[i]))
    
    # Find Undub differences
    undub_diffs = []
    for i in range(max_len):
        if original[i] != undub[i]:
            undub_diffs.append((i, original[i], undub[i]))
    
    print(f"True Analog differences: {len(ta_diffs)}")
    print(f"Undub differences: {len(undub_diffs)}")
    
    # Check for overlaps
    ta_offsets = {diff[0] for diff in ta_diffs}
    undub_offsets = {diff[0] for diff in undub_diffs}
    overlaps = ta_offsets & undub_offsets
    
    print(f"\n*** CRITICAL RESULT ***")
    print(f"Overlapping modifications: {len(overlaps)}")
    
    if len(overlaps) == 0:
        print("✓ NO CONFLICTS! Both patches can be combined safely!")
    else:
        print(f"⚠ WARNING: {len(overlaps)} conflicting locations found!")
        print("Manual resolution needed for conflicting bytes.")
    
    # Write True Analog differences to file
    ta_output = os.path.join(base_path, 'true_analog_differences.txt')
    with open(ta_output, 'w') as f:
        f.write("TRUE ANALOG vs ORIGINAL DIFFERENCES\n")
        f.write("="*50 + "\n")
        f.write(f"Total differences: {len(ta_diffs)}\n\n")
        f.write("Offset    | Original | True Analog | ASCII\n")
        f.write("-"*45 + "\n")
        
        for offset, orig, modified in ta_diffs:
            orig_char = chr(orig) if 32 <= orig <= 126 else '.'
            mod_char = chr(modified) if 32 <= modified <= 126 else '.'
            f.write(f"0x{offset:06X} |   0x{orig:02X}   |    0x{modified:02X}    | '{orig_char}' -> '{mod_char}'\n")
    
    print(f"✓ True Analog differences saved to: {ta_output}")
    
    # Write Undub differences to file
    undub_output = os.path.join(base_path, 'undub_differences.txt')
    with open(undub_output, 'w') as f:
        f.write("UNDUB vs ORIGINAL DIFFERENCES\n")
        f.write("="*50 + "\n")
        f.write(f"Total differences: {len(undub_diffs)}\n\n")
        f.write("Offset    | Original | Undub | ASCII\n")
        f.write("-"*40 + "\n")
        
        for offset, orig, modified in undub_diffs:
            orig_char = chr(orig) if 32 <= orig <= 126 else '.'
            mod_char = chr(modified) if 32 <= modified <= 126 else '.'
            f.write(f"0x{offset:06X} |   0x{orig:02X}   | 0x{modified:02X}  | '{orig_char}' -> '{mod_char}'\n")
    
    print(f"✓ Undub differences saved to: {undub_output}")
    
    # Write overlap analysis
    if overlaps:
        overlap_output = os.path.join(base_path, 'conflicts.txt')
        with open(overlap_output, 'w') as f:
            f.write("CONFLICTING LOCATIONS\n")
            f.write("="*50 + "\n")
            f.write(f"Total conflicts: {len(overlaps)}\n\n")
            f.write("Offset    | Original | True Analog | Undub | Same?\n")
            f.write("-"*55 + "\n")
            
            ta_dict = {diff[0]: diff[2] for diff in ta_diffs}
            undub_dict = {diff[0]: diff[2] for diff in undub_diffs}
            
            for offset in sorted(overlaps):
                orig_byte = original[offset]
                ta_byte = ta_dict[offset]
                undub_byte = undub_dict[offset]
                same = "YES" if ta_byte == undub_byte else "NO"
                
                f.write(f"0x{offset:06X} |   0x{orig_byte:02X}   |    0x{ta_byte:02X}     | 0x{undub_byte:02X}  | {same}\n")
        
        print(f"✓ Conflict analysis saved to: {overlap_output}")
        
        # Count real conflicts (where both patches want different values)
        real_conflicts = sum(1 for offset in overlaps 
                           if ta_dict[offset] != undub_dict[offset])
        
        if real_conflicts == 0:
            print("✓ Good news: All overlapping changes are identical!")
            print("  Both patches can be applied together without issues.")
        else:
            print(f"⚠ {real_conflicts} real conflicts need manual resolution!")
    
    # Generate combined file if no real conflicts
    if len(overlaps) == 0 or (overlaps and sum(1 for offset in overlaps 
                             if ta_dict[offset] != undub_dict[offset]) == 0):
        print("\nGenerating combined file...")
        combined = bytearray(original)
        
        # Apply True Analog changes
        for offset, orig, modified in ta_diffs:
            if offset < len(combined):
                combined[offset] = modified
        
        # Apply Undub changes
        for offset, orig, modified in undub_diffs:
            if offset < len(combined):
                combined[offset] = modified
        
        combined_path = os.path.join(base_path, 'FDAT_combined.T')
        with open(combined_path, 'wb') as f:
            f.write(combined)
        
        print(f"✓ Combined file saved as: {combined_path}")
        print("  This file should work with both patches applied!")
    else:
        print("\nSkipping combined file generation due to conflicts.")
        print("Check conflicts.txt for manual resolution guidance.")

if __name__ == "__main__":
    compare_files()