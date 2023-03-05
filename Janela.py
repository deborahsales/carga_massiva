#pyuic5 -x Window.ui -o Window.py
#pyinstaller --windowed Main.py -i logo_IP.png
#cxfreeze Main.py --target-dir "Gerador Carga Massiva Windows" --icon=logo_IP.ico --base-name=WIN32GUI

from PyQt5 import QtWidgets
from Window import Ui_MainWindow
from CargaMassiva import CargaMassiva, Usuario
import csv
import math

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
      super(MainWindow, self).__init__()
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.setup_program_ui()
    
    def setup_program_ui(self):
      self.ui.botao_extraido.clicked.connect(lambda: self.abrir_arquivo_antigo())      
      self.ui.botao_atualizada.clicked.connect(lambda: self.abrir_arquivo_novo())
      self.ui.botao_gerar.clicked.connect(lambda: self.salvar_arquivo())

    def abrir_arquivo_antigo(self):
      self._arquivo_antigo = QtWidgets.QFileDialog.getOpenFileName()[0]
      self.ui.arquivo_extraido.setText(self._arquivo_antigo)

      self._usuarios_antigos = []

      with open (self._arquivo_antigo, encoding='utf-8') as self._file_antigo:
        if ',' in self._file_antigo.readline():
          self._csvreader_antigo = csv.reader(self._file_antigo)
        else:          
          self._csvreader_antigo = csv.reader(self._file_antigo, delimiter = ';')

        for row in self._csvreader_antigo:
          if row[0] != 'Identificador':
            self._usuarios_antigos.append(Usuario(row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9],row[12],row[0], row[3]))
    
    def abrir_arquivo_novo(self):      
      self._arquivo_novo = QtWidgets.QFileDialog.getOpenFileName()[0]
      self.ui.lista_usuarios.setText(self._arquivo_novo)

      self._usuarios_novos = []

      with open(self._arquivo_novo, encoding='utf-8') as self._file_novo:        
        if ',' in self._file_novo.readline():
          self._csvreader_novo = csv.reader(self._file_novo)
        else:          
          self._csvreader_novo = csv.reader(self._file_novo, delimiter = ';')  

        for row in self._csvreader_novo:    
          if row[0] != 'Primeiro nome':
            self._usuarios_novos.append(Usuario(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    
    def salvar_arquivo(self):
      self._nome_arquivo = QtWidgets.QFileDialog.getSaveFileName()[0]
      self._carga_massiva = CargaMassiva(self._usuarios_antigos)
      self._carga_massiva.atualiza_carga_massiva(self._usuarios_novos)
      self._total_usuarios = len(self._carga_massiva._lista_users)
      self._total_arquivos = math.ceil(self._total_usuarios / 500)

      titulos = ['Identificador','Primeiro nome','Sobrenomes','Nome de usuário','Data de nascimento','Gênero','Email','Tipo de usuário','Grupo','Grau','Organização','Senha','Desativado','Motivo']

      self._inicio = 0
      if self._total_usuarios < 500:
        self._fim = self._total_usuarios
      else:
        self._fim = 500

      for i in range(1,self._total_arquivos+1):
        with open(f'{self._nome_arquivo}_CM_{i}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv.writer(csvfile, delimiter=',').writerow(titulos)
            for j in range(self._inicio,self._fim):
              csv.writer(csvfile, delimiter=',').writerow((self._carga_massiva._usuarios)[j].linha())
            self._inicio += 500            
            self._total_usuarios -= 500
            if self._total_usuarios < 500:
              self._fim += self._total_usuarios
            else:
              self._fim += 500
      
      titulos_la = ['Nome','Sobrenome','Usuário','Senha','Ano','Turma']
      
      with open(f'{self._nome_arquivo}_LA.csv', 'w', newline='', encoding='utf-8') as csvfile:
          csv.writer(csvfile, delimiter=',').writerow(titulos_la)
          for i in sorted(self._carga_massiva._usuarios):
            if i._desativado == 'Não' and i._user != "admin":
              csv.writer(csvfile, delimiter=',').writerow(i.lista_alunos())
      
      QtWidgets.QMessageBox.about(self,
             'Concluído', f'Carga atualizada com sucesso!!')     
      
      self.ui.lista_usuarios.setText('')
      self.ui.arquivo_extraido.setText('')