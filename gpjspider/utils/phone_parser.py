# -*- coding: utf-8 -*-
import re
import StringIO
from PIL import Image
from pytesseract import image_to_string
from urllib2 import urlopen, Request


class ConvertPhonePic2Num(object):

    """
# >>> ConvertPhonePic2Num('http://sh.ganji.com/tel_img/?c=k92L68WOXwcdZlbkfF5p-zJhzdzyQ__PtQyX').find_possible_num()
# ('13166118115', 0.99)
# >>> ConvertPhonePic2Num('http://nj.ganji.com/tel_img/?c=kh3LK8CCBrmcz9g90dTSiHLan.-6g__PtQyX').find_possible_num()
# ('1367555', 0.9)

>>> ConvertPhonePic2Num('http://www.che168.com/handler/CarDetail_v3/GetLinkPhone.ashx?infoId=4761577&linkType=2').find_possible_num()
('13564779931', 0.99)
>>> ConvertPhonePic2Num('http://cache.taoche.com/buycar/gettel.ashx?u=5730860&t=ciggmcamamm').find_possible_num()
('15339109099', 0.99)
    """

    def __init__(self, picurl):
        self.picurl = picurl

    def convert_remote_pic2num(self):
        im = urlopen(Request(self.picurl)).read()
        imob = Image.open(StringIO.StringIO(im))
        imob = imob.convert('RGB')
        # TODO: 在调用pytesser之前处理一下图片，如把挨得紧密的数字分开，可以提高识别的准确率,需要研究PIL库
        text = image_to_string(imob)
        return text

    def replace_similar_char2num(self):
        # 形状相似的数字和字母映射.
        similar = (('O', '0'), ('o', '0'), ('D', '0'), ('a', '0'), ('L', '1'), ('!', '1'),
                   ('|', '1'), ('l', '1'), ('I', '1'), ('Z', '2'), ('z', '2'), ('A', '4'),
                   ('S', '5'), ('s', '5'), ('b', '6'), ('T', '7'), ('B', '13'),
                   ('q', '9'),)
        reg = re.compile('[^\d]')
        text = self.convert_remote_pic2num()
        # return text
        for item in similar:
            text = text.replace(item[0], item[1])
        text = reg.sub(lambda x: '', text)
        return text

    def find_possible_num(self):
        textlist = []
        i = 0
        loop = 10
        j = loop
        rate = 0.5
        text = ''
        p_text = ''

        # while内为优先级匹配：重复的11位的数字序列>重复出的数字序列>最后的数字序列，
        while i < loop:
            if text in textlist:
                p_text, j = text, i
                if text.__len__() == 11 or (text.__len__() == 10 and p_text[0:3] == '400'):
                    break
            if text:
                textlist.append(text)
            text = self.replace_similar_char2num()
            i += 1

        if not p_text:
            p_text = text
        if i < loop:
            rate = 0.99
        else:
            if j < loop:
                rate = 0.90
            if p_text.__len__() < 11 and not(p_text.__len__() == 10 and p_text[0:3] == '400'):
                rate = 0.10
        return (p_text, rate)


def main():
    url = 'http://nj.ganji.com/tel_img/?c=kh0LK-eWCfso9p-uEcEJPTQvVEjVA__PtQyX'
    url = 'http://www.ganji.com/tel_img/?c=k9xL64ZYdHed2AEf1DAJojLzO.6Ug__PtQyX'
    ConvertPhonePic2Num(url).find_possible_num()

if __name__ == '__main__':
    # main()
    import doctest
    print(doctest.testmod())
