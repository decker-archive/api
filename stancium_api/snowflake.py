#!/usr/bin/env python

from time import time

class Sequence:
	"""A simple class used to make easy incrementalable sequences primarily for snowflake generation.
	
	Attributes
	----------
	start: :class:`int`
		An Integer used to specify the Sequence's start.
	limit: :class:`int`
		An Integer used to specify the Sequence's limit.
	value :class:`int`
		An integer which represents the Sequence's current value.
	"""
	def __init__(self, start: int=0, limit: int=999999):
		self.start = start
		self.limit = limit
		self.value = 0
		
	def increment(self, increase: int=1) -> int:
		"""The method used to increment the Sequence's current value.
		If the value surpasses the Sequence's specifies limit it's value is reset to its start attribute.
		
		Parameters
		----------
		increase: :class:`int`
			The amount that the Sequence is incremented by.
		"""
		self.value += increase
		if self.value > self.limit:
			self.value = self.start
			
			
	def __add__(self, num: int) -> int:
		return num+ self.value
		
	def __sub__(self, num: int) -> int:
		return num - self.value
		
	def __mul__(self, num: int) -> int:
		return num*self.value
	
	def __div__(self, num: int) -> int:
		return num/self.value
		
SEQUENCE = Sequence()

def create_snowflake(suffix: int) -> int:
	"""The method used to generate Stancium snowflakes.
	
	Parameters
	----------
	suffix: :class:`int`
		The last two digits of the snowflake used to identify the type of the object it represents.
		.. warning::
			If you enter a suffix that's longer than 2 digits the function raises an error.
	"""
	if len(str(suffix)) > 2:
		assert False, "Suffix must be 2 digits or shorter in length"
	SEQUENCE.increment()
	snowflake = round(time())*100000000+SEQUENCE*100+suffix
	return snowflake

id = create_snowflake(type)