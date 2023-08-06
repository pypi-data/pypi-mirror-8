usage: luxemx.py [-h] [-i INFILE] [-o OUTFILE] [-l] [-p [PRETTY]]
                 [-s [PRETTY_SPACED]]
                 [path [path ...]]

Extracts specified elements from luxem documents.

positional arguments:
  path                  A luxem array containing the path to the nodes to
                        output.

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        File to parse; defaults to stdin.
  -o OUTFILE, --outfile OUTFILE
                        File to write to; defaults to stdout.
  -l, --lines           Output only primitives, one per line.
  -p [PRETTY], --pretty [PRETTY]
                        Prettify output with PRETTY tab indentation. Defaults
                        to 1 tab indent.
  -s [PRETTY_SPACED], --pretty-spaced [PRETTY_SPACED]
                        Prettify output with PRETTY_SPACED space indentation.
                        Defaults to 4 space indent.

PATH FORMATTING: The path is a list of child selections, starting from the
array at the root of the document. Array selectors can be numbers, (*) (a
wildcard, which follows all array children), (range) [X,Y] (a range selection,
which follows all children at indexes [X,Y)), or an array of selectors. Object
selectors can be strings, (*) (a wildcard, which follows all object children),
or an array of selectors. Example (you may have to provide shell escapes):
luxemx '(*),file_info,[path,altpath]'
