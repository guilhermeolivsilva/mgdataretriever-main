# mgdataretriever

Um pacote Python simples que automatiza o download de datasets sobre a economia de Minas Gerais a partir de diversas bases de dados.

## Sobre

Criado para fins de aprendizado, o pacote implementa funções para download de datasets a partir de bases de dados remotas, com a finalidade de automatizar o processo de obtenção de dados para trabalhos essencialmente—mas não exclusivamente—econométricos.

Atualmente, é compatível com:
- Portal da Transparência do Estado

#### Roadmap
As bases a seguir foram mapeadas e serão implementadas futuramente
- DataViva
- Fundação João Pinheiro

## Sobre o autor
mgdataretriever é desenvolvido por Guilherme O. Silva, estudante de graduação em Ciências Econômicas na UFMG. O projeto não possui qualquer vínculo com a instituição.
Entre em contato!
- [Email](mailto:guilherme.olivsilva01@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/guilherme-oliveira-104090195/)

## Como usar
Na pasta do projeto a utilizar os datasets, clone o repositório com
```
git clone https://github.com/guilhermeolivsilva/mgdataretriever
```

### Portal da Transparência de MG
Basta importar o pacote e instanciar um objeto para começar a trabalhar:
```
from mgdataretriever import TransparenciaMg
meuObjeto = TransparenciaMg()
```

O Portal da Transparência disponibiliza datasets agrupados por conjuntos, de modo que um único conjunto pode possuir diversos datasets associados.

1. Liste conjuntos de datasets disponíveis com
```
meuObjeto.listarConjuntos()
```

2. Liste os datasets associados ao conjunto com
```
meuObjeto.listarDatasetsPorConjunto('nome-do-conjunto')
```
_Observe que o argumento da função deve ser **idêntico** a um dos resultados retornados no passo 1._
```
transparenciaMg.listarDatasetsPorConjunto('programa-de-financiamento-2009')
```

3. Baixe o dataset desejado
```
meuObjeto.baixarDataset('nome-do-conjunto', 'nome-do-dataset')
```
_Aqui, também é necessário que o nome do conjunto seja idêntico a um dos resultados do passo 1 e o mesmo para o nome do dataset, em relação a um dos resultados do passo 2._
```
transparenciaMg.baixarDataset('programa-de-financiamento-2009', 'PPP 2008 Aprovados')
```

4. O arquivo estará disponível no diretório
```
downloads/portal da transparencia/
```

### Fundação João Pinheiro: Minas e-Dados
Basta importar o pacote e instanciar um objeto para começar a trabalhar:
```
from mgdataretriever import FundacaoJoaoPinheiro
meuObjeto = FundacaoJoaoPinheiro()
```

Diferentemente da abordagem utilizada pelo Portal da Transparência, a plataforma da Fundação João Pinheiro agrupa as informações dentro do próprio arquivo de cada dataset. Para acessá-los, basta que

1. Liste os datasets disponíveis com
```
meuObjeto.listarDatasets()
```

2. Baixe o dataset desejado
```
meuObjeto.baixarDataset(nome-do-dataset')
```
_É necessário que o nome do dataset seja idêntico a um dos resultados do passo 1._
```
fjp.baixarDataset('Turismo')
```

3. O arquivo estará disponível no diretório
```
downloads/fundacao joao pinheiro/
```

#### Roadmap
- Habilitar a instalação com pip
