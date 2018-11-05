import sys
from cipher import Cipher

path = None
if len(sys.argv) == 3:
    path = sys.argv[1]
elif len(sys.argv) != 2:
    print('Provide the path to the encoded message as the first argument.')


c = Cipher()
c.generate_charset('alpha_low')
if path == None:
    path = 'map.txt'
c.read_mapping(path)
with open(sys.argv[1]) as infile:
    message = infile.readline()
print(c.decode(message))
