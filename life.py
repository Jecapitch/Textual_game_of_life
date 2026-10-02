#!/usr/bin/env python3

"""Conway's game of life applied on the letters on a text in a finite space"""


from functools import cached_property
from time import sleep
from typing import Iterator, TypeAlias


Bitmap: TypeAlias = list[list[int]]


class TextLife:
    """
    Run Conway's game of life on a text, on a finite (non-wrapping) grid.

    The grid has the size of the text (height = number of lines, width =
    length of the longest line). A starting pattern file defines which cells
    are alive at generation 0. When displayed, a live cell shows the letter
    of the text at that position, and a dead cell shows the `dead`
    character ("*" by default).

    Attributes:
        pattern: Lines of the pattern file ("x" or "X" marks a live cell).
        text: Lines of the text file, used as the grid and for display.
        bitmap: Current generation, 1 for a live cell and 0 for a dead one.
        bmgen: Generator that steps the simulation (see `next_state`).
        dead: Character displayed in place of a dead cell.
    """

    def __init__(self,
                 text_file: str,
                 pattern_file: str,
                 dead: str = "_"
                 ) -> None:
        """
        Load the pattern and the text, and prepare the first generation.

        Args:
            text_file: path to the text that defines the grid and the
                letters shown on live cells.
            pattern_file: path to the file describing the initial pattern.
            dead: character displayed for dead cells, "*" by default. It
                should be a single character to keep the lines aligned.
        """
        self.pattern: list[str] = self.load_text(pattern_file)
        self.text: list[str] = self.load_text(text_file)
        self.dead = dead
        self.bitmap = self._initial_bitmap
        self.bmgen = self.next_state()

    def empty_bitmap(self) -> Bitmap:
        """
        Return a new bitmap of the grid size with every cell dead.

        Returns:
            A `height` x `width` list of lists filled with 0.
        """
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    @cached_property
    def _initial_bitmap(self) -> Bitmap:
        """
        Build generation 0 by placing the pattern at the top-left corner.

        Every "x" or "X" in the pattern file becomes a live cell. The pattern
        is not centered and must fit inside the text grid.

        Returns:
            The initial bitmap.
        """
        bm = self.empty_bitmap()
        for r, row in enumerate(self.pattern):
            for c, cell in enumerate(row):
                if self.pattern[r][c] in "xX":
                    bm[r][c] = 1
        return bm

    @cached_property
    def height(self) -> int:
        """Number of rows of the grid (number of lines of the text)."""
        return len(self.text)

    @cached_property
    def width(self) -> int:
        """Number of columns of the grid (length of the longest text line)."""
        mmax = 0
        for line in self.text:
            mmax = max(mmax, len(line))
        return mmax

    def cell_neighbours(self, row: int, col: int) -> int:
        """
        Count the live neighbours of a cell in the current bitmap.

        The 8 surrounding cells are checked. Cells outside the grid are
        considered dead (no wrap-around).

        Args:
            row: row index of the cell.
            col: column index of the cell.

        Returns:
            The number of live neighbours, from 0 to 8.
        """
        n = 0
        v = (-1, 0, 1)
        for x in v:
            for y in v:
                r, c = row + y, col + x
                if (
                        not (r == row and c == col)
                        and 0 <= r < self.height and 0 <= c < self.width
                ):
                    n += (self.bitmap[r][c])
        return n

    def next_state(self) -> Iterator[bool]:
        """
        Generate the successive generations of the game.

        Each `next()` yields True while the current generation can be
        displayed, then computes the following one and stores it in
        `self.bitmap`. Rules: a cell is alive in the next generation if it
        has exactly 3 live neighbours, or if it is alive and has exactly 2.

        Yields:
            True while the simulation goes on, False once the next
            generation is identical to the current one (stable state).
        """
        bm = self.bitmap
        while True:
            yield True
            new_bm: Bitmap = self.empty_bitmap()
            for r, row in enumerate(bm):
                for c, cell in enumerate(row):
                    n = self.cell_neighbours(r, c)
                    new_bm[r][c] = int(n == 3 or (cell == 1 and n == 2))
            if new_bm == bm:
                yield False
            self.bitmap = bm = new_bm

    def load_text(self, file: str):
        """
        Read a file and normalize its lines.

        Newlines and double quotes are removed and the text is uppercased.

        Args:
            file: path to the file to read.

        Returns:
            The list of normalized lines.

        Raises:
            OSError: if the file cannot be opened.
        """
        with open(file, "r") as f:
            return [
                line.rstrip("\n").upper()
                for line in f
            ]

    def display_life_text(self) -> None:
        """
        Show the current generation and append it to "result.txt".

        Live cells display the letter of the text and dead cells display
        the `dead` character. Each line is padded up to the grid width with
        '|'. Empty lines of the text are kept as empty lines. After each
        generation, a separator line is written to the file (not to the
        terminal).
        """
        with open("result.txt", "a") as f:
            for r, row in enumerate(self.text):
                if not len(row):
                    print()
                    print(file=f)
                    continue
                s = "".join(self.text[r][c]
                            if self.bitmap[r][c]
                            else self.dead
                            for c, cell in enumerate(row)
                            )
                s += ('|' * (self.width - len(s)))
                print(s)
                print(s, file=f)
            print(file=f)
            print("================================", file=f)
            print(file=f)


if __name__ == "__main__":
    import sys
    import os
    if not 3 <= len(sys.argv) <= 4:
        print("Usage:")
        print("  python3 life.py <text_file> <pattern_file> "
              "[dead_cell_character]")
        exit()
    try:
        if os.path.exists("result.txt"):
            os.remove("result.txt")
        L = TextLife(*sys.argv[1:])
        print("\033[?47h")
        print("\033[?25l")
        on = next(L.bmgen)
        while on:
            print("\033[2J\033[H")
            L.display_life_text()
            sleep(.5)
            on = next(L.bmgen)
        sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[?25h")
        print("\033[?47l")
