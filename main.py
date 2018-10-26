

default_charset = 'abcdefghijklmnopqrstuvwxyz'


class Cipher:
    def __init__(self, charset, enc_message):
        self.charset = charset
        self.enc = enc_message
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

    def decode(self):
        dec_string = ''
        for char in self.enc:
            if char in self.mapping:
                dec_string += self.mapping[char]
            elif char in self.charset:
                dec_string += '_'
            else:
                dec_string += char
        return dec_string
