from MEG_singleplayer.math_problem_code import math_sum as mp
from MEG_singleplayer.EWA_agent_code import EWA_agent as EWA

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random


author = 'Kevin O\'Neill'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'MEG_singleplayer'
    players_per_group = None
    num_rounds = 20
    min_choice = 1
    max_choice = 7
    base_payment = 1
    scale = 1
    instructions_template = 'public_goods/Instructions.html' # temporary
    min_diff=1
    max_diff=7
    payoffmatrix = [["70",   "",   "",   "",   "",   "",   ""],
                    ["60", "80",   "",   "",   "",   "",   ""],
                    ["50", "70", "90",   "",   "",   "",   ""],
                    ["40", "60", "80","100",   "",   "",   ""],
                    ["30", "50", "70", "90","110",   "",   ""],
                    ["20", "40", "60", "80","100","120",   ""],
                    ["10", "30", "50", "70", "90","110","130"]]
    difficulty_levels = [1,2,3,4,5,6,7]
    
    agents=[EWA.EWA_Agent(),
            EWA.EWA_Agent(),
            EWA.EWA_Agent()]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    
    min_group = models.CurrencyField()
    max_payoff = models.CurrencyField()
    
    agent_weighted_payoffs = models.StringField()
    agent_attractions = models.StringField()
    agent_choice_prob = models.StringField()
    agent_choices = models.StringField()
    
    
    # with help from m_collins:
    def set_payoffs(self):
      
      contributions=[p.problem_difficulty for p in self.get_players()]+[a.make_choice() for a in Constants.agents]
      
      self.min_group = min(contributions)
      min2=sorted(contributions)[1]
      [a.update_attractions(self.min_group, min2) for a in Constants.agents]
      
      self.max_payoff = ((self.min_group - Constants.min_choice) * 10) + 70
      
      
      for p in self.get_players():
        if p.problem_difficulty == self.min_group:
          p.payoff = self.max_payoff
        else: # presuming the min_group code works right, there won't be anyone below min_group
          p.payoff = self.max_payoff - ((p.problem_difficulty - self.min_group)*10)
        
      self.agent_choices = str([a.get_last_choice() for a in Constants.agents])
      self.agent_weighted_payoffs = str([a.get_weighted_payoffs() for a in Constants.agents])
      self.agent_attractions = str([a.get_attractions() for a in Constants.agents])
      self.agent_choice_prob = str([a.get_choice_prob() for a in Constants.agents])
          

class Player(BasePlayer):
    
    wrong_math_answers=models.IntegerField(initial=0)
    
    payment=models.FloatField()
    
    subject_ID = models.CharField()
    
    gender = models.CharField(
      choices=["Male","Female","Non-binary/third gender","Prefer not to say"]
    )
    
    age=models.IntegerField(
      min=18,
      max=120,
      blank=True
    )
    
    problem_difficulty = models.IntegerField(
    min = Constants.min_diff,
    max = Constants.max_diff,
    )
    
    math_problem=models.CharField()
    math_problem_ans=models.FloatField()
    input_answer=models.FloatField(null = True)
    
    def CheckIfWrong(self, ans, p_ans):
      if ans != p_ans:
        self.wrong_math_answers+=1
    
    def CalculateTotalPayoff(self):
      # hope rewriting this doesn't cause problems
      self.payment = float((self.participant.payoff/300.0)-(self.wrong_math_answers*130))
    
    
    def GetMathProblem(self, diff):
      tmp=mp.GenerateEquationAndAnswer(diff)
      self.math_problem = tmp[0]
      self.math_problem_ans = tmp[1]
      return tmp[0]
      

    def Likert7(q):
      return models.IntegerField(
        verbose_name = q,
        choices=[
          [1,"very strongly disagree"],
          [2,"strongly disagree"],
          [3,"disagree"],
          [4,"neither agree nor disagree"],
          [5,"agree"],
          [6,"strongly agree"],
          [6,"very strongly agree"]
        ],
        widget=widgets.RadioSelect
      )
    
    DBQ1=Likert7("I didn't want to have to do a hard math problem")
    DBQ2=Likert7("I wanted a challenging math problem")
    DBQ3=Likert7("I wanted to maximize my own payoff")
    DBQ4=Likert7("I didn't want to seem self-centered")
    DBQ5=Likert7("I wanted to be a team player")
    DBQ6=Likert7("I wanted to see what would happen")
    

    
    Debrief_OtherComments = models.TextField(blank=True, 
      verbose_name='Are there any other comments you would like to share about the task you just did?')
    


