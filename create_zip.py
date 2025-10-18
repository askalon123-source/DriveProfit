import os
import zipfile
import datetime

def create_project_zip():
    print("📦 Создание ZIP-архива для GitHub...")
    
    # Исключаемые папки и файлы
    exclude_dirs = {'venv', '__pycache__', '.git'}
    exclude_files = {'.gitignore'}  # Мы добавим его вручную
    
    # Имя архива с датой
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    zip_name = f"drivee-case-{date_str}.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Добавляем файлы из корневой папки
        for root, dirs, files in os.walk('.'):
            # Пропускаем исключенные папки
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files:
                    continue
                    
                file_path = os.path.join(root, file)
                # Пропускаем сам архив и системные файлы
                if file.endswith('.zip') or file.startswith('.'):
                    continue
                
                # Относительный путь для архива
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
                print(f"✅ Добавлен: {arcname}")
    
    file_size = os.path.getsize(zip_name) / 1024 / 1024
    print(f"\n🎉 Архив создан: {zip_name}")
    print(f"💾 Размер: {file_size:.2f} MB")
    
    return zip_name

if __name__ == "__main__":
    create_project_zip()