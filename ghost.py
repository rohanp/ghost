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
		if self.val:
			return ''
		for c in self.children:
			print(c)

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
	#Words must end in $
		if s=='$':
			return True

		try:
			if s[0] in self.children:
				return self.children[s[0]].search(s[1:])
		except IndexError:
			return False

		return False

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
	"""Takes a list of multiline strings, and stacks them horizontally.

	For example, given 'aaa\naaa' and 'bbbb\nbbbb', it returns
	'aaa bbbb\naaa bbbb'.  As in:

	'aaa  +  'bbbb   =  'aaa bbbb
	 aaa'     bbbb'      aaa bbbb'

	Each block must be rectangular (all lines are the same length), but blocks
	can be different sizes.
	"""

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
	print(root.search('junk$'))
	print(root.search('dogs$'))
	print(root.searchFrag('do'))
	print(root.searchFrag('dox'))

def humanMove(root, s):
	c=input("Human Turn. Enter a charater: ")
	print(c)
	s+=c.lower()[0]
	if root.search(s+'$'):
		print("Human loses. %s is a word"%s)
	elif not root.searchFrag(s):
		print("Human loses. No words begin in %s"%s)
	else:
		print(s)
		root=root.children[s[len(s)-1]]
		return root, s

def computerMove(root, s):
	options = root.children.keys()
	choice = options[0]
	s += choice
	print("Computer chooses character %s"%choice)
	print(s)
	root = root.children[choice]
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
