#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'srocha'

from collections import Counter
from heapq import heappush,nlargest
from Model import findOrCreateLanguage,findOrCreateLetter,allLanguages,getFrequencys
from Model import updateMinFrequencys,updateMaxFrequencys,getFrequencysLetterByLanguage

VARIANCE = 0.03
PERCENT_SIMILARITY = 0.95

def getPatterProtean(text):
   dic_letter = Counter(text)
   totalLetterText = len(text)

   h = []
   for letter,count in dic_letter.items():
      percent = count/totalLetterText

      heappush(h,(percent,letter))

   return nlargest(len(h), h ,key=lambda h:h[0])


def getPatterLanguages():
   languages = allLanguages()
   return languages

def learLanguage(patter, language):
   language_id = findOrCreateLanguage(language)
   for percentage,letter in patter:
      letter_id = findOrCreateLetter(letter)
      min,max,id = getFrequencys(language_id,letter_id)
      if(min < percentage):
         updateMinFrequencys(id,percentage)
      if(max < percentage):
         updateMaxFrequencys(id,percentage)

def detectLanguage(patter):
   languages = getPatterLanguages()

   candidateLanguage = []

   for language in languages:

      count = 0
      for percentage,letter in patter:
         letter_id = findOrCreateLetter(letter)
         minLanguageLetter,maxLanguageLetter = getFrequencysLetterByLanguage(language.id,letter_id)

         if(percentage - VARIANCE <= minLanguageLetter and percentage + VARIANCE >= maxLanguageLetter):
            count += percentage
      if count >= PERCENT_SIMILARITY:
         candidateLanguage.append((language.name,count) )

   return candidateLanguage
