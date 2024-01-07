import numpy as np
import random

def generate_choices(chips):
    """
    Generate all possible combinations for an agent's chips
    Args:
        chip: an agent's chips
        eg: [1,1,2,0]
    Returns:
        ans: All possible combinations for an agent's chip
        eg:[[0, 0, 1, 0], [0, 0, 2, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 2, 0], [1, 0, 0, 0],
        [1, 0, 1, 0], [1, 0, 2, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 2, 0]]
    """
    def gen(cnts, idx=0, choice=[]):
        if idx >= len(cnts):
            if choice == [0,0,0,0] or choice == [1,1,1,1]:
                return None
            return choice
        choices = []
        for c in range(cnts[idx] + 1):
            choice.append(c)
            tmp = gen(cnts, idx + 1, choice)
            if tmp != None:
                 choices += tmp
            choice.pop()
        return choices
    choices = gen(chips)
    ans = []
    for i in range(0, len(choices), 4):
        ans.append(choices[i:i + 4])
    return ans

def generate_exchange_choices(my_chips,other_chips):
    """
    Generate all possible exchange combinations for two agents's chips
    Args:
        my_chips: my agent's chips
        other_chips: the other agent's chips
    Returns:
        All possible exchange combinations for two chips
    """
    def _isvalid(my_chip,other_chip):
        for i in range(len(my_chip)):
            if my_chip[i] > 0 and other_chip[i] > 0:
                return False
        return True
    exchange_choices = []
    my_choices = generate_choices(my_chips)
    other_choices = generate_choices(other_chips)
    for i in range(len(my_choices)):
        for j in range(len(other_choices)):
            if _isvalid(my_choices[i],other_choices[j]):
                exchange_choices.append(my_choices[i]+other_choices[j])
    return exchange_choices

def Alice(obs):
    my_chips = obs["my_chips"]
    other_chips = obs["other_chips"]
    exchange_choices = generate_exchange_choices(my_chips,other_chips)
    # The first four represent moves, the fifth represent agree, the sixth represent disagree
    choices =[[0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,0],[3,0,0,0,0,0,0,0],[4,0,0,0,0,0,0,0],[5,0,0,0,0,0,0,0]]
    choices += exchange_choices
    i = random.randint(0,len(choices)-1)
    return choices[i]