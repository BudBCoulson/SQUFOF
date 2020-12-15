from sympy.ntheory.primetest import is_square
from sympy import sqrt
import math
import os

os.system('')

def squfof(N):
	#n must not be prime or a perfect square
	
	#start at home basis of Q_1(x,y) = x**2 - ny**2
	#follow the river until it borders a perfect square, a**2 (across -c)
	#"spread the square" to another river segm. with same discrim.: a**2->ac, c->a
	#follow the river again to an ambiguous segment, should border some prime factors
	
	left, top, bottom, right = 1-N, 1, -N, 1-N
	seen = set()
	
	'''
	#slow version that goes 1 step at a time along river
	
	#follow the river to square
	while top == 1 or not is_square(top):
		print('river:')
		display_cell(left,top,bottom,right)
		if right < 0:
			left, bottom = bottom, right 
		else:
			left, top = top, right
		right = 2*(bottom+top)-left
			
	
	#spread the square
	print('to spread:')
	display_cell(left,top,bottom,right)
	a, b, c = sqrt(top), left-(top+bottom), -bottom
	top, bottom = a*c, -a
	left, right = top+bottom+b, top+bottom-b
	print('spreaded')
	display_cell(left,top,bottom,right)
	
	#follow the river to ambigious segment
	while left != right:
		print('river2')
		display_cell(left,top,bottom,right)
		if right < 0:
			left, bottom = bottom, right 
		else:
			left, top = top, right
		right = 2*(bottom+top)-left
	
	#did it work?
	print('ambig')
	display_cell(left,top,bottom,right)		
	if top * bottom == -n:
		return top, -bottom
	
	#'''
	t = cell_type(left,right)
	
	#fast version that uses quadratic formula to jump to bends directly
	while top == 1 or not is_square(top):
		if (left,top,bottom,right) in seen:
			print('no square found')
			return False
		else:
			seen.add((left,top,bottom,right))
			print(len(seen))
			
		print('looking for square')
		display_cell(left,top,bottom,right)
		if t:
			left, top, bottom, right = incr_bend(left, top, bottom, right)
			t = cell_type(left,right)
		else:
			left, top, bottom, right = jump_to_bend(left, top, bottom, right)
			t = True
	
	print('to spread')
	display_cell(left,top,bottom,right)		
	a, b, c = sqrt(top), (top+bottom)-left, -bottom
	top, bottom = a*c, -a
	left, right = top+bottom-b, top+bottom+b
	print('spreaded')
	display_cell(left,top,bottom,right)
	
	seen = set()
	t = cell_type(left,right)
	
	while True:
		if (left,top,bottom,right) in seen:
			print('not type H')
			return False
		else:
			seen.add((left,top,bottom,right))
			print(len(seen))
		
		print('looking for ambiguous')
		display_cell(left,top,bottom,right)	
		
		if t:
			left, top, bottom, right = incr_bend(left, top, bottom, right)
			t = cell_type(left,right)
		else:
			h = top + bottom - left
			up = left < 0
			region = top if up else bottom
			aregion = top + bottom - region
			
			if h > 0 or h % (2*region):
				left, top, bottom, right = jump_to_bend(left, top, bottom, right)
				t = True
				
			else:
				print('found ambiguous')
				
				s = lambda n: region*n**2+h*n+aregion
				n = -h // (2*region)
				
				left, right = s(n-1), s(n+1)
				top, bottom = s(n), region
				if up:
					top, bottom = bottom, top
				
				display_cell(left,top,bottom,right)
				
				print(N,-top*bottom)
				return N == -top*bottom
				

	#'''
		
def jump_to_bend(e,u,v,f):
	
	h = u + v - e
	
	if e < 0 and f < 0:
		up = True
		q, c = u, v
	
	elif e > 0 and f > 0:
		up = False
		q, c = v, u
		
	s = lambda n: q*n**2+h*n+c
	
	if q > 0:
		n = math.ceil((-h+sqrt(h**2-4*u*v))/(2*q))
	else:
		n = math.ceil((-h-sqrt(h**2-4*u*v))/(2*q))
	
	#l = s(n-2)
	#if up:
	#	return l, u, l+(2*n-3)*u+h, l+(4*n-4)*u+2*h
	#else:
	#	return l, l+(2*n-3)*v+h, v, l+(4*n-4)*v+2*h
	
	l,m,r = s(n-2), s(n-1), s(n)
	if up:
		return l, u, m, r
	else:
		return l, m, v, r
	
def incr_bend(e,u,v,f):
	
	h = u + v - e
	
	if e < 0 < f:
		return u, u+v+h, v, u+4*v+2*h
		
	elif e > 0 > f:
		return v, u, u+v+h, 4*u+v+2*h
		
def cell_type(left, right):
	#True for bends, False for region boundaries		
	return left < 0 < right or left > 0 > right

def next_cell(left, top, bottom, right):		
	if left < 0 < right or left > 0 > right:
		print('incr')
		return incr_bend(left, top, bottom, right)
	else:
		print('jump')
		return jump_to_bend(left, top, bottom, right)
		
def display_cell(e,u,v,f):
	el,ul,vl,fl = len(str(e)),len(str(u)),len(str(v)),len(str(f))
	dsh = max(ul,vl)
	ms,ex = divmod(dsh-min(ul,vl),2)
	
	topnumstr, botnumstr = str(u), str(v)
	if ul < dsh:
		topnumstr = ' '*(ms+ex)+topnumstr+' '*ms
	else:
		botnumstr = ' '*(ms+ex)+botnumstr+' '*ms
	
	OKBLUE = '\033[94m'
	ENDC = '\033[0m'
	
	dashes = OKBLUE + '-'*dsh + ENDC
	tlsep,trsep,blsep,brsep = '\\', '/', '/', '\\'
	
	if e < 0:
		tlsep = OKBLUE + tlsep + ENDC
	else:
		blsep = OKBLUE + blsep + ENDC
		
	if f < 0:
		trsep = OKBLUE + trsep + ENDC
	else:
		brsep = OKBLUE + brsep + ENDC
	
	print(' '*el+tlsep+topnumstr+trsep)
	print(str(e)+' '+dashes+' '+str(f))
	print(' '*el+blsep+botnumstr+brsep)

#'''
odd = [15,21,33,35,39,51,55,57,65,69,77,85,87,91,95,111,115,119]
even = [6,10,14,22,26,34,38,46,58,62,74,82,86,94,106,118]
works = []

for num in odd+even:
	if squfof(num):
		works.append(num)
	print()

print(works)
'''

fdprimes = {10007,10009,10039,10061,10069,10091,10093,10099}

works = []

for num in {x*y for x in fdprimes for y in fdprimes if x < y}:
	if squfof(num):
		works.append(num)

print(works)
'''

#squfof((10**17-1)//9)
