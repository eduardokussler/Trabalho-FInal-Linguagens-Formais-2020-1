# Trabalho-FInal-Linguagens-Formais-2020-1
 

Grupo: 
Eduardo Eugênio Kussler (315799), 
Gabriel Couto Domingues (302229), 
Thiago Sotoriva Lermen (313020)
Turma: B
Professor: Lucio Mauro Duarte

Para executar o programa use: python3 trabalho.py <arquivo_definicao_AFD>

O programa recebe por linha de comando o caminho para um arquivo com a definição de um AFD no seguinte formato:

< M >=({< q0 >,...,< qn >},{< s1 >,...,< sn >},Prog,< ini >,{ < f0 >,...,< fn >})
Prog
(< q0 >,< s1 >)=< q1 >
...
(< qn >,< sn >)=< q0 >

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

"< p1 >","< p2 >",....,"< pn >"

As palavras testadas pelo programa, usando o comando list ou word, podem conter uma contrabarra que funciona como na leitura da definição do automato.
A palavra vazia pode ser testada usando "".
Se uma palavra contem simbolos que não pertencem a lista de simbolos da linguagem, ela será rejeitada.
