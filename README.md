# Ferramenta de Identificação de Cores

Este projeto utiliza o Python com a biblioteca Tkinter para criar uma ferramenta de captura de cores da tela, identificando o nome da cor, código hexadecimal, valor RGB e o contraste da cor selecionada. Ele é útil para quem precisa identificar rapidamente cores na tela e obter informações sobre elas.

Ideal para quem trabalha com Design ou que tenha alguma limitação que o impessa de ver cores corretamente

## Requisitos

- Python 3.x
- Bibliotecas:
  - `tkinter` (geralmente incluída por padrão na instalação do Python)
  - `Pillow` (para captura de tela)
  - `csv` (para carregar os dados de cores a partir de um arquivo CSV)

Você pode instalar a biblioteca `Pillow` com o seguinte comando:

```bash
pip install Pillow
```

## Arquivo CSV de Cores

O projeto depende de um arquivo CSV (`dados.csv`) que contém a lista de cores e seus nomes correspondentes. O formato esperado do arquivo CSV é:

```
HEX,COR
#FF5733,Laranja
#33FF57,Verde
#3357FF,Azul
...
```

## Funcionalidades

- **Captura de cor da tela**: Quando o usuário posiciona o cursor sobre qualquer área da tela, a cor daquela área é identificada.
- **Exibição de informações de cor**: A ferramenta exibe o nome da cor, o valor hexadecimal, o valor RGB e o contraste (alto ou baixo) da cor selecionada.
- **Interface transparente**: A interface gráfica é exibida como uma tooltip transparente que segue o cursor na tela.

## Como Usar

1. **Execute o Script**: Execute o script Python para iniciar a ferramenta.
   
   ```bash
   python nome_do_script.py
   ```

2. **Identificar Cores**: Mova o cursor sobre qualquer parte da tela. A ferramenta irá capturar a cor da região sobre o cursor e exibir as informações relacionadas.

3. **Informações Exibidas**:
   - Nome da cor (caso esteja presente no arquivo CSV)
   - Código hexadecimal da cor
   - Valores RGB da cor
   - Contraste da cor (se é considerado "Alto" ou "Baixo")

## Exemplo de Execução

Aqui está como a janela da tooltip pode se parecer quando em uso:

```
Verde
HEX: #33FF57
RGB: (51, 255, 87)
Contraste: Alto
```

## Considerações Finais

Este é um projeto simples, mas útil para quem deseja identificar e trabalhar com cores na tela. A exibição de informações em tempo real facilita a captura de dados diretamente da interface gráfica.


## README.md

O arquivo readme.md foi gerado INTEGRALMENTE pelo ChatGPT com pequenas modificações feitas por mim.

## ME AJUDE

Você pode experienciar alguns erros, majoritariamente causados por diferenças de resolução, escala e taxa de atualização da tela.

## BASE DE DADOS

A base de dados utilizada para a verificação dos nomes das cores não é de minha autoria. Ela pode ser acessada no site [ColorNames](https://colornames.org/), ao qual todos os créditos devem ser direcionados.
