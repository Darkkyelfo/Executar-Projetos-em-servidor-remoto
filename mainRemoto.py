'''
Created on 2 de dez de 2017

@author: raul
'''
from executarremoto import ExecutarRemoto
#codigo exemplo
if __name__ == '__main__':
    
    #usuario,ip,local onde sera salvo no servidor, arquivo a ser executado e a senha
    #neste exemplo nao ha senha,pois,o servidor foi configurado para permite acesso
    #ssh sem senha para esta maquina 
    exe = ExecutarRemoto("raul","faculPC","/home/raul/projetos/execucaoRemota",fileToExecute="main.py")
    exe.apagarRemoto()#apaga o projeto que se encontra no servidor
    #exe.copiarParaRemoto()#copia o projeto para o servidor via ssh (lento)
    exe.copiarParaRemotoGit()#faz o download de um projeto do git no servidor(rápido)
    exe.executarRemoto()#Executa o projeto
    pass