# PrisonersDilemma

To run the code: 
  main.py and strategies.py need to be in the same directory
 
0 = Loyal, 1 = Betray
Game mechanics (p1,p2):
  1. 0 = Loyal, 1 = Betray
  2. Keeps tracks of player points seperately
  3. if p1 == 0 and p2 == 0, both players get 1 point
  4. if p1 == 0 and p2 == 1, player 1 gets 0 points and player 2 gets 2 points
  5. if p1 == 1 and p2 == 0, player 1 gets 2 points and player 2 gets 0 points
  6. if p1 == 1 and p2 == 1, both players get 0 points
 
Currently the following strategies are implemented:
  1. 'al' : always loyal - returns 0
  2. 'ab' : always betray - returns 1
  3. 'rb' : random betray - betrays at a set probability (default = 50%) current probability not able to be changed
  4. 'nice': custom strategy - Looks at opponent history and returns 0 if opponent has returned 0 for more than 70% of their past decisions
  5. 'repeat': cusom strategy - If opponent chose 0 previous round, chooses what it chose that round, else randomly returns 0,1 (p=50%)
  6. 'tft': tit for tat - returns opponents previous strategy

Command line argument:
  >python main.py <p1 strat> <p2 strat> (refer to list above for strategy names)
  
  e.g.
    > python main.py tft ab || p1 = tit for tat, and p2 = always betray. They will play 100 rounds
