# UniversalTuringMachine

takes in Standard Description for TMs, and runs them as text output step-by-step

## Standard Descriptions
Standard Descriptions (SDs) and Description Numbers (DNs heh) are described in https://en.wikipedia.org/wiki/Description_number

Every m-configuration for a Turing machine can be made with the following format
- Name: an m-config can be given a name like q<sub>1</sub> or q<sub>3</sub>
   - we will standardize this convention of q<sub>i</sub> to start at 1
- Symbol: the scanned symbol for an m-config can be described in the format of  s<sub>j</sub>. Currently, the assumptions are that
   - if j=0, the symbol is blank
   - if j=1, the symbol is 0
   - if j=2, the symbol is 1
- Operation: an operation has the format of a symbol to be printed with the above format, followed by an command to move left, right, or not at all
   - while this technically means we have to print a character, if we don't want any changes we can just print the same character as scanned
- Next: tells us the name of the next m-config, follows the same format as above

Turing proves that with this, TMs can be represented as a string
> The state q<sub>i</sub> is encoded by the letter 'D' followed by the letter 'A' repeated i times (a unary encoding).
The tape symbol s<sub>j</sub> is encoded by the letter 'D' followed by the letter 'C' repeated j times.
The transitions are encoded by giving the state, input symbol, symbol to write on the tape, direction to move (expressed by the letters 'L', 'R', or 'N', for left, right, or no movement), and the next state to enter, with states and symbols encoded as above.

Finally, to separate the m-configs we just have semi-colons after each one

An example of a TM that alternates printing 1 and 0 forever is *DADDCCRDAA;DAADDCRDA;* in this format

## Description Numbers
Technically speaking, DNs aren't very different or anymore useful compared to SDs, but it was essential for Turing original proof, so we include in rememberance.

To convert from a SD to a DN, we simply replace each letter with a number in this way
- "A" is replaced by 1
- "C" is replaced by 2
- "D" is replaced by 3
- "L" is replaced by 4
- "R" is replaced by 5
- "N" is replaced by 6
- ";" is replaced by 7

So every Turing Machine can be represented by a natural number!
