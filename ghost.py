import sys
from time import clock
import itertools
from random import random

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

	def search(self, s):
		return self.searchHelper(s+'$')

	def searchHelper(self, s):
		if s=='$':
			return True
		try:
			if s[0] in self.children:
				return self.children[s[0]].searchHelper(s[1:])
		except IndexError:
			return False
		return False

	"""boring search
	def search(self, s):
		if '$':
			return True
		elif s[0] in self.children:
			return self.children[s[0]].searchHelper(s[1:])

		return False

	"""

	def searchFrag(self, s):
		if s=='':
			return True

		if s[0] in self.children:
			return self.children[s[0]].searchFrag(s[1:])

		return False

	def getFrag(self, s):
		if s[0] in self.children:
			if s[1:] == '':
				return self
			else:
				return self.children[s[0]].searchFrag(s[1:])
		return null

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
		for i in xrange(display_width):
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

	for line_list in itertools.izip_longest(*split_blocks, fillvalue=None):
		for i, line in enumerate(line_list):
			if line is None:
				builder.append(' ' * block_lens[i])
			else:
				builder.append(line)
			if i != len(line_list) - 1:
				builder.append(' ')  # Padding
		builder.append('\n')

	return ''.join(builder[:-1])

def basics():
	root=Node('*')
	root.insert('cat')
	root.insert('catnip')
	root.insert('cats')
	root.insert('catnap')
	root.insert("can't")
	root.insert('cat-x')
	root.insert('dog')
	root.insert('dogs')
	root.insert('dognip')
	print(root)
	print(root.display())
	print(root.search('junk'))
	print(root.search('dogs'))
	print(root.searchFrag('do'))
	print(root.searchFrag('dox'))

def humanMove(root, s):
	c=input("Human Turn. Enter a charater: ").lower()[0]
	#print(root)
	s+=c
	if '$' in root.children and len(s)>3:
		print("Human loses. %s is a word"%s)
		exit()
	elif not c in root.children:
		print("Human loses. No words begin in %s"%s)
		exit()
	else:
		print("word: %s \n"%s)
		root=root.children[s[len(s)-1]]
		return root, s

def computerMove(root, s):
	options = list(root.children.keys())
	#print(options)
	choice = options[0]
	s += choice
	print("Computer chooses character %s"%choice)
	#print(s)
	root = root.children[choice]
	#print(root)

	if '$' in root.children and len(s)>3:
		print("Computer loses!", s, " is a word.")
		exit()

	print("word: %s \n"%s)
	return root, s

def main():
	f = open("ghostDictionary.txt")
	root=Node('*')
	for line in f:
		root.insert(line.lower().strip())

	f.close()
	s=''

	while True:
		root, s= humanMove(root, s)
		root, s= computerMove(root,s)

if __name__ == '__main__':
	main()
