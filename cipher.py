from random import choice

blank = '_'

class Cipher:
    def __init__(self, charset=None):
        self.charset = charset
        self.mapping = dict()

    def gen_blank_map(self, path='map.txt'):
        with open(path, mode='w') as outfile:
            for letter in self.charset:
                outfile.write(f'{letter}:\n')

    def read_mapping(self, path='map.txt'):
        self.mapping = dict()
        with open(path) as infile:
            for line in infile:
                line = line.strip()
                index = line.find(':')
                if index == len(line) - 1:
                    continue
                key = line[:index]
                value = line[index+1:]
                self.mapping.update({key: value})

    def decode(self, enc: str) -> str:
        if self.charset == None:
            raise CipherException('Charset must be defined before decoding.')
        dec_string = ''
        for char in enc:
            if char in self.mapping:
                dec_string += self.mapping[char]
            elif char in self.charset:
                dec_string += blank
            else:
                dec_string += char
        return dec_string

    def encode(self, dec: str) -> str:
        if self.charset == None:
            raise CipherException('Charset must be defined before encoding.')
        encode_map = {v: k for k, v in self.mapping.items()}
        enc_string = ''
        for char in dec:
            if char in encode_map:
                enc_string += encode_map[char]
            else:
                enc_string += char
        return enc_string

    def generate_charset(self, key: str) -> str:
        alphabets = {
            'alpha_low': 'abcdefghijklmnopqrstuvwxyz',
            'alpha_upp': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'numerals': '0123456789',
            'greek_low': 'αβγδεζηθικλμνξοπρστυφχψω',
            'greek_upp': 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ',
            'cyrillic_low': 'абвгдежзийклмнопрстуфхцчшщьюя',
            'cyrillic_upp': 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯ',
            'arabic': 'غظضذخثتشرقصفعسنملكيطحزوهدجبأ',
            'hebrew': 'א‬ב‬ג‬ד‬ה‬ו‬ז‬ח‬ט‬י‬כ‬מ‬נ‬ס‬ע‬פ‬צ‬ק‬ר‬ש‬ת'
            }
        combined = {
            'alpha': alphabets['alpha_upp'] + alphabets['alpha_low'],
            'alphanumeric': alphabets['alpha_upp'] + alphabets['alpha_low'] + alphabets['numerals'],
            'greek': alphabets['greek_upp'] + alphabets['greek_low'],
            'cyrillic': alphabets['cyrillic_upp'] + alphabets['cyrillic_low']
            }

        if key in alphabets:
            self.charset = alphabets[key]
            return
        if key in combined:
            self.charset = combined[key]
            return
        #use key as keyword
        key_alphabets = []
        for alphabet in alphabets:
            for char in key:
                if char in alphabets[alphabet]:
                    if alphabet not in key_alphabets:
                        key_alphabets.append(alphabet)
        charset = key
        for alpha in key_alphabets:
            for char in alphabets[alpha]:
                if char not in key:
                    charset += char
        self.charset = charset

    def generate_mapping(self, path='map.txt'):
        if self.charset == None:
            raise CipherException('Charset must be defined before generating a mapping.')
        chars = list(self.charset)
        self.mapping = dict()
        for char in self.charset:
            value = choice(chars)
            chars.remove(value)
            self.mapping.update({char: value})
        with open(path, 'w') as outfile:
            for char in self.charset:
                if char in self.mapping:
                    outfile.write(f'{char}:{self.mapping[char]}\n')

    def freq_map(self, enc: str, freq_path: str, path='freq.map'):
        ideal_freq = dict()
        with open(freq_path, encoding='utf-8') as freq_file:
            for line in freq_file:
                arr = line.strip().split(':')
                if len(arr) != 2:
                    continue
                ideal_freq.update({arr[0]: float(arr[1])})
        real_freq = dict()
        for char in self.charset:
            real_freq.update({char: enc.count(char)})
        total = sum([v for k,v in real_freq.items()])
        for char in real_freq:
            real_freq[char] = real_freq[char] / total
        sorted_ideal = sorted(ideal_freq.items(), key=lambda kv: kv[1])
        sorted_real = sorted(real_freq.items(), key=lambda kv: kv[1])
        freqmap = dict()
        for i in range(len(sorted_ideal)):
            freqmap.update({sorted_real[i][0]: sorted_ideal[i][0]})
            low = max(0, i-1)
            top = min(len(sorted_real), i+2)
        with open(path, 'w') as outfile:
            for char in self.charset:
                if char in freqmap:
                    outfile.write(f'{char}:{freqmap[char]}\n')

class CipherException(Exception):
    pass

