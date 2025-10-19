"""
Скрипт для создания иконки Keyboard Blocker
"""
from PIL import Image, ImageDraw

def create_keyboard_icon():
    
    # Создаем изображение с прозрачным фоном
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Цвета
    bg_color = (52, 152, 219, 255)  # Синий фон
    key_color = (255, 255, 255, 255)  # Белые клавиши
    outline_color = (41, 128, 185, 255)  # Темнее синий для обводки
    
    # Рисуем основной круг (фон)
    padding = 10
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=bg_color,
        outline=outline_color,
        width=4
    )
    
    # Рисуем клавиши клавиатуры (сетка 3x3 маленьких клавиш)
    key_size = 28
    key_spacing = 12
    start_x = (size - (3 * key_size + 2 * key_spacing)) // 2
    start_y = (size - (3 * key_size + 2 * key_spacing)) // 2
    
    for row in range(3):
        for col in range(3):
            x = start_x + col * (key_size + key_spacing)
            y = start_y + row * (key_size + key_spacing)
            
            # Рисуем клавишу с закругленными углами (эмуляция через ellipse)
            draw.rectangle(
                [x + 2, y, x + key_size - 2, y + key_size],
                fill=key_color
            )
            draw.rectangle(
                [x, y + 2, x + key_size, y + key_size - 2],
                fill=key_color
            )
            # Углы
            draw.ellipse([x, y, x + 4, y + 4], fill=key_color)
            draw.ellipse([x + key_size - 4, y, x + key_size, y + 4], fill=key_color)
            draw.ellipse([x, y + key_size - 4, x + 4, y + key_size], fill=key_color)
            draw.ellipse([x + key_size - 4, y + key_size - 4, x + key_size, y + key_size], fill=key_color)
    
    # Сохраняем иконку в нескольких размерах
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('icon.ico', format='ICO', sizes=icon_sizes)
    
    print("✓ Иконка создана: icon.ico")
    print(f"  Размеры: {', '.join([f'{w}x{h}' for w, h in icon_sizes])}")
    
    # Также сохраняем PNG для предварительного просмотра
    img.save('icon_preview.png', format='PNG')
    print("✓ Превью создано: icon_preview.png")

def create_locked_icon():
    """Создает иконку для заблокированного состояния (красная с замком)"""
    
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Красный фон
    bg_color = (231, 76, 60, 255)
    outline_color = (192, 57, 43, 255)
    lock_color = (255, 255, 255, 255)
    
    padding = 10
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=bg_color,
        outline=outline_color,
        width=4
    )
    
    # Рисуем замок
    lock_width = 80
    lock_height = 100
    lock_x = (size - lock_width) // 2
    lock_y = (size - lock_height) // 2 + 10
    
    # Дужка замка
    arc_top = lock_y - 30
    arc_size = 60
    arc_x = lock_x + (lock_width - arc_size) // 2
    draw.arc(
        [arc_x, arc_top, arc_x + arc_size, arc_top + arc_size],
        start=180, end=0,
        fill=lock_color, width=10
    )
    
    # Корпус замка
    draw.rectangle(
        [lock_x, lock_y, lock_x + lock_width, lock_y + lock_height],
        fill=lock_color
    )
    
    # Замочная скважина
    keyhole_x = lock_x + lock_width // 2
    keyhole_y = lock_y + lock_height // 3
    draw.ellipse(
        [keyhole_x - 8, keyhole_y - 8, keyhole_x + 8, keyhole_y + 8],
        fill=bg_color
    )
    draw.rectangle(
        [keyhole_x - 4, keyhole_y, keyhole_x + 4, keyhole_y + 30],
        fill=bg_color
    )
    
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('icon_locked.ico', format='ICO', sizes=icon_sizes)
    
    print("✓ Иконка заблокированного состояния создана: icon_locked.ico")
    img.save('icon_locked_preview.png', format='PNG')

if __name__ == "__main__":
    print("=" * 50)
    print("Keyboard Blocker Icon Creator")
    print("=" * 50)
    print()
    
    try:
        create_keyboard_icon()
        create_locked_icon()
        print()
        print("=" * 50)
        print("✓ Все иконки успешно созданы!")
        print("=" * 50)
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        print()
        print("Убедитесь, что установлена библиотека Pillow:")
        print("  pip install Pillow")