__author__ = 'Administrator'
import os
import codecs
import configparser
import configparser
import os
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

print(config.sections())
print(config.options('EMAIL'))
print(config.get('EMAIL', 'mail_pass'))

print(os.path.split(os.path.realpath(__file__))[0])

# print(configPath)
