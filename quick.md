# Dependencies

You need to install dependencies yourself. Install gtk3, python, and sqlite. This
will be different depending on what operating system you are using

# Setup

For unix systems (like macos, linux, bsd etc.) we provide a quick install script that will get everything
setup with jm dict and kanjidict. To get this set up

* Download the software from releases.
* Decompress it in a location you don't mind keeping it.
* Open a terminal in the location you downloaded it.
* run sh quick\_setup.sh. You may be prompted for your password
* open a new terminal and type dire. The program should launch

The quick install creates links in /usr/bin/ to wherever you downloaded the
software so if you move it you will need to re-run the script. If the program
did not launch you are likely missing a dependecy. Make sure you have installed
gtk3, python, and sqlite.


# Every command you need to run

Here is every command you need to run. You can copy and paste these into your
terminal.

* mkdir .dire\_store
* cd .dire\_store
* (insert download command)
* tar -xvf (name)
* cd dire
* sudo sh quick\_setup.sh
