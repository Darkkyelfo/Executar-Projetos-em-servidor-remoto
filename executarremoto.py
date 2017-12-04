'''
Created on 2 de dez de 2017

@author: raul
'''
import os
import platform
import paramiko
#import filecmp
#import glob as g
from paramiko import SSHClient
from scp import SCPClient
from exception import FalhaExecucaoException
class SSH:
    def __init__(self,user,ip,senha=""):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip,username=user,password=senha)
        self.scp = SCPClient(self.ssh.get_transport())

    def exec_cmd(self,cmd):
        print(cmd)
        stdin,stdout,stderr = self.ssh.exec_command(cmd,get_pty=False)
        if stderr.channel.recv_exit_status() != 0:
            raise FalhaExecucaoException(stderr.read())
        else:
            print (stdout.read())


class ExecutarRemoto(object):
    def __init__(self,user,ip,caminhoRemoto,senha="",fileToExecute = "main.py",osRemote = "Linux"):
        #As informacoes sao equivalentes as pedias quando se vai realizar uma conexao ssh
        #user@ip
        #passwod:senha
        self.user = user
        self.ip = ip
        self.senha = senha
        self.caminhoRemoto = caminhoRemoto#local onde sera salvo a copia do programa no servidor
        self.fileToExecute = fileToExecute#arquivo que vai executado remotamente(main do programa)
        self.ssh = SSH(self.user,self.ip,self.senha)#Realiza a conexao ssh
        if("Linux" in platform.system() or "linux" in platform.system()):
            self.barra = "/"
        elif("Windows" in platform.system() or "windows" in platform.system()):
            self.barra = "\\"
        if(osRemote=="Windows"):
            self.barraR = "\\"
        else:
            self.barraR = "/"
    
    #recebe o camando a ser executado
    def executarRemoto(self,linguagemComando = "python"):
        try:
            if(linguagemComando=="java"):
                self.ssh.exec_cmd("cd %s/; nohup java -jar %s > /dev/null 2>&1 &" %(self.caminhoRemoto,self.fileToExecute))
            elif(linguagemComando=="python"):
                self.ssh.exec_cmd("cd %s/; nohup python -u %s > /dev/null 2>&1 &"%(self.caminhoRemoto,self.fileToExecute))
            else:
                self.ssh.exec_cmd("cd %s/; nohup %s -u %s > /dev/null 2>&1 &"%(self.caminhoRemoto,linguagemComando,self.fileToExecute))
            print("programa executado")
        except FalhaExecucaoException as e:
            print(e)
        self.ssh.ssh.close()
    
    #permite visualizar a saida no console do eclipse,contudo,ao finaliza-lo
    #aplicacao tb eh finalizada. So funciona no linux
    def executarRemotoAtivo(self,linguagem = "python"):
        
        if(linguagem == "python"):
            os.system("ssh %s@%s cd %s/ && python %s"%(self.user,self.ip,self.caminhoRemoto,self.fileToExecute))
        elif(linguagem=="java"):
            os.system("ssh %s@%s cd %s/ && java -jar %s"%(self.user,self.ip,self.caminhoRemoto,self.fileToExecute)) 
        else:
            os.system("ssh %s@%s cd %s && &s %s"%(self.user,self.ip,self.caminhoRemoto,linguagem,self.fileToExecute))
        
    def apagarRemoto(self):
        try:
            self.ssh.exec_cmd("rm -r %s"%(self.caminhoRemoto))
            print("Diretorio apagado com sucesso")           
        except FalhaExecucaoException:
            print("Diretorio nao pode ser apagado,pois, nao existe")
            
    
    #Copia o projeto para o servidor
    def copiarParaRemoto(self,igOcultos=True):
        try:
            #self.apagarRemoto()#sempre apaga o anterior ao realiza uma nova copia
            self.ssh.exec_cmd("mkdir -p %s"%(self.caminhoRemoto))
            c = 0
            localDir = os.getcwd()
            tamanhoDir = len(localDir.split(self.barra))
            for dirpath, dirnames, filenames in os.walk(localDir):
                if(igOcultos and "." in dirpath ):#nao envia arquivos ocultos
                    continue
                dirRemoto = self.caminhoRemoto
                if(c!=0):
                    for folder in dirpath.split(self.barra)[tamanhoDir:]:
                        dirRemoto +=self.barraR+folder
                    self.ssh.exec_cmd("mkdir -p %s"%(dirRemoto))
                for file in filenames:
                    arqEnviado = dirpath+self.barra+file
                    self.ssh.scp.put(arqEnviado,dirRemoto+self.barraR+file)
                    print("%s enviado"%arqEnviado)
                c+=1
            #self.ssh.exec_cmd("touch %s/saida.txt"%(self.caminhoRemoto))
            print("copia realizada")
        except FalhaExecucaoException as e:
            print("Erro ao copiar: "+e)
        
    '''
    def _enviarParaRemoto(self,dirLocal,remoto):
        for file in dirLocal:
            print(file)
            arq = self._getFileName(file)
            if(os.path.isdir(file)):#Se for um diretorio
                subDirRemoto = self.caminhoRemoto+self.barraR+arq
                #Cria o subdirotio no servidor
                self.ssh.exec_cmd( "mkdir -p %s"%(subDirRemoto))
                self._enviarParaRemoto(dirLocal,subDirRemoto)
            else:
                print(arq)
                self.ssh.scp.put("%s" %arq,"%s"%(remoto))
               
    def _getFileName(self,arquivo):
        arquivoSep = arquivo.split(self.barra)
        return arquivoSep[-1]
    '''
#Versao mais simples que nao exige pacotes externos(parmiko ou scp) 
#porem so funciona em um cliente linux
class ExecutarRemotoOs(object):
    
    def __init__(self,user,ip,caminhoRemoto,fileToExecute = "main.py"):
        self.user = user
        self.ip = ip
        self.caminhoRemoto = caminhoRemoto
        self.fileToExecute = fileToExecute
        
    def executarRemoto(self,linguagem="python"):
        
        if(linguagem == "python"):
            os.system("ssh %s@%s python %s/%s"%(self.user,self.ip,self.caminhoRemoto,self.fileToExecute))
        elif(linguagem=="java"):
            os.system("ssh %s@%s java -jar %s/%s"%(self.user,self.ip,self.caminhoRemoto,self.fileToExecute)) 
        else:
            os.system("ssh %s@%s python %s/%s"%(self.user,self.ip,self.caminhoRemoto,self.fileToExecute))
    
    def copiarParaRemoto(self):
        self.apagarRemoto()
        os.system("ssh %s@%s mkdir -p %s"%(self.user,self.ip,self.caminhoRemoto))
        os.system("scp -r %s/* %s@%s:%s"%(os.getcwd(),self.user,self.ip,self.caminhoRemoto))
    
    def apagarRemoto(self):
        os.system("ssh %s@%s rm -r %s"%(self.user,self.ip,self.caminhoRemoto))
    
    '''
    def sincronizarRemoto(self,arquivos = g.glob(os.getcwd()+"/*"),dir=""):
        for file in arquivos:
            fNome,dire = self._getFileAndForlder(file)
            if(os.path.isdir(file)):
                self.sincronizarRemoto(file,fNome) 
            else:
                arqR = "%s%s/%s"%(self.caminhoRemoto,dir,fNome)
                if(filecmp.cmp(file,arqR)==False):
                    os.system("scp %s %s@%s:%s"%(file,self.user,self.ip,arqR))
                                 
    def _getFileAndForlder(self,arquivo):
        arquivoSep = arquivo.split("/")
        return arquivoSep[-1],arquivoSep[-2]
    
    def _mountarRemoto(self):
        self.pMontada = os.getcwd()+"/mnt"
        os.system("sshfs -o allow_other,default_permissions %s@%s:/ %s"%(self.user,self.ip,self.pMontada))
    '''     
    
    
    

