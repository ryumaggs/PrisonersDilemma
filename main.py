import strategies as s
import sys
import random
import statistics
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def frame(p1,p2,style="onevone",num_rounds=100, noise1 = 0.1, noise2 = 0.1):
	if style == "onevone":
		i = 0
		p1_points = 0
		p2_points = 0
		while i < num_rounds:
			#print("-------Round " + str(i) + "----------")
			p1_d = p1.decision()
			p2_d = p2.decision()

			# Add noise
			p1_d = p1_d if random.random() > noise1 else 1 - p1_d
			p2_d = p2_d if random.random() > noise2 else 1 - p2_d

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
		return 3,3
	if p1 == 0 and p2 == 1:
		return 0,5
	if p1 == 1 and p2 == 0:
		return 5,0
	return 1,1

def main():
	'''please enter all new strats created into the strats dictionary with the name
	of the strat and s.strat_name()'''

	rounds = 100

	result = [] # an array of [s1,s2,p1,p2] strat of p1, p2, and point results in a game respectively
	
	strats = {'ab':s.alwaysBetray(), 'al':s.alwaysLoyal(), 'tft':s.titfortat(),
			  'rb':s.randomBetray(), 'grudger':s.grudger(), 'nice':s.niceness(),
			  'repeat':s.repeat(),'markov':s.markov(),'mtft':s.mtitsfortat(),'tfnt':s.titforntats()}
	results = {}
	noises = list(range(0,11,1))

	strat_names = list(strats.keys()) #list of all strat names.
	for strat in strat_names:
		results[strat] = [[] for x in noises]


	#two for loops to do all possible combinations
	# j =i at the start of each j loop to prevent redundant pairings
	for i in range(len(strat_names)):
		for j in range(i,len(strat_names)):
			p1 = strats[strat_names[i]]   #strat of p1
			p2 = strats[strat_names[j]]   # strat of p2
			#print("trying", strat_names[i], " vs ", strat_names[j])
			for noise in noises:
				res = frame(p1,p2,num_rounds=rounds,noise1 = noise/10.0, noise2 = noise/10.0)
				results[strat_names[i]][noise]+=[1.0*res[0]/rounds]
				results[strat_names[j]][noise]+=[1.0*res[1]/rounds]
			result += [[strat_names[i], strat_names[j]] + frame(p1,p2, "onevone",)]

	# Get values from each test
	for noise in noises:
		fig, ax = plt.subplots()
		boxData = [results[strat][noise] for strat in strat_names]
		ax.boxplot(boxData)
		ax.set_xticklabels(strat_names,rotation=45)
		ax.set_xlabel('Strategy')
		ax.set_ylabel('Average score')
		ax.set_title("Prisoner's Dilemma " + str(noise*10) + "% Noise Tournament")

	fig, ax = plt.subplots(figsize=(10,6))

	NUM_COLORS = len(strats.keys())

	cm = plt.get_cmap('gist_rainbow')
	ax.set_prop_cycle(color=[cm(i/3*3.0/NUM_COLORS) for i in range(NUM_COLORS)],
		marker=['.',',','o','v','^','1','2','8','s','p','P','*','h','H','+','x','d'][:NUM_COLORS])

	for strat in strat_names:
		kwargs = dict(ecolor='k', capsize = 2, elinewidth = 1.1,linewidth=0.6,ms=7)
		y = [statistics.mean(res) for res in results[strat]]
		x = [noise/10.0 for noise in noises]
		yErr = [statistics.pstdev(res) for res in results[strat]]
		ax.errorbar(x,y,yerr=yErr,**kwargs,label = strat)

		ax.legend(loc='best',frameon=False,ncol=int(len(strats.keys())/2 if len(strats.keys())%2==0 else (len(strats.keys())+1)/2))

	ax.set_title("Prisoner's Dilemma Overall Tournament", fontsize=14)
	ax.set_xlabel('Noise',fontsize=12)
	ax.set_ylabel('Score',fontsize=12)




	plt.show()

		 

	# for i in range(len(result)):
	# 	print("Result of " + str(result[i][0])
	# 		  + " vs " + str(result[i][1]) + " : P1 = " + str(result[i][2]) + " || P2 = " + str(result[i][3]))

	#print(result)
main()