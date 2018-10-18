# program that will take a math equation as a string and return the answer
# Kevin O'Neill

import re


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
  
# doesn't work correctly, either fix it or remove it
def solve_parens(eq):
  for x in range(len(eq)):
    if eq[x]=="(":
      depth=0
      for y in range(len(eq[x:])):
        if eq[y]=="(":
          depth+=1
        if eq[y]==")":
          
          depth-=1
          if(depth==0):
            print "a"+eq[:x]
            print "b"+"".join(eq[x+1:y])
            print "b'"+solve("".join(eq[x+1:y]))
            print "c"+eq[y+1:]
            return eq[:x] + solve("".join(eq[x:y])) + eq[y+1:] # base case
  
  # (()())
  
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
