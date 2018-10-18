#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import pyttsx
# speak = pyttsx.init()
# voices = speak.getProperty('voices')
# for voice in voices:
#     print(voice.id, voice.age, voice.gender, voice.languages, voice.name)
# speak.setProperty('voice', 'spanish')
# # while True:
#     # phrase = str(input("Enter a text\n"))
#
# speak.say('En un lugar de la Mancha, de cuyo nombre no quiero acordarme, ')
# speak.runAndWait()

# import requests
#
# import copy
# from urllib import urlencode
# syn_parameters = {
#     'text': '',
#     'voice': 'es-ES_EnriqueVoice',
#     'download': 'true',
#     # 'accept': 'audio%2Fmp3'
# }
#
#
# def main():
#     # Get the text
#     text = raw_input('Text: ')
#     print text
#     # Synthesize it
#     s = synthesize(text)
#
#     # Write it to a `f.ogg` file, overwriting it if it exists
#     with open('f.mp3', 'wb+') as f:
#         f.write(s.content)
#
#
# def synthesize(text):
#     # Don't modify the original object
#     parameters = copy.copy(syn_parameters)
#
#     # Set the text
#     parameters['text'] = text
#
#     # Request foo!
#     print 'https://text-to-speech-demo.ng.bluemix.net/api/synthesize?' + urlencode(parameters ) + '&accept=audio%2Fmp3'
#     r = requests.get('https://text-to-speech-demo.ng.bluemix.net/api/synthesize?' + urlencode(parameters) +'&accept=audio%2Fmp3')
#     # 'https://text-to-speech-demo.mybluemix.net/api/synthesize?download=true&text=hola&voice=es-ES_EnriqueVoice&accept=audio%252Fmp3' \
#     # 'https://text-to-speech-demo.ng.bluemix.net/api/synthesize?text=hola&voice=es-ES_EnriqueVoice&download=true&accept=audio%2Fmp3'
#     return r
#
#
# if __name__ == '__main__':
#     # watsontts was called directly
#     main()

import epitran
epi = epitran.Epitran('spa-Latn')
print epi.trans_list(u'cesa')
