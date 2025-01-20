######################## PARSER/LEXER

# MACROS
CONCAT = 0xC04CA7
ETOILE = 0xE7011E
ALTERN = 0xA17E54
PROTECTION = 0xBADDAD

PARENTHESEOUVRANT = 0x16641664
PARENTHESEFERMANT = 0x51515151
DOT = 0xD07

# UTILITARY CLASS
class RegExTree:
    def __init__(self, root, subTrees):
        self.root = root
        self.subTrees = subTrees

    def __str__(self):
        if not self.subTrees:
            return self.rootToString()
        result = self.rootToString() + "(" + str(self.subTrees[0])
        for t in self.subTrees[1:]:
            result += "," + str(t)
        result += ")"
        return result

    def rootToString(self):
        if self.root == CONCAT:
            return "."
        if self.root == ETOILE:
            return "*"
        if self.root == ALTERN:
            return "|"
        if self.root == DOT:
            return "."
        return chr(self.root)

# FROM REGEX TO SYNTAX TREE
def parse(regEx):
    # BEGIN DEBUG: set conditionnal to True for debug example
    if False:
        raise Exception()
    example = exampleAhoUllman()
    if False:
        return example
    # END DEBUG

    result = []
    for c in regEx:
        result.append(RegExTree(charToRoot(c), []))
    return parse_recursive(result)

def charToRoot(c):
    if c == '.':
        return DOT
    if c == '*':
        return ETOILE
    if c == '|':
        return ALTERN
    if c == '(':
        return PARENTHESEOUVRANT
    if c == ')':
        return PARENTHESEFERMANT
    return ord(c)

def parse_recursive(result):
    while containParenthese(result):
        result = processParenthese(result)
    while containEtoile(result):
        result = processEtoile(result)
    while containConcat(result):
        result = processConcat(result)
    while containAltern(result):
        result = processAltern(result)
    if len(result) > 1:
        raise Exception()
    return removeProtection(result[0])

def containParenthese(trees):
    for t in trees:
        if t.root == PARENTHESEFERMANT or t.root == PARENTHESEOUVRANT:
            return True
    return False

def processParenthese(trees):
    result = []
    found = False
    for t in trees:
        if not found and t.root == PARENTHESEFERMANT:
            done = False
            content = []
            while not done and result:
                if result[-1].root == PARENTHESEOUVRANT:
                    done = True
                    result.pop()
                else:
                    content.insert(0, result.pop())
            if not done:
                raise Exception()
            found = True
            subTrees = [parse_recursive(content)]
            result.append(RegExTree(PROTECTION, subTrees))
        else:
            result.append(t)
    if not found:
        raise Exception()
    return result

def containEtoile(trees):
    for t in trees:
        if t.root == ETOILE and not t.subTrees:
            return True
    return False

def processEtoile(trees):
    result = []
    found = False
    for t in trees:
        if not found and t.root == ETOILE and not t.subTrees:
            if not result:
                raise Exception()
            found = True
            last = result.pop()
            subTrees = [last]
            result.append(RegExTree(ETOILE, subTrees))
        else:
            result.append(t)
    return result

def containConcat(trees):
    firstFound = False
    for t in trees:
        if not firstFound and t.root != ALTERN:
            firstFound = True
            continue
        if firstFound:
            if t.root != ALTERN:
                return True
            else:
                firstFound = False
    return False

def processConcat(trees):
    result = []
    found = False
    firstFound = False
    for t in trees:
        if not found and not firstFound and t.root != ALTERN:
            firstFound = True
            result.append(t)
            continue
        if not found and firstFound and t.root == ALTERN:
            firstFound = False
            result.append(t)
            continue
        if not found and firstFound and t.root != ALTERN:
            found = True
            last = result.pop()
            subTrees = [last, t]
            result.append(RegExTree(CONCAT, subTrees))
        else:
            result.append(t)
    return result

def containAltern(trees):
    for t in trees:
        if t.root == ALTERN and not t.subTrees:
            return True
    return False

def processAltern(trees):
    result = []
    found = False
    gauche = None
    done = False
    for t in trees:
        if not found and t.root == ALTERN and not t.subTrees:
            if not result:
                raise Exception()
            found = True
            gauche = result.pop()
            continue
        if found and not done:
            if gauche is None:
                raise Exception()
            done = True
            subTrees = [gauche, t]
            result.append(RegExTree(ALTERN, subTrees))
        else:
            result.append(t)
    return result

def removeProtection(tree):
    if tree.root == PROTECTION and len(tree.subTrees) != 1:
        raise Exception()
    if not tree.subTrees:
        return tree
    if tree.root == PROTECTION:
        return removeProtection(tree.subTrees[0])
    subTrees = [removeProtection(t) for t in tree.subTrees]
    return RegExTree(tree.root, subTrees)

def exampleAhoUllman():
    a = RegExTree(ord('a'), [])
    b = RegExTree(ord('b'), [])
    c = RegExTree(ord('c'), [])
    cEtoile = RegExTree(ETOILE, [c])
    dotBCEtoile = RegExTree(CONCAT, [b, cEtoile])
    return RegExTree(ALTERN, [a, dotBCEtoile])


#################### NDFA

class NDFA:
    def __init__(self):
        self.transitions = {} # state -> symbol -> next_state
        self.start_state = None
        self.accept_states = set()
        self.state_count = 0    

    def new_state(self):
        """
            Cree un nouvel état et retourne son numero
            Complexite: O(1)
        """
        state = self.state_count
        self.state_count += 1
        return state

    def add_transition(self, debut_state, symbol, fin_state):
        """
            Ajoute une transition entre deux etats et le stocke dans le dictionnaire {transitions}
            Complexite: O(1)
            
            debut_state: l'état de départ
            symbol: le symbole de la transition (None pour une transition epsilon)
            fin_state: l'état de fin après la transition
        """
        if debut_state in self.transitions: # transitions[debut_state] != None -> O(1)
            self.transitions[debut_state].append((symbol, fin_state))
        else:
            self.transitions[debut_state] = [(symbol, fin_state)]
            
    def get_alphabet(self):
        """
            Retourne l'alphabet de l'automate, en excluant les epsilon-transitions (None)
            Complexite: O(t) avec t transitions
        """
        alphabet = set()
        for transitions in self.transitions.values():
            for (symbol, _) in transitions:
                if symbol is not None:
                    alphabet.add(symbol)
        return alphabet
    
    # Affichage
    def display(self):
        dot = Digraph()
        for state in range(self.state_count):
            if state in self.accept_states:
                dot.node(str(state), shape="doublecircle")
            else:
                dot.node(str(state))
        for debut_state, edges in self.transitions.items():
            for (symbol, fin_state) in edges:
                label = 'ε' if symbol is None else symbol # symbole sur le graphe
                dot.edge(str(debut_state), str(fin_state), label=label)
        dot.render('ndfa', view=True)

def to_ndfa(tree):
    """
        Construit un automate fini non deterministe a partir de l'arbre syntaxique {tree}
        Complexite: O(n) avec n le nombre de noeuds
    """
    ndfa = NDFA()
    start_state, accept_state = build_ndfa(tree, ndfa)
    ndfa.start_state = start_state
    ndfa.accept_states.add(accept_state)
    return ndfa

def build_ndfa(tree, ndfa):
    """
        Construit recursivement un NDFA base sur l'arbre syntaxique
        Complexite: O(n)
        
        tree: arbre syntaxique representant l'expression reguliere
        ndfa: l'automate en cours de construction
        
        Retourne l'etat de depart et l'etat d'acceptation de l'automate construit pour cette sous-arbre
    """
    # Aho-Ullman
    if tree.subTrees == []:
        # traitement des feuilles
        start = ndfa.new_state()
        end = ndfa.new_state()
        symbol = None if tree.root == DOT else chr(tree.root)
        ndfa.add_transition(start, symbol, end)
        return start, end
    elif tree.root == ETOILE:
        # étoile
        start = ndfa.new_state()
        end = ndfa.new_state()
        ndfa_start, ndfa_end = build_ndfa(tree.subTrees[0], ndfa)
        ndfa.add_transition(start, None, ndfa_start)
        ndfa.add_transition(ndfa_end, None, ndfa_start)
        ndfa.add_transition(ndfa_end, None, end)
        ndfa.add_transition(start, None, end)
        return start, end
    elif tree.root == CONCAT:
        # concatenation
        left_start, left_end = build_ndfa(tree.subTrees[0], ndfa)
        right_start, right_end = build_ndfa(tree.subTrees[1], ndfa)
        ndfa.add_transition(left_end, None, right_start)
        return left_start, right_end
    elif tree.root == ALTERN:
        # alternative
        start = ndfa.new_state()
        end = ndfa.new_state()
        left_start, left_end = build_ndfa(tree.subTrees[0], ndfa)
        right_start, right_end = build_ndfa(tree.subTrees[1], ndfa)
        ndfa.add_transition(start, None, left_start)
        ndfa.add_transition(start, None, right_start)
        ndfa.add_transition(left_end, None, end)
        ndfa.add_transition(right_end, None, end)
        return start, end
    else:
        raise Exception("Unsupported operation")


#################### DFA

class DFA:
    def __init__(self):
        self.transitions = {}  # state -> symbol -> next_state
        self.start_state = None
        self.accept_states = set()
        self.states = set()

    def add_transition(self, debut_state, symbol, fin_state):
        """
            Ajoute une transition entre deux états du DFA avec un symbole
            Complexite: O(1)
        """
        if debut_state not in self.transitions:
            self.transitions[debut_state] = {}
        self.transitions[debut_state][symbol] = fin_state

    # Affichage
    def display(self, filename='dfa'):
        dot = Digraph()
        for state in self.states:
            state_name = self._state_to_string(state)
            if state in self.accept_states: # état sortant: double cercle
                dot.node(state_name, shape="doublecircle")
            else: # état normal
                dot.node(state_name)
        for debut_state, trans in self.transitions.items():
            debut_state_name = self._state_to_string(debut_state)
            for symbol, fin_state in trans.items():
                fin_state_name = self._state_to_string(fin_state)
                dot.edge(debut_state_name, fin_state_name, label=symbol)
        dot.render(filename, view=True)

    # pour display
    def _state_to_string(self, state):
        if isinstance(state, (frozenset, frozenset)):
            return ','.join(map(str, sorted(state)))
        else:
            return str(state)

# Subset Construction Algorithm
def ndfa_to_dfa(ndfa):
    """
        Convertit un NDFA en DFA en utilisant l'algorithme des sous-ensembles
        Complexite: O(2^n*(n^2)), explication sur le rapport partie 2.1.5
    """
    dfa = DFA()
    initial_state = epsilon_closure(ndfa, set([ndfa.start_state]))
    dfa.start_state = initial_state
    dfa.states.add(initial_state)
    if ndfa.accept_states & initial_state:
        dfa.accept_states.add(initial_state)

    unmarked_states = [initial_state]
    alphabet = ndfa.get_alphabet()

    while unmarked_states:
        current_state = unmarked_states.pop()
        for symbol in alphabet:
            if symbol is None:
                continue
            next_states = move(ndfa, current_state, symbol) # déterminer les prochains états accessibles avec ce symbole
            if not next_states:
                continue
            closure = epsilon_closure(ndfa, next_states) # fermeture epsilon des états atteints
            if closure not in dfa.states:
                dfa.states.add(closure)
                unmarked_states.append(closure)
                if ndfa.accept_states & closure:
                    dfa.accept_states.add(closure)
            dfa.add_transition(current_state, symbol, closure)
    return dfa

def epsilon_closure(ndfa, states):
    """
        Calcule la fermeture epsilon des etats donnes.
        La fermeture epsilon est l'ensemble des etats atteignables par des epsilon-transitions a partir d'un ensemble d'etats
        Complexite: O(n+t) car on doit parcourir chaque etat et chaque transition 
        -> O(n^2) car il y a au plus 2 arcs qui sortent d'un noeud
    """
    tmp = list(states)
    closure = set(states)
    while tmp:
        state = tmp.pop()
        for trans in ndfa.transitions.get(state, []):
            if trans[0] is None and trans[1] not in closure:
                closure.add(trans[1])
                tmp.append(trans[1])
    return frozenset(closure)

def move(ndfa, states, symbol):
    """
        Donne les états accessibles depuis les états {states} à partir du symbole {symbol}
        Complexite: O(n+t) car elle doit verifier toutes les transitions sortant des etats
        -> O(n^2)
    """
    next_states = set()
    for state in states:
        for trans in ndfa.transitions.get(state, []):
            if trans[0] == symbol:
                next_states.add(trans[1])
    return next_states


#################### MINI DFA

# Fonction principale de minimisation
def minimize_dfa(dfa):
    states = sorted(dfa.states)
    symbols = extract_symbols(dfa)
    paires = initialize_paires(dfa, states)
    mark_distinguishable_pairs(paires, states, symbols, dfa)
    state_sets = merge_indistinguishable_states(paires, states)
    return construct_minimized_dfa(state_sets, dfa, symbols)

# Extraction des symboles
def extract_symbols(dfa):
    symbols = set()
    for transitions in dfa.transitions.values():
        symbols.update(transitions.keys())
    return symbols

# Initialisation de la table des paires
def initialize_paires(dfa, states):
    n = len(states)
    paires = [[False] * n for _ in range(n)]
    # Marquer les paires où un état est acceptant et l'autre non
    for i in range(n):
        for j in range(i + 1, n):
            if (states[i] in dfa.accept_states) != (states[j] in dfa.accept_states):
                paires[i][j] = True
    return paires

# Marquage des paires initialement distinguables
def mark_distinguishable_pairs(paires, states, symbols, dfa):
    n = len(states)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                if not paires[i][j]:
                    for symbol in symbols:
                        next_i = dfa.transitions.get(states[i], {}).get(symbol)
                        next_j = dfa.transitions.get(states[j], {}).get(symbol)
                        
                        # Si une transition est manquante dans un état mais pas l'autre
                        if (next_i is None) != (next_j is None):
                            paires[i][j] = True
                            changed = True
                            break
                        
                        if next_i is not None and next_j is not None:
                            idx_i = states.index(next_i)
                            idx_j = states.index(next_j)
                            if idx_i > idx_j:
                                idx_i, idx_j = idx_j, idx_i
                            
                            if paires[idx_i][idx_j]:
                                paires[i][j] = True
                                changed = True
                                break

# Fusion des états indiscernables
def merge_indistinguishable_states(paires, states):
    n = len(states)
    state_sets = []
    for i in range(n):
        found = False
        for state_set in state_sets:
            representative = next(iter(state_set))
            rep_idx = states.index(representative)
            pair = (min(i, rep_idx), max(i, rep_idx))
            if not paires[pair[0]][pair[1]]:
                state_set.add(states[i])
                found = True
                break
        if not found:
            state_sets.append({states[i]})
    return state_sets

# Construction du DFA minimisé
def construct_minimized_dfa(state_sets, original_dfa, symbols):
    state_mapping = {state: idx for idx, state_set in enumerate(state_sets) for state in state_set}
    minimized_dfa = DFA()
    
    for idx, state_set in enumerate(state_sets):
        minimized_dfa.states.add(idx)
        if original_dfa.start_state in state_set:
            minimized_dfa.start_state = idx
        if original_dfa.accept_states & state_set:
            minimized_dfa.accept_states.add(idx)
    
    for idx, state_set in enumerate(state_sets):
        representative = next(iter(state_set))
        for symbol in symbols:
            next_state = original_dfa.transitions.get(representative, {}).get(symbol)
            if next_state is not None:
                to_state = state_mapping[next_state]
                minimized_dfa.add_transition(idx, symbol, to_state)
    
    return minimized_dfa


###################### REGEX SEARCH

def search_regex(dfa, text):
    matches = []
    text_length = len(text)
    symbols = set()
    for transitions in dfa.transitions.values():
        symbols.update(transitions.keys())

    for start_pos in range(text_length):
        current_state = dfa.start_state
        position = start_pos
        while position < text_length:
            symbol = text[position]
            if symbol not in symbols:
                break  # caractère non reconnu
            if symbol in dfa.transitions.get(current_state, {}):
                current_state = dfa.transitions[current_state][symbol]
                if current_state in dfa.accept_states:
                    # correspondance trouvée de start_pos à position
                    match = text[start_pos:position+1]
                    matches.append((start_pos, position+1, match))
                    break # on break sur le premier match
            else:
                break  # plus de transition possible pour "symbol"
            position += 1
    return matches

