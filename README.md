# Executar-Projetos-em-servidor-remoto
Classe que permite a execução de um projeto de software em um servidor remoto. Utiliza SSH em seu funcionamento.
A classe copia o projeto onde se encontra para um diretorio de escolha do usuário em um servidor e executa o código nele.

Este tutorial descreve os passos de configuração da máquina que será utilizada como servidor para execução de programas..

Restrições:

  -Deve-se ter o python instalado em sua máquina junto com as bibliotecas: “paramiko” e “scp”; 
  -Seu SO deve ser Linux;

1º Passo - Configurando o servidor:

  Instalado no servidor todas as bibliotecas que seu programa precisa e configure as variáveis de ambiente corretamente para que sejam executados por padrão no sistema.
Também é obrigatório ter um ssh server executando. Distribuições baseadas em debian costumam vir com um pôr padrão sem que seja necessário realizar nenhuma configuração.

2º Passo - Adquirindo ip para realizar acesso remoto:

  O script funciona através de ssh por isso é preciso obter um ip que seja acessível de fora da rede local. Existem várias formas de fazer isso a que será utilizada aqui é através do hamachi.
Instale o hamachi tanto no servidor quanto na sua máquina;
Crie uma rede no servidor;
Adicione sua máquina a rede;
Teste: Digite no terminal ou no navegador: ssh seuUsuario@ipDoHamachiServidor e veja se consegue obter acesso ao servidor.

links ensinando a usar o hamachi:
linux: https://ericlefevre.net/wordpress/2010/07/30/how-to-use-logmein-under-linux/comment-page-1/
windows:  http://www.techtudo.com.br/dicas-e-tutoriais/noticia/2012/07/como-usar-o-hamachi.html

3º Passo - Permitindo acesso ssh sem senha (opcional):

  É recomendado que sua máquina seja capaz de acessar o servidor sem necessidade de senha para tal segue a seguir um link ensinando a realizar o processo em distros linux baseadas em debian:  

http://www.linuxproblem.org/art_9.html 



