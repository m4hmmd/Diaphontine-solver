#ISSUES
#1: there is no explicit way we define mods_to_check

#2.0: can't solve equations with more than 1 solution (and probably with no solution at all too)
#   Solution: fix the line with *1

#2.1: we can 'attempt to solve' (that is, attempt to derive new information) only once.
#This is going to create problems when trying to solve equations with more than two solutions (where we will find the variables step-by-step)
#   Solution: wrap the 'attempt' part into a function and call it repeatedly (*2)
from fractions import gcd

# DISCLAIMER: The current version can solve only the terms all of whose variables are prime numbers, and that have only 1 solution.
# the terms is entered in the form sum(a_i(x_i)^y_i) = 0
# we will use a problem from JBMO 2014 as an example:
# 1. Find all triples of primes (p,q,r) satisfying 3p^4-5q^4-4r^2=26

terms = [] #stores all terms
mods_to_check = [2, 3, 5] # NOTE perhaps start with [2, 3] and add primes if the unknowns are not found

def is_prime(n):
    for t in range(2, n):
        if n % t == 0: return False
    else: return True #didn't need it, really

class Term(object):
    def __init__(self, coeff, power, is_prime):
        self.coeff = coeff
        self.power = power
        self.is_prime = is_prime
        self.residues = {} #stores the possible residues this term could be congruent modulo (mod)
        for mod in mods_to_check:
            ress = []
            for t in range(0, mod):
                residue = (coeff*pow(t, power)) % mod
                ress.append(residue)
            self.residues[mod] = list(set(ress)) #remove duplicates
        terms.append(self)
    def __str__(self):
        return "(" + str(self.coeff) + ", " + str(self.power) + ", " + str(self.is_prime) + ")"
    def __repr__(self):
        return self.__str__()

#specifying the terms
first = Term(3, 4, True)
second = Term(-5, 4, True)
third = Term(-4, 2, True)
fourth = Term(-26, 0, False)

'''
#JBMO 2015 problem 1. Has 2 solutions, so the program fails.
first = Term(1, 2, True)
second = Term(1, 2, True)
third = Term(16, 2, True)
fourth = Term(-9, 2, True)
fifth = Term(1, 0, False)
'''
solution = ['na' for i in range(len(terms))] #stores the single solution tuple

possible_residues = []

def find_possble_residue_configs(mod, n):
    if n > 1:
        for y in terms[n-1].residues[mod]:
            case_under_consideration.append(y)
            find_possble_residue_configs(mod, n-1)
            del case_under_consideration[len(case_under_consideration) - 1]
    elif n == 1:
        for x in terms[n-1].residues[mod]:
            case_under_consideration.append(x)
            if sum(case_under_consideration) % mod == 0:
                #create a new inverted (except for the first element) copy of the list
                possible_residues.append([case_under_consideration[0]] + list(reversed(case_under_consideration[1:])))
            del case_under_consideration[len(case_under_consideration) - 1]

for mod in mods_to_check:
    case_under_consideration = [mod]
    find_possble_residue_configs(mod, len(terms))
print(possible_residues)

'''
#the basic logic of the above recursive function
#not universal; only works for 4 variables
for mod in mods_to_check:
    for x1 in first.residues[mod]:
        for x2 in second.residues[mod]:
            for x3 in third.residues[mod]:
                for x4 in fourth.residues[mod]:
                    if (x1 + x2 + x3 + x4) % mod == 0:
                        possible_residues.append([mod, x1, x2, x3, x4])
print(possible_residues)
'''

for i in range(-1, len(possible_residues)-1): # *2
    if possible_residues[i-1][0] != possible_residues[i][0] and possible_residues[i][0] != possible_residues[i+1][0]: # *1
        #this means that there is only one possible case when looking mod 'possible_residues[i][0]'
        #ISSUE 2: this doesn't have all the cases. what if there are multiple configs when looking mod 3,
        #      but in both od them, some variable must be equalt to, say, 3?
        for j in range(1, len(terms) + 1):
            if possible_residues[i][j] == 0 and terms[j-1].coeff % possible_residues[i][0] != 0:
                #since all variables are prime, if a term is divisible by some prime and
                #  its coefficient is not, then the variable must be equal to that prime
                print("EUREKA! " + str(terms[j-1]) + " is " + str(possible_residues[i][0]))
                solution[j-1] = possible_residues[i][0]
                terms[j-1].coeff *= possible_residues[i][0]**terms[j-1].power
                terms[j-1].power = 0

unknown_terms = []
for t in terms:
    if t.power != 0: unknown_terms.append(t)
# if there is only one unknown left in the equation, we can calculate it
if len(unknown_terms) == 1:
    x = 0
    for known in terms:
        if known not in unknown_terms:
            x -= known.coeff
    y = pow(x / unknown_terms[0].coeff, 1.0/unknown_terms[0].power)
    for i in range(0, len(solution)):
        if solution[i] == 'na':
            solution[i] = int(y)
            break
    unknown_terms[0].coeff = x
    unknown_terms[0].power = 0

# if all unknowns are found, output the solution
if len(unknown_terms) == 0:
    print(solution)

print(terms)
print("Solution: " + str(solution))
