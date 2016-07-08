# ABC End View
Something fun -- or supposed to be.

*Heads up: This is highly unoptimized - I am too lazy for that.*

## General description
- The solver, with commandline prompt is the method `solve_main(int)` in `utils_nextgen.py`. The file requires imports from `BeautifulSoup4`.
- The `int` parameter is problem number (1-530) from http://www.janko.at/Raetsel/Abc-End-View/index.htm, when input will tell the method to fetch it and solve. Otherwise, it will ask for input via CLI.

`utils_nextgen.py` have properly-documented methods, some of them are nightly experimental, so feel free to meddle around. `test_generate()` is not completely implemented, but it will work if you explicitly give the `clue_count` parameter.

The GUI is in `utils_gui.py`, which requires imports from wxPython. It is precompiled for Windows 10, 64-bit into the given executable. If it doesn't work, please run it from source.

## Dependencies
Technically, you can comment out `BeautifulSoup4` and the fetch methods as it is already cached in the `janko_cache` folder. In contrary, the `wxPython` module is required for GUI.

`BeautifulSoup4` can be installed via `pip` for most OSes. `wxPython` has an installer that works fine on Windows, but messes up on El Capitan. Another way to get `wxPython` on Mac that worked for me is installing through Homebrew with `brew install wxpython`. I never tried on Linux, but it should be either the case of standalone, or via a package manager.

## How to run
There are 4 ways to run this - 2 for each file:
- Run `python utils_nextgen.py <problem_number>`.
- Import `utils_nextgen.py` and run solve_main().
- Run the precompiled `utils_gui.exe`.
- Run `python utils_gui.py`.

## How it works
Every cell has a label that includes the possible choices to be filled. The algorithm would find cells that only have one possible choice, then do attritions on every neighboring cells (either on the same column, row, or diagonal, depending on the requirement of the board. If all possible attritions are made and the board is still not completely solved, then trial-and-error occur. Since it's partially bruteforcing, it will yield all possible solutions for a puzzle, and is guaranteed to terminate given enough time.

## Footnote
You're free to fork this and and do whatever you want to with it. I'm also looking to find more efficient ways to do this, preferably more math-y approaches; so if you have suggestions, or anything at all you want to tell me, feel free to shoot an email to ngoc@underlandian.com.
