import tkinter as tk
from PIL import ImageGrab
import csv
import colorsys
import json
import numpy as np
from sklearn.cluster import KMeans

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
    except Exception as e:
        print(f"Error at {x}, {y}: {e}")
        return "Error", "#000000", (0, 0, 0)

def calculate_contrast(rgb):
    r, g, b = [c / 255.0 for c in rgb]
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    contrast = "Alto" if lum < 0.5 else "Baixo"
    recommended_bg = "white" if contrast == "Baixo" else "black"
    return contrast, recommended_bg

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    return colorsys.rgb_to_hls(r, g, b)

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return tuple(int(c * 255) for c in (r, g, b))

def generate_palette(hex_color):
    rgb = hex_to_rgb(hex_color)
    h, s, l = rgb_to_hsl(rgb)

    complementary_hue = (h + 0.5) % 1.0  # Complementar
    analogous_hue_1 = (h + 0.1) % 1.0   # Análogas
    analogous_hue_2 = (h - 0.1) % 1.0

    complementary_color = hsl_to_rgb(complementary_hue, s, l)
    analogous_color_1 = hsl_to_rgb(analogous_hue_1, s, l)
    analogous_color_2 = hsl_to_rgb(analogous_hue_2, s, l)

    return {
        'original': hex_color,
        'complementary': '#{:02x}{:02x}{:02x}'.format(*complementary_color),
        'analogous_1': '#{:02x}{:02x}{:02x}'.format(*analogous_color_1),
        'analogous_2': '#{:02x}{:02x}{:02x}'.format(*analogous_color_2),
    }

def capture_colors(x, y, width=10, height=10):
    """Captura uma área da tela e extrai as cores dominantes usando K-Means"""
    bbox = (x * screen_scale, y * screen_scale, (x+width) * screen_scale, (y+height) * screen_scale)
    image = ImageGrab.grab(bbox)
    pixels = np.array(image)
    pixels = pixels.reshape((-1, 3))  # Transforma em um vetor de pixels (RGB)

    # Usando K-Means para encontrar os centros das cores
    kmeans = KMeans(n_clusters=3, random_state=0).fit(pixels)
    
    # Obtém os centros de cada cluster (cores dominantes)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    return dominant_colors

def generate_complementary_from_kmeans(dominant_colors):
    """Gera cores complementares a partir dos centros de K-Means"""
    complementaries = []
    
    for color in dominant_colors:
        # Complementaridade simples: inverter os valores de RGB (para um tom oposto)
        complementary = [255 - c for c in color]
        complementaries.append(tuple(complementary))
    
    return complementaries

def export_palette_to_json(palette):
    # Exporta a paleta para um arquivo JSON
    with open('color_palette.json', 'w') as outfile:
        json.dump(palette, outfile, indent=4)

def update_label():
    global fixed, fixed_color_name, fixed_hex_color, fixed_rgb
    
    if not fixed:
        x, y = root.winfo_pointerx(), root.winfo_pointery()
        fixed_color_name, fixed_hex_color, fixed_rgb = get_color_info(x, y)
    
    # Gerar paleta de cores
    palette = generate_palette(fixed_hex_color)
    
    # Captura as cores dominantes usando K-Means
    dominant_colors = capture_colors(x, y)
    complementary_colors = generate_complementary_from_kmeans(dominant_colors)

    # Calcular o contraste e sugerir fundo
    contrast, recommended_bg = calculate_contrast(fixed_rgb)

    text_color = "white"  # Cor do texto
    bg_color = "black"    # Cor de fundo
    
    # Exibir paleta e sugestões
    label.config(
        text=f"{fixed_color_name}\nHEX: {fixed_hex_color}\nRGB: {fixed_rgb}\nContraste: {contrast}\nFundo recomendado: {recommended_bg}\n\n"
             f"Paleta:\nOriginal: {palette['original']}\nComplementar: {palette['complementary']}\n"
             f"Análoga 1: {palette['analogous_1']}\nAnáloga 2: {palette['analogous_2']}\n\n"
             f"Cores Complementares (K-Means): {complementary_colors}",
        fg=text_color,
        bg=bg_color
    )

    # Exportar a paleta para JSON
    export_palette_to_json(palette)
    
    tooltip.geometry(f"+{x+15}+{y+15}")
    tooltip.after(1, update_label)

# Ajuste de escala
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image_width, image_height = ImageGrab.grab().size
screen_scale = image_width / screen_width

root.withdraw()

# Cria uma tooltip transparente
tooltip = tk.Toplevel(root)
tooltip.overrideredirect(True)
tooltip.attributes('-topmost', True)
tooltip.attributes('-transparentcolor', 'black')

# Cria uma label sem fundo
label = tk.Label(tooltip, font=("Helvetica", 15), justify="left", padx=2, pady=1, bg="black")
label.pack()

# Variáveis globais
fixed = False
fixed_color_name = ""
fixed_hex_color = "#000000"
fixed_rgb = (0, 0, 0)

update_label()
tooltip.mainloop()