from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random



class InputSubjectID(Page):
    form_model = models.Player
    form_fields = ['subject_ID', 'gender', 'age']
    def is_displayed(self):
      return self.round_number == 1


class MathProblemLevelOfEffort(Page):
    form_model = models.Player
    form_fields = ['problem_difficulty']


class MathProblemInput(Page):
    timeout_seconds = 90
    timeout_submission = None
    form_model = models.Player
    form_fields = ['input_answer']
    
    def before_next_page(self):
      self.player.CheckIfWrong(self.player.math_problem_ans, self.player.input_answer)
    
    def vars_for_template(self):
        return {'problem': self.player.GetMathProblem(self.player.problem_difficulty)}
    

class MathProblemFeedback(Page):
    timeout_seconds = 5
    form_model = models.Player
    
    def vars_for_template(self):
        return {'answer'    : self.player.math_problem_ans,
                'input_ans' : self.player.input_answer,
                'correct' : self.player.math_problem_ans == self.player.input_answer}
  
class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute"

class Results(Page):
    #timeout_seconds = 120
    def vars_for_template(self):
      return {
      }

class Counterfactuals(Page):
    #timeout_seconds = 120
    def vars_for_template(self):
      return {"choose_lower": self.player.problem_difficulty-1,
              "choose_higher": self.player.problem_difficulty+1,
              "min_higher": self.group.min_group+1
      }
      
# set to a number other than 1 if debugging rest of experiment
instructions_round_number = 1
      
class Instructions1(Page):
  def is_displayed(self):
    return self.round_number == instructions_round_number

class Instructions2(Page):
  def is_displayed(self):
    return self.round_number == instructions_round_number

class Instructions3(Page):
  def is_displayed(self):
    return self.round_number == instructions_round_number

class Instructions4(Page):
  def is_displayed(self):
    return self.round_number == instructions_round_number

class InstructionsWaitPage(WaitPage):
  body_text = "Waiting for other participants to finish reading instructions"
  def is_displayed(self):
    return self.round_number == instructions_round_number

class DebriefQuestions(Page):
  form_model = models.Player
  form_fields=['DBQ1','DBQ2','DBQ3','DBQ4','DBQ5','DBQ6','Debrief_OtherComments']
  
  def before_next_page(self):
    self.player.CalculateTotalPayoff()
  
  def is_displayed(self):
    return self.round_number == models.Constants.num_rounds
  
  def get_form_fields(self):
    fields = self.form_fields[:len(self.form_fields)-1]
    random.shuffle(fields)
    return fields+[self.form_fields[len(self.form_fields)-1]]


page_sequence = [
    InputSubjectID,
    Instructions1,
    Instructions2,
    Instructions3,
    MathProblemLevelOfEffort,
    MathProblemInput,
    MathProblemFeedback,
    ResultsWaitPage,
    Results,
    Counterfactuals,
    DebriefQuestions
]
