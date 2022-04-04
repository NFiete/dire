#!/bin/sh

set -e

jm_url='https://github.com/FooSoft/yomichan/raw/master/dl/dict/jmdict_english.zip'
kanji_url='https://github.com/FooSoft/yomichan/raw/master/dl/dict/kanjidic_english.zip'
if [ ! -d ./converters/dicts ]; then
	mkdir ./converters/dicts
fi
if [ ! -d ./converters/kanji_dicts ];then
	mkdir ./converters/kanji_dicts
fi
wget "$jm_url" -O ./jm.zip
wget "$kanji_url" -O ./kanji.zip
if [ ! -d ./converters/dicts/jm ];then
	mkdir ./converters/dicts/jm
fi
if [ ! -d ./converters/dicts/kanji_dicts/kanji];then
	 mkdir ./converters/kanji_dicts/kanji
fi
unzip jm.zip -d ./converters/dicts/jm
unzip kanji.zip -d ./converters/kanji_dicts/kanji
python3 ./converters/add_yomichan_dict.py ./converters/dicts
python3 ./converters/add_kanji_dict.py ./converters/kanji_dicts
python3 ./converters/add_yomi_conj_dict.py ./converters/deinflect.json
sudo ln -s "$(pwd)/main.py" /usr/bin/dire
sudo ln -s "$(pwd)/dire_send_text.py" /usr/bin/dire_send_text
sudo ln -s "$(pwd)/dire_cli" /usr/bin/dire_cli
if [ ! -d /usr/share/dire ];then
	sudo mkdir /usr/share/dire
fi
sudo cp default_config.py /usr/share/dire/config.py
