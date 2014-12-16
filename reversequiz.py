#############################
#        Rohan Pandit       #
#          Period 1         #
#          12/4/14          #
#############################

def reverseLst(Lst1):
	#This function is just one line, why not just put it in main?
	#Why bother with all these messy indicies instead of just using clean, fast, built in methods?
	#It is unclear whether Lst1 modfified when you put it in a method
	return [Lst1[i] for i in range(len(Lst1)-1,-1,-1)]
#-------------------------------------------------------------------------------------------------

def main():
	#-- Method 1. Use the built-in reverse function.
	Lst1= [1,2,3,4,5,]
	Lst2 = Lst1[:]
	Lst2.reverse()
	print('Method 1. ', Lst1, Lst2)
	#-------------------------------------------------------------------

	#-- Method 2. Use the built-in reversed function.
	Lst1= [1,2,3,4,5,]
	Lst2= list(reversed(Lst1))
	print('Method 2. ', Lst1, Lst2)

	#-------------------------------------------------------------------
	#-- Method 3. Use slicing only.
	Lst1= [1,2,3,4,5,]
	Lst2= Lst1[::-1]
	print('Method 3. ',Lst1, Lst2)

	#-------------------------------------------------------------------
	#-- Method 4. Use a loop that works on this swap principle: a,b = b,a.
	Lst1= [1,2,3,4,5,]
	Lst2= Lst1[:]
	L= len(Lst1)
	for i in range(L):
		Lst2[i],Lst2[L-1-i] = Lst1[L-1-i], Lst1[i]
	print('Method 4. ',Lst1,Lst2)

	#-------------------------------------------------------------------
	#-- Method 5. Use a loop (not a comprehension) that runs backward and copies each element.
	Lst1= [1,2,3,4,5,]
	Lst2= []
	for i in range(L-1,-1,-1):
		Lst2.append(Lst1[i])
	print('Method 5. ', Lst1, Lst2)

	#-------------------------------------------------------------------
	#-- Method 6. Same as method 5, except it uses a list comprehension.
	Lst1 = [1,2,3,4,5,]
	Lst2 = [Lst1[i] for i in range(L-1,-1,-1)]
	print('Method 6. ', Lst1, Lst2)

	#-------------------------------------------------------------------
	#-- Method 7. This time, place method 6 in a function. Anticipate what you can be criticized for even if your function works perfectly.
	Lst1 = [1,2,3,4,5,]
	Lst2 = reverseLst(Lst1)
	print('Method 7. ', Lst1, Lst2)

if __name__ == '__main__':
	main()

####################################################################################

