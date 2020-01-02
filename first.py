import sys
import requests
import argparse
import yaml
import bs4
from ipdb import set_trace


class BaseContextManager(object):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type, exc_val)
        return True


class Scraper(object):

    def __init__(self, sys_args, *args, **kwargs):
        self.call_module = CallModule()
        self.bs4 = bs4

        self.parsed_params = []
        if sys_args.path:
            with open(sys_args.path) as file:
                params = yaml.load(file, Loader=yaml.SafeLoader)
            self.parsed_params = self._parse_params(params)

    def _parse_params(self, params):
        return params

    def _scrap(self, call_params, scraping_params, **kwargs):
        with BaseContextManager():
            call_result = self.call_module.request(**call_params)
        bs4_res = self.bs4.BeautifulSoup(call_result.text)
        print(bs4_res.text.__sizeof__()/1000000)
        print(bs4_res.title)

    def run_scraping(self):
        if not self.parsed_params:
            raise ValueError
        for p in self.parsed_params:
            self._scrap(**p)


class CallModule(object):

    def __init__(self):
        self._requests = requests

    def request(self, get=None, post=None, **kwargs):
        if get:
            return self._get(**get)
        elif post:
            return self._post(**post)
        else:
            raise AttributeError

    def _get(self, *args, **kwargs):
        url = kwargs.get('url')
        params = kwargs.get('params')
        return self._requests.get(url, params)

    def _post(self, post, *args, **kwargs):
        pass


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('path')
    sys_args = arg_parser.parse_args()
    a = Scraper(sys_args)
    a.run_scraping()
