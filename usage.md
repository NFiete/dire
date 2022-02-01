There are currently three interfaces for dire. A gtk3 interface, a cli tool, and a neovim
plugin. If you do not have a preference
between these the gtk3 version is likely best for you.
Usage between them is largely similar but differs in some ways.


# Gtk3

## Basic Usage
To launch the gtk3 version you can use dire -n \<NAME\> \<FILE NAME\> to open
the file with FILE NAME and the dire session will be named NAME. If you omit
NAME a name will be randomly chosen.

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

## Extending

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


### how dire\_send\_text works
NOTE: This starts with some kind of technical stuff if you don't care how it
works (ie you are not trying to write your own client program) then you can skip
ahead.

When launched a socket will be created in ~/.config/dire/sockets/ with the name
of the current dire instance. When you write to the socket the gtk verison will
read the first character and look for 's', 'a', or 'p'. It will then take the
corresponding action described in dire\_send\_text using the rest of the string
as the text. If none of those are found it will set the text.


# Neovim

We provide a neovim plugin in extensions/dire.vim. The neovim plugin creates the
following functions:

|Function|What it does|
|:--- |:---|
|DireLookup|Looks up the text under the cursor. Opens it in a split.|
|DireSearchLine|Looks up the current line. Opens in a split|
|DireSearch|Prompts the user to type in a word to lookup|
|DireGlob|Prompts the user for a glob search|

This does not create any keybindings. Currently both vim and neovim are
supported but this may change in the future.


# dire\_cli

dire\_cli is a pure cli tool. To search a word type dire\_cli \<WORD\>. It will
be intelligent in the search like pressing 'a' in the gtk version. You can pass
in the -g flag to search globbing, and the -q flag to list possibilities.


# Glob searching
Dire supports glob searching. This works like GLOB in sqlite. What this does is
it means '?' can represent a character you do not know, and '\*' represents
any set of characters. For example '?at' would match 'bat', and 'cat' (and some
other words), and '\*at' would match 'at', 'bat', 'cat', 'that', 'what',
'combat' and some other words.
