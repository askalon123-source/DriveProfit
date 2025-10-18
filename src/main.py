import pandas as pd
import numpy as np
from analysis import DataAnalyzer
from model import AcceptancePredictor
from optimization import PriceOptimizer
from visualization import InterfaceDesigner
import json

def main():
    print("🚗 Запуск умного помощника Drivee...")
    
    # Шаг 1: Анализ данных
    print("\n📊 Шаг 1: Анализ данных...")
    analyzer = DataAnalyzer('../data/train.csv')
    data = analyzer.analyze_acceptance_patterns()
    
    # Шаг 2: Обучение модели
    print("\n🤖 Шаг 2: Обучение модели...")
    predictor = AcceptancePredictor()
    model = predictor.train(data)
    
    # Сохраняем модель
    predictor.save_model('../models/acceptance_model.joblib')
    
    # Шаг 3: Оптимизация цены для примера заказа
    print("\n💰 Шаг 3: Оптимизация цены...")
    optimizer = PriceOptimizer(predictor)
    
    # Пример заказа
    sample_order = {
        'price_start_local': 300,
        'order_hour': 18,
        'order_day_of_week': 4,  # Пятница
        'driver_rating': 4.8,
        'user_rating': 4.5,
        'distance_in_meters': 5000,
        'duration_in_seconds': 900,
        'pickup_in_meters': 1000,
        'pickup_in_seconds': 300,
        'driver_experience_days': 180
    }
    
    # Находим оптимальную цену
    result = optimizer.find_optimal_price(sample_order)
    
    print(f"\n🎯 Результаты оптимизации:")
    print(f"Базовая цена: {result['base_price']}₽")
    print(f"Оптимальная цена: {result['optimal']['price']:.0f}₽")
    print(f"Вероятность принятия: {result['optimal']['probability']:.1%}")
    print(f"Ожидаемый доход: {result['optimal']['expected_revenue']:.0f}₽")
    
    # Визуализация оптимизации
    optimizer.plot_optimization_results(result)
    
    # Шаг 4: Создание интерфейса
    print("\n🎨 Шаг 4: Создание интерфейса...")
    designer = InterfaceDesigner()
    
    order_info = {
        'distance_km': sample_order['distance_in_meters'] / 1000,
        'duration_min': sample_order['duration_in_seconds'] / 60,
        'base_price': sample_order['price_start_local']
    }
    
    interface_fig = designer.create_driver_interface(order_info, result)
    interface_fig.savefig('../output/driver_interface.png', dpi=150, bbox_inches='tight')
    print("💾 Интерфейс сохранен в output/driver_interface.png")
    
    # Шаг 5: Генерация отчета
    generate_report(result, sample_order)
    
    print("\n✅ Умный помощник успешно запущен!")

def generate_report(optimization_result, order_features):
    """Генерация отчета с рекомендациями"""
    report = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'order_features': order_features,
        'recommendations': {
            'optimal_price': optimization_result['optimal']['price'],
            'optimal_probability': optimization_result['optimal']['probability'],
            'expected_revenue': optimization_result['optimal']['expected_revenue'],
            'safe_price': optimization_result.get('safe', {}).get('price'),
            'safe_probability': optimization_result.get('safe', {}).get('probability')
        },
        'analysis': {
            'bid_increase_percent': ((optimization_result['optimal']['price'] - 
                                    order_features['price_start_local']) / 
                                    order_features['price_start_local'] * 100),
            'revenue_improvement': ((optimization_result['optimal']['expected_revenue'] - 
                                   order_features['price_start_local']) / 
                                   order_features['price_start_local'] * 100)
        }
    }
    
    with open('../output/recommendation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("📄 Отчет сохранен в output/recommendation_report.json")

if __name__ == "__main__":
    main()