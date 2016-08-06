# ABC End View
Something fun -- or supposed to be.

## General description
- The solver, with commandline prompt is the method `solve_main(int)` in `utils_input.py`.
- The `int` parameter is problem number (1-530) from http://www.janko.at/Raetsel/Abc-End-View/index.htm, when input will tell the method to fetch it and solve. If inserted `0`, it will ask for a problem number explicitly. If inserted `-1` or left blank, it will ask for input via CLI.

A screenshot of the GUI - with the infamous Janko problem number 480:

![alt text](http://i.imgur.com/GRNVSAG.png "It has 46,670 solutions, so don't bother trying solving.")

`utils_*.py` have properly-documented methods, some of them are nightly experimental, so feel free to meddle around.

The GUI is in `utils_gui.py`, which requires imports from wxPython. Since the precompiled executable doesn't consistently run on all machines, please run from source.

## Dependencies
`BeautifulSoup4` is required to fetch problems from Janko - however if it is already cached, it won't be imported, and thus is not needed. The `wxPython` module is required for GUI.

`BeautifulSoup4` can be installed via `pip` for most OSes. `wxPython` has an installer that works fine on Windows, but messes up on El Capitan. Another way to get `wxPython` on Mac that worked for me is installing through Homebrew with `brew install wxpython`. I never tried on Linux, but it should be easy to be installed via either a standalone, or a package manager.

## How to run
There are 3 ways to run this - the first 2 are almost equivalent:
- Run `python utils_input.py <problem_number>`.
- Import `utils_input.py` and invoke `solve_main()`.
- Run `python utils_gui.py`.

## How it works
Every cell has a label that includes the possible choices to be filled. The algorithm would find cells that only have one possible choice, then do attritions on every neighboring cells (either on the same column, row, or diagonal, depending on the requirement of the board. If all possible attritions are made and the board is still not completely solved, then trial-and-error occur. Since it's partially bruteforcing, it will yield all possible solutions for a puzzle, and is guaranteed to terminate given enough time.

## Footnote
You're free to fork this and and do whatever you want to with it. I'm also looking to find more efficient ways to do this, preferably more math-y approaches; so if you have suggestions, or anything at all you want to tell me, feel free to shoot an email to ngoc@underlandian.com.
