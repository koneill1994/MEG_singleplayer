# script which will generate a math problem of varying difficulty based on user input
# Kevin O'Neill

import random, os, re


########################

## parameters


no_of_levels = 7
# determines the number of difficulty levels

max_digits=1
# the maximum number of digits in a single number

max_terms=7
# the maximum number of numbers one is asked to do operations on


#######################


def ScaleXtoY(x,xmax,ymax,ymin):
  return max(int(round((1.0*x/xmax)*ymax)),ymin)


def GenerateEquationAndAnswer(lvl):
  if lvl == '': lvl = 1
  current_level=int(lvl)
  
  # generate equation & answer
  '''
  terms=ScaleXtoY(current_level,no_of_levels,max_terms,2)
  digits=ScaleXtoY(current_level,no_of_levels,max_digits,1)
  '''
  # simplified as per alex's instructions
  terms = lvl+1
  digits = 1
  
  numbers=[]
  
  for x in range(terms):
    numbers.append(random.randrange(1,10**digits))
  
  
  s=""
  ans=0
  for t in range(len(numbers)):
    
    # add operator (+ or -)
    if t!=0 or numbers[t] < 0 :
      if numbers[t] < 0:
        s+=" - "
      else:
        s+=" + "
    # add number
    s+=str(abs(numbers[t]))
    
    ans+=numbers[t]
    
  eq=s
  correct_ans = ans
  
  return (eq,correct_ans)

