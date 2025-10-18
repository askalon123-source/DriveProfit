import os
import sys
import subprocess

def run_script(script_name):
    """Запуск скрипта и проверка результата"""
    print(f"\n🎯 Запуск {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              cwd=os.path.dirname(script_name),
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {script_name} выполнен успешно")
            print(result.stdout)
        else:
            print(f"❌ Ошибка в {script_name}:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Не удалось запустить {script_name}: {e}")

def main():
    print("🚗 ЗАПУСК ПОЛНОГО ПАЙПЛАЙНА DRIVEE")
    print("=" * 50)
    
    # Создаем папки
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    scripts = [
        'src/analysis.py',
        'src/model.py', 
        'src/optimization.py',
        'src/visualization.py'
    ]
    
    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f"❌ Файл {script} не найден")
    
    # Проверяем результаты
    print("\n📁 ПРОВЕРКА СОЗДАННЫХ ФАЙЛОВ:")
    output_files = os.listdir('output')
    if output_files:
        print("✅ Файлы в папке output:")
        for file in output_files:
            print(f"   - {file}")
    else:
        print("❌ В папке output нет файлов")
    
    data_files = os.listdir('data')
    if data_files:
        print("✅ Файлы в папке data:")
        for file in data_files:
            print(f"   - {file}")
    
    models_files = os.listdir('models')
    if models_files:
        print("✅ Файлы в папке models:")
        for file in models_files:
            print(f"   - {file}")

if __name__ == "__main__":
    main()