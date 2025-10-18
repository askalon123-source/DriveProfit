import matplotlib.pyplot as plt
import numpy as np
import os

print("🧪 Тестирование сохранения файлов...")

# Создаем папку output если ее нет
os.makedirs('output', exist_ok=True)

# Простой график для теста
plt.figure(figsize=(10, 6))
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title('Тестовый график')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)

# Сохраняем
plt.savefig('output/test_plot.png', dpi=150, bbox_inches='tight')
print("✅ График сохранен в output/test_plot.png")

# Проверяем, что файл создался
if os.path.exists('output/test_plot.png'):
    print("✅ Файл успешно создан!")
else:
    print("❌ Файл не создан. Проверьте права доступа.")

plt.show()