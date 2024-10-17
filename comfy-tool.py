import os
import sys
import importlib.util
from colorama import init, Fore, Style

def main():
    init(autoreset=True)

    current_directory = os.getcwd()
    print(f"{Fore.CYAN}Scanning directory: {current_directory}")

    results = []

    for root, dirs, files in os.walk(current_directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"{Fore.BLUE}Scanning file: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Ищем импорт модуля folder_paths
                    if 'import folder_paths' in content or 'from folder_paths' in content:
                        # Загружаем модуль folder_paths из того же каталога
                        folder_paths_path = os.path.join(root, 'folder_paths.py')
                        if os.path.exists(folder_paths_path):
                            spec = importlib.util.spec_from_file_location("folder_paths", folder_paths_path)
                            folder_paths = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(folder_paths)

                            # Получаем информацию о путях
                            for key, (paths, extensions) in folder_paths.folder_names_and_paths.items():
                                node_info = {
                                    'Node': file[:-3],
                                    'Key': key,
                                    'Paths': paths,
                                    'FullPaths': [],
                                    'Extensions': extensions,
                                    'Available_models': []
                                }
                                folder_names = []
                                for path in paths:
                                    folder_name = os.path.basename(os.path.normpath(path))
                                    folder_names.append(folder_name)
                                    full_path = os.path.join(root, path) if not os.path.isabs(path) else path
                                    node_info['FullPaths'].append(full_path)
                                    if os.path.exists(full_path):
                                        for model_file in os.listdir(full_path):
                                            if any(model_file.endswith(ext) for ext in extensions):
                                                model_full_path = os.path.join(full_path, model_file)
                                                size_mb = os.path.getsize(model_full_path) / (1024 * 1024)
                                                node_info['Available_models'].append((model_file, size_mb))
                                node_info['FolderNames'] = folder_names
                                results.append(node_info)
                except Exception as e:
                    print(f"{Fore.RED}Error processing file {file_path}: {e}")

    for node_info in results:
        print(f"\n{Fore.GREEN}Node: {node_info['Node']}")
        print(f"{Fore.YELLOW}Key: {node_info['Key']}")
        print(f"{Fore.CYAN}Paths: {node_info['FolderNames']}")
        print(f"{Fore.CYAN}Full Paths: {node_info['FullPaths']}")
        print(f"{Fore.MAGENTA}Extensions: {node_info['Extensions']}")
        print(f"{Fore.BLUE}Available models:")
        if node_info['Available_models']:
            for model_file, size_mb in node_info['Available_models']:
                print(f" - {model_file} ({size_mb:.2f} MB)")
        else:
            print(f" - No models found")
        print(f"{Style.DIM}---------------------------------------{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
