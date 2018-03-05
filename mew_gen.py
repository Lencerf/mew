import yaml

word_text = '''ansatz 假设
enzyme 酶'''

list_name = 'list1'

word_list = {}

for line in word_text.split('\n'):
    wm = line.split(' ')
    word_list[wm[0]] = {
        'f':1,
        'm':wm[1:]
    }
print(yaml.dump({list_name:word_list}, allow_unicode=True)) 
