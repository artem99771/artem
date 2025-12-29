#!/usr/bin/env python3
"""
Launcher script for Thermal Network Calculator
"""

import sys
import os
from thermal_network_calculator import main

def run():
    """Run the thermal network calculator application"""
    print("Запуск программы гидравлического расчета тепловой сети...")
    print("Thermal Network Hydraulic Calculator")
    print("Версия: 1.0")
    print("-" * 40)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка при запуске программы: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()