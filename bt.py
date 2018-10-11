#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import logging
import subprocess
import string
import time

print ("Go\n")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

stop = True

#IDEA:
#cron
#ssh-ключи
#ps axuf
#netstat -tunlp - DONE
#events from file system → we can use inotifywait
# any idea?

first_ports = False

def start(bot, update):
	"""Send a miss"""
	print (update.message.text)
	monitoring_process(bot, update)
	send_analisy_file(bot,update)
	
def stop(bot, update):
	""" stop send after finnish game """
	stop = False
	
def error(bot, update, error):
	print("error")
	logger.warning('update "%s" coz error "%s"', update, error)
	
def echo(bot, update):
	print (update.message.text)
	update.message.reply_text(update.message.text)

def monitoring_process(bot, update):
	""" ps aux diff with one 30 sec again"""
	global first_ports
	old_ports_size = 0
	while True:
		try:
			command = "netstat -anltp | grep \"LISTEN\""
			process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
			p = process.communicate()
			ports = p[0].split('LISTEN')
			ports = [e.strip() for e in ports]
			new_ports_size = len(ports)
			if first_ports == False:
				first_ports = True
				old_ports_size = new_ports_size
				update.message.reply_text(' \n '.join(ports))
				""" first send port to chat"""
				""" scan open port in confid"""
			else:
				if new_ports_size != old_ports_size:
					update.message.reply_text(' \n '.join(ports))
					old_ports_size = new_ports_size
				else:
					print("Nothing")
			time.sleep(30)
		except KeyboardInterrupt, e:
			print "error"
		
		

def send_analisy_file(bot, update):
	""" send to chat after stat analis"""
	#bot.send_document(chat_id=update.message.chat_id, document=open('test.php', 'rb'))
	
	
def main():
	print("Start")
	updater = Updater("TOKEN")
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("stop", stop))
	dp.add_handler(MessageHandler(Filters.text, echo))
	dp.add_error_handler(error)
	updater.start_polling()
	updater.idle()
	print("End")
	
if __name__ == '__main__':
	main()
