# Word and glyph dictionaries
Dire does not come with any word or glyph dictionaries but it currently supports yomichan
dictionaries, and there are plans to add other dictionary formats later.

The following scripts are provided to help:

|script name|function|
|:---|:---|
|add\_kanji\_dict.py|Adds kanjidict from yomichan to glyphs|
|add\_yomichan\_dict.py|Add a yomichan dictionary to words|


To use these create a folder and have each subfolder of that folder contain the
json files you want to add to the dictionary. It should look something like
this:



add\_yomichan\_dict.py

dicts/

    my_first_dict/

        term_bank_1.json

        term_bank_2.json

        ...

    my_second_dict/

        term_bank_1.json

        ...


Then run the script


# Adding conjugations

Dire does come with a conjugation table (borrowed from yomichan). You can add it
with add\_yomi\_conj\_dict.py. To add conjuations run python
add\_yomi\_conj\_dict.py deinflection.json. If you did not name the file
deinflection.json change it accordingly.


