# notes on implementing Camerer's damned EWA function
# (because if you make your papers easy to understand someone might steal your work)

import numpy

# this is a list which stores the weightings of the payoffs, 
# which will be used to calculate the choices
weighted_payoffs = [0]*7
choices=range(1,8)

# Free parameters
# set these more accurately once you've done some model fitting

delta = .5 # depreciation parameter
rho = .5 # "observation-previous-experience" parameter whatever that is
N_prev=0 # initial N value
phi = .5 # some sort of attraction parameter 
lamb = .5 # (lambda) modifies the attraction value 
attraction_prev = [0]*7 # initial attraction




# what the player actually chose that round
choice = 7

minimum = 7

# this is the function that returns the payoff for each potential choice 
# (even ones below minimum -- it works out in the math, don't worry about it)
def payoff(choice,minimum):
    max_payoff = ((minimum - 1) * 10) + 70
    if choice ==minimum:
        return max_payoff
    else:
        if choice < minimum:
            return ((choice - 1) * 10) + 70
        else:
            return max_payoff - (choice-minimum)*10
        
    
# this is the method which updates that dictionary
for option in choices:
    weighted_payoffs[option-1]=payoff(option,minimum)*(delta + (1-delta)*int(option==choice))
   
print("weighted payoffs:")   
print(weighted_payoffs)



# setting our "observation-previous-experience" parameter whatever that is

# rho, N_prev are set above
N_current=rho*N_prev+1
# for each round this is us updating payoffs

# phi, attraction_prev are set above
attraction = attraction_prev[:]

for option in choices:
    attraction[option-1]=(phi * N_prev * attraction_prev[option-1] + weighted_payoffs[option-1])/N_current

print("\nattractions:")
print(attraction)


# choice probability

choice_prob=[0]*7

for option in choices:
    choice_prob[option-1]=numpy.exp(lamb*attraction[option-1])/sum(numpy.exp( [lamb*n for n in attraction] ))

print("\nchoice probabilities:")
print(choice_prob)


# this is just to prove that this random choice mechanism works properly
a={1:0,2:0,3:0,4:0,5:0,6:0,7:0}

for i in range(1,1000):
    
    a[numpy.random.choice(choices,p=choice_prob)]+=1

print("\n\n\n")
print(a)

