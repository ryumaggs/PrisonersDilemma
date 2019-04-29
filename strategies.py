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

# Forgiving tit for tat
class titforntats():
	def __init__(self, n = 2):
		self.title = "titforntats"
		self.opp_history = []
		
		self.n = n

	def decision(self):
		if len(self.opp_history) == 0:
			return 0
		else:
			if sum(self.opp_history[-1*self.n:]) == self.n:
				return 1
			else: 
				return 0
			

	def record(self,opp_move,my_move):
		self.opp_history.append(opp_move)

# Grudge  tit for tat
class mtitsfortat():
	def __init__(self, m = 2):
		self.title = "mtitsfortat"
		self.opp_history = []
		
		self.m = m
		self.num_def = 0

	def decision(self):
		if len(self.opp_history) == 0:
			return 0
		else:
			if (self.opp_history[-1] == 0):
				if self.num_def > 0 and self.num_def != self.m:
					self.num_def += 1
					return 1
				else: 
					self.num_def = 0
					return 0
			else:
				self.num_def = 0
				return 1
			

	def record(self,opp_move,my_move):
		self.opp_history.append(opp_move)


# Markov based strategy
class markov():
	def __init__(self,max_chain = 20):
		self.title = "markov"
		self.opp_history = []
		self.my_history = []
		self.max_chain = max_chain

	def decision(self,num = 20):

		# Get the previous history to compare against
		my_prev = self.my_history[-1*num:]
		opp_prev = self.opp_history[-1*num:]

		# Keep track of the possible choices. Will be the opponent's choice following the matching pattern
		choices = []

		# Iterate backwards through the history
		hist_iter = len(self.opp_history) - 2
		while hist_iter >= 0:
			i = 0

			# Find matching patterns
			while i < num and hist_iter-i >= 0:
				
				# Pattern found
				if my_prev[-1*i] == self.my_history[hist_iter-i] and opp_prev[-1*i] == self.opp_history[hist_iter-i]:
					# chance of this option being picked is related to how long of a pattern is matched
					try:
						choices += [self.opp_history[hist_iter + 1]]
					except:
						print(self.opp_history, len(self.opp_history),hist_iter)

					i += 1
				else: 
					break

			hist_iter -= 1
					

		# No patterns found
		if (len(choices) == 0):
			my_move = 0

		# Randomly pick next move based on the choices already determined
		else:
			my_move = random.choice(choices)

		self.my_history.append(my_move)
		return my_move

	def record(self, opp_move, my_move):
		self.opp_history.append(opp_move)

class DBS():
	def __init__(self):
		self.title = "DBS"
		self.move_history = []
		self.outcome_history = {}
		self.opponent_schema = {(0,0): 1,(0,1): 1,(1,0): 0,(1,1): 0} #probabilistic
		self.opponent_strategies = {} #known
		self.cur_opponent_name = ""
		self.test_phase_counter = 0

	def decision(self):
		#not sure if i need this., think we make a new player each round
		if 1 == 0:
			self.move_history = []
			self.outcome_history = {} #takes previous moves as key, and current move as value
			self.opponent_schema = {(0,0): 1,(0,1): 1,(1,0): 0,(1,1): 0} #these are probabilistic
			self.opponent_strategies = {} #these are known strategies
			self.test_phase_counter = 0
			return 0
		else:
			if len(self.move_history) == 0:
				return 0
			last_move = self.move_history[-1]
			if last_move in self.opponent_strategies:
				if self.opponent_strategies[last_move] == 0:
					return 0
				else:
					return 1
			else:
				collude_probability = self.opponent_schema[last_move]
				if collude_probability > .6:
					return 0
				else:
					return 1

	def record(self,opp_move,my_move):
		#add test phase recording here l0l
		#FIRST. TO TAKE CARE OF 100% STRATEGIES:
		#takes care of the first round
		if len(self.move_history) == 0:
			self.move_history.append((my_move,opp_move))
			return
		#current timeline
		self.move_history.append((my_move,opp_move))

		l = list(self.move_history[-1])
		print("aa",l)
		l_t = tuple(l)
		l.append(opp_move)
		print("bb",l)
		t = tuple(l)

		#alternate timeline
		alt = 0
		alt_ochist = []
		if opp_move == 1:
			l.append(0)
		else:
			alt = 1
			l.append(1)
		
		alt_ochist = tuple(l)

		#records previous round with new opponent choice. If it is an unseen option, make new dictionary entry
		#records (prev_my_move,prev_opp_move,current_opp_move)
		if t in self.outcome_history:
			if self.outcome_history[t] < 3:
				self.outcome_history[t] += 1 #records previous opponent move with current choice
			#an opponent has repeated the same strategy 3 times, record it as a permanent strategy
			if self.outcome_history[t] == 3 and l_t not in self.opponent_strategies:
				self.opponent_strategies[l_t] = opp_move
		else:
			self.outcome_history[t] = 0

		#if i recorded an opponent strategy, but they did the opposite
		#then decrement their promotion count by 1
		if l_t in self.opponent_strategies and self.opponent_strategies[l_t] == alt:
			self.outcome_history[alt_ochist] -= 1
			#if a permanent strategy fails 3 times in a row, delete it from learned strategies
			if self.outcome_history[alt_ochist] == 0:
				del self.opponent_strategies[l_t]

		if l_t in self.opponent_strategies:
			opponent_choice = self.opponent_strategies[l_t]
			if opponent_choice == 1:
				return 1
			else:
				return 0
		#only updated schema if pure strategy cannot be found
		self.update_schema()

		likely_opponent_choice = self.opponent_schema[l_t]
		if likely_opponent_choice > .6:
			return 0
		else:
			return 1
		#OK NOW WE HAVE TO TAKE CARE OF PROBABILISTIC ONES

	def update_schema(self):
		print("updating schema")
		alpha = 0.75
		lead_to_collude = 0
		lead_to_betray = 0
		i = 0
		for i in range(len(self.move_history)-1):
			if self.move_history[i] == self.move_history[-1]:
				if self.move_history[i+1][1] == 0:
					lead_to_collude += 1 * (i/len(self.move_history))
				else:
					print("i got betrayed")
					lead_to_betray += 1 * (i/len(self.move_history))
		total = lead_to_collude + lead_to_betray
		if total > 0:
			self.opponent_schema[self.move_history[-1]] = lead_to_collude/total

	def printall(self):
		print("")
		print("SCHEMA: ", self.opponent_schema)
		print("KNOWN STRAT: ", self.opponent_strategies)
		print("outcome_history: ", self.outcome_history)
		print("move_history: ", self.move_history)
		print("")


class simplePrediction():
	def __init__(self):
		self.opponent_dict = {}

	def decision(self):
		#if options are tied, will assume that they will collude (0)
		if len(self.opponent_dict) == 0:
			return 0
		Keymax = max(self.opponent_dict, key=self.opponent_dict.get)
		if Keymax == 0:
			return 0
		else:
			return 1

	def record(self,opp_move,my_move):
		if opp_move in self.opponent_dict:
			self.opponent_dict[opp_move] += 1
		else:
			self.opponent_dict[opp_move] = 0

class poke():
	def __init__(self):
		self.title = "DBS"
		self.move_history = []
		self.outcome_history = {}
		self.opponent_schema = {(0,0): 1,(0,1): 1,(1,0): 0,(1,1): 0} #probabilistic
		self.opponent_strategies = {} #known
		self.cur_opponent_name = ""
		self.test_phase_counter = 0
		self.collude_tracker = 0
		self.collude_limit = 3
		self.betray_test = False
		self.betray_tracker = 0 #could have gotten 3 points if continued to collude
		self.potential_points = 0
		self.betray_probability = 1
		self.test_limit = 3

	def decision(self):
		#not sure if i need this., think we make a new player each round
		if 1 == 0:
			self.move_history = []
			self.outcome_history = {} #takes previous moves as key, and current move as value
			self.opponent_schema = {(0,0): 1,(0,1): 1,(1,0): 0,(1,1): 0} #these are probabilistic
			self.opponent_strategies = {} #these are known strategies
			self.test_phase_counter = 0
			return 0
		else:
			if len(self.move_history) == 0:
				return 0
			last_move = self.move_history[-1]
			if last_move in self.opponent_strategies:
				if self.opponent_strategies[last_move] == 0:
					#if I am not already in the middle of betray testing and my conditions have been met
					if self.betray_test == False and self.collude_tracker == self.collude_limit:
						b = random.randint(0,100)
						if b <= betray_probability * 100:
							self.collude_tracker = 0
							self.betray_test = True
							self.betray_tracker = 0
							return 1
					else:
						return 0
				else:
					return 1
			else:
				collude_probability = self.opponent_schema[last_move]
				if collude_probability > .6:
					if self.collude_tracker == 3:
						self.betray_test = True
						self.betray_tracker = 0
						return 1
					return 0
				else:
					return 1

	def record(self,opp_move,my_move):
		#add test phase recording here l0l
		#FIRST. TO TAKE CARE OF 100% STRATEGIES:
		#takes care of the first round

		if self.betray_test == True:
			self.betray_tracker += 1
			if opp_move == 0 and my_move == 0:
				self.potential_points + 1
			elif opp_move == 0 and my_move == 1:
				self.potential_points + 2
			if self.betray_tracker == self.test_limit:
				self.collude_tracker = 0
				self.betray_test = False
				self.betray_tracker = 0
				#if i did well. make it more likely to betray more often
				if self.potential_points > 3:
					if self.betray_probability < 1:
						self.betray_probability += .1
					if self.collude_limit > 0:
						self.collude_limit = self.collude_limit - 1
					if self.test_limit > 0:
						self.test_limit -= 1
				else:
				#if test went badd, make it less likely and less often to betray
					if self.betray_probability > 0:
						self.betray_probability = self.betray_probability - .1
					if self.test_limit < 3:
						self.test_limit += 1
					if self.collude_limit < 3:
						self.collude_limit += 1
				self.potential_points = 0

		if opp_move == 0:
			self.collude_tracker += 1
		else:
			self.collude_tracker = 0

		#if self.collude_tracker >= self.collude_limit:
	#		self.betray_test = True
	#		self.betray_tracker = 0

		if len(self.move_history) == 0:
			self.move_history.append((my_move,opp_move))
			return
		#current timeline
		self.move_history.append((my_move,opp_move))

		l = list(self.move_history[-1])
		print("aa",l)
		l_t = tuple(l)
		l.append(opp_move)
		print("bb",l)
		t = tuple(l)

		#alternate timeline
		alt = 0
		alt_ochist = []
		if opp_move == 1:
			l.append(0)
		else:
			alt = 1
			l.append(1)
		
		alt_ochist = tuple(l)

		#records previous round with new opponent choice. If it is an unseen option, make new dictionary entry
		#records (prev_my_move,prev_opp_move,current_opp_move)
		if t in self.outcome_history:
			if self.outcome_history[t] < 3:
				self.outcome_history[t] += 1 #records previous opponent move with current choice
			#an opponent has repeated the same strategy 3 times, record it as a permanent strategy
			if self.outcome_history[t] == 3 and l_t not in self.opponent_strategies:
				self.opponent_strategies[l_t] = opp_move
		else:
			self.outcome_history[t] = 0

		#if i recorded an opponent strategy, but they did the opposite
		#then decrement their promotion count by 1
		if l_t in self.opponent_strategies and self.opponent_strategies[l_t] == alt:
			self.outcome_history[alt_ochist] -= 1
			#if a permanent strategy fails 3 times in a row, delete it from learned strategies
			if self.outcome_history[alt_ochist] == 0:
				del self.opponent_strategies[l_t]


		if l_t in self.opponent_strategies:
			opponent_choice = self.opponent_strategies[l_t]
			if opponent_choice == 1:
				return 1
			else:
				return 0
		#only updated schema if pure strategy cannot be found
		self.update_schema()

		likely_opponent_choice = self.opponent_schema[l_t]
		if likely_opponent_choice > .6:
			return 0
		else:
			return 1
		#OK NOW WE HAVE TO TAKE CARE OF PROBABILISTIC ONES
	def update_schema(self):
		print("updating schema")
		alpha = 0.75
		lead_to_collude = 0
		lead_to_betray = 0
		i = 0
		for i in range(len(self.move_history)-1):
			if self.move_history[i] == self.move_history[-1]:
				if self.move_history[i+1][1] == 0:
					lead_to_collude += 1 * (i/len(self.move_history))
				else:
					print("i got betrayed")
					lead_to_betray += 1 * (i/len(self.move_history))
		total = lead_to_collude + lead_to_betray
		if total > 0:
			self.opponent_schema[self.move_history[-1]] = lead_to_collude/total

	def printall(self):
		print("")
		print("SCHEMA: ", self.opponent_schema)
		print("KNOWN STRAT: ", self.opponent_strategies)
		print("outcome_history: ", self.outcome_history)
		print("move_history: ", self.move_history)
		print("")



simple = poke()
dibbs = DBS()
rounds = 10
p1_points = 0
p2_points = 0
for i in range(rounds):
	dibbs.printall()
	simple_choice = simple.decision()
	dibbs_choice = dibbs.decision()
	if simple_choice == 0 and dibbs_choice == 0:
		p1_points += 1
		p2_points += 1
	elif simple_choice == 1 and dibbs_choice == 0:
		p1_points += 2
	elif dibbs_choice == 1 and simple_choice == 0:
		p2_points += 2

	print("Current score: ", p1_points, p2_points)
	simple.record(dibbs_choice,simple_choice)
	dibbs.record(simple_choice,dibbs_choice)