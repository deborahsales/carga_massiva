import re
from unicodedata import normalize

class CargaMassiva:

    def __init__(self,usuarios):
        self._usuarios = usuarios
        self._lista_users = []
        for i in self._usuarios:
            self._lista_users.append(i._user)

    def atualiza_usuarios_antigos(self,usuarios_novos):
        for i in self._usuarios:
            
            if i not in usuarios_novos and i._user != 'admin':
                i._desativado = 'Sim'
                i._motivo = 'Migração'
                
            for j in usuarios_novos:
                if i == j and i._user != 'admin':
                    i._grupo = j._grupo
                    i._grau = j._grau
                    i._desativado = 'Não'
                    i._motivo = ''

                    if j._d_nasc != '01-01-1970':                    
                        i._d_nasc = j._d_nasc

                    if j._email != '':
                        i._email = j._email 

            if i._user == 'admin':
                i._desativado = 'Não'
                i._motivo = ''
        
        for k in range(1,len(self._usuarios)):
            if self._usuarios[k] in self._usuarios[:k]:
                self._usuarios[k]._desativado = 'Sim'
                self._usuarios[k]._motivo = 'Migração'
    
    def insere_novos_usuarios(self, usuarios_novos):
        for i in usuarios_novos:
            if i not in self._usuarios:
                self._usuarios.append(i)
                j = 2
                while True:
                    if i._tipo == 'Estudantes':
                        self._user_padrao = i._nome.lower()
                        self._user_teste = f'{i._nome.lower()}{j}'
                    elif i._tipo == 'Professores':
                        if i._genero == 'Feminino':
                            self._user_padrao = f'professora{i._nome.lower()}'
                            self._user_teste = f'professora{i._nome.lower()}{j}'
                        else:                            
                            self._user_padrao = f'professor{i._nome.lower()}'
                            self._user_teste = f'professor{i._nome.lower()}{j}'
                    elif i._tipo == 'Diretor':
                        if i._genero == 'Feminino':                           
                            self._user_padrao = f'diretora{i._nome.lower()}'
                            self._user_teste = f'diretora{i._nome.lower()}{j}'
                        else:                     
                            self._user_padrao = f'diretor{i._nome.lower()}'
                            self._user_teste = f'diretor{i._nome.lower()}{j}'
                    if self._user_padrao.replace(' ','') not in self._lista_users:
                        i._user = self._user_padrao.replace(' ','')
                        self._lista_users.append(i._user)                        
                        break;                        
                    elif self._user_teste.replace(' ','') not in self._lista_users:
                        i._user = self._user_teste.replace(' ','')
                        self._lista_users.append(i._user)                        
                        break;
                    else:
                        j += 1

    def atualiza_carga_massiva(self,usuarios_novos):
        self.atualiza_usuarios_antigos(usuarios_novos)
        self.insere_novos_usuarios(usuarios_novos)

    def __str__(self):
        string = ''
        for user in self._usuarios:
            string += f'{user}\n'
        return string
                    

class Usuario:

    def __init__(self, nome, sobrenome, d_nasc, genero, email, tipo, grupo, grau, desativado = 'Não', id = '0', user = ''):
        self._id = id
        self._nome = normalize('NFKD', re.sub('\s+',' ',str.title(nome.strip()))).encode('ASCII','ignore').decode('ASCII') 
        self._sobrenome = normalize('NFKD', re.sub('\s+',' ',str.title(sobrenome.strip()))).encode('ASCII','ignore').decode('ASCII')
        self._user = user.strip().lower()
        self._d_nasc = d_nasc.strip().replace('/','-')
        self._genero = str.title(genero.strip())
        self._email = email.strip().lower()
        self._tipo = str.title(tipo.strip())
        self._grupo = grupo.strip().upper()
        self._grau = grau.strip().upper()
        self._desativado = str.title(desativado.strip())

        if d_nasc == '' or d_nasc == '#REF!':
            self._d_nasc = '01-01-1970'

        if self._id == '0':
            if self._tipo == 'Estudantes':
                self._senha = '1'
            else:
                self._senha = '1234'
        else:
            self._senha = ''

        if self._desativado.lower() == 'sim':
            self._motivo = 'Migração'
        else:
            self._motivo = ''

        if self._id == '0':
            self._organizacao = 'Sergipe'
        else:
            self._organizacao = ''
    
    def __str__(self):
        return f'{self._id},{self._nome},{self._sobrenome},{self._user},{self._d_nasc},{self._genero},{self._email},{self._tipo},{self._grupo},{self._grau},{self._organizacao},{self._senha},{self._desativado},{self._motivo}'

    def linha(self):
        return [self._id,self._nome,self._sobrenome,self._user,self._d_nasc,self._genero,self._email,self._tipo,self._grupo,self._grau,self._organizacao,self._senha,self._desativado,self._motivo]
    
    def lista_alunos(self):
        if self._tipo == 'Estudantes':
            self._senha_la = '1'
        else:
            self._senha_la = '1234'
        return [self._nome,self._sobrenome,self._user,self._senha_la,self._grau,self._grupo]

    def __eq__(self, user2):
        return f'{self._nome} {self._sobrenome}' == f'{user2._nome} {user2._sobrenome}' and self._tipo == user2._tipo
    
    def __gt__(self, user2):
        if self._grau == user2._grau:
            return self._grupo > user2._grupo
        else:
            return self._grau > user2._grau