import os
import subprocess

def check_gitignore():
    print("🔍 Проверка работы .gitignore")
    print("=" * 40)
    
    # Создаем тестовые файлы, которые должны игнорироваться
    test_files = [
        'venv/test.txt',           # Должен игнорироваться
        'data/test.csv',           # Должен игнорироваться  
        'data/train.csv',          # НЕ должен игнорироваться
        'models/test_model.joblib', # Должен игнорироваться
        'models/acceptance_model.joblib', # НЕ должен игнорироваться
        '__pycache__/test.pyc',    # Должен игнорироваться
    ]
    
    # Создаем папки и файлы
    for file_path in test_files:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write('test content')
        print(f"📄 Создан: {file_path}")
    
    # Проверяем статус git
    print("\n📊 Статус Git (игнорируемые файлы):")
    result = subprocess.run(['git', 'status', '--ignored'], capture_output=True, text=True)
    print(result.stdout)
    
    # Очистка тестовых файлов
    for file_path in test_files:
        if os.path.exists(file_path):
            os.remove(file_path)
    print("🧹 Тестовые файлы удалены")

if __name__ == "__main__":
    check_gitignore()