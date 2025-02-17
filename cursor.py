import tkinter as tk
from PIL import ImageGrab
import webcolors

def get_color_name(rgb):
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        return "Unknown"

def get_color_info(x, y):
    try:
        bbox = (x * screen_scale, y * screen_scale, (x+1) * screen_scale, (y+1) * screen_scale)
        image = ImageGrab.grab(bbox)
        rgb = image.getpixel((0, 0))
        hex_color = '#%02x%02x%02x' % rgb
        color_name = get_color_name(rgb)
        return color_name, hex_color, rgb
    except Exception:
        return "Error", "#000000", (0, 0, 0)

def update_label():
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    color_name, hex_color, rgb = get_color_info(x, y)

    # Atualiza o texto da label sem fundo
    label.config(
        text=f"{color_name}\n{hex_color}\n{rgb}",
        fg="black" if sum(rgb) > 382 else "white",  # Alterna entre preto e branco para melhor visibilidade
        bg="black"  # Mesma cor do transparentcolor para remover fundo
    )

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