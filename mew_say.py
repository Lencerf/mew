import subprocess
import sys
import os

def main():   
    print('/'.join(os.path.realpath(__file__).split('/')[:-1]))
    word = sys.argv[1]
    s1 = word[0]
    s3 = ['_', '_', '_']
    s5 = ['_', '_', '_', '_', '_']
    for i, c in zip(range(3), word):
        s3[i] = c
    for i, c in zip(range(5), word):
        s5[i] = c
    path = f"http://dictionary.cambridge.org/media/english/us_pron/{s1}/{''.join(s3)}/{''.join(s5)}/{word}.mp3"
    p = subprocess.Popen(['mpg123', "-q", path,], stderr=subprocess.PIPE)
    _, errs = p.communicate()
    if len(errs) > 0:
        subprocess.Popen(['say', word])

if __name__ == '__main__':
    main()