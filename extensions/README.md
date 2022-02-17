# Extensions

This directory contains several extensons as well as some info on how to write
your own.


## Mpv extension

To use the mpv extension move mpv\_dire.lua to
~/.config/mpv/scripts/ and then when a video is playing you can press 'd' and it
will try to send text to a dire instance named video. It uses dire\_send\_text
to do this. It will append text to the end.


## Sentence search

sentence\_search.py defines a function that can be used to search for example
sentences. In ~/.config/dire/ create a directory named 'line\_bank' and in it
you can put files which contain sentences. sentence\_search will search through
each and return the first found example sentence with the word, the name of the
file.


### Cleaning common file types

The following may be different depending on your environment. I attempted to only
use POSIX functionality, but there may be errors. Please check the output.

If you have subtitles in the srt file format you can run the following command
to convert them into a file full of sentences:

```bash
find -type f | grep '\.srt$' | xargs cat | grep -v '^[0-9]\|^\s*$'  > out_file
```

This will combine all the srt files in all subdirectories the command is run in.
This should also work fairly well for vtt files, but will not remove the header.

Similarly for ass files you can use the following command

```bash
find -type f | grep '\.ass$' | xargs cat | sed 's/{.*}//' | awk -F',' '/^Dialogue/ {print $NF}' > out_file
```

The ass file format is a bit more complicated than srt so there may be some
errors.


For html files you can use w3m to convert to plain text

```bash
w3m -dump my_file.html > my_file.txt
```

## Vim extension

There is a vim extension which uses dire\_cli to get a lot of the functionality
of dire in vim. See usage.md for more detail. To use this put dire.vim somewhere
vim/neovim will see it. I have it in ~/.config/nvim/plugin/dire.nvim


## Forvo search

The forvo search is adapted from the migaku dictionary. It supports several
options. See forvo\_search.py for more infomation
