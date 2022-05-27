from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt
import os
import parsing


# Word Cloud

with open(parsing.resfilePath, 'r', encoding='utf-8') as f:
    text = f.read()

okt = Okt()
nouns = okt.nouns(text)

words = [n for n in nouns if len(n) > 1]
c = Counter(words)

# 불용어

stwd = set(STOPWORDS)
# stwd.add('이미지')
# stwd.add('순서')

wc = WordCloud(stopwords=stwd, font_path='Maplestory Light.ttf', width=500, height=500, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(c)
plt.figure()
plt.imshow(gen)

makingWCTitle = ('./' + '%s' % parsing.gallInfo + '.png')
wcPath = ('%s' % makingWCTitle)

wc.to_file('%s' % wcPath)

os.system("pause")