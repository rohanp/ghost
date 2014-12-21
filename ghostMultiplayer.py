##########################################
# 	 ____       _                    #
#	|  _ \ ___ | |__   __ _ _ __     #
#	| |_) / _ \| '_ \ / _` | '_ \    #
#	|  _ < (_) | | | | (_| | | | |   #
#	|_| \_\___/|_| |_|\__,_|_| |_|   #
#		Period 1		 #
#		12/9/14			 #
##########################################
#Created by Rohan Pandit. Do not use without permission

import sys
from time import clock
from random import random
from itertools import zip_longest
import pickle
import sys
from time import sleep

players=list(input("Input H for human, C for computer, in the desired order \n"))
N=len(players)

class Node:
	def __init__(self,value):
		self.val=value
		self.children={}

	def insert(self, s):
		if len(s)<1:
			self.children['$']=Node('$')

		elif s[0] in self.children:
			self.children[s[0]].insert(s[1:])

		else:
			p=Node(s[0])
			self.children[s[0]]=p
			p.insert(s[1:])

	def mustSpellWord(self):
		if 1==len(self.children.keys()):
			lastLetter = list(self.children.values())[0]
			if 1==len(lastLetter.children) and '$'==list(lastLetter.children.keys())[0]:
				return True
		return False

def loser(root, player):
	nextPlayer = player+1
	if nextPlayer > N:
		nextPlayer=1

	if root.mustSpellWord():
		return nextPlayer

	for o in root.children.values():
		if loser(o, nextPlayer) != nextPlayer:
			return player

	return nextPlayer

def computerMove(root, s, player):
	options = list(root.children.values())
	for o in options:
		if '$' not in o.children.keys():
			choice=o.val
			break
	else:
		choice=options[0].val
	s += choice
	print("Computer chooses character %s"%choice)
	root = root.children[choice]

	if '$' in root.children and len(s)>3:
		print("Computer loses!", s, " is a word.")
		exit()

	print("word: %s \n"%s)
	return root, s

def humanMove(root, s, player):
	c=input("Human Turn. Enter a charater: ").lower()[0]
	#print(root)
	while c == '?':
		start=clock()
		validMoves = ', '.join(root.children.keys())
		print("valid moves = ", validMoves,)
		print("calculated in ", clock()-start, "s \n")

		start=clock()
		times=[]
		validMoves=root.children.values()

		for o in validMoves:
			miniStart=clock()
			if player != loser(o,player):
				times.append(1000)
			else:
				times.append(round((clock()-miniStart)*10000, 2))

		validMoves=[move.val for move in validMoves]
		sortedMoves = ', '.join([move for (t, move) in reversed(sorted(zip(times,validMoves)))])
		print("sorted valid moves ", sortedMoves)
		print("calculated in ", clock()-start, '\n')

		start=clock()
		validMoves=root.children
		optimalMoves = [o.val for o in validMoves.values() if loser(o, player) != player]
		optimalMoves = ', '.join(list(optimalMoves))
		print("optimal moves = ", optimalMoves)
		print("calculated in ", clock()-start, "s \n")
		c=input("Human Turn. Enter a charater: ").lower()[0]
	s+=c

	choice = root.children[c]
	if '$' in choice.children.keys() and len(s)>3:
		print("Human loses. %s is a word"%s)
		exit()
	elif not c in root.children:
		print("Human loses. No words begin in %s"%s)
		exit()
	else:
		print("word: %s \n"%s)
		root=root.children[s[len(s)-1]]
		return root, s

def main():
	f = open("ghostDictionary.txt")
	root=Node('*')
	for line in f:
		s = line.lower().strip()
		if 3<len(s):
			root.insert(line.lower().strip())

	f.close()
	s=''

	while True:
		for i,p in enumerate(players):
			if p == 'H':
				root, s= humanMove(root, s, i)
			elif p == 'C':
				root, s= computerMove(root,s, i)
			else:
				print("you broke the game.")
				exit()

if __name__ == '__main__':
	main()
