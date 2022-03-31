All configuration is done in config.py. The defaults should be in /usr/share/dire/config.py. For your own configuration copy /usr/share/dire/config.py to ~/.config/dire/config.py


# Dictionary order

To control dictionary order there is a python dictionary.
For example if you have two dictionaries 'foo' and 'bar', and want foo to
come before bar you would write

```python
dict_order = {'foo': 0, 'bar': 1}
```

If you do not care about order you can leave it as None

```python
dict_order = None
```


# Removing dictionaries

If you do not want a dictionary to show up in results remove it from the
dictionary. For example if you do not want results from 'foo', but do want
results from 'bar' you would write

```python
dict_order = {'bar': 1}
```

# Custom searches

It is possible do define your own search functions. In extensionts/ there is a
function that can search for example sentences, and one that searches forvo (the forvo one is adapted from the Migaku dictionary).

All search functions are given two arguments, the first is what the program
believes the word to be and the second is the original text. For example, the
first might be 'to walk' and the original may be 'walked'. For Japanese an
example could be '面白い' and 'おもしろかった'.

Search functions return a list of strings or None. If None is returned nothing
will be displayed in results.

There are two kinds of custom searches: user\_defined\_searches and
user\_possible\_searches.

## user\_defined\_searches

Functions in user\_defined\_searches will only search if there are any results
from searching normally. For example if you were to search 'hjkl', but 'hjkl'
was not in the dictionary then there would be no searches performed by any
user\_defined\_searches.

For example, if I wanted to just print out the word and the original form I
might have this in my config.py


```python
def foo(word, orig):
	return [word, orig]

user_defined_searches = [foo]

dict_order = {'foo': 0}
```


## user\_possible\_searches

user\_possible\_searches will run even if no word has been found. Functions in
user\_possible\_searches will take two arguments. Both will be the same string
(this is done so you can switch methods between user\_possible\_searches and
user\_defined\_searches). Both will be the raw text being looked up, and it will
run for every possible length. So if the original text were 'very happy' then
the functions in user\_possible\_searches would run for 'very happy', 'very
happ', 'very hap', etc.

For example, if you want 'bar' to display no matter what you search you could
put the following in config.py


```python
def foo(word, word):
	return ['bar']

user_possible_searches = [foo]

dict_order = {'foo': 0}
```

I recommend you do not use this.


For additional details on custom searches see extensions/


# Custom keybindings

You can change keybindings by editing their values in a python dictionary. This
only applies to the gtk3 interface. The key names are those used by gtk3.


# Other options

## defn\_seperator

This will print out before each definition

## result\_sperator

This will print out before each result

## copy\_command
This command should copy stdin to the clipboard

## paste\_command
This command should print the contents of the clipboard to stdout

## width
Default window width

## height
Default window height

## font\_size
Default font size

## card\_starts

When creating a flashcard dire will select text to send as the third argument.
The entries in card\_starts are characters where the search should stop going to
the left. For example, if card\_starts were ['('] and I were to create a card in
the text "(This is a example sentence)" Then the sentence sent would start with
"(This is...".

## card\_ends

Similar to card\_starts except going to the right. For example, if card\_ends
were [')'] then "(This is a example sentence)" would select text ending with
"...sentence)".


## context\_starts

When creating a flashcard dire will select text to send as the fourth argument.
The entries in context\_starts are characters where the search should stop going to
the left. For example, if context\_starts were ['('] and I were to create a card in
the text "(This is a example context)" Then the context sent would start with
"(This is...".


## context\_ends

Similar to context\_starts except going to the right. For example, if context\_ends
were [')'] then "(This is a example context)" would select text ending with
"...context)".


## make\_card
This function will be called when creating a flashcard. It is sent four
arguments:

|Arg|Description|
|:--- |:--- |
|words|A list of possible words. Words are in the order they are in when looking up a word|
|defns|A list of possible definitions. Each element of a defns is a list of definitions for the given word. The order of the words is the same as that in words.|
|sentence|The sentence as selected by finding text which starts with a element of card\_starts, and ending with a element of card\_ends|
|context|The context as selected by finding text which starts with a element of context\_starts, and ending with a element of context\_ends|


## max\_word\_length

The maximum length to scan for a word. The bigger this is the more accurate the
results will be, but it will be slower.

## min\_context\_left

The minimum number of characters to scan left when grabbing context

## min\_context\_right

The minimum number of characters to scan right when grabbing context

## max\_context\_left

The maximum number of characters to scan right when grabbing context. Set to
None to scan to the end of the document.

## min\_sentance\_left

The minimum number of characters to scan left when grabbing sentance

## min\_sentance\_right

The minimum number of characters to scan right when grabbing sentance

## max\_sentance\_left

The maximum number of characters to scan right when grabbing sentance. Set to
None to scan to the end of the document.

## defaut\_margin

The default margin size
