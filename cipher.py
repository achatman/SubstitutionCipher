from random import choice

class Cipher:
    """
    A class used to contain a monoalphabetic cipher.

    Attributes
    ----------
    blank : char
        a character to be used in decoding when the mapping is not complete
    charset : str
        a string containing allowed characters in the cipher
    mapping : dict
        a dictionary that represents a map from the encoded alphabet to the normal alphabet

    Methods
    -------
    gen_blank_map(path='map.txt')
        writes a blank map to the path provided using this Cipher's charset
    read_mapping(path='map.txt')
        takes in the file specified at path and stores it in this Cipher's mapping. The file should be a series of lines in the form: <Encoded letter>:<Decoded letter>
    decode(enc)
        takes an string enc and returns a decoded string according to this Cipher's charset
    encode(dec)
        takes a string dec and returns an encoded string according to this Cipher's charset
    generate_charset(key)
        takes a key and sets this Cipher's charset to the corresponding charset.
    generate_mapping(path='map.txt')
        generates a map over the current charset. The new map is set as this Cipher's mapping as well as output to the file specified in path.
    freq_map(enc, freq_path, path='freq.map')
        uses a basic frequency analysis to generate a mapping. The language frequencies are read from freq_path. The encoded frequencies are read from the string enc. The generated mapping is set to this Cipher's mapping and also output to path.
    """

    def __init__(self, blank_char='_'):
        """
        Initializes a Cipher object with empty charset and mapping.

        Parameters
        ----------
        blank_char : char, optional
            Character to be used as the default decoding.
        """
        self.blank = blank_char
        self.charset = ''
        self.mapping = dict()

    def gen_blank_map(self, path='map.txt'):
        """
        Outputs a blank map based off self.charset to path.

        Parameters
        ----------
        path : str, optional
            Path to output the blank map to. Defaults to 'map.txt'.
        """

        with open(path, mode='w') as outfile:
            for letter in self.charset:
                outfile.write(f'{letter}:\n')

    def read_mapping(self, path='map.txt'):
        """
        Reads the file at path to fill self.mapping. The file should be a list of relations of the form:
        <Encoded letter>:<Decoded letter>
        For a charset consisting of lower case Latin letters, this may look like:
        a:d
        b:c
        c:
        d:g
        ...
        z:q
        Note that in this example 'c' was not given a value in the map. Characters without a value will be decoded to self.blank.

        Parameters
        ----------
        path : str, optional
            Path to read the mapping from. Defaults to 'map.txt'.
        """

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
        """
        Decodes the string enc using self.mapping and returns the decoded string.

        Parameters
        ----------
        enc : str
            Encoded string to be decoded.

        Returns
        -------
        The decoded version of enc, by self.mapping.

        Raises
        ------
        CipherException
            If the current charset is None.
        """

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
        """
        Encodes the string dec using self.mapping and returns the encoded string.

        Parameters
        ----------
        dec : str
            String to be encoded.

        Returns
        -------
        The encoded version of dec, by self.mapping.

        Raises
        ------
        CipherException
            If the current charset is None.
        """

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
        """
        Sets self.charset based on the provided key. Available alphabets are: latin (alpha), greek, cyrillic, arabic, and hebrew. If an alphabet has upper and lower case characters, the charset will be upper followed by lower. A single case can be retrieved by appending '_low' or '_up' for lower or upper case, respectively. If the key parameter does not correspond to a provided charset, the key will be used as the basis for the charset (minus repeats). The rest of the alphabet will be appended in order, minus the charaters from the key. For example, for the key 'hello', the charset will be: 'heloabcdfgijkmnpqrstuvwxyz'.

        Parameters
        ----------
        key : str
            Selects a charset.
        """

        alphabets = {
            'alpha_low': 'abcdefghijklmnopqrstuvwxyz',
            'alpha_up': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'numerals': '0123456789',
            'greek_low': 'αβγδεζηθικλμνξοπρστυφχψω',
            'greek_up': 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ',
            'cyrillic_low': 'абвгдежзийклмнопрстуфхцчшщьюя',
            'cyrillic_up': 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯ',
            'arabic': 'غظضذخثتشرقصفعسنملكيطحزوهدجبأ',
            'hebrew': 'א‬ב‬ג‬ד‬ה‬ו‬ז‬ח‬ט‬י‬כ‬מ‬נ‬ס‬ע‬פ‬צ‬ק‬ר‬ש‬ת'
            }
        combined = {
            'alpha': alphabets['alpha_up'] + alphabets['alpha_low'],
            'alphanumeric': alphabets['alpha_up'] + alphabets['alpha_low'] + alphabets['numerals'],
            'greek': alphabets['greek_up'] + alphabets['greek_low'],
            'cyrillic': alphabets['cyrillic_up'] + alphabets['cyrillic_low'],
            'latin_low' : alphabets['alpha_low'],
            'latin_up' : alphabets['alpha_up'],
            'latin' : alphabets['alpha_up'] + alphabets['alpha_low']
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
        charset = ''.join(sorted(set(key), key=key.index))
        for alpha in key_alphabets:
            for char in alphabets[alpha]:
                if char not in key:
                    charset += char
        self.charset = charset

    def generate_mapping(self, path='map.txt'):
        """
        Creates a random mapping from the current charset. The new mapping is output to path and also saved to self.mapping.

        Parameters
        ----------
        path : str, optional
            Path to output the new mapping to. Defaults to 'map.txt'.

        Raises
        ------
        CipherException
            If the current charset is None.
        """

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
        """
        The file at freq_path should be a list of ideal frequencies based on the language. This file is a similar form to the map files, except with a double, i.e.
        a:0.0812
        b:0.0149
        ...
        z:0.0007
        The encoded frequencies are calculated from the input string enc. The frequency analysis orders encoded characters to decoded letters by ordering by frequency. This is a fairly primitive approach and should not be considered reliable. If the string enc is fairly representative of the language (i.e. of sufficient size and written with normal semantics), the most common letters are often correctly mapped.

        After the mapping is created, it is written to the file at path and stored in self.mapping.

        Parameters
        ----------
        enc : str
            Encoded string from which to calculate real frequencies.
        freq_path : str
            Path to read ideal frequencies from.
        path : str, optional
            Path to output the mapping to. Defaults to 'freq.map'.
        """

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
        self.mapping = freqmap

class CipherException(Exception):
    pass

