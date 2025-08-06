# Armored Core PS1 - Undub + True Analog Patch Fusion

I wanted to be able to have Armored Core on PS1 with the undub patch as well as the true analogs patch. Though I have no knowledge of reverse engineering or ROM modding or whatever, but I know how to use Python and AI. So I made this to help me understand the structural difference between patched versions of the game compared to the normal version of it so that I could just use hexadecimal code of the file to manually mix them.

## What This Does

Basically I compare a normal version of the game with the undub version and the true analog version and it compares the hexadecimal of the file. The undub version is always bigger so the code isn't at the same offset but I realized it just has moved downward so I just need to place the true analog code further in the file of the undub and boom it works.

## Current Status

Right now I'm working on making a Python file capable of doing this on its own because it's tedious so it probably could be used for other games as well or whatever.

At some point maybe I'll make a guide on how to use this and make it work yourself but I'm too lazy yet.

## Files

- `checkion.py` - Compare all 3 files and mix them if there is no conflict
- Analysis output files .txt (tracked with Git LFS due to size)

## How It Works

1. Analyzes the FDAT.T file from three versions (original, undub, true analogs)
2. Identifies conflicts between patches using hexadecimal comparison
3. Output a text file for the differences between original and undub
4. Output a text file for the differences between original and true analogs
5. Output a text file with the conflicts between the 2.
6. If no conflicts, will output a file that combines both patches
