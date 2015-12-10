# !/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml


class ClassConfig(object):
    """Класс для парсинга настроек"""

    def __init__(self, account):
        self.account = account
        self.config = yaml.load(open('config.yml', 'r'))

    def __getitem__(self, key):
        return self.config[key]

    def settings(self):
        return self.config['aori'][self.account]

    def accounts(self):
        return self.config['aori']

    def path(self):
        return self.config['path_file']
