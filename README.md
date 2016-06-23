# ABC End View
Something fun -- or supposed to be.

*Heads up: This is highly unoptimized - I am too lazy for that.*

## General description
Everything in this code is in `utils.py` and `utils_janko.py`.
- The solver, with commandline prompt is the method `solve()` in `utils.py`.
- `utils_janko.py` includes a method `solver_janko(no = 0, pass_on = False)` that would ask for a problem number (1-530) from http://www.janko.at/Raetsel/Abc-End-View/index.htm, then fetch it and solve.

The rest are experimental code testing out other stuffs.

## How it works
Every cell has a label that includes the possible choices to be filled. The algorithm would find cells that only have one possible choice, then do attritions on every neighboring cells (either on the same column, row, or diagonal, depending on the requirement of the board. If all possible attritions are made and the board is still not completely solved, then trial-and-error occur. Since it's partially bruteforcing, it will yield all possible solutions for a puzzle, and is guaranteed to terminate given enough time.

## Footnote
You're free to fork this and and do whatever you want to with it. I'm also looking to find more efficient ways to do this, preferably more math-y approaches; so if you have suggestions, or anything at all you want to tell me, feel free to shoot an email to ngoc@underlandian.com.
