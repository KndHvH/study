# Comandos Git básicos

## 1. git config
Quando você está utilizando o Git pela primeira vez ou com uma instalação nova, em um projeto colaborativo, esse comando é fundamental para configurar sua identidade de usuário, inserindo informações como nome e email que serão empregadas em cada commit.
```
$ git config –global user.name “Seu nome”

$ git config –global user.email “Seu email”
```
## 2. git init
Esse é o comando que você irá utilizar para criar um novo projeto de git. O comando irá criar um repositório novo em branco e, a partir daí, será possível armazenar seu código fonte, alterar, salvaguardar alterações etc.

```
$ git init

Se você já possui um repositório anterior ou deseja criar um repositório com um nome em específico, você pode passar o nome como parâmetro do comando:

$ git init <O nome do seu repositório>
```
## 3. git clone
Esse comando Git cria uma cópia exata de um repositório já existente.

Então… quando usar git init e quando usar git clone? O git clone é mais avançado, uma vez que ele mesmo executa um comando git init internamente. Além disso, ele verifica todo o conteúdo do projeto.

Exemplo:
```
git clone <URL do seu projeto>
```
## 4. git add


Esse comando Git adiciona os arquivos especificados de código ao seu repositório, sejam arquivos novos ou arquivos anteriores que foram alterados. Oferece diferentes possibilidades de sintaxe.

Exemplo:
```
$ git add seu_arquivo (esse comando irá adicionar o arquivo em específico ao repositório)

$ git add * (esse comando irá adicionar todos os arquivos novos e/ou modificados ao repositório)
```
## 5. git commit
É fundamental se estabelecer uma diferença entre git add e git commit:

git add adiciona seus arquivos modificados à fila para serem submetidos a um commit posteriormente. Os arquivos não passaram por um commit.
O git commit executa o commit dos arquivos que foram adicionados e cria uma nova revisão com um log. Por outro lado, se você não adicionar nenhum arquivo, o git não fará o commit de nada.
É possível combinar as duas ações em um único comando: 
```

$ git commit -a.
```
Também é possível adicionar uma mensagem para a execução de um commit. Exemplo:
```
$ git commit -m “seu comentário”
```
## 6. git branch
É comum na maior parte do tempo possuir múltiplas variações em seu repositório Git, chamadas de branches (“ramificações”). A grosso modo, um branch é um caminho independente de desenvolvimento, uma alternativa.

A princípio pode parecer fácil se perder em diversos caminhos, mas o comando git branch facilita o gerenciamento de tudo isso. Com diferentes parâmetros, é possível listar, criar ou apagar os branches.

Exemplos:
```
$ git branch (lista todas as ramificações)

$ git branch <nome_do_branch> (cria um branch com o nome especificado)

$ git branch -d <nome_do_branch> (deleta o branch com o nome especificado)
```
## 7. git checkout
Ainda sobre branches, esse comando Git pode ser utilizado para trocar de uma ramificação para outra.

Exemplo:
```
$ git checkout <nome_do_branch>

Também é possível combinar operações, criando e fazendo o checkout de um novo branch com um único comando:

$ git checkout -b <nome_do_branch_novo>
```
# Comandos Git intermediários
## 8. git remote
O comando Git remote estabelece uma conexão entre seu repositório local e um repositório remoto.

Exemplo:
```
$ git remote add <nomecurto> <url>
```
## 9. git push


Esse comando serve para subir suas modificações para um repositório remoto conectado anteriormente com git remote.

Exemplo:
```
$ git push -u <nome_curto> <nome_do_branch>

É importante especificar a origem e o upstream antes de usar o git push. Veja o exemplo:

$ git push –set-upstream <nome_curto> <nome_do_branch>

$ git push -u origin <branch>
```
## 10. git fetch
Quando você precisa baixar as mudanças criadas por outros membros do seu projeto colaborativo, você precisa do comando Git fetch. A partir desse comando, você irá receber todas as informações de commits, para avaliar, antes de aplicar essas alterações na sua versão local do repositório.

Exemplo:
```
$ git fetch
```
## 11. git pull
O comando Git pull baixa o conteúdo (não os metadados) do que foi alterado no repositório remoto para o seu repositório local e imediatamente atualiza seu contreúdo para a última versão.

Exemplo:
```
$ git pull <URL>
```
## 12. git stash


Esse comando Git armazena temporariamente seus arquivos modificados em uma área chamada stash (“esconderijo”), sem interagir com os outros arquivos até ser necessário.

Exemplo:
```
$ git stash

Para listar todos os seus “esconderijos”, usamos:

$ git stash list

Quando for o momento de aplicar o conteúdo do stash a um branch, usamos o parâmetro “apply”:

$ git stash apply
```
## 13. git show
Quer detalhes específicos sobre um commit que o log não mostra? O comando Git show é a resposta.

Exemplo:
```
$ git show <hash_do_commit>
```
## 14. git rm
Para remover arquivos da sua pasta, você pode utilizar o comando Git rm.

Exemplo:
```
$ git rm <nome_do_arquivo>
```
## 15. git help
Existem inúmeros comandos no Git, muito mais do que os 25 dessa lista, cada um com sua função, parâmetros e características. Felizmente, o próprio Git tem o comando help para trazer ajuda diretamente no terminal.

Exemplo:
```
$ git help <comando que se tem dúvida>
```
## 16. git merge


Esse comando Git integra as mudanças de dois branches diferentes em um único branch. Ele precisa ser iniciado a partir de um branch já selecionado, que será mesclado com outro, com o nome passado por parâmetro.

Exemplo:
```
$ git merge <nome_do_branch>
```
# Comandos Git avançados
## 17. git rebase
Git rebase a princípio parece fazer o mesmo que um comando git merge: ele integra dois branches em um branch único. Porém, esse comando refaz o histórico de commits, tornando-o linear. É o mais indicado para consolidar múltiplos branches.

Exemplo:
```
$ git rebase <base>
```
## 18. git pull –rebase
Essa é uma variação do comando pull mostrado anteriormente. A partir dessa instrução, o Git irá fazer um rebase (não um merge) depois de se utilizar um comando pull.

Exemplo:
```
$ git pull –rebase
```
## 19. git cherry-pick
Esse é um comando poderoso que permite selecionar qualquer commit específico de um brach e aplicá-lo a outro branch, sem precisar de uma mescla completa. A operação fica adicionada no histórico.

Exemplo:
```
$ git cherry-pick <commit-hash>
```
## 20. git archive


Esse comando Git combina múltiplos arquivos em um único arquivo, como se fosse um arquivo zipado. Esse pacote pode ser aberto depois e os arquivos contidos podem ser extraídos individualmente.

Exemplo:
```
$ git archive –format zip HEAD > archive-HEAD.zip
```
## 21. git blame
O comando “dedo-duro”, blame ajuda a determinar qual usuário realizou qual mudança em um determinado arquivo.

Exemplo:
```
$ git blame <nome_do_arquivo>
```
## 22. git tag
Tags são uma boa opção para marcar uma branch e evitar alteração, principalmente em releases públicos.

Exemplo:
```
$ git tag -a v1.0.0
```
## 23. git diff
Para comparar dois arquivos gits ou dois branches antes de passarem por um commit ou um push, é importante executar esse comando Git.

Exemplos:
```
comparando o repositório ativo com o repositório local: $ git diff HEAD <nome_do_arquivo>
comparando duas ramificações: $ git diff <branch de origem> <branch de destino>
```
## 24. git citool
Esse comando Git oferece uma alternativa gráfica ao commit.

Exemplo:
```
$ git citool
```
## 25. git whatchanged
Esse comando oferece informações de log, mas em formato raw.

Exemplo:
```
$ git whatchanged
```

## 26. git reset
volta um numero especifico de commits (3)
```

$ git reset --soft HEAD~3 
```

## 27. git reflog 
mostra a log
```

$ git reflog
```

## 27. git git reset
colta um add
```

$ git reset .\FIAP\RedesNeurais\s2\
```

## 27. git reset 
volta a um ponto especifico
```

$ git reset --hard a0d3fe6
```