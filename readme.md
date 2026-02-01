```
  ___   ____ ____      ____ _____  _  _____ ____  
 / _ \ / ___|  _ \    / ___|_   _|/ \|_   _/ ___| 
| | | | |   | |_) |___\___ \ | | / _ \ | | \___ \ 
| |_| | |___|  _ <_____|__) || |/ ___ \| |  ___) |
 \___/ \____|_| \_\   |____/ |_/_/   \_\_| |____/ 
```
# I - Introduction

Let's imagine that you are a small business buying and selling things on Vinted and Leboncoin.
You know that you sell with a better price than you buy but you want to know what is your real
margin. However, you don't necessarily have time to compute your profit yourself because it is
kind of hard to get data from both platforms. 
Let me introduce you, OCR-Stats. A small program that knows how to differentiate a screenshot
from Leboncoin and from Vinted. You just have to take multiple screenshots of all your
transactions for a given period of time, the program will detect if they are purchases or sales
and then apply Image-To-Text (OCR) technology to extract valuable information such as the title
of the transaction and the price associated thus building an Excel-like file with all your 
transactions. You can then generate graphs and summarize your data in just a few clicks !

# II - How to use it 

### Generate statistics

It is very easy to use. You need to put your screenshots in the folder `data/real/` from the
root. And then, launch `python compute_statistics.py`. And voila ! Your `statistics.csv` file
is generated. You can customize where this file is stored and called using the `-o` parameter.
For instance, if I want my file to be stored in `data` and be called `new_statistics.csv` I 
would call `python compute_statistics.py -o ./data/new_statistics.csv`.

### View usefull data

Using the `compute_graphs.py` file, you can compute different kind of statistics such as
profit or turnover.

# III - How to setup

In order to be able to use the python files, you will need to launch 3 commands to install the requirements.
First, you should use `pip install torch torchvision torchaudio`. Then you need to use 
`pip install git+https://github.com/openai/CLIP.git` and finally `pip install -r requirements.txt` to install 
most of the requirements. When done, you are free to use the files.

# IV - How does it work

First, we need to distinguish between Leboncoin and Vinted screenshots. This could be done by 
analysing the color of the background but it is not robust to different phone sizes or 
different application themes. This is why I trained a simple classifier (ANN). I apply
a simple preprocessing strategy which is resizing the image to `(224,224)` such that the
phone size doesn't matter anymore. Then, I will have a `ViT-B/32` pretrained model extract
features from the image thus giving back a vector of length 512. This vector is given to the 
classifier which answer the question "Is it from Leboncoin or from Vinted ?". The inference
pipeline is the same.
With this classifier, now I needed to know if it was a purchase or a sale. To do this, the top
of the screenshot has a more or less highlighted bar depending of the type of the transaction.
I extract a rectangle with the same width as the original photo and with an enough high height
to not depend on the phone size. The last step is just a binarization and a simple count of 
which half has more pixels to one.
Finally, the last step was to extract data. I use the PaddleOCR library which uses the PP-OCR 
technology. The extraction only depends on the plateform and not on the type of transaction.
Therefore, the automatisation was quite straightforward. It remains some extraction error
where text of the previous line is extracted with the current line. But this does not alter
the price-related information which seems to be always right. I set a couple of images in the
`data/real/` folder to let you play with this program ! Enjoy !