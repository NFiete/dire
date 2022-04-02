#!/bin/sh

set -e

jm_url='https://foosoft.net/projects/yomichan/dl/dict/jmdict_english.zip'
kanji_url='https://foosoft.net/projects/yomichan/dl/dict/kanjidic_english.zip'
mkdir ./converters/dicts
mkdir ./converters/kanji_dicts
wget "$jm_url" -O ./jm.zip
wget "$kanji_url" -O ./kanji.zip
mkdir ./converters/dicts/jm
mkdir ./converters/kanji_dicts/kanji
unzip jm.zip -d ./converters/dicts/jm
unzip kanji.zip -d ./converters/kanji_dicts/kanji
python3 ./converters/add_yomichan_dict.py ./converters/dicts
python3 ./converters/add_kanji_dict.py ./converters/kanji_dicts
python3 ./converters/add_yomi_conj_dict.py ./converters/deinflect.json
sudo ln -s "$(pwd)/main.py" /usr/bin/dire
sudo ln -s "$(pwd)/dire_send_text.py" /usr/bin/dire_send_text
sudo ln -s "$(pwd)/dire_cli" /usr/bin/dire_cli
sudo mkdir /usr/share/dire
sudo cp default_config.py /usr/share/dire/config.py
