from PIL import Image
import os

files = ['kaledo_transparent.png', 'halo_transparent.png', 'fog_transparent.png']

for file_name in files:
    if not os.path.exists(file_name):
        print(f"[!] Chybí zdroják: {file_name}")
        continue

    print(f"[*] Optimalizuji luminance masku pro: {file_name} (vektorizovaně)")
    img = Image.open(file_name).convert("RGBA")
    
    # 1. Získáme jasovou složku (L) pomocí standardních koeficientů
    luma = img.convert("L")
    
    # 2. Vytvoříme Lookup Table (LUT) pro bleskovou transformaci jasu na alfu
    def calc_alpha(v):
        if v > 245: return 0
        if v < 80: return 255
        return int(255 - ((v - 80) * (255 / (245 - 80))))

    lut = [calc_alpha(i) for i in range(256)]
    alpha_mask = luma.point(lut)
    
    # 3. Aplikujeme novou masku na původní RGB kanály
    r, g, b, _ = img.split()
    img = Image.merge("RGBA", (r, g, b, alpha_mask))
    
    output_path = f"OVERLAY_{file_name}"
    img.save(output_path, "PNG")
    print(f"[+] Hotovo. Čistý optický overlay: {output_path}")