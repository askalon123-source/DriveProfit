import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
import sys
from typing import Dict, Any

print("💰 Запуск оптимизации цены...")

# Получаем абсолютные пути
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
models_dir = os.path.join(project_root, 'models')
output_dir = os.path.join(project_root, 'output')

# Создаем папки если их нет
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Корень проекта: {project_root}")
print(f"📁 Папка models: {models_dir}")
print(f"📁 Папка output: {output_dir}")

# Проверяем существование модели
model_path = os.path.join(models_dir, 'acceptance_model.joblib')
if not os.path.exists(model_path):
    print(f"❌ Модель не найдена: {model_path}")
    print("💡 Сначала запустите: python src/model.py")
    sys.exit(1)

try:
    # Загружаем модель
    print("📥 Загрузка модели...")
    model = joblib.load(model_path)
    print("✅ Модель успешно загружена")
except Exception as e:
    print(f"❌ Ошибка загрузки модели: {e}")
    sys.exit(1)

class PriceOptimizer:
    def __init__(self, model):
        self.model = model
        # Определяем признаки, которые использует модель
        self.features = [
            'price_start_local', 'price_bid_local', 'price_ratio',
            'driver_rating', 'distance_km', 'order_hour'
        ]
        print(f"🔧 Оптимизатор инициализирован с {len(self.features)} признаками")
    
    def predict_probability(self, order_features: Dict[str, Any], bid_price: float) -> float:
        """Предсказание вероятности принятия для конкретной цены"""
        try:
            # Копируем и обновляем признаки
            features = order_features.copy()
            features['price_bid_local'] = bid_price
            features['price_ratio'] = bid_price / features['price_start_local']
            
            # Создаем DataFrame с правильным порядком признаков
            # Используем только те признаки, которые есть в features
            input_data = {}
            for feature in self.features:
                if feature in features:
                    input_data[feature] = [features[feature]]
                else:
                    print(f"⚠️ Признак {feature} отсутствует, используем значение по умолчанию")
                    # Значения по умолчанию
                    if feature == 'driver_rating':
                        input_data[feature] = [4.5]
                    elif feature == 'distance_km':
                        input_data[feature] = [5.0]
                    elif feature == 'order_hour':
                        input_data[feature] = [12]
            
            input_df = pd.DataFrame(input_data)
            
            # Убедимся, что порядок признаков правильный
            input_df = input_df[self.features]
            
            probability = self.model.predict_proba(input_df)[0, 1]
            return probability
        except Exception as e:
            print(f"❌ Ошибка предсказания: {e}")
            return 0.5
    
    def find_optimal_price(self, order_features: Dict[str, Any], 
                          min_markup: float = 0.0, 
                          max_markup: float = 0.5, 
                          steps: int = 50) -> Dict[str, Any]:
        """Находит оптимальную цену для максимизации ожидаемого дохода"""
        
        base_price = order_features['price_start_local']
        
        # Генерируем варианты цен
        markups = np.linspace(min_markup, max_markup, steps)
        price_options = [base_price * (1 + markup) for markup in markups]
        
        results = []
        
        print("🔍 Расчет оптимальной цены...")
        for i, price in enumerate(price_options):
            if i % 10 == 0:  # Прогресс каждые 10 шагов
                print(f"   ...расчет {i+1}/{len(price_options)}")
                
            prob = self.predict_probability(order_features, price)
            expected_revenue = price * prob
            
            results.append({
                'price': price,
                'probability': prob,
                'expected_revenue': expected_revenue,
                'markup_percent': ((price - base_price) / base_price) * 100
            })
        
        df_results = pd.DataFrame(results)
        
        # Находим оптимальную цену
        optimal_idx = df_results['expected_revenue'].idxmax()
        optimal = df_results.loc[optimal_idx]
        
        # Находим безопасную цену (высокая вероятность)
        safe_candidates = df_results[df_results['probability'] >= 0.7]
        safe = safe_candidates.loc[safe_candidates['expected_revenue'].idxmax()] if len(safe_candidates) > 0 else optimal
        
        return {
            'optimal': optimal.to_dict(),
            'safe': safe.to_dict() if not safe.empty else None,
            'all_options': df_results,
            'base_price': base_price
        }
    
    def plot_optimization(self, optimization_result: Dict[str, Any]):
        """Визуализация результатов оптимизации"""
        df = optimization_result['all_options']
        optimal = optimization_result['optimal']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # График 1: Вероятность принятия
        ax1.plot(df['price'], df['probability'], 'b-', linewidth=2, label='Вероятность принятия')
        ax1.axvline(optimal['price'], color='r', linestyle='--', 
                   label=f"Оптимальная цена: {optimal['price']:.0f}₽")
        ax1.set_xlabel('Цена бида (₽)')
        ax1.set_ylabel('Вероятность принятия')
        ax1.set_title('Зависимость вероятности от цены')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # График 2: Ожидаемый доход
        ax2.plot(df['price'], df['expected_revenue'], 'g-', linewidth=2, label='Ожидаемый доход')
        ax2.axvline(optimal['price'], color='r', linestyle='--',
                   label=f"Максимум: {optimal['expected_revenue']:.0f}₽")
        ax2.set_xlabel('Цена бида (₽)')
        ax2.set_ylabel('Ожидаемый доход (₽)')
        ax2.set_title('Оптимизация ожидаемого дохода')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Сохраняем график
        output_path = os.path.join(output_dir, 'price_optimization.png')
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ График оптимизации сохранен: {output_path}")
        
        return fig

# Демонстрация работы
if __name__ == "__main__":
    try:
        # Инициализируем оптимизатор
        optimizer = PriceOptimizer(model)
        
        # Пример заказа
        sample_order = {
            'price_start_local': 300,
            'driver_rating': 4.7,
            'distance_km': 5.2,
            'order_hour': 18
        }
        
        print("\n🔍 Анализ заказа:")
        print(f"   - Базовая цена: {sample_order['price_start_local']}₽")
        print(f"   - Дистанция: {sample_order['distance_km']} км")
        print(f"   - Рейтинг водителя: {sample_order['driver_rating']}")
        print(f"   - Время заказа: {sample_order['order_hour']}:00")
        
        # Находим оптимальную цену
        result = optimizer.find_optimal_price(sample_order)
        
        print("\n🎯 Рекомендации:")
        print(f"   💰 Базовая цена: {result['base_price']}₽")
        print(f"   ⭐ Оптимальная цена: {result['optimal']['price']:.0f}₽")
        print(f"   📊 Вероятность принятия: {result['optimal']['probability']:.1%}")
        print(f"   💵 Ожидаемый доход: {result['optimal']['expected_revenue']:.0f}₽")
        print(f"   📈 Надбавка: {result['optimal']['markup_percent']:.1f}%")
        
        if result['safe'] and result['safe']['price'] != result['optimal']['price']:
            print(f"   🔒 Безопасная цена: {result['safe']['price']:.0f}₽")
            print(f"   🛡️  Вероятность принятия: {result['safe']['probability']:.1%}")
        
        # Визуализация
        print("\n🎨 Создание графика оптимизации...")
        optimizer.plot_optimization(result)
        
        # Дополнительные примеры
        print("\n🔍 Дополнительные сценарии:")
        
        scenarios = [
            {"name": "Высокий рейтинг, короткая поездка", "rating": 4.9, "distance": 3.0, "hour": 10},
            {"name": "Низкий рейтинг, дальняя поездка", "rating": 4.0, "distance": 20.0, "hour": 3},
            {"name": "Вечерний час пик", "rating": 4.5, "distance": 8.0, "hour": 19}
        ]
        
        for scenario in scenarios:
            test_order = {
                'price_start_local': 300,
                'driver_rating': scenario["rating"],
                'distance_km': scenario["distance"],
                'order_hour': scenario["hour"]
            }
            
            test_result = optimizer.find_optimal_price(test_order)
            optimal = test_result['optimal']
            
            print(f"   {scenario['name']}:")
            print(f"      - Оптимальная цена: {optimal['price']:.0f}₽")
            print(f"      - Вероятность: {optimal['probability']:.1%}")
            print(f"      - Доход: {optimal['expected_revenue']:.0f}₽")
        
        print("\n🎉 Оптимизация завершена!")
        print("🚀 Теперь можно запустить визуализацию интерфейса:")
        print("   python src/visualization.py")
        
        # Показываем график
        plt.show()
        
    except Exception as e:
        print(f"❌ Ошибка в оптимизации: {e}")
        import traceback
        traceback.print_exc()