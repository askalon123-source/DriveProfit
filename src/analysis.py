import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

print("🚗 Анализ данных Drivee...")

# Получаем абсолютные пути
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
data_dir = os.path.join(project_root, 'data')
output_dir = os.path.join(project_root, 'output')

# Создаем папки если их нет
os.makedirs(data_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Рабочая директория: {current_dir}")
print(f"📁 Корень проекта: {project_root}")
print(f"📁 Папка data: {data_dir}")
print(f"📁 Папка output: {output_dir}")

# Создаем тестовые данные
np.random.seed(42)
n_samples = 1000

print("📊 Создание тестовых данных...")
data = pd.DataFrame({
    'price_start_local': np.random.randint(200, 500, n_samples),
    'price_bid_local': np.random.randint(250, 600, n_samples),
    'driver_rating': np.random.uniform(3.5, 5.0, n_samples),
    'distance_km': np.random.uniform(1, 20, n_samples),
    'is_done': np.random.choice([0, 1], n_samples, p=[0.3, 0.7])
})

# Сохраняем данные
data_path = os.path.join(data_dir, 'train.csv')
data.to_csv(data_path, index=False)
print(f"✅ Данные сохранены в {data_path}")

# Проверяем сохранение данных
if os.path.exists(data_path):
    file_size = os.path.getsize(data_path)
    print(f"✅ Файл данных создан, размер: {file_size} байт")
else:
    print("❌ Файл данных НЕ создан!")

# Создаем графики
print("🎨 Создание графиков...")

# График 1: Распределение цен
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.hist(data['price_start_local'], alpha=0.7, label='Стартовая цена', bins=20, color='blue')
plt.hist(data['price_bid_local'], alpha=0.7, label='Цена бида', bins=20, color='orange')
plt.legend()
plt.title('Распределение цен')
plt.xlabel('Цена (₽)')
plt.ylabel('Количество')

# График 2: Статистика принятия
plt.subplot(2, 2, 2)
acceptance_rate = data['is_done'].mean()
labels = [f'Принято\n{acceptance_rate:.1%}', f'Отклонено\n{1-acceptance_rate:.1%}']
sizes = [acceptance_rate, 1 - acceptance_rate]
colors = ['#4CAF50', '#F44336']
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Статистика принятия заказов')

# График 3: Принятие по рейтингу
plt.subplot(2, 2, 3)
accepted = data[data['is_done'] == 1]
rejected = data[data['is_done'] == 0]
plt.hist(accepted['driver_rating'], alpha=0.7, label='Принятые', bins=15, color='green', density=True)
plt.hist(rejected['driver_rating'], alpha=0.7, label='Отклоненные', bins=15, color='red', density=True)
plt.xlabel('Рейтинг водителя')
plt.ylabel('Плотность')
plt.title('Принятие по рейтингу')
plt.legend()

# График 4: Принятие по дистанции
plt.subplot(2, 2, 4)
plt.scatter(accepted['distance_km'], accepted['price_bid_local'], alpha=0.5, label='Принятые', color='green')
plt.scatter(rejected['distance_km'], rejected['price_bid_local'], alpha=0.5, label='Отклоненные', color='red')
plt.xlabel('Дистанция (км)')
plt.ylabel('Цена бида (₽)')
plt.title('Принятие по дистанции и цене')
plt.legend()

plt.tight_layout()

# Сохраняем график ДО показа
output_path = os.path.join(output_dir, 'analysis_results.png')
print(f"💾 Сохраняем график в: {output_path}")
plt.savefig(output_path, dpi=150, bbox_inches='tight')

# Проверяем сохранение графика
if os.path.exists(output_path):
    file_size = os.path.getsize(output_path)
    print(f"✅ График сохранен, размер: {file_size} байт")
else:
    print("❌ График НЕ сохранен!")

# Показываем график
print("🖼️ Показываем график...")
plt.show()

print("🎉 Анализ завершен!")
print(f"📊 Проанализировано {len(data)} заказов")
print(f"✅ Принято: {data['is_done'].sum()} ({data['is_done'].mean():.1%})")