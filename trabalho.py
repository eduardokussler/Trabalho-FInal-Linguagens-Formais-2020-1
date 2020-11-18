import csv
import argparse

class GLUD:
    
    # Construtor da classe
    def __init__(self):
        file_name = self.parse_args()
        lines = self.get_lines(file_name)
        equals_pos = lines[0].find('=')
        # Esta no primeiro estado
        lines[0] = lines[0][equals_pos+1:].strip()[1:].strip()[1:]
        self.variables, lines[0] = self.read_curly_braces(lines[0])
        lines[0] = lines[0][1:].strip()[1:].strip()
        self.alphabet, lines[0] = self.read_curly_braces(lines[0])
        lines[0] = lines[0][1:].strip()
        self.prog, lines[0] = self.read_string(lines[0])
        lines[0] = lines[0].strip()
        self.initial_symbol, lines[0] = self.read_string(lines[0])
        lines[0] = lines[0].strip()[1:].strip()
        self.final_states, lines[0] = self.read_curly_braces(lines[0])
        self.prod = self.read_function(lines)
        self.empty_prod()

    # Retorna o nome do arquivo que foi passado como argumento na linha de comando
    def parse_args(self):
      parser = argparse.ArgumentParser(description="Creates a grammar from a DFA")
      parser.add_argument("DFA", metavar="DFA", type=str, help="File to read DFA")
      return parser.parse_args().DFA
    
    # Salva as linhas do arquivo
    def get_lines(self, file_name):
        with open(file_name) as input_file:
            lines = input_file.read().splitlines()
            return lines

    # Le caracteres que estão entre chaves
    def read_curly_braces(self, line):
        end_curly = False
        string = ""
        lst = []
        i = 0
        while(not end_curly):
            symbol = line[i]
            if(line[i] != '\\'):
                if(line[i] == ','):
                    lst.append(string.strip())
                    string = ""
                elif(line[i] == '}'):
                    lst.append(string.strip())
                    end_curly = True
                else:
                    string += symbol
            else:
                i += 1
                symbol = line[i]
                string += symbol

            i += 1

        return lst, line[i:]

    # Le uma string verificando caracteres especiais
    def read_string(self, line):
        end_string = False
        string = ""
        i = 0
        while(not end_string):
            symbol = line[i]
            if(line[i] != '\\'):
                if(line[i] == ','):
                    end_string = True
                else:
                    string += symbol
            else:
                i += 1
                symbol = line[i]
                string += symbol

            i += 1
        return string.strip(), line[i:]

    # Le a funcao programa realizando os tratamentos necessarios de string
    def read_function(self,lines):
        lines = lines[2:]
        prod = {}
        for line in lines:
            line = line.strip()[1:].strip()
            end_string = False
            lst = []
            string = ""
            i = 0
            
            while(not end_string):
              symbol = line[i]
              if(line[i] != '\\'):
                  if(line[i] == ','):
                      lst.append(string.strip())
                      string = ""
                  elif(line[i] == ')'):
                      lst.append(string.strip())
                      end_string = True
                  else:
                      string += symbol
              else:
                  i += 1
                  symbol = line[i]
                  string += symbol
              i += 1
            line = line.strip()[i+1:].strip()
            i = 0
            string = ""
            while(len(line[i:]) != 0):
                symbol = line[i]
                if(line[i] != '\\'):
                    string += symbol
                else:
                    i += 1
                    symbol = line[i]
                    string += symbol

                i += 1
            lst.append(string.strip())
            if not prod.get(lst[0]):
                prod[lst[0]] = []
            prod[lst[0]].append((lst[1],lst[2]))
                
        return prod
    
    # Define a lista de produções vazias
    def empty_prod(self):
        for state in self.final_states: # percorre a lista de estados finais para adicionar as produções F -> ε
            if not self.prod.get(state): # se não há nenhuma produção com o estado F, cria a lista de produções
                self.prod[state] = []
            self.prod[state].append(('','')) # adiciona a produção com ε como uma tupla ('','')

    # Inicializa interface shell para execucao dos comandos
    # - exit: sai do programa
    # - word: le uma palavra via input
    # - list: le uma lista de palavras dada atraves de um caminho para um arquivo CSV    
    def shell(self):
        while(True):
            string = input("$ ").strip()
            if string == 'exit':
                break
            else:
                lst = string.split(' ')
                if len(lst) == 2 and lst[0] == 'word':
                    self.word(lst[1])
                elif len(lst) == 2 and lst[0] == 'list':
                    self.read_csv(lst[1])
                else: # se o usuario digitar um com mais argumentos do que o necessario, considera um comando invalido
                    print("INVALID COMMAND")

    # Verifica se a palavra faz parte da linguagem de entrada
    # Se a palavra for aceita printa uma mensagem de aceitação 
    # e a respectiva derivação       
    def word(self, word):
        accepted, derivation = self.check_word(word)
        if not accepted:
            print("Palavra não aceita")
        else:
            print("Palavra aceita")
            print("Derivação: ")
            self.print_derivation(derivation)
    
    # Printa a derivação da palavra dada como entrada
    def print_derivation(self, derivation):
        print(derivation[0][0],end = '')
        for val in derivation[1:]:
            temp = "".join(val)
            print(f"->{temp}",end = '')
        print()

    # Le o arquivo CSV dado com a lista de palavras
    def read_csv(self, file_name):
      word_list = []
      try:
        with open(file_name) as file:
          word_list = file.read()
          word_list = word_list.split(',')
        word_list = [i.strip()[1:-1] for i in word_list]
        self.list_words(word_list)
      except:
        print("Couldn't open file")

    # Verifica se as palavras de uma dada lista de palavras (CSV file)
    # são aceitas ou rejeitadas pela linguagem. Printa os conjuntos
    # ACEITA e REJEITA da linguagem
    def list_words(self, word_list):
        accepted_list = []
        rejected_list = []
        for word in word_list: # loop para verificar cada palavra da lista
            accepted = self.check_word(word)[0]
            if accepted:
                accepted_list.append(word)
            else:
                rejected_list.append(word)
        # imprime os conjuntos ACEITA e REJEITA
        print("ACEITA:")
        for i in accepted_list:
            print(i)
        print()
        print("REJEITA")
        for i in rejected_list:
          print(i)

    # verifica se a palavra pertence a linguagem gerada pela gramnatica?
    def check_word(self, word):
        symbol_list = self.parse_word(word)
        not_symbols = [i for i in symbol_list if i not in self.alphabet]
        if not_symbols:
            return False, None
        derivation = [[self.initial_symbol]]
            
        for symbol in symbol_list:
            prod_list = self.prod.get(derivation[-1][-1])
            if not prod_list:
                return False, None
            found = False
            for i,j in prod_list:
                if i == symbol:
                    temp = derivation[-1][:-1]
                    temp.append(i)
                    temp.append(j)
                    derivation.append(temp)
                    found = True 
                    break
            if not found:
               return False, None
    
        prod_list = self.prod.get(derivation[-1][-1])
        if not prod_list:
            return False, None
        found = False
        for i,j in prod_list:
            if i == '':
                derivation.append(derivation[-1][:][:-1])
                found = True 
                break
        if not found:
           return False, None
        return True, derivation 
    
    # Faz o parse da palavra, como um simbolo pode ter mais de um caractere coloca cada simbolo da palavra em uma lista
    def parse_word(self, word):
        lst = []
        string = ""
        for c in word: 
            # Para cada caractere na palavra le o caractere, adiciona a string atual, e verifica se a string atual é um simbolo do alfabeto
            # Se for, adiciona a string na lista de simbolos da palavra e zera a string
            # Se não for, continua lendo caracteres até que encontre um simbolo do alfabeto
            string += c
            if(string in self.alphabet):
              lst.append(string)
              string = ""
        # se terminou de ler a palavra e o conjunto de simbolos final não representa um simbolo, coloca a string atual como simbolo na lista
        if string != "":
            lst.append(string)
        return lst


glud = GLUD() # cria a gramatica a partir do arquivo com a definição do automato
glud.shell() #shell para a execução das funções