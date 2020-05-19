import re, os


# https://babaiswiki.fandom.com/wiki/User:TheEmbracedOne/ColorList
pattern="src=\"(.+?\.gif.+?)\""

page = 'ColorList'
paths = []
for l in open(page):
    paths += re.findall(pattern, l)

for p in set(paths):
    if not re.search('data:', p):
        out_name = re.search('\/(.+?\.gif)', p).group(1).split('/')[-1]
        if out_name[:5] == 'Text_':
            out_dir = './sprites/text/'
            out_name = out_name[5:]
        else:
            out_dir = './sprites/icon/'

        out_name = out_name[:-6] + '.gif'
        out_path = out_dir + out_name

        os.system('wget ' + p + ' -O ' + out_path)


