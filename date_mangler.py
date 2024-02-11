from enum import Enum, auto
from datetime import datetime as dt, timedelta as td

class Operions(Enum):
	add = auto()
	sub = auto()
	mul = auto()
	div = auto()

	# sub month
	# add month
	# sub year
	# add year

	def oper(self, op1, op2):
		try:
			if self is self.__class__.add: return op1 + op2
			if self is self.__class__.sub: return op1 - op2
			if self is self.__class__.mul: return op1 * op2
			if self is self.__class__.div: return op1 / op2
		except TypeError:
			return op2

class CommandProcessor:
	UNIX_START_YEAR = 1970

	def __init__(self):
		self.val = 0
		self.operation = Operions.add
		self.multiplier = 1
		self.num = ''

	def run_command(self, command):
		for c in command:
			if c.isdigit(): self.num += c
			elif self.num:
				self.multiplier = int(self.num)
				self.num = ''

			if c.isspace(): continue

			if c == '+': self.operation = Operions.add; continue
			if c == '-': self.operation = Operions.sub; continue
			if c == '*': self.operation = Operions.mul; continue
			if c == '/': self.operation = Operions.div; continue
			if c == '^': self.val = self.multiplier; continue

			if   c == 'S': op2 = td(seconds = self.multiplier)
			elif c == 'M': op2 = td(minutes = self.multiplier)
			elif c == 'H': op2 = td(hours   = self.multiplier)
			elif c == 'D': op2 = td(days    = self.multiplier)

			elif c == '.': op2 = self.multiplier
			elif c == '_': op2 = -self.multiplier

			elif c == 'm':
				op2 = dt(
					year=self.UNIX_START_YEAR, month=self.multiplier, day=1
				) - td(1)

			elif c == 'y':
				op2 = dt(year=self.multiplier, month=1, day=1) - td(1)

			elif c == 'u':
				op2 = dt.utcfromtimestamp(self.multiplier)
				self.multiplier = 1

			elif c == 'n':
				op2 = dt.now()

			else: continue

			self.val = self.operation.oper(self.val, op2)
			self.multiplier = 1


		if self.num:
			self.multiplier = int(self.num)
			self.num = ''

if __name__ == '__main__':
	processor = CommandProcessor()

	while 1:
		print(f'{processor.val.__class__.__name__} {processor.val}')
		print(f'{processor.operation}')
		print(f'multiplier = {processor.multiplier}')
		try:
			cmd = input('> ')
		except KeyboardInterrupt:
			break

		processor.run_command(cmd)
		print()
