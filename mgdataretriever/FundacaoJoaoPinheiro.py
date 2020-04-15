# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 00:26:24 2020

@author: Guilherme
"""
import re
import requests
import os
from bs4 import BeautifulSoup
from ftfy import fix_encoding

class FundacaoJoaoPinheiro:
    
    """
    Construtor. Inicializa variáveis importantes e configura o diretório.
    """
    def __init__(self):
        self.directory = 'fundacao joao pinheiro'
    
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        try:
            os.mkdir('downloads')
        except FileExistsError:
            print('')
        
        try:
            os.mkdir(f'downloads/{self.directory}')
        except FileExistsError:
            print('')
        
        self.reqUrl = 'http://minasedados.fjp.mg.gov.br/'

    """
    Funções core
    """
    def getDatasetList(self):
        response = requests.get(self.reqUrl)        
        linkList = BeautifulSoup(response.text, "html.parser").find_all('a')
        fixedList = list()
        datasetList = list()
        
        for link in linkList:
            fixedList.append(fix_encoding(link.get('href')))

        for item in fixedList:
            if item.find('Bases') != -1:
                fixedItem = re.sub('Bases/|.xlsx', '', item)
                datasetList.append(fixedItem)
        
        response.close()
        return datasetList
    
    def downloadDatasetByName(self, datasetName):
        downloadLink = self.reqUrl + f'Bases/{datasetName}.xlsx'     
        downloadFile = requests.get(downloadLink)
        if(downloadFile.status_code == 404):
            raise ValueError('Dataset não encontrado — nome inválido')
        
        open(f'downloads/{self.directory}/{datasetName}.xlsx', 'wb').write(downloadFile.content)
        downloadFile.close()
             
        
    """
    Funções para o usuário final
    """
    def listarDatasets(self):
        datasetList = self.getDatasetList()
        for dataset in datasetList:
            print(dataset)
            
    def baixarDataset(self, datasetName):
        try:
            self.downloadDatasetByName(datasetName)
            print(f'{datasetName} foi baixado com sucesso.')
            print('O arquivo está disponível em ' + os.path.dirname(os.path.abspath(__file__)) + f'\downloads\{self.directory}\{datasetName}.xlsx')
        except ValueError as e:
            print(f'Erro no download de {datasetName}: ' + str(e))