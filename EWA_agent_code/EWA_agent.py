# Agent which will run EWA reasoning
# 
# Kevin O\'Neill
# with theoretical assistance from M_Collins

# this is to encapsulate the logic and keep track of each agent's variables

# NOTA BENE: This assumes choices are 1:7 (inclusive)
# several places are hardcoded with this assumption
# if that ever changes, go through and find all of them and fix them


import numpy


class EWA_Agent:
    
    def __init__(self):
        # this is a list which stores the weightings of the payoffs, 
        # which will be used to calculate the choices
        self.weighted_payoffs = [0]*7
        self.choices=range(1,8)

        # Free parameters
        # set these more accurately once you've done some model fitting

        self.delta = 1 # depreciation parameter
        self.rho = .6 # "observation-previous-experience" parameter whatever that is
        self.N_prev=0 # initial N value
        self.phi = .7 # some sort of attraction parameter 
        self.lamb = .2 # (lambda) modifies the attraction value 
        self.attraction_prev = [0]*7 # initial attraction

        # list to hold the attraction values
        self.attraction = self.attraction_prev[:]
        
        #list to hold choice probability
        self.choice_prob=[1.0/7]*7
        
        # initial choice for sanity testing
        self.choice=0 # not possible to get normally
        self.last_payoff=0

        
    # this is the function that returns the payoff for each potential choice 
    # (even ones below minimum -- it works out in the math, don't worry about it)
    def payoff(self,choice,minimum):
        max_payoff = ((minimum - 1) * 10) + 70
        if choice ==minimum:
            return max_payoff
        else:
            if choice < minimum:
                return ((choice - 1) * 10) + 70
            else:
                return max_payoff - (choice-minimum)*10
            
    def get_last_choice(self):
        return int(self.choice)
    
    def get_last_payoff(self):
        return int(self.last_payoff)
            
    def get_weighted_payoffs(self):
        return self.weighted_payoffs
        
    def get_attractions(self):
        return self.attraction
        
    def get_choice_prob(self):
        return self.choice_prob
            
    def make_choice(self):
        self.choice = numpy.random.choice(self.choices,p=self.choice_prob)
        return int(self.choice)
        
    def update_attractions(self, minimum):
        assert(self.choice >= minimum)
        
        self.last_payoff=self.payoff(self.choice, minimum)
        
        # this is the method which updates that dictionary
        for option in self.choices:
            self.weighted_payoffs[option-1]=self.payoff(option,minimum)*(self.delta + (1-self.delta)*int(option==self.choice))
           
        # rho, N_prev are set above
        self.N_current=self.rho*self.N_prev+1
        # for each round this is us updating payoffs

        # phi, attraction_prev are set above

        for option in self.choices:
            self.attraction[option-1]=(self.phi * self.N_prev * self.attraction_prev[option-1] + self.weighted_payoffs[option-1])/self.N_current

        self.N_prev = self.N_current
        self.attraction_prev=self.attraction[:]

        for option in self.choices:
            self.choice_prob[option-1]=numpy.exp(self.lamb*self.attraction[option-1])/sum(numpy.exp( [self.lamb*n for n in self.attraction] ))
    
    def report_state(self):
        
        print("\n\n\n\n")
        
        # print parameters
        print("\nFree parameters")
        print("delta:   "+str(self.delta))
        print("rho:     "+str(self.rho))
        print("phi:     "+str(self.phi))
        print("lambda:  "+str(self.lamb))
        
        print("\nPrevious choice")
        print(self.choice)
        
        print("Weighted payoffs:")   
        print(self.weighted_payoffs)

        print("\nAttractions:")
        print(self.attraction)

        print("\nChoice probabilities:")
        print(self.choice_prob)




# k=EWA_Agent()

# for n in range(1,10):
    # m=k.make_choice()
    # k.update_attractions(min(m,4))
    # k.report_state()

