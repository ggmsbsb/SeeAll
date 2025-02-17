import pandas as pd

# Carregar o arquivo TXT, especificando que o delimitador é a vírgula
data = pd.read_csv("colornames.txt", delimiter=",", header=None, names=["hexCode", "bestName", "votes"])

# Remover a primeira linha duplicada (se houver)
data = data.iloc[1:].reset_index(drop=True)

# Remover a coluna 'votes'
data = data.drop(columns=["votes"])

# Salvar os dados em um arquivo CSV
data.to_csv("dados.csv", index=False, sep=",")

print("Arquivo CSV gerado com sucesso!")
