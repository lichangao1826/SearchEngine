from config.settings import *
import jieba
import os


def get_stop_words():
    """
    选取哈工大停用词表
    """
    with open(os.path.join(BASE_DIR, 'files/stop_words/HIT.txt'), 'r', encoding='utf8') as f:
        stop_words = [_.strip() for _ in f.readlines()]
    return stop_words


def text_seg(text: str, stop_words: list = None) -> list:
    """
    对输入的文本利用 jieba 进行分词
    """
    seg_list = []
    if not stop_words:
        stop_words = get_stop_words()
    for each in jieba.cut(text):
        if each not in stop_words and not each.isspace():
            seg_list.append(each.lower())

    return seg_list


if __name__ == '__main__':
    print(text_seg('乔布斯的管理课'))
