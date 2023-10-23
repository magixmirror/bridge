from experta import *
import json
import pickle
from cubes import PointCut, Cell
import os

#Global variables
rules = []
rule = []
result = ""
allFactBase = []
i = 0
data = None

rules_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"rules.json")


#extract all facts from the data
def extractAllFactBase(data):
    global allFactBase
    for key,value in data.items():
        if(data[key] is not None):
            allFactBase = allFactBase + list(data[key].values())



#extract all rules from the data
def extractRules(data):
    global rules
    rule = []
    for key1, value1 in data.items():
        rule = []
        rule.append(key1)
        for key2, value2 in value1.items():
            rule.append(key2)
            rules.append(rule.copy())
            rule.pop()
            



#get the result of the rule
def getResult(data,rule):
    global result
    result = data[rule[0]][rule[1]]

def setResult(res):
    global result
    result = res



with open(rules_path, 'r') as f:
        data = json.load(f)
extractAllFactBase(data)
extractRules(data)

class Word(Fact):
    """Information on the hand shape and palm orientation"""
    pass


#Create the rules
class IdentifyRules(KnowledgeEngine):
    global i, result
    j = -1
    for rule in rules:
        j += 1
        factsList = []
        for fact in rule:
            factsList.append(fact)
        i = 0
        getResult(data,rule)
        locals()[f'rule_{j+1}'] = Rule(Word(*factsList))
        (locals()[f'rule_{j+1}'])(lambda self, result = result: setResult(result))
        


def predict_frame(facts):
    engine = IdentifyRules()
    engine.reset()
    #Initialise fact base 
    for fact in allFactBase:
        globals()[f'{fact}'] = False
    engine.declare(Word(*facts))
    engine.run()


def predict_video(frames):
    list_facts = []
    predictions = []
    for frame in frames:
        facts = []
        facts.append(frame["Decision.palm_orientation"])
        facts.append(frame["Decision.hand_gesture"])
        list_facts.append(facts)
    
    list_facts_without_repetition = remove_repetition(list_facts)

    for facts in list_facts_without_repetition:
        predict_frame(facts)
        predictions.append(result)

    return predictions




def browse_cube(cube_browser, video_id):
    cuts = [
        PointCut(dimension="Frame", path=[1]),
        PointCut(dimension="Video", path=[video_id])
        ]
    cell = Cell(cube_browser.cube, cuts = cuts)
    result = list(cube_browser.facts(cell))
    return result


def remove_repetition(lists):
    "takes a lists of lists, and removes the repetitive consecutive lists (leaves one)"
    result = [lists[0]]  # Start with the first element
    # Iterate through the list of lists
    for sublist in lists[1:]:
        if sublist != result[-1]:
            result.append(sublist)
    return result


def process_cube(cube_browser, video_id):
    frames = browse_cube(cube_browser = cube_browser, video_id = video_id)
    if(len(frames) == 0):
        return ["No sign language found in video"]
    else:
        return predict_video(frames = frames)