# Author: Christiano Braga
# Oct. 2020
# Univ. Fed. Fluminense

from predparsing import Grammar
import pprint
import pandas as pd
from tabulate import tabulate

# An item of a production A -> alpha is a triple
# (A, (a0, a1, ..., an), i)
# where the first projection
# is a string representing A, the snd. projection is a tuple representing alpha,
# and the third projection is a natural number denoting the position of the dot
# in alpha, such that if alpha = a0 * a1 a2 ... an, the third projection is the
# number 1, where '*' denotes the dot. 

def closure(s, g):
    '''
    Calculates the closure of a set of items as of Dragon 2ed. pg. 243.
    '''
    assert(type(s) == set)
    clos = set()
    # Initially add every item in s to closure of s.
    clos = clos.union(s)
    # If A -> alpha * B beta is in closure(s) and B -> gamma is a
    # production then add item B -> * gamma to closure(s), if it is not
    # already there. Apply this rule until no more items can be added
    # to closure(s).
    while True:
        clos_size = len(clos)
        # Python does not allow a set to change while iterating over it.
        # We need to collect new items and then unite them with the closure
        # being calculated.
        new_items = set()
        for lhs, rhs, dot_idx in clos:
            if dot_idx < len(rhs):
                B = rhs[dot_idx]
                if(B in g.non_terminals):
                    for pRule in g.production_rules[B]:
                        item = (B, pRule, 0)
                        if(item not in clos):
                            new_items.add(item)
        clos = clos.union(new_items)
        new_clos_size = len(clos)
        if clos_size == new_clos_size:
            break
    return clos

def goto(s, x, g):
    '''
    Calculates GOTO(s, x) as defined to be the closure of the set of all items
    [A -> alpha X * beta] such that [A -> alpha * X beta] is in s.
    '''
    goto_sx = set()
    for lhs, rhs, dot_idx in s:
        if dot_idx < len(rhs):
            X = rhs[dot_idx]
            if X == x:
                item = (lhs, rhs, dot_idx+1)
                if(item not in goto_sx):
                    goto_sx.add(item)
        goto_sx = closure(goto_sx, g)
    return goto_sx

def augment(g):
    new_start_symbol = g.start_symbol + "'"
    assert(not new_start_symbol in g.non_terminals)
    g.production_rules[new_start_symbol] = [tuple(g.start_symbol)]
    g.start_symbol = new_start_symbol
    g.non_terminals.append(new_start_symbol)
    g.first_tab[new_start_symbol] = set()
    g.follow_tab[new_start_symbol] = set()    

def canonical_items(g):
    '''
    Calculates the canonical collection of sets of LR(0) items.
    '''
    # Dragon book, 2nd ed, pg 246
    # void items(G') {
    #   C = {closure({[S'-> * S]})}
    #   repeat
    #      for each set of items I in C
    #          for each grammar symbol X
    #              if GOTO(I, X) is not empty and not in C
    #                 add GOTO(I, X) to C
    #   until no new set of items are added to C on a round
    # }
    
    # Grammar g is assumed augmented
    s = g.start_symbol          # S'
    orig_s = s[:len(s) - 1]     # S
    start_item = (s, orig_s, 0) # S' -> * S
    # I chose to represent C as a list of set of items
    # instead of a set so we can assign a natural number to 
    # each set of items I beig its position in the
    # list representing C.
    can = [closure({start_item}, g)]
    while True:
        can_size = len(can)
        for I in can:
            for X in g.getSymbols():
                if(len(goto(I,X,g)) != 0 and goto(I,X,g) not in can):
                    can.append(goto(I,X,g))
        new_can_size = len(can)
        if new_can_size == can_size:
            break
    return can

def slr_parsing_table(g):
    '''
    Computes SLR parsing table according to Dragon 2nd ed. pgs 253, 254.
    '''
    # Grammar g is assumed to augmented.
    assert(g.follow_computed)
    # 1. Construct C = {I0, I1, ... In},􏰉 the collection of sets of LR(0)
    # items for G.
    can = canonical_items(g)
    # Initializes ACTION and GOTO tables.
    action_tab = {}
    goto_tab = {}
    for st in range(len(can)):
        d = {}
        for t in g.terminals:
            d[t] = []
        d["$"] = []
        action_tab[st] = d
        d = {}
        for v in g.non_terminals:
            d[v] = []
        goto_tab[st] = d
    # 2. State i is constructed from Ii.
    # (They are encoded as the indices of 'can'.)􏰋
    # The parsing actions for state i are deter mined as follows:
    for state_l, l in enumerate(can):
        for i, item in enumerate(l):
            lhs = item[0]
            rhs = item[1]
            dot_idx = item[2]
            if dot_idx < len(rhs):
                a = rhs[dot_idx]
                # (a)􏰈 If 􏰧[A -> alpha * a beta]􏰂is in Ii
                #      and GOTO(Ii, a) = Ij then
                #        set ACTION[i,􏰥a] =􏰙shift j.
                #      Here a must be a terminal.􏰋
                if a in g.terminals: action_tab[state_l][a].append(('shift', can.index(goto(l,a,g))))
            else:
                # (b) If [A -> alpha *] is in Ii, then set
                # ACTION[i, a] = "reduce A -> alpha" to
                # all a in FOLLOW(A); here A may not be S'.
                # (c) If [S' -> S *] is in Ii, then set
                # ACTION[i, $] = "accept".
                if lhs != g.start_symbol:
                    for a in g.follow_tab[lhs]:
                        action_tab[state_l][a].append(('reduce', (lhs, rhs)))
                else:
                    action_tab[state_l]['$'].append(('accept',))
                
        # 3. The goto transitions for state i are constructed for all
        # nonterminals A using the rule􏰗 If GOTO(Ii, A) = Ij 􏰉
        # then GOTO[i,􏰥A] = j.􏰋
        for A in g.non_terminals:
            gotoVar = goto(l, A, g)
            if(gotoVar in can):
                goto_tab[state_l][A].append(can.index(gotoVar))
    return (action_tab, goto_tab)

def print_slr_table(act_tb, goto_tb):
    print("ACTION table")
    df = pd.DataFrame(act_tb).T
    df.fillna(0, inplace=True)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print("GOTO table")    
    df = pd.DataFrame(goto_tb).T
    df.fillna(0, inplace=True)
    print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == '__main__':
    # Production rules for Expression Grammar 4.1
    p = {"E" : [("E", "+", "T"), tuple("T")],
         "T" : [("T", "*", "F"), tuple("F")],
         "F" : [("(", "E", ")"), ("id",)]}
    g = Grammar("E", p, ["E", "T", "F"],
                ["+", "*", "(", ")", "id"])

    print("Example 4.40, 244")
    pp = pprint.PrettyPrinter()
    pp.pprint(closure({("E'", "E", 0)}, g))

    print("Example 4.4.1, pg 246")
    pp.pprint(goto({("E'", "E", 1), ("E", ("E","+","T"), 1)}, "+", g))
    augment(g)
    pp.pprint(canonical_items(g))
    print("\n# Production rules for Example 4.45, pg 251, Exp. Grammar 4.1.")
    g.print_productions()
    g.compute_first()
    g.compute_follow()
    act_tb, goto_tb = slr_parsing_table(g)
    print_slr_table(act_tb, goto_tb)

    print("\n# Production rules for grammar 4.28")
    p = {"E" : [("T", "E2")],
         "E2" : [("+", "T", "E2"), ("epsilon",)],
         "T" : [("F", "T'")],
         "T'" : [("*", "F", "T'"), ("epsilon",)],
         "F" : [("(", "E", ")"), ("id",)]}
    # Grammar 4.28
    g = Grammar("E", p, ["E", "E2", "T", "T'", "F"],
                ["+", "*", "(", ")", "id"])
    augment(g)
    print("\n# Production rules for Example 4.32, pg. 225, Grammar 4.28.")    
    g.print_productions()
    g.compute_first()
    g.compute_follow()
    act_tb, goto_tb = slr_parsing_table(g)
    print_slr_table(act_tb, goto_tb)