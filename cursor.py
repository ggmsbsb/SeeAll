import tkinter as tk
from PIL import ImageGrab
import csv

# Carrega o dataset CSV
color_names = {}
with open('dados.csv', mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)  # Pula o cabeçalho
    for rows in reader:
        hex_code = rows[0].strip().lower()
        name = rows[1].strip()
        color_names[hex_code] = name

def get_color_name_from_csv(hex_color):
    hex_color = hex_color.lstrip('#').lower()
    return color_names.get(hex_color, "Nome não encontrado")

def get_color_info(x, y):
    try:
        bbox = (x * screen_scale, y * screen_scale, (x+1) * screen_scale, (y+1) * screen_scale)
        image = ImageGrab.grab(bbox)
        rgb = image.getpixel((0, 0))
        hex_color = '#%02x%02x%02x' % rgb
        color_name = get_color_name_from_csv(hex_color)
        return color_name, hex_color, rgb
    except Exception:
        return "Error", "#000000", (0, 0, 0)

def update_label():
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    color_name, hex_color, rgb = get_color_info(x, y)

    # Calcula a luminosidade da cor de fundo
    luminosity = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    
    # Usa fundo preto com opacidade baixa, mantendo o texto branco
    text_color = "white"  # Cor do texto sempre branca para boa legibilidade
    bg_color = "black"  # Fundo preto

    # Atualiza o texto da label com fundo preto semi-transparente
    label.config(
        text=f"{color_name}\nHEX: {hex_color}\nRGB: {rgb}",
        fg=text_color,  # Cor de texto branca
        bg=bg_color,  # Fundo preto
    )

    # Ajusta a opacidade do fundo da tooltip para dar um efeito semi-transparente
    tooltip.attributes('-alpha', 1)  #Opacidade

    tooltip.geometry(f"+{x+15}+{y+15}")  # Move a tooltip sem definir tamanho fixo
    tooltip.after(100, update_label)

# Ajusta a captura de tela para monitores com escala diferente de 100%
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image_width, image_height = ImageGrab.grab().size
screen_scale = image_width / screen_width  # Ajusta captura para monitores com escala diferente de 100%

root.withdraw()  # Oculta a janela principal

# Cria uma tooltip transparente
tooltip = tk.Toplevel(root)
tooltip.overrideredirect(True)
tooltip.attributes('-topmost', True)
tooltip.attributes('-transparentcolor', 'black')  # Faz o fundo do texto desaparecer

# Cria uma label sem fundo
label = tk.Label(tooltip, font=("Helvetica", 10), justify="left", padx=2, pady=1, bg="black")  # Cor igual ao transparentcolor
label.pack()

update_label()
tooltip.mainloop()