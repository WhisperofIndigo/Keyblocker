from PIL import Image, ImageDraw

# Создаем иконку
img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Рисуем круг (фон)
draw.ellipse([8, 8, 56, 56], fill='#2E7D32', outline='white', width=2)

# Рисуем символ клавиатуры
for x in range(20, 45, 8):
    for y in range(25, 40, 7):
        draw.rectangle([x, y, x+5, y+4], fill='white')

# Сохраняем как ICO
img.save('icon.ico', format='ICO')
print("✓ Иконка создана: icon.ico")
