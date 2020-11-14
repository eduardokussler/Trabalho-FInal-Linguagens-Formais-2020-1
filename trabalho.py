
class GLUD:
    
    def __init__(self, file_name):
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
        lines[0] = lines[0][1:].strip()
        self.final_states, lines[0] = self.read_curly_braces(lines[0])
        self.prod = self.read_function(lines)
        self.empty_prod()

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
            
                
         
    def parse_word(self, word):
        lst = []
        string = ""
        for c in word:
            string += c
            if(string in self.alphabet):
              lst.append(string)
              string = ""
        
        if string != "":
            lst.append(string)
        return lst

    def empty_prod(self):
        for state in self.final_states:
            if not self.prod.get(state):
                self.prod[state] = []
            self.prod[state].append(('',''))

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

    def get_lines(self, file_name):
        ''' Given a file, returns a list where each element is the corresponding line of the file'''
        with open(file_name) as input_file: # with automatically closes file
            lines = input_file.read().splitlines()
            return lines

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


glud = GLUD('formato_entrada.txt')
print(glud.prod)

print(glud.check_word("R$1.00R$1.00R$1.00")[1])
print(glud.check_word("R$1.00R$5.00")[1])
print(glud.check_word("R$2.00R$2.00R$5.00")[1])
print(glud.check_word("R$2.00R$5.00R$5.00")[1])
print(glud.check_word("R$5.00R$5.00R$5.00")[1])
print(glud.check_word("R$0.50R$1.00R$1.00R$1.00")[1])
print(glud.check_word("R$0.50R$1.00R$5.00")[1])
print(glud.check_word("R$0.50R$2.00R$2.00R$5.00")[1])
print(glud.check_word("R$0.50R$2.00R$5.00R$5.00")[1])
print(glud.check_word("R$0.50R$5.00R$5.00R$5.00")[1])