'''
Condorcet's jury theorem is a political science theorem about the relative probability of a given group of individuals arriving at a correct decision. The theorem was first expressed by the Marquis de Condorcet in his 1785 work Essay on the Application of Analysis to the Probability of Majority Decisions.[1]

The assumptions of the theorem are that a group wishes to reach a decision by majority vote. One of the two outcomes of the vote is correct, and each voter has an independent probability p of voting for the correct decision. The theorem asks how many voters we should include in the group. The result depends on whether p is greater than or less than 1/2:

If p is greater than 1/2 (each voter is more likely to vote correctly), then adding more voters increases the probability that the majority decision is correct. In the limit, the probability that the majority votes correctly approaches 1 as the number of voters increases.
On the other hand, if p is less than 1/2 (each voter is more likely to vote incorrectly), then adding more voters makes things worse: the optimal jury consists of a single voter.
Since Condorcet, many other researchers have proved various other jury theorems, relaxing some or all of Condorcet's assumptions.
'''
from random import random


final_decision = []
jurors = []
below_half = []
above_half = []
names = [
    "earl",
    "sam",
    "maddie",
    "allison",
    "gert",
    "jones",
    "timmy",
    "rochelle",
    "barry",
    "jerry",
    "suzanne",
    "cole",
    "warren",
    "zach",
    "yvonne",
    "uther"
]

class Juror():
    def __init__(self, name:str):
        self.name = name
        self.being_right = random()
    def __str__(self) -> str:
        return f'This Juror\'s name is: {self.name}'

# each juror is representative of a model. however models can be good or bad at producing an accurate outcome, ie voting correctly.
# in other words, this has been reutilized in other disciplines as an "averaging theorem"

def build_jury():
    for each in names:
        jurors.append(Juror(each))
    # print(jurors[0].being_right)  # works fine

build_jury()

def condorcet_theorem(the_jury:list):
    result = int()
    print("post declaration:", result)

    for juror in the_jury:
        result += juror.being_right
    print("post accumulation:", result)

    result = result/len(the_jury)
    print("final result:", result)

condorcet_theorem(jurors)