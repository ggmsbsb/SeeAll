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

def calculate_contrast(rgb):
    # Calcula a luminância relativa
    r, g, b = [c / 255.0 for c in rgb]
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    contrast = "Alto" if lum < 0.5 else "Baixo"
    return contrast

def update_label():
    global fixed, fixed_color_name, fixed_hex_color, fixed_rgb
    
    if not fixed:
        x, y = root.winfo_pointerx(), root.winfo_pointery()
        fixed_color_name, fixed_hex_color, fixed_rgb = get_color_info(x, y)
    
    contrast = calculate_contrast(fixed_rgb)
    text_color = "white"  # Cor do texto
    bg_color = "black" #Cor de fundo
    
    label.config(
        text=f"{fixed_color_name}\nHEX: {fixed_hex_color}\nRGB: {fixed_rgb}\nContraste: {contrast}",
        fg=text_color,
        bg=bg_color
    )
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
label = tk.Label(tooltip, font=("Helvetica", 10), justify="left", padx=2, pady=1, bg="black")
label.pack()

# Variáveis globais
fixed = False
fixed_color_name = ""
fixed_hex_color = "#000000"
fixed_rgb = (0, 0, 0)

update_label()
tooltip.mainloop()