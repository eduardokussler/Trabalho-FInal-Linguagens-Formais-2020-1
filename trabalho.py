import csv
import argparse

class GLUD:
    
    # Construtor da classe
    def __init__(self):
        # le o arquivo com a definição
        file_name = self.parse_args()
        lines = self.get_lines(file_name)
        # le os estados, que serão as variaveis da gramatica
        equals_pos = lines[0].find('=')
        lines[0] = lines[0][equals_pos+1:].strip()[1:].strip()[1:].strip()
        self.variables, lines[0] = self.read_until_end_char(lines[0],'}')
        # le o alfabeto, que serão os simbolos terminais da gramatica
        lines[0] = lines[0].strip()[1:].strip()[1:].strip()
        self.alphabet, lines[0] = self.read_until_end_char(lines[0],'}')
        lines[0] = lines[0].strip()[1:].strip()
        # le o nome da fução programa
        self.prog, lines[0] = self.read_string(lines[0])
        lines[0] = lines[0].strip()
        # le o simbolo inicial
        self.initial_symbol, lines[0] = self.read_string(lines[0])
        lines[0] = lines[0].strip()[1:].strip()
        # le os estados finais
        self.final_states, lines[0] = self.read_until_end_char(lines[0],'}')
        # cria as produções do automato lendo a função
        self.prod = self.read_function(lines)
        # coloca as produções vazias necessarias na transformação para gramatica
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

    # Le caracteres até marcador de fim
    def read_until_end_char(self, line, end_char):
        end_string = False
        string = ""
        lst = []
        i = 0
        while(not end_string and i < len(line)): # enquanto não encontrar o marcador le o proximo simbolo
            symbol = line[i]
            if(line[i] != '\\'): # se não é barra 
                if(line[i] == ','): # verifica se for virgula para colocar a string atual na lista e reseta a string
                    lst.append(string.strip())
                    string = ""
                elif(line[i] == end_char): # se é o marcador coloca o que tem atualmente na lista para terminar o loop
                    lst.append(string.strip())
                    end_string = True
                else: # se é um caractere normal adiciona a string
                    string += symbol
            else: # se é uma barra, adiciona o proximo caractere independente do que ele é
                i += 1
                symbol = line[i]
                string += symbol

            i += 1

        return lst, line[i:]

    # Le uma string verificando caracteres especiais
    def read_string(self, line,separator = ','):
        end_string = False
        string = ""
        i = 0
        while(not end_string and i < len(line)): # enquanto não termina a string ou não encontra o marcador(',') le a string
            symbol = line[i]
            if(line[i] != '\\'): # se não for barra verifica se é o separador para  terminar a leitura, e se não for o separador le o simbolo
                if(line[i] == separator):
                    end_string = True
                else:
                    string += symbol
            else: # se é uma barra le o proximo simbolo
                i += 1
                symbol = line[i]
                string += symbol

            i += 1
        return string.strip(), line[i:]

    # Le a funcao programa realizando os tratamentos necessarios de string
    def read_function(self,lines):
        lines = lines[2:]
        prod = {}
        for line in lines: #loop para cada (< qi >, < si >) = < qj > da função
            # leitura de (< qi >, < si >)
            line = line.strip()[1:].strip()
            lst, line = self.read_until_end_char(line,')')  
            line = line.strip()[1:].strip()
            # leitura de < qj >
            lst.append(self.read_string(line)[0])
            # adiciona a produção < qi > -> < si >< qj >
            if not prod.get(lst[0]): # se a lista de produções de < qi > está vazia cria a lista
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
                pos_space = string.find(' ')
                command = string[:pos_space]
                arg = string[pos_space:].strip().split(' ')
                if len(arg) == 1 and command == 'word':
                    self.word(self.read_string(arg[0][1:-1],'')[0])
                elif len(arg) == 1 and command == 'list':
                    self.read_csv(arg[0])
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
            word_list = self.read_word_list(word_list)
        self.list_words(word_list)
      except:
        print("Couldn't open file")
    
    # Le a string com as palavras do csv e retorna uma lista com essas palavras
    def read_word_list(self, word_list):
        lst = []
        i = 0
        while word_list != '': # loop para ler a string com as palavras
            # Encontra a posição das primeiras aspas
            pos_beg = word_list.find('''"''')
            # retira as primeiras aspas da string
            word_list = word_list[pos_beg+1:]
            pos_end = word_list.find('''"''')
            string = ""
            # Se o caractere anterior as aspas for uma \
            # significa que a quote faz parte da palavra e não 
            # representa o fim da palavra
            while pos_end - 1 >= 0 and word_list[pos_end - 1] == '\\': # loop para ler os quotes da palavra
                string += word_list[:pos_end - 1] + word_list[pos_end]
                word_list = word_list[pos_end+1:]
                pos_end = word_list.find('''"''')

            string += word_list[:pos_end]
            lst.append(string)
            word_list = word_list[pos_end+1:]
        
        return [self.read_string(i, '')[0] for i in lst]

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
        # separa a palavra em uma lista de simbolos
        symbol_list = self.parse_word(word)
        # se algum dos simbolos não pertence ao alfabeto, rejeita a palavra
        not_symbols = [i for i in symbol_list if i not in self.alphabet]
        if not_symbols:
            return False, None

        derivation = [[self.initial_symbol]] # inicia com o simbolo inicial    
        for symbol in symbol_list: # le os simbolos da palavra 
            # procura a lista de produções do simbolo, se não encontrar então a palavra não é rejeitada
            prod_list = self.prod.get(derivation[-1][-1])
            if not prod_list:
                return False, None
            # busca na lista de produções uma produção para gerar o simbolo atual    
            found = False
            for i,j in prod_list:
                if i == symbol: # simbolo encontrado, coloca um novo passo da derivação
                    derivation.append(derivation[-1][:-1] + [i, j])
                    found = True 
                    break
            if not found: # simbolo não encontrado e portanto a palavra deve ser rejeitada
               return False, None

        # busca para a variavel mais a direita se há porduções dela, se não houver então a palavra é rejeitada
        prod_list = self.prod.get(derivation[-1][-1])
        if not prod_list:
            return False, None
        # se há produções, busca se há a produção vazia    
        found = False
        for i,j in prod_list:
            if i == '': # encontrou a produção vazia
                derivation.append(derivation[-1][:][:-1]) # coloca um novo passo da derivação
                found = True 
                break
        if not found: # não encontrou, portanto a palavra não é reconhecida
           return False, None
        else: # encontrou retorna a palavra e a derivação
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