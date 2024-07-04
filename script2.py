from PIL import Image, ImageDraw, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox

def hex_to_rgba(hex_color, alpha):
    """Перетворює HEX колір у RGBA."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb + (alpha,)

def create_striped_image(width, height, black_stripe_width, white_stripe_width, orientation, black_color, white_color, angle):
    # Створимо нове зображення
    image = Image.new("RGBA", (width, height), white_color)
    draw = ImageDraw.Draw(image)

    total_stripe_width = black_stripe_width + white_stripe_width

    if orientation == 'vertical':
        for x in range(0, width, total_stripe_width):
            draw.rectangle([x, 0, x + black_stripe_width - 1, height], fill=black_color)
    elif orientation == 'horizontal':
        for y in range(0, height, total_stripe_width):
            draw.rectangle([0, y, width, y + black_stripe_width - 1], fill=black_color)
    elif orientation == 'grid':
        for x in range(0, width, total_stripe_width):
            for y in range(0, height, total_stripe_width):
                draw.rectangle([x, y, x + black_stripe_width - 1, y + black_stripe_width - 1], fill=black_color)
    
    if angle != 0:
        image = image.rotate(angle, expand=1, fillcolor=white_color)
        image = image.crop((0, 0, width, height))
    
    return image

def save_image(image, file_name):
    try:
        image.save(file_name)
        messagebox.showinfo("Успіх", f"Зображення успішно збережено як {file_name}")
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка під час збереження зображення: {e}")

def browse_file():
    file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_name:
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(0, file_name)

def choose_color(entry):
    color_code = colorchooser.askcolor(title="Виберіть колір")[1]
    if color_code:
        entry.delete(0, tk.END)
        entry.insert(0, color_code)

def preview_image(image):
    preview_window = tk.Toplevel(root)
    preview_window.title("Перегляд зображення")
    preview_window.geometry(f"{image.width}x{image.height}")

    img = ImageTk.PhotoImage(image)
    img_label = tk.Label(preview_window, image=img)
    img_label.image = img  # Збереження посилання на зображення, щоб уникнути його видалення
    img_label.pack()

    preview_window.bind("<Escape>", lambda e: preview_window.destroy())
    preview_window.bind("<F11>", lambda e: toggle_fullscreen(preview_window))

def toggle_fullscreen(window):
    is_fullscreen = window.attributes("-fullscreen")
    window.attributes("-fullscreen", not is_fullscreen)

def create_image():
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        black_stripe_width = int(black_stripe_width_entry.get())
        white_stripe_width = int(white_stripe_width_entry.get())
        orientation = orientation_var.get()
        angle = int(angle_entry.get())
        black_color_hex = black_color_entry.get()
        white_color_hex = white_color_entry.get()
        black_alpha = int(black_alpha_entry.get())
        white_alpha = int(white_alpha_entry.get())
        file_name = file_name_entry.get()

        black_color = hex_to_rgba(black_color_hex, black_alpha)
        white_color = hex_to_rgba(white_color_hex, white_alpha)

        if orientation not in ['vertical', 'horizontal', 'grid']:
            messagebox.showerror("Помилка", "Неправильна орієнтація. Використовуйте 'vertical', 'horizontal' або 'grid'.")
            return

        image = create_striped_image(width, height, black_stripe_width, white_stripe_width, orientation, black_color, white_color, angle)

        preview_image(image)
        save_image(image, file_name)
    except ValueError:
        messagebox.showerror("Помилка", "Перевірте, що всі введені дані є правильними числами.")

# Створення головного вікна
root = tk.Tk()
root.title("Генератор смуг та сіток")

# Параметри зображення
tk.Label(root, text="Ширина зображення (у пікселях):").grid(row=0, column=0, sticky=tk.W)
width_entry = tk.Entry(root)
width_entry.grid(row=0, column=1)
width_entry.insert(0, "1920")

tk.Label(root, text="Висота зображення (у пікселях):").grid(row=1, column=0, sticky=tk.W)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)
height_entry.insert(0, "1080")

# Товщина ліній
tk.Label(root, text="Товщина чорних ліній (у пікселях):").grid(row=2, column=0, sticky=tk.W)
black_stripe_width_entry = tk.Entry(root)
black_stripe_width_entry.grid(row=2, column=1)
black_stripe_width_entry.insert(0, "1")

tk.Label(root, text="Товщина білих ліній (у пікселях):").grid(row=3, column=0, sticky=tk.W)
white_stripe_width_entry = tk.Entry(root)
white_stripe_width_entry.grid(row=3, column=1)
white_stripe_width_entry.insert(0, "1")

# Орієнтація ліній
orientation_var = tk.StringVar(value="vertical")
tk.Label(root, text="Орієнтація ліній:").grid(row=4, column=0, sticky=tk.W)
tk.Radiobutton(root, text="Вертикальна", variable=orientation_var, value="vertical").grid(row=4, column=1, sticky=tk.W)
tk.Radiobutton(root, text="Горизонтальна", variable=orientation_var, value="horizontal").grid(row=4, column=2, sticky=tk.W)
tk.Radiobutton(root, text="Сітка", variable=orientation_var, value="grid").grid(row=4, column=3, sticky=tk.W)

# Колір ліній
tk.Label(root, text="Колір чорних ліній (HEX):").grid(row=5, column=0, sticky=tk.W)
black_color_entry = tk.Entry(root)
black_color_entry.grid(row=5, column=1)
black_color_entry.insert(0, "#000000")
tk.Button(root, text="Вибрати колір", command=lambda: choose_color(black_color_entry)).grid(row=5, column=2)

tk.Label(root, text="Колір білих ліній (HEX):").grid(row=6, column=0, sticky=tk.W)
white_color_entry = tk.Entry(root)
white_color_entry.grid(row=6, column=1)
white_color_entry.insert(0, "#FFFFFF")
tk.Button(root, text="Вибрати колір", command=lambda: choose_color(white_color_entry)).grid(row=6, column=2)

# Прозорість ліній
tk.Label(root, text="Прозорість чорних ліній (0-255):").grid(row=7, column=0, sticky=tk.W)
black_alpha_entry = tk.Entry(root)
black_alpha_entry.grid(row=7, column=1)
black_alpha_entry.insert(0, "255")

tk.Label(root, text="Прозорість білих ліній (0-255):").grid(row=8, column=0, sticky=tk.W)
white_alpha_entry = tk.Entry(root)
white_alpha_entry.grid(row=8, column=1)
white_alpha_entry.insert(0, "255")

# Кут повороту
tk.Label(root, text="Кут повороту (0-360 градусів):").grid(row=9, column=0, sticky=tk.W)
angle_entry = tk.Entry(root)
angle_entry.grid(row=9, column=1)
angle_entry.insert(0, "0")

# Назва файлу
tk.Label(root, text="Назва файлу (з розширенням .png):").grid(row=10, column=0, sticky=tk.W)
file_name_entry = tk.Entry(root)
file_name_entry.grid(row=10, column=1)
file_name_entry.insert(0, "black_and_white_stripes.png")
tk.Button(root, text="Огляд...", command=browse_file).grid(row=10, column=2)

# Кнопка створення зображення
tk.Button(root, text="Створити зображення", command=create_image).grid(row=11, column=0, columnspan=3)

# Запуск головного циклу програми
root.mainloop()
