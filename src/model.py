import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import sys

print("🤖 Запуск обучения ML-модели...")

# Получаем абсолютные пути
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
data_dir = os.path.join(project_root, 'data')
models_dir = os.path.join(project_root, 'models')
output_dir = os.path.join(project_root, 'output')

# Создаем папки если их нет
os.makedirs(data_dir, exist_ok=True)
os.makedirs(models_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Корень проекта: {project_root}")
print(f"📁 Папка data: {data_dir}")
print(f"📁 Папка models: {models_dir}")

# Проверяем существование данных
data_path = os.path.join(data_dir, 'train.csv')
if not os.path.exists(data_path):
    print(f"❌ Файл {data_path} не найден!")
    print("💡 Сначала запустите: python src/analysis.py")
    sys.exit(1)

try:
    # Загружаем данные
    print("📥 Загрузка данных...")
    data = pd.read_csv(data_path)
    print(f"✅ Данные загружены: {len(data)} записей, {len(data.columns)} колонок")
    print(f"📊 Колонки: {list(data.columns)}")
except Exception as e:
    print(f"❌ Ошибка загрузки данных: {e}")
    sys.exit(1)

# Проверяем целевую переменную
if 'is_done' not in data.columns:
    print("❌ В данных нет колонки 'is_done' (целевая переменная)")
    sys.exit(1)

# Предобработка данных
print("🔧 Подготовка данных...")

# Создаем дополнительные признаки если их нет
if 'distance_km' not in data.columns:
    data['distance_km'] = data.get('distance_in_meters', 5000) / 1000

if 'price_ratio' not in data.columns:
    data['price_ratio'] = data['price_bid_local'] / data['price_start_local']

# Выбираем доступные признаки
available_features = []
for feature in ['price_start_local', 'price_bid_local', 'price_ratio', 
                'driver_rating', 'distance_km', 'order_hour']:
    if feature in data.columns:
        available_features.append(feature)
    else:
        print(f"⚠️ Признак {feature} отсутствует в данных")

print(f"📊 Используется {len(available_features)} признаков: {available_features}")

# Удаляем пропуски
data_clean = data[available_features + ['is_done']].dropna()
print(f"📈 После очистки: {len(data_clean)} записей")

if len(data_clean) == 0:
    print("❌ Нет данных для обучения после очистки!")
    sys.exit(1)

X = data_clean[available_features]
y = data_clean['is_done']

# Разделяем на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"📊 Разделение данных:")
print(f"   - Обучающая выборка: {X_train.shape[0]} записей")
print(f"   - Тестовая выборка: {X_test.shape[0]} записей")
print(f"   - Принято заказов: {y_train.mean():.1%}")

# Обучаем модель
print("🎯 Обучение модели RandomForest...")

try:
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    print("✅ Модель успешно обучена")
except Exception as e:
    print(f"❌ Ошибка обучения модели: {e}")
    sys.exit(1)

# Предсказания
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Оценка модели
accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

print("\n📊 Результаты модели:")
print(f"   - Accuracy: {accuracy:.3f}")
print(f"   - ROC-AUC: {roc_auc:.3f}")

# Детальный отчет
print("\n📋 Детальный отчет:")
print(classification_report(y_test, y_pred, target_names=['Отклонен', 'Принят']))

# Важность признаков
feature_importance = pd.DataFrame({
    'feature': available_features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🔝 Важность признаков:")
for _, row in feature_importance.iterrows():
    print(f"   - {row['feature']}: {row['importance']:.3f}")

# Визуализация важности признаков
plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance, x='importance', y='feature')
plt.title('Важность признаков в модели')
plt.xlabel('Важность')
plt.tight_layout()

# Сохраняем график
feature_importance_path = os.path.join(output_dir, 'feature_importance.png')
plt.savefig(feature_importance_path, dpi=150, bbox_inches='tight')
print(f"✅ График важности признаков сохранен: {feature_importance_path}")

# Сохраняем модель
model_path = os.path.join(models_dir, 'acceptance_model.joblib')
joblib.dump(model, model_path)
print(f"💾 Модель сохранена: {model_path}")

# Проверяем сохранение
if os.path.exists(model_path):
    file_size = os.path.getsize(model_path)
    print(f"✅ Модель успешно сохранена, размер: {file_size} байт")
else:
    print("❌ Модель не сохранена!")

# Демонстрация работы модели
print("\n🎪 Демонстрация работы модели:")

def predict_acceptance_probability(features_dict):
    """Предсказание вероятности принятия заказа"""
    try:
        # Создаем DataFrame с правильным порядком признаков
        input_data = pd.DataFrame([features_dict])[available_features]
        probability = model.predict_proba(input_data)[0, 1]
        return probability
    except Exception as e:
        print(f"❌ Ошибка предсказания: {e}")
        return 0.5

# Примеры предсказаний
examples = [
    {
        'price_start_local': 300,
        'price_bid_local': 320,
        'price_ratio': 320/300,
        'driver_rating': 4.8,
        'distance_km': 5.0,
        'order_hour': 18
    },
    {
        'price_start_local': 300,
        'price_bid_local': 400,
        'price_ratio': 400/300,
        'driver_rating': 4.2,
        'distance_km': 15.0,
        'order_hour': 3
    }
]

for i, example in enumerate(examples, 1):
    # Проверяем, что все признаки присутствуют
    missing_features = [f for f in available_features if f not in example]
    if missing_features:
        print(f"⚠️ В примере {i} отсутствуют признаки: {missing_features}")
        continue
        
    prob = predict_acceptance_probability(example)
    print(f"   Пример {i}:")
    print(f"      - Базовая цена: {example['price_start_local']}₽")
    print(f"      - Цена бида: {example['price_bid_local']}₽")
    print(f"      - Надбавка: {((example['price_ratio']-1)*100):.1f}%")
    print(f"      - Рейтинг водителя: {example['driver_rating']}")
    print(f"      - Вероятность принятия: {prob:.1%}")

print("\n🎉 Обучение модели завершено!")
print("🚀 Теперь можно запустить оптимизацию цены:")
print("   python src/optimization.py")

# Показываем график в конце
plt.show()