from enum import Enum, auto
from datetime import datetime as dt, timedelta as td
from dateutil.relativedelta import relativedelta as rd

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

class monthdelta:
	'''
	An intermediate date representation that collapses into a real datetime object
	when it is added with a timedelta object. More info in __add__.
	'''

	UNIX_START_YEAR = 1970

	def __init__(self, months=0, *, years=0):
		self.months = months + years * 12

	def __repr__(self):
		return f'{self.__class__.__name__}(months={self.months})'

	def __str__(self):
		y, m = divmod(self.months, 12)
		return f'{y} years, {m} months'  # no plural stuff; it's fine

	def __add__(self, other, default_year = 1):
		'''
		Adds two time objects together.

		Adding a datetime.timedelta object will result in a datetime.dateime object
		created from the year and month corresponding to this monthdelta object
		and the timedelta object will be added to it.

		monthdelta(years=2020, months=6) + td(days=13) == datetime(year=2020, month=6, day=13)

		The actual logic of calculating this as follows:
		monthdelta(years=y, months=m) + td(days=d) = datetime(year=y, month=m, day=1) + td(days=d) - td(days=1)

		This leads to some edge cases that may be confusing:
		monthdelta(years=2020, months=6) + td(days=0) == datetime(year=2020, month=5, day=31)
		monthdelta(years=2020, months=6) + td(days=-1) == datetime(year=2020, month=5, day=30)
		'''

		if isinstance(other, self.__class__):
			return self.__class__(self.months + other.months)

		if isinstance(other, dt):
			out = other + rd(months=self.months)
			# print(out)
			return out

		if isinstance(other, td):
			y, m = divmod(self.months, 12)
			if m == 0: m = 12; y -= 1
			if y <= 0: y = default_year  # cuz year 0 is not supported.
			# converts to dt
			return dt(year=y, month=m, day=1)+other-td(1)

		raise TypeError(f'Cannot add {self.__class__.__name__!r} with {other.__class__.__name__!r}')

	def __radd__(self, other):
		return self + other

	def __rsub__(self, other):
		if isinstance(other, self.__class__):
			return self.__class__(other.months - self.months)

		if isinstance(other, dt):
			months = other.month + other.year*12 - self.months

			y, m = divmod(months, 12)

			return other.replace(year=y, month=m)

		raise TypeError(f'Cannot subtract {self.__class__.__name__!r} from {other.__class__.__name__!r}')

	def __mul__(self, other):
		return self.__class__(self.months * other)

	def __truediv__(self, other):
		if not isinstance(other, self.__class__):
			raise TypeError(f'Cannot divide {self.__class__.__name__} by {other.__class__.__name__}')

		return self.months / other.months

class CommandProcessor:
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
				op2 = monthdelta(months=self.multiplier)
				self.multiplier = 1

			elif c == 'y':
				op2 = monthdelta(years=self.multiplier)
				self.multiplier = 1

			elif c == 'Y':  # force the year field
				if isinstance(self.val, dt):
					self.val = self.val.replace(year=self.multiplier)
					self.multiplier = 1
					continue

				if isinstance(self.val, monthdelta):
					m = self.val.months%12
					if m == 0: m = 12
					self.val = monthdelta(years=self.multiplier, months=m)
					self.multiplier = 1
					continue

				op2 = monthdelta(years=self.multiplier)
				self.multiplier = 1

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
