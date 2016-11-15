import copy

class GrammarAutomata(object):
    def __init__(self, g_source=None, a_source=None):
        self.grammar_source = g_source
        self.automata_source = a_source
        self.grammar_details = {}
        self.automata_details = {}

    @staticmethod
    def parse_productions(productions):
        result = {}
        for production in productions:
            lhs, rhs = production.strip().split('->')
            for r in rhs.split('|'):
                if not lhs in result.keys():
                    result[lhs] = [r]
                else:
                    result[lhs].append(r)
        return result

    @staticmethod
    def parse_transitions(transitions):
        result = {}
        for transition in transitions:
            lhs, rhs = transition.strip().split(':')
            key = tuple(lhs.split(','))
            try:
                value = rhs.split(',')
            except:
                value = list(rhs)
            result[key] = value
        return result

    def read_grammar_keyboard(self):
        nonterminals, terminals, prods = [], [], []

        len_nonterminals = int(raw_input('How many nonterminals?: '))
        for i in range(1, len_nonterminals + 1):
            nonterminals.append(raw_input('Nonterminal {}: '.format(i)))

        len_terminals = int(raw_input('How many terminals?: '))
        for i in range(1, len_terminals + 1):
            terminals.append(raw_input('Terminal {}: '.format(i)))

        len_prod = int(raw_input('How many productions in the set?: '))
        for i in range(1, len_prod + 1):
            prods.append(raw_input('Production {}: '.format(i)))

        self.grammar_details['nonterminals'] = nonterminals
        self.grammar_details['terminals'] = terminals
        self.grammar_details['init_state'] = raw_input('Enter initial state: ')
        self.grammar_details['productions'] = self.parse_productions(prods)

    def read_grammar_file(self):
        """ Order of elements in file!
        - nonterminals, terminals, initial state, productions
        """
        with open(self.grammar_source, "r") as f:
            self.grammar_details['nonterminals'] = f.readline().split()
            self.grammar_details['terminals'] = f.readline().split()
            self.grammar_details['init_state'] = f.readline().strip()
            prods = f.readlines()
            self.grammar_details['productions'] = self.parse_productions(prods)

    def print_elements_grammar(self):
        grammar_details = self.grammar_details
        if not grammar_details:
            print('No grammar inserted')
            return
        print 'Set of nonterminals: ', grammar_details['nonterminals']
        print 'Set of terminals: ', grammar_details['terminals']
        print 'Initial state: ', grammar_details['init_state']
        print 'Set of productions: '
        for key, value in grammar_details['productions'].items():
            for v in value:
                print '{} -> {}'.format(key, ''.join(v))

    def read_automata_keyboard(self):
        states, alphabet, transitions, final_states = [], [], [], []
        len_states = int(raw_input('Length of set of states? '))
        print 'Enter set of states:'
        for i in range(1, len_states + 1):
            states.append(raw_input('State {} -->'.format(i)))

        len_alphabet = int(raw_input('Length of set of alphabet? '))
        print 'Enter alphabet:'
        for i in range(1, len_alphabet + 1):
            alphabet.append(raw_input('Alphabet {} -->'.format(i)))

        len_transitions = int(raw_input('Length of set of transitions? '))
        print 'Enter set of transitions: '
        for i in range(1, len_transitions + 1):
            transitions.append(raw_input('Transition {} -->'.format(i)))

        len_final_states = int(raw_input('Length of set of final states? '))
        print 'Enter set of states:'
        for i in range(1, len_final_states + 1):
            final_states.append(raw_input('Final state {} -->'.format(i)))

        self.automata_details['states'] = states
        self.automata_details['alphabet'] = alphabet
        self.automata_details['trans'] = self.parse_transitions(transitions)
        self.automata_details['final_states'] = final_states
        self.automata_details['init_state'] = raw_input('Enter init state: ')

    def read_automata_file(self):
        """File order!
        - states, alphabet, final states, transitions
        """
        with open(self.automata_source, "r") as f:
            self.automata_details['states'] = f.readline().split()
            self.automata_details['alphabet'] = f.readline().split()
            self.automata_details['final_states'] = f.readline().strip()
            self.automata_details['init_state'] = f.readline()
            trans = f.readlines()
            self.automata_details['trans'] = self.parse_transitions(trans)

    def print_elements_automata(self):
        automata_details = self.automata_details
        if not automata_details:
            print('No automata inserted')
            return
        print 'Set of states:', automata_details['states']
        print 'Alphabet: ', automata_details['alphabet']
        print 'Final states: ', automata_details['final_states']
        print 'initial_state: ', automata_details['init_state']
        print 'Transitions'
        for key, value in automata_details['trans'].items():
            print '%s, %s -> %s' % (key[0], key[1], '|'.join(value))

    def is_regular(self):
        print("Is it regular? ")
        grammar = self.grammar_details

        epsilon = True if '#' in grammar['terminals'] else False
        for key, value in grammar['productions'].items():
            if key not in grammar['nonterminals']:
                return "key not in nons"
            # parse each list in value (value is a list of lists)
            print(key, value)
            for v in value:
                print(v[0])
                if len(v) not in [1, 2]:
                    return "len prob"
                if len(v) == 1 and v[0] not in grammar['terminals']:
                    return "v[0] not in terms"
                if len(v) == 2:
                    if v[0] not in grammar['terminals'] and v[1] not in grammar['nonterminals']:
                        return "not in terms and nons"
                    if epsilon and key in v:
                        return "eps prob"
        return True

    def get_productions(self):
        production = productions.get(nonterminal_symbol)
        if production:
            print 'The productions of %s are: ' % nonterminal_symbol
            for p in production:
                print '%s -> %s' % (nonterminal_symbol, ''.join(p))
        else:
            print 'Symbol %s doesn\'t have any productions' % nonterminal_symbol

    def get_productions_symbol(self):
        production = productions.get(nonterminal_symbol)
        if production:
            print 'The productions of %s are: ' % nonterminal_symbol
            for p in production:
                print '%s -> %s' % (nonterminal_symbol, ''.join(p))
        else:
            print 'Symbol %s doesn\'t have any productions' % nonterminal_symbol

    def grammar_in_automata(self):
        """
        We need to compute M=(Q, E, f, q0, F) where:
            * Q = N U {k}, k not in N                   states
            * E - the same                              alphabet
            * q0 = S                                    initial state
            * F = k / {S,k}                             final states
            * f = {B/(A->aB) in P} U K                  transitions
        """
        states = copy.copy(nonterminals)
        states.append('k')
        alphabet = copy.copy(terminals)
        final_states = ['k']
        for value in productions[initial_state]:
            if '#' in value:
                final_states.append('#')
        transitions = {}
        for key, value in productions.items():
            for symbols in value:
                if len(symbols) == 2:
                    if not transitions.get((key, symbols[0])):
                        transitions[(key, symbols[0])] = [symbols[1]]
                    else:
                        transitions[(key, symbols[0])].append(symbols[1])
                elif len(symbols) == 1:
                    if not transitions.get((key, symbols[0])):
                        transitions[(key, symbols[0])] = ['k']
                    else:
                        transitions[(key, symbols[0])].append('k')
        display_automata(
            states, alphabet, transitions, final_states, initial_state
        )

    def automata_in_grammar(self):
        """
        We need to compute G=(N,E,P,S) where:
            * N = Q
            * S = q0
            * E - the same
            * P = {A->aB|f(A,a) in B} U {A->a|f(A,a) in B, B in F}
        """
        nonterminals = copy.copy(states)
        initial_state = automata_initial_state
        terminals = copy.copy(alphabet)
        productions = {}
        for key, value in transitions.items():
            b = set(value).intersection(final_states)
            if productions.get(key[0]):
                productions[key[0]].append([key[1], value[0]])
            else:
                productions[key[0]] = [key[1], value[0]]
            if b:
                productions[key[0]].append(key[1])
        if initial_state in final_states:
            if productions.get(initial_state):
                productions[initial_state].append('#')
            else:
                productions[initial_state] = ['#']
        display_grammar(nonterminals, terminals, productions, initial_state)

    @staticmethod
    def display_menu():
        return '1 - Read grammar from keyboard\n' + \
               '2 - Read grammar from file\n' + \
               '3 - Print grammar\n' + \
               '4 - Read finite automata from keyboard\n' + \
               '5 - Read finite automata from file\n' + \
               '6 - Display finite automata\n' + \
               '7 - Check regular grammar\n' + \
               '8 - Get productions\n' + \
               '9 - Get productions based on symbol\n' + \
               '10- From regular grammar into finite automata\n' + \
               '11- From finite automata into regular grammar\n0 - EXIT'

    def run(self):
        print(self.display_menu())
        menu = {
            1: self.read_grammar_keyboard,
            2: self.read_grammar_file,
            3: self.print_elements_grammar,
            4: self.read_automata_keyboard,
            5: self.read_automata_file,
            6: self.print_elements_automata,
            7: self.is_regular,
            8: self.get_productions,
            9: self.get_productions_symbol,
            10: self.grammar_in_automata,
            11: self.automata_in_grammar,
            0: exit,
        }
        option = True
        while option:
            try:
                option = int(raw_input())
                print(menu[option]())
            except ValueError as ve:
                print "Please select an option listed above this time"
            except KeyError as ke:
                print "Option not in list, try again"

if __name__ == '__main__':
    ga = GrammarAutomata(g_source="grammar.txt", a_source="automata.txt")
    ga.run()
