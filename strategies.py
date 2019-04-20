import random
random.seed(65)
class alwaysBetray():
	def __init__(self):
		self.title = "alwaysBetray"

	def decision(self):
		return 1

	def record(self,opp_move,my_move):
		return 0

#1 is betray
#0 is loyal
class alwaysLoyal():
	def __init__(self):
		self.title = "alwaysLoyal"

	def decision(self):
		return 0

	def record(self,opp_move,my_move):
		return 0

class randomBetray():
	def __init__(self,p=.5):
		self.title = "randomBetray"
		self.prob = p

	def decision(self):
		a = random.randint(0,100)
		if a > 50:
			return 0
		else:
			return 1

	def record(self,opp_move,my_move):
		return 0

class grudger():
	def __init__(self):
		self.title = "grudger"
		self.opp_history = []
		self.nice = True

	def decision(self):
		if self.nice == False:
			return 1
		elif self.opp_history:
			if self.opp_history[-1] == 0:
				return 0
			else:
				self.nice = False
				return 1
		else:
			return 0

	def record(self,opp_move,my_move):
		self.opp_history.append(opp_move)

class niceness():
	def __init__(self):
		self.title = "niceness"
		self.opp_history = []

	def decision(self):
		if len(self.opp_history) > 0:
			s = sum(self.opp_history)/len(self.opp_history)
			if s < 0.3:
				return 0
			else:
				return 1
		else:
			return 0

	def record(self,opp_move,my_move):
		self.opp_history.append(opp_move)

class repeat():
	def __init__(self):
		self.title = "repeat"
		self.opp_history = []
		self.my_history = []

	def decision(self):
		if len(self.opp_history) == 0:
			self.myHistory.append(0)
			return 0
		if self.opp_history[-1] == 0:
			self.myHistory.append(0)
			return self.myHistory[-1]
		else:
			return random.randint(0,1)

	def record(self,opp_move,my_move):
		self.opp_history.append(opp_move)

class titfortat():
	def __init__(self):
		self.title = "titfortat"
		self.opp_history = []

	def decision(self):
		if len(self.opp_history) == 0:
			return 0
		else:
			return self.opp_history[-1]

	def record(self,opp_move,my_move):
		self.opp_history.append(opp_move)