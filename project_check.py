import os
import sys

def check_project():
    print("🔍 ПРОВЕРКА ЗАВЕРШЕННОСТИ ПРОЕКТА")
    print("=" * 50)
    
    required_files = {
        '📊 Данные': ['data/train.csv'],
        '🤖 Модели': ['models/acceptance_model.joblib'],
        '📈 Результаты': [
            'output/analysis_results.png',
            'output/feature_importance.png', 
            'output/price_optimization.png',
            'output/driver_interface.png'
        ],
        '🐍 Исходный код': [
            'src/analysis.py',
            'src/model.py',
            'src/optimization.py',
            'src/visualization.py'
        ],
        '📄 Документация': [
            'README.md',
            'requirements.txt',
            'final_demo.py'
        ]
    }
    
    all_good = True
    
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"   ✅ {file} ({size} байт)")
            else:
                print(f"   ❌ {file} - ОТСУТСТВУЕТ")
                all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ВСЕ ФАЙЛЫ НА МЕСТЕ! ПРОЕКТ ЗАВЕРШЕН!")
        print("\n🚀 Проект готов к сдаче на конкурс!")
    else:
        print("⚠️  НЕКОТОРЫЕ ФАЙЛЫ ОТСУТСТВУЮТ")
        print("\n💡 Запустите скрипты для создания отсутствующих файлов")
    
    return all_good

if __name__ == "__main__":
    if check_project():
        sys.exit(0)
    else:
        sys.exit(1)