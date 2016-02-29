#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pony.orm import db_session,select,Database
from configparser import ConfigParser
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Protean - db')


__author__ = 'srocha'

try:
   config = ConfigParser()
   config.read('config')
   database = config['dbConfig']['database']
   user = config['dbConfig']['user']
   password = config['dbConfig']['password']
   host = config['dbConfig']['host']
   db = Database('postgres',
                 user=user,
                 password=password,
                 host=host,
                 database=database)
except KeyError as e:
   db = None
   logger.info('could not make connection to the database')

@db_session
def allLanguages():
   return db.select('id,name FROM languages')

@db_session
def findOrCreateLanguage(language):
   findLanguage = db.select('id FROM languages WHERE name = $language')
   if len(findLanguage) is 1:
      id = db.get('id FROM languages WHERE NAME = $language')
   else:
      id = db.insert('languages',name = language, returning = 'id')
      logger.info('New Language : {LANGUAGE}'.format(LANGUAGE=language))
   return id

@db_session
def findOrCreateLetter(character):
   let = db.select('id FROM letters WHERE character = $character')
   if len(let) is 1:
      id = db.get('id FROM letters WHERE character = $character')
   else:
      id = db.insert('letters',character = character, returning = 'id')
      logger.info('New character: "%s"' % character)
   return id

@db_session
def getPatterProtean(language_id,letter_id):
   min,max,id = db.get('min,max,id FROM frequencys WHERE language_id = $language_id AND letter_id = $letter_id')
   return min,max,id

@db_session
def updateMinFrequencys(id,min):
   sql = 'UPDATE frequencys SET min = %s WHERE id = %s' %  (min,id)
   db.execute(sql)
   db.commit()

@db_session
def updateMaxFrequencys(id,max):
   sql = 'UPDATE frequencys SET max = %s WHERE id = %s' %  (max,id)
   db.execute( sql)
   db.commit()

@db_session
def getFrequencysLetterByLanguage(language_id,letter_id):
   min,max = db.get('min,max FROM frequencys WHERE language_id = $language_id AND letter_id = $letter_id')
   return min,max

@db_session
def getFrequencys(language_id,letter_id):
   min,max,id = db.get('min,max,id FROM frequencys WHERE language_id = $language_id AND letter_id = $letter_id')
   return min,max,id