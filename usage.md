There are currently three interfaces for dire. A gtk3 interface, a cli tool, and a neovim
plugin. If you do not have a preference
between these the gtk3 version is likely best for you.
Usage between them is largely similar but differs in some ways.


# Gtk3

## Basic Usage
To launch the gtk3 version you can use dire -n \<NAME\> \<FILE NAME\> to open
the file with FILE NAME and the dire session will be named NAME. If you omit
NAME a name will be randomly chosen. Alternatively you can use dire -s \<SEARCH\> to search the term in search. dire -t \<TEXT\> will open dire with the desired text.

From here you will see the text from the file you opened. You can move the
cursor using the arrow keys, mouse, or using a subset of the vi keybindings
(full list of keybindings below). There is currently no way to customize
keybindings but it is planned.

|Key|Action|
|:--- |:---|
|a|Lookup word after cursor|
|q|Get list of possible words after cursor|
|e|Lookup current line|
|s|Create a search box. Will search similar to pressing a|
|d|Search definition|
|r|Search with globing. Supports * and ? (more detail below)|
|m+key|Create a mark with the name of the next key|
|'+key|Jump to mark with name key|
|g|Jump to beginning of text|
|G|Jump to end of text|
|-|Decrease font size|
|+|Increae font size|
|w|Jump forward to next non-kana character (only functional for Japanese)|
|b|Jump back (only functional for Japanese)|
|arrow keys|Allow movement in text|
|hjkl|Similar to vi|
|i|allow editing of text|
|Escape|Disable editing|
|slash|Get text to search forward in the text|
|n|Jump to next match for text search|
|N|Jump to previous match for text search|
|H|Back in history|
|L|Forward in history|
|J|Jump to next definition|
|K|Jump to previous definition|
|f|Jump to next result|
|F|Jump to previous result|
|z|Scroll so cursor is at the center of the screen|
|t|Scroll so cursor is at the top of the screen|
|y|Copy definition (requires xclip. This should hopefully be improved soon.)|
|p|Search clipboard (also needs xclip)|
|c|Create flashcard (see more detail below)|
|[|Decrease the margin size|
|]|Increase the margin size|


## Creating flashcards

Dire can automatically create flashcards from text. By default the flashcards
are made to work well with anki though this can be easily customized if you use
another flash card program. By default flashcards are created with a sentence on
the front and definitions, and context on the back. This can also be customized.
By default, flashcards are stored in a csv file which can easily be imported
into anki. For more detail see [contig.md](config.md).

## Extending

### Custom searches

Dire supports the ability to define your own searches in config.py. These custom
searches are treated just like dictionaries (see config.md for more detail).
These are a few examples in extensions/. For more detail see config.md.

### dire\_send\_text

You can use dire\_send\_text -t \<TYPE\> \<NAME\> \<TEXT\> to send TEXT to the dire
instance with the specified NAME. The -t argument is optional. The possible
types as s for set, p for push and a for append. s will have the default
behavior of setting the text to NAME. p will put the text at the beginning but
will not delete existing text. a will add TEXT to the end but will not overwrite
any text.


### Usage with mpv

We provide a mpv extension located as extensions/mpv\_dire.lua. Move this into
~/.config/mpv/scripts/ and then when a video is playing you can press 'd' and it
will try to send text to a dire instance named video.


We also support automatic flash card creation. To set this up
move extensions/mpv\_select\_text.py To ~/.config/mpv/scripts/ and make sure you
have ffmpeg and imagemagick installed (if you are using linux there is a very
high probability these are already installed). Additionally the script makes the
assumption your Anki user is called 'User 1' (this is the default). If it is not
make sure to change the media variable the beginning of the script.

To create an Anki card press 'c' and a prompt will come up. Select the character
you want to start lookup at and the flashcard will be created with a screenshot
and audio in the context. For example if the prompt says '吾[0]輩[1]は[2]猫[3]で[4]あ[5]る[6]' and you want to create a flashcard for 猫 then you would type in '3' and hit enter.


# Neovim

We provide a neovim plugin in extensions/dire.vim. The neovim plugin creates the
following functions:

|Function|What it does|
|:--- |:---|
|DireLookup|Looks up the text under the cursor. Opens it in a split.|
|DireSearchLine|Looks up the current line. Opens in a split|
|DireSearch|Prompts the user to type in a word to lookup|
|DireGlob|Prompts the user for a glob search|
|DireDefinitionSearch|Search the definition of words|

This does not create any keybindings. Currently both vim and neovim are
supported but this may change in the future.


# dire\_cli

dire\_cli is a pure cli tool. To search a word type dire\_cli \<WORD\>. It will
be intelligent in the search like pressing 'a' in the gtk version. You can pass
in the -g flag to search globbing, -d to search definition, and the -q flag to list possibilities.

If you use the -c flag you can create a flashcard using the settings in
config.py. The arguments are dire\_cli -c \<TERM\> \<SENTENCE\> \<CONTEXT\>,
were term starts with the word you want to look up (it can be conjugated and
there can be words following it like there is when using dire).


# Glob searching
Dire supports glob searching. This works like GLOB in sqlite. What this does is
it means '?' can represent a character you do not know, and '\*' represents
any set of characters. For example '?at' would match 'bat', and 'cat' (and some
other words), and '\*at' would match 'at', 'bat', 'cat', 'that', 'what',
'combat' and some other words.
