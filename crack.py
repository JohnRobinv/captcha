#-*- coding:utf8 -*-
from PIL import Image
import hashlib
import time
import math
import os
im = Image.open('captcha.gif')

im_new = Image.new('P',im.size,255)
# print(im.size)

for y in range(im.size[1]):
    for x in range(im.size[0]):
        pix = im.getpixel((x,y))
        if pix == 220 or pix == 227:
            im_new.putpixel((x,y),0)

inletter = False
foundletter = False

start = 0
end = 0
letters = []
for x in range(im_new.size[0]):
    for y in range(im_new.size[1]):
        pix = im_new.getpixel((x,y))
        if pix != 255 :
            inletter = True

    if foundletter == False and inletter == True:
        foundletter = True
        start = x
    if foundletter == True and inletter == False:
        foundletter = False
        end = x

        letters.append((start,end))

    inletter = False
# print(letters)



class VectorCompare:
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count**2
        return  math.sqrt(total)
    def relation(self,concordance1,concordance2):
        relevance = 0
        topvalue = 0
        for word,count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]

        return topvalue/ (self.magnitude(concordance1)*self.magnitude(concordance2))

def buildvector(im):
        d1 = {}
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
        return d1
v = VectorCompare()
iconset = list('0123456789abcdefghijklmnopqrstuvwxyz')

imageset = []
for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if img!= "Thumbs.db" and img!= ".DS_Store":
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})

# count = 0
# for letter in letters:
#     m = hashlib.md5()
#     im_new_c = im_new.crop((letter[0],0,letter[1],im_new.size[1]))
#     keyy = "%s%s"%(time.time(),count)
#     keyy = keyy.encode('utf8')
#     m.update(keyy)
#     im_new_c.save("./%s.gif"%(m.hexdigest()))
#     count += 1
count = 0
for letter in letters:
    m = hashlib.md5()
    im_new_c = im_new.crop((letter[0],0,letter[1],im_new.size[1]))

    guess= []

    for img in imageset:
        for x,y in img.items():
            if len(y)!=0:
                guess.append((v.relation(y[0],buildvector(im_new_c)),x))
    guess.sort(reverse=True)
    print("",guess[0])
    count+=1




#
# im1=im.histogram()
# print(im1)
# im.convert("P")
# im.save('captcha_8bit.gif')
# im2=im.histogram()
# print(im2)
#
# values = {}
# for i in range(256):
#     values[i] = im2[i]
# for j,k in sorted(values.items(),key=lambda x:x[1],reverse = True)[:10]:
#     print(j,k)
#
