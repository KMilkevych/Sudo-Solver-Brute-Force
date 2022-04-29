# Sudoku-Solver-Brute-Force
A graphical Sudoku-board solver using a recursive brute force algorithm (backtracking), and pygame.

## Usage
Upon running the application, a graphical board will pop up.
- Use the mouse to hover over a cell.
- Press a number (1-9) to input this number into the hovered cell.
- Press SPACE to empty the hovered cell.
- Press ENTER to run the solving algorithm.

## Details
Upon running, the algorithm will check for illegal cells (such duplicate number in a block, row or column).
If no conflict has been found, the algorithm will solve the board graphically.
Otherwise, the algorithm prints out the coordinates of the cell that caused a conflict (first illegal cell), as well as the board, and terminates.
