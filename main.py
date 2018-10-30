from random import choice
from random import shuffle

blank = '_'

def min_function(*args, charset):
    if len(args) != len(charset):
        raise CipherException('A value is required for each char.')
    rounded = [int(g) for g in args]
    mapping = dict()
    for i in range(len(args)):
        mapping.update({charset[i]: charset[rounded[i]]})
    d = decode(mapping)
    print(mapping)
    return chi2test(d, mapping)

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

    def decode(self, enc):
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

    def encode(self, dec):
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

    def generate_charset(self, key):
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
            for k, v in self.mapping.items():
                outfile.write(f'{k}:{v}\n')

    def frequency_analysis(self, encoded, freq_path, outpath='map.txt'):
        fa = FreqAnalysis(self.charset, encoded, freq_path)
        self.mapping = fa.analyze(outpath)




class FreqAnalysis:
    def __init__(self, charset, encoded, freq_path):
        self.charset = charset
        self.ideal_freq = self.load_frequency(freq_path)
        self.e = encoded

    def load_frequency(self, path):
        freq = dict()
        with open(path) as infile:
            for line in infile:
                k, v = line.strip().split(':')
                freq.update({k: float(v)})
        return freq

    def decode(self, mapping=None):
        if mapping == None:
            mapping = self.mapping
        d = ''
        for char in self.e:
            if char in mapping:
                d += mapping[char]
            elif char in self.charset:
                d += blank
            else:
                d += char
        return d

    def chi2test(self, decoded, mapping=None):
        if mapping == None:
            mapping = self.mapping
        max_chi2 = 0
        max_char = self.charset[0]
        sum_chi2 = 0
        total = 0
        for char in decoded:
            if char in self.charset or char == blank:
                total += 1
        for char in self.charset:
            if char not in mapping:
                continue
            observed = decoded.count(char)
            expected = self.ideal_freq[char] * total
            chi2 = (observed - expected)**2 / expected
            print(char, chi2)
            if chi2 > max_chi2:
                max_chi2 = chi2
                max_char = char
            sum_chi2 += chi2
        return sum_chi2, max_char

    def freq_map(self):
        real_freq = dict()
        for char in self.charset:
            real_freq.update({char: self.e.count(char)})
        total = sum([v for k,v in real_freq.items()])
        for char in real_freq:
            real_freq[char] = real_freq[char] / total
        sorted_ideal = sorted(self.ideal_freq.items(), key=lambda kv: kv[1])
        sorted_real = sorted(real_freq.items(), key=lambda kv: kv[1])
        self.mapping = dict()
        for i in range(len(sorted_ideal)):
            self.mapping.update({sorted_real[i][0]: sorted_ideal[i][0]})




    def analyze(self, outpath='map.txt'):
        #find initial mapping based on frequency only
        self.freq_map()
        first_decode = self.decode()
        #print(self.chi2test(first_decode))

        args = (list(range(26)))
        shuffle(args)
        print(args)
        print(min_function(*args, self.charset))




        return dict()

        with open(outpath, 'w') as outfile:
            for char in self.charset:
                outfile.write(f'{char}:{self.mapping[char]}\n')
        return self.mapping


class CipherException(Exception):
    pass


enc = '''jhwabylk zopw av wpyhal ihzl: dl ohcl jhwabylk h zjpluapmpj clzzls pu aol dhalyz ulhy aol svuzkhsl yllm.  aolf hyl zabkfpun zvtl uld zwljplz vm mpzo.  p dvukly pm aolf jhbnoa hufaopun klspjpvbz?
wpyhal ihzl av jhwabylk zopw: nvvk dvyr!  kpylja aol jvbyzl vm fvby zopw avdhykz tlpauly pzshuk huk wpjr bw zvtl jvjvubaz aolyl mvy kpuuly avupnoa.  adluaf vm aolt zovbsk il luvbno.
jhwabylk zopw av wpyhal ihzl: dl nva svza olhkpun av tlpauly pzshuk huk dlua aol vwwvzpal kpyljapvu puzalhk, av ovwwly pzshuk.  hdhpapun mbyaoly puzaybjapvuz.  dl hszv zhd h nyvbw vm dohslz.  aol zjpluapzaz zhpk pa pz jhsslk h ‘wvk.’
wpyhal ihzl av jhwabylk zopw: dlss, zpujl fvb dlua aol dyvun dhf, fvb tpnoa hz dlss nv vu av lttf uvlaoly pzshuk.  aolyl hyl zvtl upjl thunvlz vcly aolyl mvy fvb av wpjr huk iypun ihjr.
jhwabylk zopw av wpyhal ihzl: p aovbnoa zvtlvul dhz hsslynpj av thunvlz... iba fvb hyl aol ivzz.  hufdhfz, pa pz upjl av ohcl aolzl zjpluapzaz av rllw bz jvtwhuf.  pa dhz nlaapun svulsf dhpapun hss aolzl flhyz vba pu aopz klzlyalk wshjl mvy zvtlivkf dl jvbsk rpkuhw.  dl hyl jbyyluasf uvyaolhza vm lttf uvlaoly pzshuk.
wpyhal ihzl av jhwabylk zopw: aoha pz nylha aoha fvb thkl zvtl uld myplukz.  wslhzl jvtl ihjr mvy kpuuly aovbno.  dl hyl nlaapun obunyf olyl.  aol wpyhal zald pz wpwpun ova.
jhwabylk zopw av wpyhal ihzl: dl dvbsk svcl av jvtl ihjr mvy kpuuly, iba aolyl pz h zspnoa wyvislt.  dl nva h ipa avv lejpalk dolu dl jhwabylk aol zopw huk dl aoyld aol leayh mbls vclyivhyk.  uvd dl ohcl ybu vba vm nhz huk hyl msvhapun hyvbuk hptslzzsf.  wslhzl zluk olsw.  vby jbyylua svjhapvu pz aol zaypjrshuk zvbuk.
wpyhal ihzl av jhwabylk zopw: nylha dvyr, nbfz!  (p ovwl aoha zhyjhzt jhu il ayhuztpaalk vcly aol yhkpv).  dl hyl zlukpun vba h zthss tvavyivha av iypun fvb leayh mbls.  dl hyl nvpun av zahya lhapun kpuuly dpaovba fvb.  pa pz zptwsf avv svun av dhpa, huk dl dhua wsluaf vm aptl slma mvy klzzlya.  vy pz pa klzlya?  p jhu ulcly yltltily ovd av zwlss aoha vul.
jhwabylk zopw av wpyhal ihzl: aol ylzjbl ivha hyypclkhuk dl nva aol mbls aoha dl ullklk.  dl hyl vu aol dhf ihjr av ihzl huk hyl kyvwwpun hujovy pu aol thaolthapjphu’z jvcl.  slhcl zvtl mvvk mvy bz!
'''
c = Cipher()
c.generate_charset('alpha_low')
c.frequency_analysis(enc, 'frequencies/english.freq')
#print(c.decode(enc))
