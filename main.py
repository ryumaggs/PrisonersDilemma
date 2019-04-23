import strategies as s
import sys


def frame(p1,p2,style="normal",num_rounds=100):
	if style == "onevone":
		i = 0
		p1_points = 0
		p2_points = 0
		while i < num_rounds:
			#print("-------Round " + str(i) + "----------")
			p1_d = p1.decision()
			p2_d = p2.decision()
			p1_p,p2_p = points(p1_d,p2_d)
			p1.record(p2_d,p1_d)
			p2.record(p1_d,p2_d)
			p1_points += p1_p
			p2_points += p2_p
			#print("P1 chose:", p1_d)
			#print("P2 chose:", p2_d)
			#print(" ")
			i += 1

		#print("Final point tally: P1 = " + str(p1_points) + "|| P2 = " + str(p2_points))
	#return an array of p1 points and p2 points
	return [p1_points, p2_points]

def points(p1,p2):
	if p1 == 0 and p2 == 0:
		return 1,1
	if p1 == 0 and p2 == 1:
		return 0,2
	if p1 == 1 and p2 == 0:
		return 2,0
	return 0,0

def main():
	'''please enter all new strats created into the strats dictionary with the name
	of the strat and s.strat_name()'''

	result = [] # an array of [s1,s2,p1,p2] strat of p1, p2, and point results in a game respectively



	strats = {'ab':s.alwaysBetray(), 'al':s.alwaysLoyal(), 'tft':s.titfortat(),
			  'rb':s.randomBetray(), 'grudger':s.grudger(), 'nice':s.niceness(),
			  'repeat':s.repeat()}

	strat_names = list(strats.keys()) #list of all strat names.

	#two for loops to do all possible combinations
	# j =i at the start of each j loop to prevent redundant pairings

	for i in range(len(strat_names)):
		for j in range(i,len(strat_names)):
			p1 = strats[strat_names[i]]   #strat of p1
			p2 = strats[strat_names[j]]   # strat of p2
			#print("trying", strat_names[i], " vs ", strat_names[j])
			result += [[strat_names[i], strat_names[j]] + frame(p1,p2, "onevone")]



	'''temp = sys.argv[1:]
	p1 = strats[temp[0]]
	p2 = None
	if "rest" == temp[1]:
		return
	else:
		p2 = strats[temp[1]]

	result += [frame(p1,p2, "onevone")]
	print("Final point tally of " +str(result[0][0])
		  +" vs " +str(result[0][1]) +" : P1 = " + str(result[0][2]) + "|| P2 = " + str(result[0][3]))'''
	for i in range(len(result)):
		print("Result of " + str(result[i][0])
			  + " vs " + str(result[i][1]) + " : P1 = " + str(result[i][2]) + " || P2 = " + str(result[i][3]))

	#print(result)
main()