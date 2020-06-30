import generate_text.generate_character as draw_char
import pickle
import numpy as np
import random
import cv2 as cv

FONTS_PATH = '../fonts/'
FONT_SIZE = 0.2
IMAGESIZE = 400

def compile_datasets(dataset_size):
    infile = open(FONTS_PATH + 'multifont_mapping.pkl', 'rb')
    unicode_mapping_dict = pickle.load(infile)
    unicode_count = len(unicode_mapping_dict)
    infile.close()
    unicode_chars_anchors = list(unicode_mapping_dict.keys())
    unicode_chars_samples = list(unicode_mapping_dict.keys())
    anchors = np.empty((dataset_size, IMAGESIZE, IMAGESIZE), dtype=np.uint8)
    positives = np.empty((dataset_size, IMAGESIZE, IMAGESIZE), dtype=np.uint8)
    negatives = np.empty((dataset_size, IMAGESIZE, IMAGESIZE), dtype=np.uint8)
    for i in range(dataset_size):
        anchor_char = unicode_chars_anchors[random.randint(0, len(unicode_chars_anchors)-1)]
        unicode_chars_anchors.remove(anchor_char)
        negative_char = anchor_char
        while negative_char == anchor_char:
            negative_char = unicode_chars_samples[random.randint(0, unicode_count - 1)]
        supported_anchor_fonts = unicode_mapping_dict[anchor_char]
        supported_negative_fonts = unicode_mapping_dict[negative_char]
        anchor_font = FONTS_PATH + supported_anchor_fonts[random.randint(0, len(supported_anchor_fonts) - 1)]
        positive_font = FONTS_PATH + supported_anchor_fonts[random.randint(0, len(supported_anchor_fonts) - 1)]
        negative_font = FONTS_PATH + supported_negative_fonts[random.randint(0, len(supported_negative_fonts) - 1)]
        anchors[i] = draw_char.transformImg(draw_char.drawChar(IMAGESIZE, chr(anchor_char), FONT_SIZE, anchor_font))
        positives[i] = draw_char.transformImg(draw_char.drawChar(IMAGESIZE, chr(anchor_char), FONT_SIZE, positive_font))
        negatives[i] = draw_char.transformImg(draw_char.drawChar(IMAGESIZE, chr(negative_char), FONT_SIZE, negative_font))
    return anchors, positives, negatives

def test():
    # 17 corrupt unicode chars
    # 3600 invalid pixel size
    infile = open(FONTS_PATH + 'multifont_mapping.pkl', 'rb')
    unicode_mapping_dict = pickle.load(infile)
    infile.close()
    for i in unicode_mapping_dict.keys():
        try:
            a = random.randint(0,len(unicode_mapping_dict[i])-1)
            #print(a)
            draw_char.transformImg(draw_char.drawChar(IMAGESIZE, chr(i), FONT_SIZE, FONTS_PATH + unicode_mapping_dict[i][a]))
        except (ValueError,OSError) as e:
            print(e,i,unicode_mapping_dict[i][a])


if __name__ == '__main__':
    dataset_size = 5000
    anchors, positives, negatives = compile_datasets(dataset_size)
    for i in range(dataset_size):
        cv.imshow('anchor',anchors[i])
        cv.imshow('positive',positives[i])
        cv.imshow('negative',negatives[i])
        cv.waitKey(0)
        cv.destroyAllWindows()

