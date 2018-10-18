# script which will generate a math problem of varying difficulty based on user input
# Kevin O'Neill

import random, os, re


########################

## parameters


no_of_levels = 7
# determines the number of difficulty levels

max_digits=2
# the maximum number of digits in a single number

max_terms=4
# the maximum number of numbers one is asked to do operations on

max_operations=['+','-']
# different operations to be performed on the numbers, in order of increasing difficulty
# all supported is ['+','-','*','/','^']


#######################


def op(a,b,o):
  if o=="^":
    return a**b
  if o=="*":
    return a*b
  elif o=="/":
    return a/b
  elif o=="+":
    return a+b
  elif o=="-":
    return a-b
  else:
    return float.NaN


def do_pemdas_step(eq,step):
  newlist=[]
  c=0
  while c < len(eq):
    if eq[c]==step:
      newlist.pop()
      newlist.append(op(float(eq[c-1]),float(eq[c+1]),step))
      c+=1
    else:
      newlist.append(eq[c])
    c+=1
  return newlist
  
  
def solve(equation):
  eq=re.split('(\D)+',equation)
  
  # remember pemdas
  
  #eq=solve_parens(eq)
  
  for step in ["^","*","/","+","-"]:
    eq=do_pemdas_step(eq,step)
  
  if len(eq) == 1:
    return eq[0]
  else:
    return float.NaN


def ScaleXtoY(x,xmax,ymax,ymin):
  return max(int(round((1.0*x/xmax)*ymax)),ymin)


def GenerateEquationAndAnswer(lvl):
  if lvl == '': lvl = 1
  current_level=int(lvl)
  
  # generate equation & answer
  terms=ScaleXtoY(current_level,no_of_levels,max_terms,2)
  digits=ScaleXtoY(current_level,no_of_levels,max_digits,1)
  operations=max_operations[:ScaleXtoY(current_level,no_of_levels,len(max_operations),1)]
  
  numbers=[]
  ops=[]
  
  for x in range(terms):
    numbers.append(random.randrange(0,10**digits))
  
  for x in range(terms-1):
    ops.append(operations[random.randrange(0,len(operations))])
  
  
  s=""
  for t in range(len(numbers)):
    s+=str(numbers[t])
    if t<len(ops):
      s+=ops[t]
    
  eq=s
  
  
  correct_ans = solve(s)
  
  return (eq,correct_ans)

