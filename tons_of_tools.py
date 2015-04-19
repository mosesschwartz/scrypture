from boltons import strutils
def bytes_to_human(bytes):
    '''Turns an integer value of nbytes into a human readable format'''
    try:
        b = int(bytes)
    except:
        b = 0
    return strutils.bytes2human(b)

print bytes_to_human(128991)
print bytes_to_human(100001221)

from boltons import strutils
def camelcase_to_underscores(s):
    '''Converts a camelcased string to underscores'''
    return strutils.camel2under(s)

print camelcase_to_underscores('CamelCaseTest')

def text_to_upper(s):
    '''Converts a string to all upper case'''
    return s.upper()
print text_to_upper('upper')

def text_to_lower(s):
    '''Converts a string to all lower case'''
    return s.lower()
print text_to_lower('LOWER')

def reverse_characters(s):
    '''Reverse the characters in a string'''
    s =''.join(reversed(s))
    return s
print reverse_characters('Reverse')

def reverse_words(s):
    '''Reverse the words in a string (space delimeted)'''
    s =' '.join(reversed(s.split(' ')))
    return s
print reverse_words('This is a sentence.')

import random
def shuffle_characters(s):
    '''Randomly shuffle the characters in a string'''
    s = list(s)
    random.shuffle(s)
    s =''.join(s)
    return s
print shuffle_characters('Shuffle characters')

import random
def shuffle_words(s):
    '''Randomly shuffle the words in a string (space delimeted)'''
    s = s.split(' ')
    random.shuffle(s)
    s =' '.join(s)
    return s
print shuffle_words('This is a sentence and maybe shuffled.')

import json
def json_pretty_print(s):
    s = json.loads(s)
    return json.dumps(s, 
                      sort_keys=True,
                      indent=4, 
                      separators=(',', ': '))
print json_pretty_print('{"4": 5, "6": 7}')

def uniq(lines):
    '''eliminate duplicate lines, like `uniq`'''
    lines = [l.strip() for l in lines.split('\n')
             if l != '']
    lines = list(set(lines))
    return lines
print uniq('Hello\n\nHello\n\n\n\nThe\nEnd')

import jsbeautifier
def javascript_pretty_print(js):
    '''Runs jsbeautifier on inputted Javascript strings'''
    return jsbeautifier.beautify(js)
print javascript_pretty_print('var a = 4; var b = [1,2,3];')


TODO = '''
NERTWORKY
  whois
  ipwhois

REVERSEY
  strings
  peinfo
  swf decompile
  binwalk

Texty
  That Markdown conversion tool?
  Password gen? XKCD?

Programmy
Linters?
pep8 formatter
'''
















