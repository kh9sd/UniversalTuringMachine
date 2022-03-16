# UniversalTuringMachine

runs Standard Descriptions and Description Numbers of Turing machines

## Setup and usage
Download the files, you only need to worry about two of them, `config.py` and `main.py`

`config.py` contains a dictionary `sym_dict` that defines what character are 
defined by the 0th symbol, 1st symbol, etc

Example: we have the dictionary
```
sym_dict = {
    0: " ",
    1: "0",
    2: "1"
}
```
So the 0th symbol is a space, the 1st symbol is a 0, and the 2nd symbol is a 1.
If you want to change this mapping, go ahead but remember these key things:
1. Don't change the name *sym_dict* or any of the syntax braces, colons, etc
2. The values on the lefthand side must be plain integers
3. The values on the righthand side must be surrounded by quotes

By default, new tape squares start with the 0th symbol. We keep a default_dict in the file just for your reference.

It also contains `tape_array` and `cur_pos`, which can be set to get a custom
starting tape. `tape_array` defines the order and characters on each square,
and `cur_pos` tells which square the Turing Machine is currently located at,
leftmost square is 0.

So for example, if I wanted a tape 

**[a][bee][c][<ins>d</ins>][2][1]** where the underlined square is the current one

then I would set 
```
tape_array = ["a", "bee", "c", "d", "2", "1"]
cur_pos = 3
```

Note that this custom tape doesn't care about the symbol_dict at all, like why should it

`turingrunner.py` is what you'll be using to actually run the UTM.
Once it starts, it will read everything from the config.py,
and ask you for your Standard Description or Description Number to run.


Now, the actual Standard Descriptions and Description Numbers are a bit more complicated

## Standard Descriptions
Standard Descriptions (SDs) and Description Numbers (DNs heh) are described in 
https://en.wikipedia.org/wiki/Description_number

Every m-configuration for a Turing machine can be made with the following format
- Name: an m-config can be given a name like q<sub>1</sub> or q<sub>3</sub>
   - we will standardize this convention of q<sub>i</sub> to start at 1
- Symbol: the scanned symbol for an m-config can be described in the format of  s<sub>j</sub>. 
The exact symbol values are defined in the config.py file
   - if *j = 0*, the symbol is the 0th symbol
   - if *j = 1*, the symbol is the 1st symbol
   - if *j = 2*, the symbol is the 2nd symbol
- Operation: an operation has the format of a symbol to be printed with the above format, 
followed by a command to move left, right, or not at all
   - while this technically means we have to print a character, if we don't want any changes 
  we can just print the same character as scanned
- Next: tells us the name of the next m-config, follows the same format as above

Turing proves that with this, TMs can be represented as a string
> The state q<sub>i</sub> is encoded by the letter 'D' followed by the letter 'A' repeated i times (a unary encoding).
The tape symbol s<sub>j</sub> is encoded by the letter 'D' followed by the letter 'C' repeated j times.
The transitions are encoded by giving the state, input symbol, symbol to write on the tape, direction to move (expressed by the letters 'L', 'R', or 'N', for left, right, or no movement), and the next state to enter, with states and symbols encoded as above.

Finally, to separate the m-configs we just have semicolons after each one

An example of a TM that alternates printing 1 and 0 forever is *DADDCCRDAA;DAADDCRDA;* in this format

## Description Numbers
Technically speaking, DNs aren't very different or any more useful compared to SDs, 
but it was essential for Turing's original proof, so we include in rememberance.

To convert from a SD to a DN, we simply replace each letter with a number in this way
- "A" is replaced by 1
- "C" is replaced by 2
- "D" is replaced by 3
- "L" is replaced by 4
- "R" is replaced by 5
- "N" is replaced by 6
- ";" is replaced by 7

So every Turing Machine can be represented by a natural number!

##Examples of SDs and DNs
Here are a few to use and try:

`DADDCRDAA;DAADDRDAAA;DAAADDCCRDAAAA;DAAAADDRDA;` prints 0 and 1 to the right forever

`31332531173113353111731113322531111731111335317` is the same as above in a DN format

`DADDCRDAA;DADCDCLDAA;DAADDCLDA;DAADCDCRDAAA;` will halt
