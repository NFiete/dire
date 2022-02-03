# Dependencies

You need to install dependencies yourself. Install gtk3, python3, and sqlite3. This
will be different depending on what operating system you are using. These are
all fairly common so there is a decent chance you already have them installed.
Additionally to run the setup script you will need wget and unzip. These are
also fairly common.

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
did not launch you are likely missing a dependency. Make sure you have installed
gtk3, python3, and sqlite3.


# Every command you need to run

Here is every command you need to run. You can copy and paste these into your
terminal.

* mkdir .dire\_store
* cd .dire\_store
* wget "https://github.com/NFiete/dire/releases/download/v0.1.0/dire-0.1.0.tar.gz"
* tar -xvf tar xvf dire-0.1.0.tar.gz
* sh quick\_setup.sh
