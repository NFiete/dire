All configuration is done in config.py. The defaults should be in /usr/share/dire/config.py. For your own configuration copy /usr/share/dire/config.py to ~/.config/dire/config.py


Currently there is only one supported option which controls the order of the
dictionaries in the output. This is a python dictionary of dictionary names to
rank. For example if you have two dictionaries 'foo' and 'bar', and want foo to
come before bar you would write

dict\_order = {'foo': 0, 'bar': 1}
