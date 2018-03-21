import yaml
import sys

word_text = ""

filename = sys.argv[1]
list_name = filename.split("/").pop()

with open(sys.argv[1], 'r') as f:
    word_text = f.read()

word_list = {}

for line in word_text.split('\n'):
    wm = list(filter(lambda s:len(s)>0, line.split(' ')))
    if len(wm) < 2:
        continue
    word_list[wm[0]] = {
        'f':1,
        'm':wm[1:],
        'h':1
    }
print(yaml.dump({list_name:word_list}, allow_unicode=True)) 
