#######################################
# 	 ____       _                    #
#	|  _ \ ___ | |__   __ _ _ __     #
#	| |_) / _ \| '_ \ / _` | '_ \    #
#	|  _ < (_) | | | | (_| | | | |   #
#	|_| \_\___/|_| |_|\__,_|_| |_|   #
#			  Period 1				 #
#			   12/9/14				 #
######################################

import sys
from time import clock
from random import random
from itertools import zip_longest
import pickle
import sys
from time import sleep
from re import match
sys.setrecursionlimit(10000)
N=2

class Node:
	def __init__(self,value):
		self.val=value
		self.children={}

	def __repr__(self):
		self.__str__()
		return ''

	def __str__(self):
		print("\nval = %s"%self.val)
		print("     children: ", end="")
		for c in self.children:
			print(c, end="")
		print("")
		return ''

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

	def display(self):
		if not self.children:
			return self.val

		child_strs = [child.display() for child in self.children.values()]
		child_widths = [block_width(s) for s in child_strs]

		# How wide is this block?
		display_width = max(len(self.val),
					sum(child_widths) + len(child_widths) - 1)

		# Determines midpoints of child blocks
		child_midpoints = []
		child_end = 0
		for width in child_widths:
			child_midpoints.append(child_end + (width // 2))
			child_end += width + 1

		# Builds up the brace, using the child midpoints
		brace_builder = []
		for i in range(display_width):
			if i < child_midpoints[0] or i > child_midpoints[-1]:
				brace_builder.append(' ')
			elif i in child_midpoints:
				brace_builder.append('+')
			else:
				brace_builder.append('-')
		brace = ''.join(brace_builder)

		name_str = '{:^{}}'.format(self.val, display_width)
		below = stack_str_blocks(child_strs)

		return name_str + '\n' + brace + '\n' + below

def block_width(block):
	try:
		return block.index('\n')
	except ValueError:
		return len(block)

def stack_str_blocks(blocks):
	builder = []
	block_lens = [block_width(bl) for bl in blocks]
	split_blocks = [bl.split('\n') for bl in blocks]

	for line_list in zip_longest(*split_blocks, fillvalue=None):
		for i, line in enumerate(line_list):
			if line is None:
				builder.append(' ' * block_lens[i])
			else:
				builder.append(line)
			if i != len(line_list) - 1:
				builder.append(' ')  # Padding
		builder.append('\n')

	return ''.join(builder[:-1])


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

def computerMove(root, s):
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


def humanMove(root, s):
	c=input("Human Turn. Enter a charater: ").lower()[0]

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
			if 1 != loser(o,1):
				times.append(1000)
			else:
				times.append(round((clock()-miniStart)*10000, 2))
		validMoves=[move.val for move in validMoves]
		sortedMoves = ', '.join([move for (t, move) in reversed(sorted(zip(times,validMoves)))])
		print("sorted valid moves ", sortedMoves)
		print("calculated in ", clock()-start, '\n')

		start=clock()
		validMoves=root.children
		optimalMoves = [o.val for o in validMoves.values() if loser(o, 1) != 1]
		optimalMoves = ', '.join(list(optimalMoves))
		print("optimal moves = ", optimalMoves)
		print("calculated in ", clock()-start, "s \n")
		c=input("Human Turn. Enter a charater: ").lower()[0]
	s+=c

	try:
		choice = root.children[c]
	except KeyError:
		print("Human loses. No words begin in %s"%s)
		exit()

	if '$' in choice.children.keys() and len(s)>3:
		print("Human loses. %s is a word"%s)
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
		root, s= humanMove(root, s)
		root, s= computerMove(root,s)

if __name__ == '__main__':
	main()
