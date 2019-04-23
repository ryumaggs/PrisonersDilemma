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
			self.my_history.append(0)
			return 0
		if self.opp_history[-1] == 0:
			self.my_history.append(0)
			return self.my_history[-1]
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

class markov():
    def __init__(self,max_chain = 20):
        self.title = "markov"
        self.opp_history = []
        self.my_history = []
        self.max_chain = max_chain

    def decision(self,num = 20):

        # Zip histories together, need to check both opponent's choices and our choices
        # hist = zip(self.opp_history, self.my_history)

        # Get the previous history to compare against
        my_prev = self.my_history[-1*num:]
        opp_prev = self.opp_history[-1*num:]
        # Keep track of the possible choices. Will be the opponent's choice following the matching pattern
        choices = []

        # Iterate backwards through the history
        hist_iter = len(self.my_history) - 2
        while hist_iter >= 0:
            i = 0

            # Find matching patterns
            while i < num and hist_iter-i >= 0:
                
                # Pattern found
                if my_prev[-1*i] == self.my_history[hist_iter-i] and opp_prev[-1*i] == self.opp_history[hist_iter-i]:
                    # chance of this option being picked is related to how long of a pattern is matched
                    choices += [self.opp_history[hist_iter + 1]]
                    i += 1
                else: 
                    break

            hist_iter -= 1
                    

        # Randomly pick next move based on the choices already determined
        # No patterns found
        if (len(choices) == 0):
            my_move = 0
        else:
            my_move = random.choice(choices)
        self.my_history.append(my_move)
        return my_move

    def record(self, opp_move, my_move):
        self.opp_history.append(opp_move)