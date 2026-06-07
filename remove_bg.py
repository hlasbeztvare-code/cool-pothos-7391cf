import sys
from PIL import Image

def remove_white_bg(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        # Check if pixel is white or very close to white
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            # Fully transparent
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    img.save(output_path, "PNG")
    print(f"Processed {output_path}")

for file in sys.argv[1:]:
    remove_white_bg(file, file)
