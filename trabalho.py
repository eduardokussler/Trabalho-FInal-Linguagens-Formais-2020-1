'''
Trabalho final (ETAPA 2) - Linguagens Formais e Autômatos

Grupo: 
Eduardo Eugênio Kussler (315799), 
Gabriel Couto Domingues (302229), 
Thiago Sotoriva Lermen (313020)
Turma: B
Professor: Lucio Mauro Duarte

Para executar o programa use: python3 trabalho.py <arquivo_definicao_AFD>

O programa recebe por linha de comando o caminho para um arquivo com a definição de um AFD no seguinte formato:

<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},Prog,<ini>,{ <f0>,...,<fn>})
Prog
(<q0>,<s1>)=<q1>
...
(<qn>,<sn>)=<q0>

onde:
< M >: nome dado ao autômato;
< qi >: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado do autômato;
< si >: para 1 ≤ i ≤ n, com n ∈ N e n ≥ 1, representa um símbolo do alfabeto da
linguagem reconhecida pelo autômato;
< ini >: indica o estado inicial do autômato, sendo que ini é um estado do autômato;
< f i >: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado final do autômato,
sendo que f i é um estado do autômato;
(< qi >, < si >) = < qj >: descreve a função programa aplicada a um estado qi e um
símbolo de entrada si que leva a computação a um estado qj.

Sendo que se algum dos caracteres usados como separador na definição ('=', '(', ')', '{', '}', ',') é usado como um simbolo/estado/nome deve ser usado
uma contrabarra ('\') antes dele para garantir que ele seja lido corretamente na definição, já que foi definido que sempre que for encontrada uma 
contrabarra na leitura o próximo simbolo será lido como sendo parte da string. 

O programa então constroi uma gramática linear unitária à direita equivalente a esse automato, sendo que diferente do algoritmo mostrado em 
aula, e semelhante à forma como o JFLAP faz a conversão, não é criado um simbolo novo S para ser usado como simbolo inicial, já que esse
simbolo S só teria uma produção que substitui S pelo simbolo que representa o estado inicial do automato, portanto não sendo necessario para
o reconhecimento da linguagem.

Após a criação do automato, o programa inicializa a interface shell para execução dos comandos:
    # - exit: sai do programa
    # - word "<palavra>": le uma palavra via input e imprime sua derivação caso a palavra seja aceita
    # - list <caminho>: le uma lista de palavras dada atraves de um caminho para um arquivo CSV e mostra quais palavras são geradas pela gramatica
Sendo que o arquivo CSV deve ter o seguinte formato:
"<p1>","<p2>",....,"<pn>"

As palavras testadas pelo programa, usando o comando list ou word, podem conter uma contrabarra que funciona como na leitura da definição do automato.
A palavra vazia pode ser testada usando "".

'''
import csv
import argparse

class GLUD:
    
    def __init__(self):
        '''Construtor da classe.'''

        # le o arquivo com a definição
        file_name = self.parse_args()
        lines = self.get_lines(file_name)
        # le o nome do automato
        lines[0] = self.read_string(lines[0],'=')[1]
        # le os estados, que serão as variaveis da gramatica
        lines[0] = lines[0][lines[0].find('{') + 1:]
        self.variables, lines[0] = self.read_until_end_char(lines[0],'}')
        # le o alfabeto, que serão os simbolos terminais da gramatica
        lines[0] = lines[0][lines[0].find('{') + 1:]
        self.alphabet, lines[0] = self.read_until_end_char(lines[0],'}')
        # le o nome da fução programa
        lines[0] = lines[0][lines[0].find(',') + 1:]
        self.prog, lines[0] = self.read_string(lines[0])
        # le o simbolo inicial
        self.initial_symbol, lines[0] = self.read_string(lines[0])
        # le os estados finais
        lines[0] = lines[0][lines[0].find('{') + 1:]
        self.final_states, lines[0] = self.read_until_end_char(lines[0],'}')
        # cria as produções do automato lendo a função
        self.prod = self.read_function(lines[2:])
        # coloca as produções vazias necessarias na transformação para uma gramatica
        self.empty_prod()

    def parse_args(self):
      '''Retorna o nome do arquivo que foi passado como argumento na linha de comando.'''
      parser = argparse.ArgumentParser(description="Creates a grammar from a DFA")
      parser.add_argument("DFA", metavar="DFA", type=str, help="File to read DFA")
      return parser.parse_args().DFA
    
    def get_lines(self, file_name):
        '''Retorna as linhas do arquivo em uma lista.'''
        with open(file_name) as input_file:
            lines = input_file.read().splitlines()
            return lines

    def read_string(self, line, separator = ','):
        '''
        Le uma string até que o separador seja encontrado ou a string termine.
        Caso uma contrabarra seja encontrada, le o próximo simbolo como fazendo parte da string.
        Retorna uma tupla com: 
            A string lida, removendo os espaços em branco no inicio e no fim da string;
            A substring que começa com o caractere após a leitura do separador até o fim da string passada como argumento.
        Caso a string seja lida até o fim a substring será "".
        '''
        end_string = False
        string = ""
        i = 0
        while(not end_string and i < len(line)): # enquanto não termina a string ou não encontra o separador le a string
            symbol = line[i]
            if(line[i] != '\\'): # se não for barra verifica se é o separador para terminar a leitura, e se não for o separador le o simbolo
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

    def read_until_end_char(self, line, end_char):
        '''
        Le uma string até que o caractere de fim seja encontrado ou a string termine.
        Considera a virgula (',') como separador dos simbolos.
        Caso uma contrabarra seja encontrada, le o próximo simbolo como fazendo parte da string.
        Retorna uma tupla com: 
            A lista com as strings lidas, removendo os espaços em branco no inicio e no fim das strings;
            A substring que começa com o caractere após a leitura do marcador de fim até o fim da string passada como argumento.
        Caso a string seja lida até o fim a substring será "".
        '''
        end_string = False
        string = ""
        lst = []
        i = 0
        while(not end_string and i < len(line)): # enquanto não encontrar o marcador ou não terminar a string le o proximo simbolo
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

        if i == len(line): # se não encontrou o marcador, coloca a ultima string na lista.
            lst.append(string.strip())

        return lst, line[i:]

    def read_function(self,lines):
        '''
        Le a funcao programa realizando os tratamentos necessarios de string. Retorna um dicionario em que as chaves são as variaveis da gramatica e 
        para cada variavel é armazenada uma lista com tuplas que representam as produções da seguinte forma:
        
        q0 : [(s1,q1),(s2,q2)...]

        Considerando que na função programa temos:

        (q0,s1)=q1
        (q0,s2)=q2
        '''

        prod = {}
        for line in lines: # loop para cada (< qi >, < si >) = < qj > da função
            # leitura de (< qi >, < si >)
            line = line[line.find('(') + 1:]
            lst, line = self.read_until_end_char(line,')')  
            line = line[line.find('=') + 1:]
            # leitura de < qj >
            lst.append(self.read_string(line)[0])
            # adiciona a produção < qi > -> < si >< qj >
            if not prod.get(lst[0]): # se a lista de produções de < qi > está vazia cria a lista
                prod[lst[0]] = []
            prod[lst[0]].append((lst[1],lst[2]))
                
        return prod
    
    def empty_prod(self):
        '''
        Adiciona as produções vazias à gramatica.
        Para cada estado final é adicionado ('','') à lista de produções.
        '''
        for state in self.final_states: # percorre a lista de estados finais para adicionar as produções F -> ε
            if not self.prod.get(state): # se não há nenhuma produção com o estado F, cria a lista de produções
                self.prod[state] = []
            self.prod[state].append(('','')) # adiciona a produção com ε como uma tupla ('','')
  
    def shell(self):
        '''
        Inicializa interface shell para execução dos comandos:
            # - exit: sai do programa
            # - word "<palavra>": le uma palavra via input e imprime sua derivação caso a palavra seja aceita
            # - list <caminho>: le uma lista de palavras dada atraves de um caminho para um arquivo CSV e mostra quais palavras são geradas pela gramatica
        Sendo que o arquivo CSV deve ter o seguinte formato:
        "<p1>","<p2>",....,"<pn>"

        As palavras testadas pelo programa, usando o comando list ou word, podem conter uma contrabarra que funciona como 
        na leitura da definição do automato.
        A palavra vazia pode ser testada usando "".
        '''
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
                else: # se o usuario digitar um comando mais argumentos do que o necessario, considera como um comando invalido
                    print("INVALID COMMAND")

    def word(self, word):
        '''
        Verifica se a palavra faz parte da linguagem de entrada Se a palavra for aceita printa uma mensagem de aceitação 
        e a respectiva derivação.  
        '''
        accepted, derivation = self.check_word(word)
        if not accepted:
            print("Palavra não pertence à linguagem")
        else:
            print("Palavra aceita, derivação: ", end = '')
            self.print_derivation(derivation)

    def check_word(self, word):
        '''
        Verifica se a palavra pertence a linguagem gerada pela gramatica.
        Retorna uma tupla com:

            Um booleano indicando se a palavra é gerada pela gramatica;
            A derivação da palavra.

        Caso a palavra não possa ser derivada, retorna None em vez de retornar a derivação.
        '''
        symbol_list = self.parse_word(word) # separa a palavra em uma lista de simbolos
        # se algum dos simbolos não pertence ao alfabeto, rejeita a palavra
        not_symbols = [i for i in symbol_list if i not in self.alphabet]
        if not_symbols:
            return False, None

        symbol_list.append('') # coloca '' para quando a palavra original for lida verificar se é possivel gerar a palavra vazia com a ultima variavel
        # inicia a derivação com o simbolo inicial
        # a derivação é uma lista de listas em que cada sub-lista é um conjunto de simbolos que representa a string em um passo de derivação    
        derivation = [[self.initial_symbol]]
        for symbol in symbol_list: # le os simbolos da palavra 
            # procura a lista de produções da variavel, se não encontrar então a palavra é rejeitada
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

        return True, derivation
    
    def parse_word(self, word):
        '''
        Faz o parse da palavra, como um simbolo pode ter mais de um caractere coloca cada simbolo da palavra em uma lista.
        Retorna uma lista com os simbolos da palavra.
        '''
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
        # se terminou de ler a palavra e o conjunto de caracteres final não representa um simbolo, coloca a string atual como simbolo na lista
        if string != "":
            lst.append(string)
        return lst
    
    def print_derivation(self, derivation):
        '''
        Printa a derivação da palavra dada como entrada. A derivação é uma lista de listas em que 
        cada sub-lista é um conjunto de simbolos que representa a string em um passo de derivação    
        '''
        print(derivation[0][0],end = '')
        for val in derivation[1:]:
            temp = "".join(val)
            print(f"->{temp}",end = '')
        print()

    def read_csv(self, file_name):
      '''Le o arquivo CSV dado com a lista de palavras. Imprime o conjunto das palavras aceitas e rejeitadas'''
      word_list = []
      try:
        with open(file_name) as file:
            word_list = file.read()
            word_list = self.read_word_list(word_list)
        self.list_words(word_list)
      except:
        print("Couldn't open file")
    
    def read_word_list(self, word_list):
        '''Le a string com as palavras do csv e retorna uma lista com essas palavras.'''
        lst = []
        while word_list != '': # loop para ler a string com as palavras
            # Encontra a posição das primeiras aspas
            pos_beg = word_list.find('''"''')
            # retira as primeiras aspas da string
            word_list = word_list[pos_beg+1:]
            # Se o caractere anterior as aspas for uma \
            # significa que a quote faz parte da palavra e não 
            # representa o fim da palavra
            string = ""
            pos_end = word_list.find('''"''')
            while pos_end - 1 >= 0 and word_list[pos_end - 1] == '\\': # loop para ler os quotes da palavra
                string += word_list[:pos_end - 1] + word_list[pos_end]
                word_list = word_list[pos_end+1:]
                pos_end = word_list.find('''"''')

            string += word_list[:pos_end]
            lst.append(string)
            word_list = word_list[pos_end+1:]
        
        return [self.read_string(i, '')[0] for i in lst]

    def list_words(self, word_list):
        '''
        Verifica se as palavras de uma dada lista de palavras
        são aceitas ou rejeitadas pela linguagem. Printa os conjuntos
        ACEITA e REJEITA da linguagem.
        '''
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


glud = GLUD() # cria a gramatica a partir do arquivo com a definição do automato
glud.shell() #shell para a execução das funções