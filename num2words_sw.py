#!/usr/bin/env python3

__author__  = (
	'Machaku Banga',
	)
__license__ = 'Apache License, 2.0 (Apache-2.0)'
__version__ = '2012.03.16'

import sys
import re

mamoja=['','moja','mbili','tatu','nne','tano','sita','saba','nane','tisa']
makumi=['','kumi','ishirini','thelathini','arobaini','hamsini','sitini','sabini','themanini','tisini']
mamia=['','mia moja','mia mbili','mia tatu','mia nne','mia tano','mia sita','mia saba','mia nane','mia tisa']
cheo=['','elfu','milioni','bilioni','trilioni','kuadrilioni','kuintilioni','seksitilioni','septilioni','oktilioni','nonilioni','desilioni','anidesilioni','dodesilioni','tradesilioni','kuatuordesilion','kuindesilioni','seksidesilioni','septendesilioni','oktodesilioni','novemdesilioni','vijintilioni']

class Number:
	
	def __init__(self,number):
		self.number = number
		if self.number is None:
			return ''
		else:
			try:
				int(self.number)
			except TypeError:
				return "Kosa. Hujaingiza inteja."
		
	def get_order(self,number):
		order = 0
		while number >= 1000:
			order += 1
			number = number//1000
		return order
		
			
	def get_order_remainder(self,number):
		order = self.get_order(number)
		remainder = number%pow(10,3*order)
		return remainder
		
	def convert_to_words_hundreds(self,number):
		word = ''
		if number < 0:
			number -= number
			word += 'hasi '
		if number <1000:
			if number >= 100:
				hundred = number//100
				hundredr = number%100
				if hundredr:
					ten = hundredr//10
					one = hundredr%10
					word += mamia[hundred]
					if ten:
						word += ' na '+ makumi[ten]
					if one:
						word+=' na '+mamoja[one]
				else:
					word += mamia[hundred]
			if 100> number >= 10:
				ten = number//10
				one = number%10
				word += makumi[ten]
				if one:
					word +=' na ' +mamoja[one]
			elif number<10:
				word += mamoja[number]
				
		return word
		
	def convert_to_words_order(self,number):
		word =''
		order = self.get_order(number)
		hundred = number//pow(10,3*order)
		if order == 1 and hundred >= 100:
			laki = hundred//100
			lakir = hundred%100
			word += 'laki '+ mamoja[laki]
			if lakir:
				word += ' na elfu '+self.convert_to_words_hundreds(lakir)
			return word
		return cheo[order]+' '+self.convert_to_words_hundreds(hundred)
		
	def convert_to_words_order_r(self,number):
		word =''
		order = self.get_order(number)
		hundred = number//pow(10,3*order)
		if order == 1 and hundred >= 100:
			laki = hundred//100
			lakir = hundred%100
			word += 'laki '+ mamoja[laki]
			if lakir:
				word += ' na '+self.convert_to_words_hundreds(lakir)+' elfu '
			return word
		return self.convert_to_words_hundreds(hundred)+' '+cheo[order]

	def convert_to_digits(self,snumber):
		word=''
		word_l=[]
		digits=list(snumber)
		for i in digits:
			if int(i)==0:
				word_l.append('sifuri')
			else:
				word_l.append(mamoja[int(i)])
		word=' '.join(word_l)
		return word
	
	def get_fraction_digits(self,integer=False):
		number_s=str(self.number)
		try:
			number_ls = re.split('[.]',number_s)
			digits = number_ls[1]
			if integer:
				digits = int(digits)
		except:
			digits = False
		return digits
	
	def convert_to_words(self):
		word=''
		fraction = self.get_fraction_digits()
		try:
			number_s=str(self.number)
			number_ls = re.split('[.]',number_s)
			self.number = int(number_ls[0])
		except:
			pass
		if number_ls[0][0] == '-':
			self.number = -self.number
			word += 'hasi '
		if self.number==0:
			word += 'sifuri'
		number = self.number
		if number < 1000:
			word += self.convert_to_words_hundreds(number)
		else:
			if number%1000:
				terminator =' na '
			else:
				terminator =''
			while number >= 1000:
				order = self.get_order(number)
				digits_in_order = number//pow(10,3*order)
				value_in_order = (digits_in_order * pow(10,3*order))
				next_number = number - value_in_order
				if 0<number%10000<100 and number>=10000 and next_number<100:
					word+=self.convert_to_words_order_r(number)
				else:
					word += self.convert_to_words_order(number)
				number = next_number
				if number:
					word += ','
				if order >= 1 and number:
					word += ' '
			else:
				if terminator:
					word = word[:-2]
					#if number>9:
					word+=terminator
					word += self.convert_to_words_hundreds(number)
		if fraction:
			word+= ' nukta '+self.convert_to_digits(fraction)
		return word

if __name__ == "__main__":
	try:
		for i in range(1,len(sys.argv)):
			try:
				no = Number(int(sys.argv[i]))
			except ValueError:
				no = Number(float(sys.argv[i]))
			print (no.convert_to_words())
	except KeyError:
		pass
