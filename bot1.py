# -*- coding: utf-8 -*-

import telebot, time

import xml.etree.ElementTree as ET
from datetime import datetime as dt
from datetime import timedelta as td
import urllib.request as UR

class CBParser():
    ''' Class for Central Bank currency rate parser.
    Methods:
    
    parser() - downloads xml and parses it. Stores codenames and rates in
    self.db, enabled currency codenames in self.currs.
    
    get_codes() - returns a list of enabled currencies' codenames.
    
    send_rate(name) - returns a [name] currency's rate.'''
    def __init__(self):
        self.parser()
    def parser(self):
        # текущая дата в нужном формате для подстановки в url.
        self.date = dt.now()
        # т.к. ЦБ РФ не публикует курс в вс/пн, ставим курс на сб
        if self.date.weekday() == 6:
            self.date = self.date + td(days=-1)
        elif self.date.weekday() == 0:
            self.date = self.date + td(days=-2)
        self.date = self.date.strftime('%d/%m/%Y')
    
        # url с текущей датой
        url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='+self.date
        file = UR.urlopen(url)
        
        # парсим файл
        tree = ET.parse(file)
        root = tree.getroot()
        
        self.db = {valute[1].text: [valute[2].text,
                               valute[3].text,
                               valute[4].text] for valute in root}
                               
        self.currs = [valute[1].text for valute in root]

    def get_codes(self):
        cur_codes = ', /'.join(self.currs)
        return cur_codes
  
    def send_rate(self, name):
        query = name[1:]
        reply = 'Курс на '+self.date+':\n{0} {1} = {2} рублей.'.format(self.db[query][0],
                                                self.db[query][1],
                                                self.db[query][2])
        return reply
        
cbparser = CBParser()

welcome_msg = '''Hello! This is a simple bot for my studies.
It tells you today's foreign currency exchange rate 
according to Central Bank of Russia.
Commands: 

/start and /help - gives you this info.
 
/get - gives you codenames of enabled currencies.
The most used will appear on keyboard markup.

If you send a 3-letter currency codename as a comand (ex. /USD), 
it will give you this currency's exchange rate for today.

Please note that there're no rates published on Sunday and Monday - 
Saturday's rate will be given instead.

The rest is echoed - just because.'''

codes = cbparser.get_codes()
codes = codes.split(', /')

token = '127006823:AAEd4T_pdda2HQrKE6CFIwxDnMh5gNrthzA'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start','help'])
def start_help(message):
    bot.send_message(message.chat.id, welcome_msg)

@bot.message_handler(commands=['get'])
def get_enabled(message):
    codes = cbparser.get_codes()
    bot.send_message(message.chat.id,codes,reply_markup=markup)
    
@bot.message_handler(commands=codes)
def get_rate(message):
    cur_name = message.text
    rate = cbparser.send_rate(cur_name)
    bot.send_message(message.chat.id, rate)
    
@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, message.text)
    
markup = telebot.types.ReplyKeyboardMarkup(row_width=4)
markup.add('/USD','/EUR','/GBP','/NOK')
markup.add('/SEK','/CAD','/DKK','/CHF')


if __name__=='__main__':
    #bot.set_webhook()
    bot.polling(none_stop=True)
    time.sleep(100)
    



    
    
