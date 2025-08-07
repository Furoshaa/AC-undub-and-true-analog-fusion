# Armored Core PS1 - Undub + True Analog Patch Fusion

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

If anaything is wrong just create an issue and i'll answer it asaic


## What This Does

Basically I compare a normal version of the game with the undub version and the true analog version and it compares the hexadecimal of the file. The undub version is always bigger so the code isn't at the same offset but I realized it just has moved downward so I just need to place the true analog code further in the file of the undub and boom it works.

## Current Status

Right now I'm working on making a Python file capable of doing this on its own because it's tedious so it probably could be used for other games as well or whatever. This file is done and should be working fine but somhow isn't so use at your own risk. The patches are already made anyway and are ready to use.

At some point maybe I'll make a guide on how to use this and make it work yourself but I'm too lazy yet.

## Files

- `checkion.py` - Compare all 3 files and mix them if there is no conflict
- Analysis output files .txt (tracked with Git LFS due to size) in the checkion folder
- `smart_patch_mixer.py` - In theory this python file is smart enough to understand the true-analogs patches changes compare to the original and apply them to the undub by changing the offset to match the place where the true-analogs patch SHOULD be applied and output the file in the mixed folder. In theory it works but for some reason that i dont know, i doesn't. I used it on the FDAT.T file of one of the game and when i recompiled the game it didn't work. I tried this many times and it never worked even tho the hexa code looked fine so idk.
- `logs` when using the smart_patch_mixer.py it will output a log file to tell you basically everything it did.

## How It Works

1. Analyzes the file from three versions (original, undub, true analogs)
2. Identifies conflicts between patches using hexadecimal comparison.
3. Output a text file for the differences between original and undub.
4. Output a text file for the differences between original and true analogs.
5. Output a text file with the conflicts between the 2 if there is.
6. If no conflicts, will output a file that combines both patches.
