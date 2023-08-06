# -*- coding: utf-8 -*-
"""
HTMLPurifier testing
This is not doc- or unit tests.
"""

import time
from purifier import HTMLPurifier

import bleach


test_data_files = [
    '../test-data/google.ru.html',
    '../test-data/megatyumen.ru.catalogue.html',
    '../test-data/megatyumen.ru.html',
    '../test-data/simple.html',
    '../test-data/quoted_test.html',
    '../test-data/custom-1.html',
]

HTMLPurifier_test_whitelist = {
    '*': ['*'],
}

bleach_test_whitelist = {
    'tags': ['p', 'div', 'b', 'i'],
    'attrs': ['attr-2']
}


def read_file(name):
    return open(name).read()


def HTMLPurifier_test(index=3, whitelist=HTMLPurifier_test_whitelist):
    purifier = HTMLPurifier(whitelist)
    return purifier.feed(read_file(test_data_files[index]))


def bleach_test(index=3):
    return bleach.clean(
        read_file(test_data_files[index]),
        tags = bleach_test_whitelist['tags'],
        attributes = bleach_test_whitelist['attrs'],
        strip = False
    )

if __name__ == '__main__':
    start_time = time.clock()
    index = 5
    print(HTMLPurifier_test(index))
    print(time.clock() - start_time, 's')
