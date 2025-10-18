import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os
import sys

print("🎨 Создание интерфейса для водителя...")

# Получаем абсолютные пути
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
output_dir = os.path.join(project_root, 'output')

# Создаем папку output если ее нет
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Папка output: {output_dir}")

class InterfaceDesigner:
    def __init__(self):
        self.fig = None
        self.ax = None
    
    def create_driver_interface(self, order_info, recommendations):
        """
        Создает макет интерфейса для водителя
        """
        # Создаем фигуру
        self.fig, self.ax = plt.subplots(1, 1, figsize=(8, 10))
        
        # Настройка области отображения
        self.ax.set_xlim(0, 400)
        self.ax.set_ylim(0, 600)
        self.ax.axis('off')
        
        # Заголовок
        self._add_text(200, 580, "Drivee - Умный помощник", size=16, weight='bold')
        
        # Информация о заказе
        self._add_order_info(order_info, 200, 520)
        
        # Рекомендации по цене
        self._add_price_recommendations(recommendations, 200, 400)
        
        # Шкала вероятности
        self._add_probability_scale(recommendations, 200, 250)
        
        # Кнопка действия
        self._add_action_button(200, 150, recommendations)
        
        plt.tight_layout()
        return self.fig
    
    def _add_text(self, x, y, text, size=12, weight='normal', color='black'):
        """Добавляет текст на интерфейс"""
        self.ax.text(x, y, text, 
                    fontsize=size, 
                    weight=weight, 
                    color=color,
                    ha='center', va='center',
                    fontfamily='DejaVu Sans')
    
    def _add_order_info(self, order_info, x, y):
        """Блок информации о заказе"""
        # Фон блока
        rect = FancyBboxPatch((x-180, y-80), 360, 100,
                             boxstyle="round,pad=0.02",
                             facecolor='lightblue', alpha=0.3)
        self.ax.add_patch(rect)
        
        self._add_text(x, y, "Информация о заказе", size=14, weight='bold')
        self._add_text(x, y-20, f"Маршрут: {order_info['distance_km']:.1f} км")
        self._add_text(x, y-40, f"Время: {order_info['duration_min']:.0f} мин")
        self._add_text(x, y-60, f"Базовая цена: {order_info['base_price']}₽")
    
    def _add_price_recommendations(self, recommendations, x, y):
        """Блок рекомендаций по цене"""
        optimal = recommendations['optimal']
        safe = recommendations.get('safe')
        
        self._add_text(x, y, "Рекомендуемые цены", size=14, weight='bold')
        
        # Безопасный вариант
        if safe:
            safe_rect = FancyBboxPatch((x-180, y-60), 360, 40,
                                     boxstyle="round,pad=0.02",
                                     facecolor='green', alpha=0.3)
            self.ax.add_patch(safe_rect)
            self._add_text(x, y-40, f"Надежный: {safe['price']:.0f}₽ (шанс: {safe['probability']:.0%})")
        
        # Оптимальный вариант
        optimal_rect = FancyBboxPatch((x-180, y-110), 360, 40,
                                    boxstyle="round,pad=0.02", 
                                    facecolor='orange', alpha=0.3)
        self.ax.add_patch(optimal_rect)
        self._add_text(x, y-90, f"Оптимальный: {optimal['price']:.0f}₽ (доход: {optimal['expected_revenue']:.0f}₽)")
        
        # Рискованный вариант
        risky_price = optimal['price'] * 1.2
        self._add_text(x, y-140, f"Рискованный: {risky_price:.0f}₽")
    
    def _add_probability_scale(self, recommendations, x, y):
        """Шкала вероятности принятия"""
        self._add_text(x, y, "Шанс принятия заказа", size=14, weight='bold')
        
        # Шкала
        scale_rect = patches.Rectangle((x-100, y-30), 200, 20, 
                                     facecolor='lightgray', alpha=0.5)
        self.ax.add_patch(scale_rect)
        
        # Заполнение в зависимости от вероятности
        prob = recommendations['optimal']['probability']
        fill_width = 200 * prob
        fill_rect = patches.Rectangle((x-100, y-30), fill_width, 20,
                                    facecolor='blue', alpha=0.7)
        self.ax.add_patch(fill_rect)
        
        # Текст вероятности
        self._add_text(x, y-20, f"{prob:.0%}", size=12, weight='bold', color='white')
    
    def _add_action_button(self, x, y, recommendations):
        """Кнопка действия"""
        button_rect = FancyBboxPatch((x-80, y-30), 160, 50,
                                   boxstyle="round,pad=0.1",
                                   facecolor='#4CAF50', alpha=0.8)
        self.ax.add_patch(button_rect)
        self._add_text(x, y-5, "ПОДТВЕРДИТЬ", size=14, weight='bold', color='white')
        self._add_text(x, y-20, f"{recommendations['optimal']['price']:.0f}₽", 
                      size=16, weight='bold', color='white')

# Основная часть скрипта
def main():
    try:
        # Создаем дизайнер
        designer = InterfaceDesigner()
        
        # Тестовые данные
        sample_recommendations = {
            'optimal': {
                'price': 350,
                'probability': 0.75,
                'expected_revenue': 262.5
            },
            'safe': {
                'price': 320,
                'probability': 0.9,
                'expected_revenue': 288
            }
        }
        
        sample_order_info = {
            'distance_km': 5.2,
            'duration_min': 15,
            'base_price': 300
        }
        
        print("📋 Создание интерфейса с тестовыми данными...")
        print(f"   - Базовая цена: {sample_order_info['base_price']}₽")
        print(f"   - Оптимальная цена: {sample_recommendations['optimal']['price']}₽")
        print(f"   - Вероятность принятия: {sample_recommendations['optimal']['probability']:.1%}")
        
        # Создаем интерфейс
        fig = designer.create_driver_interface(sample_order_info, sample_recommendations)
        
        # Сохраняем в несколько форматов на всякий случай
        output_paths = [
            os.path.join(output_dir, 'driver_interface.png'),
            os.path.join(output_dir, 'interface.png')
        ]
        
        for output_path in output_paths:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ Интерфейс сохранен: {output_path} ({file_size} байт)")
            else:
                print(f"❌ Не удалось сохранить: {output_path}")
        
        # Показываем интерфейс
        print("🖼️ Показываем интерфейс...")
        plt.show()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании интерфейса: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Визуализация завершена!")
        print("🚀 Интерфейс водителя создан и сохранен")
    else:
        print("\n💥 Визуализация не удалась")
        sys.exit(1)