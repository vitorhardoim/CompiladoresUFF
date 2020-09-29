# Author: Christiano Braga
# Sep. 2020
# Univ. Fed. Fluminense

import pprint
import pandas as pd
from tabulate import tabulate

# Calculates FIRST, FOLLOW and predictive parsing table
# as described on pg. 221 - 224 of the Dragon book, 2nd. ed.

class Grammar:
    def __init__(self, s, p, nt, t):
        self.start_symbol = s
        # Production rules are represented as a dictionary
        # where each entry has a symbol S as a key and a list of
        # tuples, denoting the RHS of the productions where S
        # is the LHS, as value.
        # A -> Y_1 Y_2 Y_3 | K_1 K_2
        # ~>  "A" : [(Y_1,Y_2,Y_3),(K_1, K_2)]
        self.production_rules = p
        self.non_terminals = nt
        self.terminals = t
        # Initializes first_tab and follow_tab with the empty set,
        # for each symbol in V U T.
        symbols = self.non_terminals.copy()
        for s in self.terminals:
            symbols.append(s)
        self.first_tab = {}
        self.follow_tab = {}
        self.pred_parsing_tab = {}
        for s in symbols:
            self.first_tab[s] = set()
            if s in self.non_terminals:
                self.follow_tab[s] = set()
        # Initializes the predictive parsing table.
        # The parsing table is a dictionary of dictionaries.
        # For each non terminals, there exists a dictionary of
        # terminals associating them um a production,
        # represented as a tuple.
        for t in self.non_terminals:
            self.pred_parsing_tab[t] = {}
            for a in self.terminals:
                self.pred_parsing_tab[t].update({a : []})
            self.pred_parsing_tab[t].update({'$' : []})                
        self.first_trace = []
        self.follow_trace = []
        self.pred_parsing_trace = []
        self.pp = pprint.PrettyPrinter()
        self.first_computed = False
    
    def getSymbols(self):
        symbols = self.non_terminals.copy()
        for s in self.terminals:
            symbols.append(s)
        return symbols
    
    def print_production(self, s, rhs):
        rhs_as_str = ''.join(rhs)
        print(str(s) + " -> " + rhs_as_str)
        
    def print_productions(self):
        for s in self.production_rules.keys():
            for rhs in self.production_rules[s]:
                self.print_production(s, rhs)

    def compute_first(self):
        for s in self.getSymbols():
            self.first(s)
        self.first_computed = True
            
    def firstW(self, w):
        '''
        Calculates FIRST(w), where w is a word represented as a tuple of
        strings. 
        Precondition: execution of compute_first.
        '''
        # The word w is represented as a tuple of strings.
        assert(self.first_computed)
        if w != ():
            first_w = set()
            x_1 = w[0]
            # "Add to FIRST(X_1 X_2 ... X_n) all non-epsilon symbols of
            # FIRST(X_1)."

            ### Do your magic!

            # Also add the non-epsilon symbols of FIRST(X_2), if epsilon is in
            # FIRST(X_1), and so on until X_n.

            ### Do your magic!
            
            # Finally, add epsilon to FIRST(X_1 X_2 ... X_n) if for all i
            # epsilon \in FIRST(X_i).

            ### Do your magic!
            
            return first_w
        else:
            return set()
        
    def first(self, s):
        '''
        Calculates the set FIRST for a given symbol s.
        Updates attribute first_tab[s]. 
        '''
        if s in self.terminals:
            self.first_tab[s].add(s)
        else:
            assert(s in self.non_terminals)
            for rhs in self.production_rules[s]:
                y_1 = rhs[0]
                # We assume that if the first symbol in the RHS
                # of the prodution rule is epsilon, than is a
                # production of the form A -> epsilon.
                if y_1 == "epsilon":
                    self.first_log(s, "epsilon", rhs)
                    self.first_tab[s].add("epsilon")
                    break
                # We must first calculate FIRST(y_1) before
                # use it.
                if self.first_tab[y_1] == set():
                    self.first(y_1)
                # FIRST(y_1) \subseteq FIRST(s)    
                for a in self.first_tab[y_1]:
                    self.first_log(s, a, rhs)                    
                    self.first_tab[s].add(a)
                # FIRST(y_i) \subseteq FIRST(s), iff
                # epsilon \in FISRT(y_j), for every 1 <= j <= i.
                # We assume y_i may not be epsilon, unless i = 1.
                for i in range(1, len(rhs)):
                    y_ant = rhs[i - 1] # ant =  i - 1
                    y_i = rhs[i]
                    # We must first calculate FIRST(y_ant) before
                    # use it.
                    if self.first_tab[y_ant] == set():
                        self.first(y_ant)
                    # FIRST(y_i) is included in FIRST(s) iff
                    # epsilon \in FISRT(y_j), for every 1 <= j <= i.
                    # However, we only reach j if every k 1 <= k < j
                    # has been reached before.

                    ### Do your magic!

                    
            # If all symbols in the rhs derive epsilon, than epsilon
            # must be included in FIRST(s).
            add_epsilon = True
            for rhs in self.production_rules[s]:
                for a in rhs:
                    if not a == "epsilon":
                        if not("epsilon" in self.first_tab[a]):
                            add_epsilon = False
            if add_epsilon:
                self.first_tab[s].add("epsilon")

    def print_first(self):
        self.pp.pprint(self.first_tab)

    def first_log(self, symb, first, rhs):
        '''
        Traces the execution of the algorithm for calculating FIRST.
        '''
        if not first in self.first_tab[symb]:
            self.first_trace.append("Added " + str(first) + " to FIRST(" + str(symb) + ") " + \
                                    "while processing rule " + str(symb) + " -> " +  ''.join(rhs))
            
    def print_first_log(self):
        for m in self.first_trace:
            print(m)
            
    def print_follow(self):
        self.pp.pprint(self.follow_tab)
        
    def tab_size(self, t):
        size = 0
        for r in list(t.values()):
            size += len(r)
        return size

    def follow_tab_size(self):
        return self.tab_size(self.follow_tab)

    def follow_log(self, symb, follow, rhs):
        '''
        Traces the execution of the algorithm for calculating FOLLOW.
        '''
        if not follow.issubset(self.follow_tab[symb]):
            self.follow_trace.append("Added " + str(follow) + " to FOLLOW(" + str(symb) + ") " + \
                                     "while processing rule " + str(symb) + " -> " +  ''.join(rhs))

    def print_follow_log(self):
        for m in self.follow_trace:
            print(m)
            
    def compute_follow(self):
        '''
        Calculates FOLLOW table.
        '''
        # Place $􏰗in FOLLOW(S) where S is the start symbol􏰞
        # and $􏰗is the input right endmarker.
        self.follow_tab[self.start_symbol].add("$")
        # To compute FOLLOW(A), for all non terminals A,
        # apply the following rules until nothing can be
        # added to any FOLLOW set.
        while True:
            ### Do your magic!
            pass

            
    def follow(self, s):
        '''
        Computes the FOLLOW of a given non terminal symbol.
        '''
        assert(s in self.non_terminals)
        for rhs in self.production_rules[s]:
            for i in range(len(rhs)):
                B = rhs[i]
                if B in self.non_terminals:
                    beta = rhs[(i + 1):]
                    if beta != ():
                        # If there is a production A -> alpha􏰐B beta then everything in
                        # FIRST(beta),􏰚except epsilon, is in FOLLOW(B).
                        
                        ### Do your magic!

                        # If there is a production A -> alpha B beta
                        # where FIRST(beta) contains epsilon, then FOLLOW(A) \subset FOLLOW(B) 􏰛􏰂

                        ### Do your magic! 
                        pass
                    else:
                        # If there is a production A -> alpha B
                        # then FOLLOW(A) \subset FOLLOW(B) 􏰛􏰂

                        ### Do your magic!
                        pass
    def compute_pred_parsing_tab(self):
        '''
        Computes the predictive parsing table of a given grammar.
        Precondition: the execution of compute_first and compute_follow.
        '''
        # For each production A -> alpha do:
        for A in self.non_terminals:
            for alpha in self.production_rules[A]:
                # If epsilon is in FIRST(alpha), then for each terminal
                # b in FOLLOW(A) add A -> alpha to M[A, b]. Also, if $
                # is in FOLLOW(A), add A -> alpha to M[A, $] as well.
                if alpha == ("epsilon",) or \
                   (alpha != ("epsilon",) and ("epsilon" in self.firstW(alpha))):

                    ### Do your magic!

                else:
                    # For each terminal a in FIRST(alpha), 
                    # add A -> alpha to M[A, a]

                    ### Do your magic!
                    
    def print_pred_parsing_tab(self):
        # self.pp.pprint(self.pred_parsing_tab)
        df = pd.DataFrame(self.pred_parsing_tab).T
        df.fillna(0, inplace=True)
        print(tabulate(df, headers='keys', tablefmt='psql'))

class Exercise:
    def __init__(self, s, g):
        self.statement = s
        self.grammar = g
        
    def solve(self):
        print("\n|- " + str(self.statement))
        print("Production rules")
        self.grammar.print_productions()
        print("\nFIRST table")
        self.grammar.compute_first()
        self.grammar.print_first()
        print("\nFIRST log")    
        self.grammar.print_first_log()
        print("\nFOLLOW table")
        self.grammar.compute_follow()
        self.grammar.print_follow()
        print("\nFOLLOW log")    
        self.grammar.print_follow_log()
        print("\nPredictive parsing table")
        self.grammar.compute_pred_parsing_tab()
        self.grammar.print_pred_parsing_tab()
        
if __name__ == '__main__':
    # Production rules for grammar 4.28
    p = {"E" : [("T", "E'")],
         "E'" : [("+", "T", "E'"), ("epsilon",)],
         "T" : [("F", "T'")],
         "T'" : [("*", "F", "T'"), ("epsilon",)],
         "F" : [("(", "E", ")"), ("id",)]}
    # Grammar 4.28
    g = Grammar("E", p, ["E", "E'", "T", "T'", "F"],
                ["+", "*", "(", ")", "id"])

    ex = Exercise("Example 4.30 of the Dragon book, 2nd.", g)
    ex.solve()
    
    # Production rules for Example 4.33
    p = {"S" : [("i", "E", "t", "S", "S'"), ("a", )],
         "S'" : [("e", "S"), ("epsilon",)],
         "E" : [("b",)]}
    g = Grammar("S", p, ["S", "S'", "E"],
                ["a", "b", "e", "i", "t"])

    ex = Exercise("Example 4.33 of the Dragon book, 2nd.", g)
    ex.solve()
    
