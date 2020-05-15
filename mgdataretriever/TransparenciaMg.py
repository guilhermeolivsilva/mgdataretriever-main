# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:08:04 2020

@author: Guilherme
"""
import requests
import os
import re

class TransparenciaMg:
    
    """
    Construtor. Inicializa variáveis importantes e configura o diretório.
    """
    def __init__(self):
        self.directory = 'portal da transparencia'
        self.datasetFileName = ''
    
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        try:
            os.mkdir('downloads')
        except FileExistsError:
            print('')
        
        try:
            os.mkdir(f'downloads/{self.directory}')
        except FileExistsError:
            print('')
            
        """
        Parâmetros globais das requisições
        """
        self.reqUrl = 'http://www.transparencia.dadosabertos.mg.gov.br/api/3/action/'
        
        self.cookies = {
            'ROUTEID': '.1',
        }
        
        self.headers = {
            'Accept': 'application/json',
        }
    
    
    """
    Funções core
    """
    def getPackageList(self):
        response = requests.get(f'{self.reqUrl}/package_list', headers=self.headers, cookies=self.cookies, verify=False)
        response.close()
        
        return ((response.json())['result'])
    
    def listPackages(self, packageList):
        for packageName in packageList:
            print(packageName)
    
    def getDatasetListByPackage(self, packageName):
        self.params = (('id', packageName),)
        response = requests.get(f'{self.reqUrl}/package_show', headers=self.headers, params=self.params, cookies=self.cookies, verify=False)
        
        response.close()
        try:
            return (response.json())['result']['resources']
        except:
            raise ValueError('Nome de Conjunto inválido')
    
    def listDatasetsByPackage(self, packageName):
        for dataset in packageName:
            print(dataset['name'])
    
    def getDownloadLinkByDatasetName(self, packageName, datasetName):
        datasetList = self.getDatasetListByPackage(packageName)
        datasetIndex = next((index for (index, d) in enumerate(datasetList) if d["name"] == datasetName), None)
        try:
            return datasetList[datasetIndex]['url']
        except:
            raise ValueError('Nome de Dataset inválido')
    
    def downloadDatasetByName(self, packageName, datasetName):
        downloadLink = self.getDownloadLinkByDatasetName(packageName, datasetName)
        
        downloadFile = requests.get(downloadLink)
        self.datasetFileName = re.findall(r"/download/(\w*.\w*)",downloadLink)[0]
        open(f'downloads/{self.directory}/{self.datasetFileName}', 'wb').write(downloadFile.content)
        downloadFile.close()


    """
    Funções para o usuário final
    """
    def listarConjuntos(self):
        self.listPackages(self.getPackageList())
        
    def listarDatasetsPorConjunto(self, packageName):
        try:
            self.listDatasetsByPackage(self.getDatasetListByPackage(packageName))
        except ValueError as e:
            print('Erro ao listar Conjuntos: ' + str(e))
        
    def baixarDataset(self, packageName, datasetName):
        try:
            self.downloadDatasetByName(packageName, datasetName)
            print(f'{datasetName} foi baixado com sucesso')
            print('O arquivo está disponível em ' + os.path.dirname(os.path.abspath(__file__)) + f'\downloads\{self.directory}\{self.datasetFileName}')
        except ValueError as e:
            print(str(e) + f'. Erro no download de {datasetName}')
        