# Armored Core PS1 - Undub + True Analog Patch Fusion

## ⚠️ Important Credits

**I have not created the undub patches nor the true analogs patches. I just found a way to make them both work on a single ROM.**

- **Credit for the undub patches goes to "swosho"**
- **Credit for the true analogs patch goes to "VanLaser"**

---

I wanted to be able to have Armored Core on PS1 with the undub patch as well as the true analogs patch. Though I have no knowledge of reverse engineering or ROM modding or whatever, but I know how to use Python and AI. So I made this to help me understand the structural difference between patched versions of the game compared to the normal version of it so that I could just use hexadecimal code of the files to manually mix them.

## Patches

Theses patches can be find in the "Patches" folder of this repo or in the release package section.
To be used with xdelta.

1. Armored Core (Undub + True-Analogs) patch.xdelta
Usable with the v1.1 USA version of Armored Core. (SLUS-01323)

2. Armored Core Prototype (True-Analogs) patch.xdelta
Can be used with the prototype version of Armored Core which is an already undub version for preview only. (SLPS-00900 prototype)

3. Armored Core - Project Phantasma (Undub + True-Analogs) patch.xdelta
To use with the USA version of the game. (SLUS-00670)

4. Armored Core - Master of Arena (Disc 1) (Undub + True-Analogs) patch.xdelta
To use with the USA version (SLUS-01030)

5. Armored Core - Master of Arena (Disc 2) (Undub + True-Analogs) patch.xdelta
Same thing, just use it with the USA version (SLUS-01081)

If anything is wrong just create an issue and I'll answer it ASAP


## What This Does

Basically I compare a normal version of the game with the undub version and the true analog version and it compares the hexadecimal of the file. The undub version is always bigger so the code isn't at the same offset but I realized it just has moved downward so I just need to place the true analog code further in the file of the undub and boom it works.

## Current Status

Right now I'm working on making a Python file capable of doing this on its own because it's tedious so it probably could be used for other games as well or whatever. This file is done and should be working fine but somehow isn't, so use at your own risk. The patches are already made anyway and are ready to use.

At some point maybe I'll make a guide on how to use this and make it work yourself but I'm too lazy yet.

## Files

- `checkion.py` - Compare all 3 files and mix them if there is no conflict
- Analysis output files .txt (tracked with Git LFS due to size) in the checkion folder
- `smart_patch_mixer.py` - In theory this python file is smart enough to understand the true-analogs patches changes compared to the original and apply them to the undub by changing the offset to match the place where the true-analogs patch SHOULD be applied and output the file in the mixed folder. In theory it works but for some reason that I don't know, it doesn't. I used it on the FDAT.T file of one of the games and when I recompiled the game it didn't work. I tried this many times and it never worked even though the hex code looked fine so I don't know why.
- `logs/` - When using the smart_patch_mixer.py it will output a log file to tell you basically everything it did.

## How It Works

1. Analyzes the file from three versions (original, undub, true analogs)
2. Identifies conflicts between patches using hexadecimal comparison
3. Outputs a text file for the differences between original and undub
4. Outputs a text file for the differences between original and true analogs
5. Outputs a text file with the conflicts between the 2 patches if there are any
6. If no conflicts, will output a file that combines both patches

## Quick Start

### Using the Pre-made Patches (Recommended)
1. Download the appropriate `.xdelta` patch from the Patches folder or releases
2. Use xdelta to apply the patch to your ROM
3. Enjoy your undubbed game with true analog support!

### Using the Python Tools (For Development/Research)
**Note**: The Python tools work with extracted files, not ROM files directly.

1. **Extract ROMs using CDMage B5**: Extract all your ROM versions (original, undub, true analog)
2. **Locate FDAT.T files**: From each extracted ROM, navigate to `/GG/COM/` and copy the `FDAT.T` file
3. **Place FDAT.T files in appropriate folders**:
   - `original/` - FDAT.T from your original ROM
   - `undub/` - FDAT.T from your undubbed ROM  
   - `true analog/` - FDAT.T from your true analog patched ROM
4. Run `python checkion.py` to analyze differences and conflicts
5. Check the `checkion/` folder for detailed analysis files
6. If no conflicts, find your combined FDAT.T file in the `mixed/` folder
7. **Rebuild ROM using CDMage B5**: Replace the original `FDAT.T` in your ROM with the patched version

## Requirements

- Python 3.x (for development tools only)
- xdelta (for applying patches)
- CDMage B5 (for ROM extraction/rebuilding when using Python tools)
- Original Armored Core ROM files (BIN/CUE format)

## Folder Structure
```
├── original/         # Place FDAT.T files from original ROMs here
├── undub/            # Place FDAT.T files from undub patched ROMs here  
├── true analog/      # Place FDAT.T files from true analog patched ROMs here
├── mixed/            # Combined FDAT.T output files appear here
├── checkion/         # Analysis output files
├── logs/             # Smart patch mixer logs
└── Patches/          # Ready-to-use xdelta patches (apply to ROM files directly)
```
