#!/usr/bin/env python

import requests


########################################################################################################################


class Eikeskog_dev(object):
    def __init__(self):
        pass

    def test(self, url="https://example.com"):
        r = requests.get(url)
        print(r)


########################################################################################################################


if __name__ == '__main__':
    eikeskog_dev = Eikeskog_dev()
    eikeskog_dev.test()