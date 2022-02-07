import requests
import re
import base64
import subprocess

'''
This is adapted from the Migaku Dictoinary (GPLv3).
More info here: https://github.com/migaku-official/Migaku-Dictionary-Addon
'''

def decodeURL(url1, url2, protocol, audiohost, server):
    url2 = protocol + "//" + server + "/player-mp3-highHandler.php?path=" + url2;
    url1 = protocol + "//" + audiohost + "/mp3/" + base64.b64decode(url1).decode("utf-8", "strict")
    return url1, url2


def get_forvo_word(word, orig_text):
    url = "https://forvo.com/word/{}/#ja".format(word)
    session = requests.session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
                Gecko/20100101 Firefox/10.0"
        }
    )
    try:
        html = session.get(url).text
    except:
        return None

    audio = re.findall(r'var pronunciations = \[([\w\W\n]*?)\];', html)

    if not audio:
        return None

    audio = audio[0]
    data = re.findall("Japanese" + r'.*?Pronunciation by (?:<a.*?>)?(\w+).*?class="lang_xx"\>(.*?)\<.*?,.*?,.*?,.*?,\'(.+?)\',.*?,.*?,.*?\'(.+?)\'', audio)
    if not data:
        return None
    server = re.search(r"var _SERVER_HOST=\'(.+?)\';", html).group(1)
    audiohost = re.search(r'var _AUDIO_HTTP_HOST=\'(.+?)\';', html).group(1)
    protocol = 'https:'
    urls = []
    for datum in data:
        url1, url2 = decodeURL(datum[2],datum[3],protocol, audiohost, server)
        urls.append([datum[0],datum[1], url1, url2])

    '''
    This will download all of the audio. I am personally not a big fan of this
    but it could be helpful
    for audio_url in urls:
        defaut_audio = session.get(audio_url[2])
        f = open(audio_url[0] + '.mp3', 'wb')
        f.write(defaut_audio.content)
    return ['audio downloaded']
    '''

    '''This will generate a webpage which can be nice
    web_combine = []
    for audio_url in urls:
        web_combine.append(f'<p>{audio_url[0]}</p>')
        web_combine.append(f'<p><a href = "{audio_url[2]}">{audio_url[1]}</a></p>')

    f = open(word + '_audio_results.html', 'w')
    f.write('\n'.join(web_combine))
    f.close()
    subprocess.run(['firefox', word+'_audio_results.html'])
    return ['results in browser']
    '''


    '''This just prints out the results. Works well with vim and a shortcut to
    play audio'''
    result = []
    for audio_url in urls:
        result.append('\n'.join(audio_url))

    return result




