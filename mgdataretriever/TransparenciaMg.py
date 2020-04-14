# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 15:08:04 2020

@author: Guilherme
"""
import requests
import json
import os
import re

class TransparenciaMg:
    
    """
    Construção de funções
    """
    def __init__(self):
        self.directory = 'portal da transparencia'
    
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        try:
            os.mkdir('downloads')
        except FileExistsError:
            print("downloads main folder already exists")
        
        try:
            os.mkdir(f'downloads/{self.directory}')
        except FileExistsError:
            print(f"{self.directory} subfolder already exists")
            
        """
        Parâmetros globais das requisições
        """
        self.reqUrl = 'http://www.transparencia.dadosabertos.mg.gov.br/api/3/action/'
        
        self.cookies = {
            'ROUTEID': '.1',
        }
        
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    
    
    """
    Funções core
    """
    def getPackageList(self):
        response = requests.get(f'{self.reqUrl}/package_list', headers=self.headers, cookies=self.cookies, verify=False)
        return (json.loads(response.text)['result'])
    
    def listPackages(self, packageList):
        for packageName in packageList:
            print(packageName)
    
    def getDatasetListByPackage(self, packageName):
        self.params = (('id', packageName),)
        response = requests.get(f'{self.reqUrl}/package_show', headers=self.headers, params=self.params, cookies=self.cookies, verify=False)
        try:
            return (json.loads(response.text))['result']['resources']
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
        datasetFileName = re.findall(r"/download/(\w*.\w*)",downloadLink)[0]
        open(f'downloads/{self.directory}/{datasetFileName}', 'wb').write(downloadFile.content)


    """
    Funções para o usuário final
    """
    def listarConjuntos(self):
        self.listPackages(self.getPackageList())
        
    def listarDatasetsPorConjunto(self, packageName):
        self.listDatasetsByPackage(self.getDatasetListByPackage(packageName))
        
    def baixarDataset(self, packageName, datasetName):
        try:
            self.downloadDatasetByName(packageName, datasetName)
            print(f'{datasetName} foi baixado com sucesso')
        except ValueError as e:
            print(str(e) + f'. Erro no download de {datasetName}')
        