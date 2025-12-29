#!/usr/bin/env python3
"""
Installation script for Thermal Network Calculator
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Проверка зависимостей...")
    
    # Check if tkinter is available
    try:
        import tkinter
        print("✓ Tkinter установлен")
    except ImportError:
        print("✗ Tkinter не установлен")
        return False
    
    # Check if ttk is available
    try:
        from tkinter import ttk
        print("✓ Tkinter.ttk установлен")
    except ImportError:
        print("✗ Tkinter.ttk не установлен")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Установка зависимостей...")
    
    try:
        # For systems where tkinter needs to be installed separately
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinter"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Tkinter установлен")
    except subprocess.CalledProcessError:
        print("! Не удалось установить tkinter напрямую, проверьте системную установку")
    
    # Tkinter is usually included with Python, so we mainly need to check for it

def main():
    print("Установка программы гидравлического расчета тепловой сети...")
    print("=" * 50)
    
    # Check dependencies
    if check_dependencies():
        print("✓ Все зависимости установлены")
    else:
        print("Установка недостающих зависимостей...")
        install_dependencies()
        
        # Check again after installation
        if not check_dependencies():
            print("✗ Установка не завершена успешно. Проверьте зависимости вручную.")
            return 1
    
    print("=" * 50)
    print("Установка завершена!")
    print("Для запуска программы выполните:")
    print(f"  python3 {os.path.join(os.getcwd(), 'thermal_network_calculator.py')}")
    print("")
    print("Или используйте ярлык:")
    print(f"  {os.path.join(os.getcwd(), 'thermal_network_calculator.desktop')}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())