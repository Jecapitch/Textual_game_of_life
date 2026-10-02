# TextLife

Conway's Game of Life played **on the letters of a text**.

The text defines the grid. A pattern file defines which cells are alive at  
generation 0. Live cells show the letter of the text at their position, and  
dead cells are replaced by a filler character (`*` by default).

## Requirements

- Python 3.10 or later
- No third-party dependency
- A terminal that supports ANSI escape sequences

## Usage

```
python3 life.py <text_file> <pattern_file> [dead_cell_character]
```

| Argument              | Required | Description                                                                                    |
|-----------------------|----------|------------------------------------------------------------------------------------------------|
| `text_file`           | yes      | Text that defines the grid and the letters shown on live cells                                 |
| `pattern_file`        | yes      | Initial pattern, where `x` or `X` is a live cell                                               |
| `dead_cell_character` | no       | Character displayed for dead cells (default `*`). Use a single character to keep lines aligned |

The simulation runs with a 0.5 second delay between generations. Press
`Ctrl+C` to stop it at any time.

## Example

`text.txt`:

```
THE QUICK BROWN FOX
JUMPS OVER THE LAZY
DOG AND KEEPS RUNNING
THROUGH THE WHOLE FIELD
UNTIL THE SUN GOES DOWN
```

`glider.txt`:

```
 x
  x
xxx
```

```
python3 life.py text.txt glider.txt
```

Generation 0:

```
*H*****************||||
**M****************||||
DOG******************||
***********************
***********************
```

Generation 1:

```
*******************||||
J*M****************||||
*OG******************||
*H*********************
***********************
```

The glider moves one step diagonally every four generations, as in the
classic game.

## How it works

- **Grid:** its height is the number of lines of the text, and its width is
  the length of the longest line.
- **Pattern placement:** the pattern is placed at the top-left corner of the
  grid. It is not centered and must fit inside the text.
- **Rules:** a cell is alive in the next generation if it has exactly 3 live
  neighbours, or if it is alive and has exactly 2.
- **Borders:** the grid is finite and does not wrap around. Cells outside it
  are considered dead.
- **End of the simulation:** it stops when a generation is identical to the
  previous one (still life or empty grid). Oscillators and gliders that keep
  moving never trigger it, so stop those with `Ctrl+C`.

## Input files

Both files go through the same normalization:

- trailing newlines are removed
- everything is converted to uppercase

Empty lines of the text are kept as empty lines in the output.

## Output

- **Terminal:** the screen is cleared at each generation, in the terminal's
  alternate screen, with the cursor hidden. Both are restored on exit.
- **`result.txt`:** every generation is also appended to this file in the
  current directory, followed by a separator line. The file is deleted at
  the start of each run.
- **Padding:** lines shorter than the grid width are padded with `|` so that
  they all have the same length.

## Project layout

```
life.py     # TextLife class and command-line entry point
```

| Method              | Role |
|---------------------|----------------------------------------------------|
| `load_text`         | Reads and normalizes a file                        |
| `_initial_bitmap`   | Builds generation 0 from the pattern               |
| `cell_neighbours`   | Counts the live neighbours of a cell               |
| `next_state`        | Generator that computes the successive generations |
| `display_life_text` | Prints a generation and appends it to `result.txt` |

## Documentation
- [Conway's Game of Life](https://playgameoflife.com) : generator with explanation and examples.  
  (last consulted 2026-10-02)
- [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), in *Wikipedia*.  
  (last consulted 2026-10-02)
# Textual_game_of_life
