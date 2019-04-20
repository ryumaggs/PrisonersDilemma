import strategies as s
import sys


def frame(p1,p2,style="normal",num_rounds=100):
	if style == "onevone":
		i = 0
		p1_points = 0
		p2_points = 0
		while i < num_rounds:
			print("-------Round " + str(i) + "----------")
			p1_d = p1.decision()
			p2_d = p2.decision()
			p1_p,p2_p = points(p1_d,p2_d)
			p1.record(p2_d,p1_d)
			p2.record(p1_d,p2_d)
			p1_points += p1_p
			p2_points += p2_p
			print("P1 chose:", p1_d)
			print("P2 chose:", p2_d)
			print(" ")
			i += 1

		print("Final point tally: P1 = " + str(p1_points) + "|| P2 = " + str(p2_points))
	return 0

def points(p1,p2):
	if p1 == 0 and p2 == 0:
		return 1,1
	if p1 == 0 and p2 == 1:
		return 0,2
	if p1 == 1 and p2 == 0:
		return 2,0
	return 0,0
def main():
	strats = {'ab':s.alwaysBetray(), 'al':s.alwaysLoyal(), 'tft':s.titfortat(), 'rb':s.randomBetray(), 'grudger':s.grudger(), 'nice':s.niceness(), 'repeat':s.repeat()}
	temp = sys.argv[1:]
	p1 = strats[temp[0]]
	p2 = None
	if "rest" == temp[1]:
		return
	else:
		p2 = strats[temp[1]]
	frame(p1,p2)
main()