import os
import win32api, win32gui, win32ui, win32con
from PIL import Image
import customtkinter as ctk

exe_path = r"C:\Users\emersonbruno.iel\Desktop\Automações\Reenvio de link.exe"  # Caminho do executável alvo

# 1. Obter dimensões padrão de ícone (geralmente 32x32 para ícone grande no Windows)
ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)  # largura do ícone padrão
ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)  # altura do ícone padrão

# 2. Extrair os handles do ícone (grande e pequeno) do executável
large_icons, small_icons = win32gui.ExtractIconEx(exe_path, 0)  
if small_icons:
    win32gui.DestroyIcon(small_icons[0])  # libera recursos do ícone pequeno

# Seleciona o handle do ícone grande para usar
hicon = large_icons[0] if large_icons else None
if hicon is None:
    raise RuntimeError("Nenhum ícone encontrado no executável.")

# 3. Criar um DC (Device Context) compatível com a tela e um bitmap compatível para desenhar o ícone
hdc_screen = win32gui.GetDC(0)  # DC da tela (desktop)
hdc_mem = win32ui.CreateDCFromHandle(hdc_screen)
hdc_compat = hdc_mem.CreateCompatibleDC()
bmp = win32ui.CreateBitmap()
bmp.CreateCompatibleBitmap(hdc_mem, ico_x, ico_y)

# Seleciona o bitmap no DC em memória e desenha o ícone nele
hdc_compat.SelectObject(bmp)
hdc_compat.DrawIcon((0, 0), hicon)

# 4. Obtém bits do bitmap e converte para uma imagem PIL
bmp_bits = bmp.GetBitmapBits(True)
icon_image = Image.frombuffer('RGBA', (ico_x, ico_y), bmp_bits, 'raw', 'BGRA', 0, 1)

# 5. Liberar recursos corretamente
win32gui.DestroyIcon(hicon)  # Libera o ícone
hdc_compat.DeleteDC()        # Deleta o DC de memória
win32gui.ReleaseDC(0, hdc_screen)  # Libera o DC da tela
win32gui.DeleteObject(bmp.GetHandle())  # Corrigido: liberar o bitmap

# Exibir a imagem no CustomTkinter
app = ctk.CTk()  # janela CustomTkinter
ctk_icon = ctk.CTkImage(light_image=icon_image, size=(ico_x, ico_y))
label = ctk.CTkLabel(app, image=ctk_icon, text="")  # Label com imagem, texto vazio
label.pack(padx=10, pady=10)

app.mainloop()
