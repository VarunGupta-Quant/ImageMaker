import matplotlib as plt
import numpy as np
# from wordcloud import WordCloud
import tarfile

file = tarfile.open('wordcloud-1.8.1.tar.gz')
file.extractall('wordcloud-extract')
file.close()

print(file)

def genWordcloud(words, m, h, w, font='Sans Serif'):
    cloud = WordCloud(font_path = None, width = w, height = h, mask = m)
    cloud.generate(words)
    
    plt.imshow(cloud, interpolation="bilinear")
    plt.show()

def test():
    text = "square"

    x, y = np.ogrid[:300, :300]

    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)


    wc = WordCloud(background_color="white", repeat=True, mask=mask)
    wc.generate(text)

    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.show()