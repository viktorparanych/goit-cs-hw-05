import asyncio
import argparse
import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path: Path, output_folder: Path):
    try:
       
        ext = file_path.suffix.lstrip('.').lower()
        if not ext:
            ext = 'no_extension'
        
        target_folder = output_folder / ext
        
        await asyncio.to_thread(target_folder.mkdir, parents=True, exist_ok=True)
        
        target_path = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy2, file_path, target_path)
        
    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {file_path}: {e}")

async def read_folder(source_folder: Path, output_folder: Path):
    try:
        tasks = []
        for item in source_folder.rglob('*'):
            if item.is_file():
                tasks.append(copy_file(item, output_folder))

        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка при читанні папки {source_folder}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output", type=str, help="Шлях до папки призначення")
    
    args = parser.parse_args()
    
    source_folder = Path(args.source)
    output_folder = Path(args.output)
    
    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Вихідна папка {source_folder} не існує або не є директорією.")
        return

    asyncio.run(read_folder(source_folder, output_folder))
    print(f"Сортування завершено. Перевірте папку: {output_folder}")

if __name__ == "__main__":
    main()
