# -*- coding: utf-8 -*-
import re
import StringIO
from PIL import Image
from pytesseract import image_to_string
from urllib2 import urlopen, Request
import logging
logger = logging.getLogger(__name__)

# @added by y10n
# hack for error:
#
# IOError: image file is truncated (5 bytes not processed)
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import datetime

class ConvertPhonePic2Num(object):

    """
>>> ConvertPhonePic2Num('http://sh.ganji.com/tel_img/?c=k92L68WOXwcdZlbkfF5p-zJhzdzyQ__PtQyX').find_possible_num()\
# 13166118115
('13166118115', 0.99)
>>> ConvertPhonePic2Num('http://nj.ganji.com/tel_img/?c=kh3LK8CCBrmcz9g90dTSiHLan.-6g__PtQyX').find_possible_num()\
# 13675151805
('13675151805', 0.99)

# >>> ConvertPhonePic2Num('http://www.che168.com/handler/CarDetail_v3/GetLinkPhone.ashx?infoId=4761577&linkType=2').find_possible_num()
# ('18917761263', 0.99)
# >>> ConvertPhonePic2Num('http://cache.taoche.com/buycar/gettel.ashx?u=5730860&t=ciggmcamamm').find_possible_num()
# ('15339109099', 0.99)
>>> ConvertPhonePic2Num('http://cache.taoche.com/buycar/gettel.ashx?u=.&t=acegtiosbm').find_possible_num()
('0123455789', 0.1)

for taoche, failed to parse 6 compared with 5, others work
# acegtiosbm
# 0123456789
    """

    MOBILE_PHONE_EX = ('133/153/180/181/189/177/'
                      '130/131/132/155/156/185/186/145/176/'
                      '134/135/136/137/138/139/150/151/152/157/158/159/182/183/184/187/188/147/178/'
                      '170')
    '''
    -1 will be ocred as 4, or other error,using guess is better now
    '''
    TAOCHE_DIGIT_MAP=(
        'acegtiosbmj',
        '0123456789-',
    )
    OCR_TRY_TIMES = 10

    def __init__(self, picurl):
        self.picurl = picurl

    @classmethod
    def guess(cls, url):
        from urlparse import urlparse,parse_qs
        url_parts = urlparse(url)
        try:
            if url_parts.hostname=='cache.taoche.com':
                qsa = parse_qs(url_parts.query)
                t=qsa.get('t')[0]
                m=dict(zip(*cls.TAOCHE_DIGIT_MAP))
                return ''.join([m[x] for x in t])
        except:
            logger.error('guess phone error for:%s' % url, exc_info=True)
            return ''

    @classmethod
    def valid_taoche(cls,urls):
        if not urls:
            return 0
        success_cnt = 0
        for url in urls:
            logger.debug('checking url %s' % url)
            ocred_phone = re.sub('[^0-9]', '', cls(url).find_possible_num(guess=False)[0])
            guessed_phone = cls.guess(url).strip()
            logger.debug('guessed %s'% guessed_phone)
            logger.debug('ocred %s' % ocred_phone)
            if guessed_phone.replace('6', '5')==ocred_phone:
                success_cnt += 1
                logger.debug('match')
            else:
                logger.debug('not match')
        return round(success_cnt*100/len(urls))

    def convert_remote_pic2num(self):
        im = urlopen(Request(self.picurl)).read()
        try:
            imob = Image.open(StringIO.StringIO(im))
            if imob.mode == 'RGBA':
                imob = self.replace_rgba_transparency(imob)
        except Exception as e:
            with open('/tmp/gpjspider/phone_ocr_fail.log', 'a') as f:
                f.write(str(datetime.datetime.now()))
                f.write("\n")
                f.write(self.picurl)
                f.write("\n")
                f.write(e.message)
                f.write("\n")
                f.write(im)
            raise e
        else:
            imob = imob.convert('RGB')
            # TODO: 在调用pytesser之前处理一下图片，如把挨得紧密的数字分开，可以提高识别的准确率,需要研究PIL库
            text = image_to_string(imob)
        # print text
        return text

    def replace_rgba_transparency(self, im):
        # 使用白色来填充背景,测试发现如果不填充，当背景为透明时，
        # 转换为RGB格式后图片中背景和数字会变成一坨
        # refer to :
        # http://outofmemory.cn/code-snippet/7453/python-through-pil-png-tupian-fill-background-color
        x, y = im.size
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        return p

    def replace_similar_char2num(self):
        # 形状相似的数字和字母映射.
        similar = (('O', '0'), ('o', '0'), ('D', '0'), ('a', '0'), ('L', '1'), ('!', '1'),
                   ('|', '1'), ('l', '1'), ('I', '1'), ('Z',
                                                        '2'), ('z', '2'), ('A', '4'),
                   ('S', '5'), ('s', '5'), ('b', '6'), ('T', '7'), ('B', '13'),
                   ('q', '9'),)
        reg = re.compile('[^\d]')
        text = self.convert_remote_pic2num()
        # return text
        for item in similar:
            text = text.replace(item[0], item[1])
        text = reg.sub(lambda x: '', text)
        return text

    def find_possible_num(self, guess=True):
        p_text = ''
        rate = 0.5

        if guess:
            p_text=self.guess(self.picurl)
            if p_text:
                rate=0.99
                return self.format_phone_string(p_text, rate)

        textlist = []
        i = 0
        loop=self.OCR_TRY_TIMES
        j = loop
        text = ''

        # while内为优先级匹配：重复的11位的数字序列>重复出的数字序列>最后的数字序列，
        while i < loop:
            if text in textlist:
                p_text, j = text, i
                if (text.__len__() == 11 and p_text[0:3] in self.MOBILE_PHONE_EX) \
                   or (text.__len__() >= 10 and p_text[0:3] == '400'):
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
        return (self.format_phone_string(p_text), rate)

    def format_phone_string(self, phone):
        # rule 1， 400号码第十位后加-
        if phone[0:3] == '400' and len(phone) > 10:
            phone = phone[0:10] + '-' + phone[10:]

        return phone


def main():
    #url = 'http://nj.ganji.com/tel_img/?c=kh0LK-eWCfso9p-uEcEJPTQvVEjVA__PtQyX'
    #url = 'http://www.ganji.com/tel_img/?c=k9xL64ZYdHed2AEf1DAJojLzO.6Ug__PtQyX'
    #url = 'http://nj.ganji.com/tel_img/?c=kh3LK8CCBrmcz9g90dTSiHLan.-6g__PtQyX'
    #url = 'http://www.che168.com/handler/CarDetail_v3/GetLinkPhone.ashx?infoId=5740591&linkType=3&phone='
    url = 'http://used.xcar.com.cn/public/load/CarObj.3276841.imgPhone'
    #url = 'http://used.xcar.com.cn/public/load/CarObj.3279485.imgPhone'
    #url = 'http://cache.taoche.com/buycar/gettel.ashx?u=6950596&t=taabcgbote&p=1'
    #url = 'http://www.che168.com/handler/CarDetail_v3/GetLinkPhone.ashx?infoId=4761577&linkType=2'
    print ConvertPhonePic2Num(url).find_possible_num()

if __name__ == '__main__':
    # main()
    import doctest
    print(doctest.testmod())
