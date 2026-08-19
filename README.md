# Sistema de Tempo de Serviço e Reserva Remunerada - QOPMA

Esta é uma aplicação web interativa desenvolvida em Python (Streamlit) para gerenciar dados de policiais militares (QOPMA) e calcular de forma automatizada e com precisão de 100% o tempo de serviço acumulado, o pedágio referente à reforma da previdência (Lei Federal 13.954/2019) e o tempo faltante para a Reserva Remunerada (RR).

## 🚀 Como Executar a Aplicação (Localmente no Windows)

### Passo 1: Instalar o Python
Caso você ainda não tenha o Python instalado, faça o download da versão mais recente do Python 3 (recomendado 3.10 ou superior) em [python.org](https://www.python.org/downloads/) e instale-o. 
> ⚠️ **IMPORTANTE:** Durante a instalação, lembre-se de marcar a caixinha **"Add Python to PATH"** (Adicionar Python ao PATH).

### Passo 2: Instalar as Dependências
Abra o terminal (PowerShell ou Prompt de Comando) na pasta do projeto e execute o comando abaixo para instalar as bibliotecas necessárias:
```powershell
pip install -r requirements.txt
```

### Passo 3: Iniciar a Aplicação
Com as dependências instaladas, inicie o servidor local do Streamlit executando o seguinte comando no terminal:
```powershell
streamlit run app.py
```

Uma aba do navegador se abrirá automaticamente no endereço `http://localhost:8501` exibindo a aplicação.

---

## 📂 Estrutura do Projeto

* `app.py`: Interface do usuário do Streamlit com o Dashboard interativo, gráficos de estatísticas, formulários de edição e memorial de cálculo.
* `data_loader.py`: Mecanismo matemático de cálculo e funções de banco de dados.
* `database/officers.json`: Banco de dados local inicial pré-carregado com os **68 oficiais** da sua planilha original.
* `requirements.txt`: Lista de dependências Python.

---

## ⚙️ Regras Matemáticas e Correções de Bugs da Planilha
A aplicação realiza os cálculos de tempo baseando-se em data de início e de projeção usando a exatidão do calendário e soma administrativa de tempo (onde 30 dias se tornam 1 mês e 12 meses se tornam 1 ano).

💡 **Nota de Correção:** A aplicação corrige automaticamente 4 erros de cálculo manuais que estavam presentes no seu arquivo original:
1. **José Wellington de Oliveira Barros Jr (ID 37)**: Havia um erro na soma dos dias que não levava o carry de 1 mês para a coluna de meses. O correto é `32 anos e 17 dias` acumulados.
2. **Glauco Soares de Almeida (ID 41)**: O mês da coluna FFAA (1 mês) não foi somado na planilha original.
3. **Wellington Leite de Souza (ID 43)**: O mês da coluna Civil (1 mês) não foi somado na planilha original.
4. **Claudio Jean da Silva Pires (ID 45)**: A soma dos dias acumulou 33 dias, mas o carry de 1 mês para a coluna de meses foi esquecido na planilha original.

---

## ⚡ Funcionalidades Especiais
* **Projeção de Datas**: No painel lateral, altere a "Data de Projeção / Cálculo" para qualquer data futura (ex: 2028, 2030) e a aplicação recalculará instantaneamente quem estará apto, ajudando a planejar as datas de aposentadoria futura de todo o quadro!
* **Exportação**: Você pode exportar a planilha final calculada a qualquer momento de volta para o formato Excel (XLSX) utilizando o botão de download abaixo da tabela principal.
