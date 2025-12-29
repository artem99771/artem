import tkinter as tk
from tkinter import ttk, messagebox
import math

class ThermalNetworkCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Гидравлический расчет тепловой сети")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Create title
        title_label = ttk.Label(self.main_frame, text="Гидравлический расчет тепловой сети", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create input fields
        self.create_input_fields()
        
        # Create calculate button
        self.calc_button = ttk.Button(self.main_frame, text="Рассчитать", command=self.calculate)
        self.calc_button.grid(row=10, column=0, columnspan=2, pady=20)
        
        # Create result frame
        self.result_frame = ttk.LabelFrame(self.main_frame, text="Результаты расчета", padding="10")
        self.result_frame.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.result_frame.columnconfigure(0, weight=1)
        
        # Result labels
        self.result_text = tk.Text(self.result_frame, height=10, width=70, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Create menu
        self.create_menu()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистить", command=self.clear_fields)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_input_fields(self):
        # Parameters frame
        params_frame = ttk.LabelFrame(self.main_frame, text="Входные параметры", padding="10")
        params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Flow rate
        ttk.Label(params_frame, text="Расход теплоносителя (м³/ч):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.flow_rate_var = tk.DoubleVar(value=100.0)
        self.flow_rate_entry = ttk.Entry(params_frame, textvariable=self.flow_rate_var, width=20)
        self.flow_rate_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Pipe diameter
        ttk.Label(params_frame, text="Диаметр трубы (мм):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.diameter_var = tk.DoubleVar(value=200.0)
        self.diameter_entry = ttk.Entry(params_frame, textvariable=self.diameter_var, width=20)
        self.diameter_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Pipe length
        ttk.Label(params_frame, text="Длина участка (м):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.DoubleVar(value=100.0)
        self.length_entry = ttk.Entry(params_frame, textvariable=self.length_var, width=20)
        self.length_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Pipe roughness
        ttk.Label(params_frame, text="Шероховатость трубы (мм):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.roughness_var = tk.DoubleVar(value=0.5)
        self.roughness_entry = ttk.Entry(params_frame, textvariable=self.roughness_var, width=20)
        self.roughness_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Temperature
        ttk.Label(params_frame, text="Температура теплоносителя (°C):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.temp_var = tk.DoubleVar(value=95.0)
        self.temp_entry = ttk.Entry(params_frame, textvariable=self.temp_var, width=20)
        self.temp_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Additional parameters
        additional_frame = ttk.LabelFrame(self.main_frame, text="Дополнительные параметры", padding="10")
        additional_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Local resistance coefficients
        ttk.Label(additional_frame, text="Коэффициенты местных сопротивлений:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.local_resistance_var = tk.DoubleVar(value=2.0)
        self.local_resistance_entry = ttk.Entry(additional_frame, textvariable=self.local_resistance_var, width=20)
        self.local_resistance_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Number of bends
        ttk.Label(additional_frame, text="Количество поворотов:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bends_var = tk.IntVar(value=5)
        self.bends_entry = ttk.Entry(additional_frame, textvariable=self.bends_var, width=20)
        self.bends_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Number of fittings
        ttk.Label(additional_frame, text="Количество арматуры:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.fittings_var = tk.IntVar(value=3)
        self.fittings_entry = ttk.Entry(additional_frame, textvariable=self.fittings_var, width=20)
        self.fittings_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Configure column weights for responsive design
        params_frame.columnconfigure(1, weight=1)
        additional_frame.columnconfigure(1, weight=1)
    
    def calculate(self):
        try:
            # Get input values
            flow_rate = self.flow_rate_var.get()  # м³/ч
            diameter = self.diameter_var.get() / 1000  # Convert mm to m
            length = self.length_var.get()  # m
            roughness = self.roughness_var.get() / 1000  # Convert mm to m
            temp = self.temp_var.get()  # °C
            local_resistance = self.local_resistance_var.get()
            bends = self.bends_var.get()
            fittings = self.fittings_var.get()
            
            # Physical properties of water at given temperature
            density, viscosity = self.get_water_properties(temp)
            
            # Calculate velocity
            area = math.pi * (diameter / 2) ** 2
            velocity = (flow_rate / 3600) / area  # Convert m³/h to m³/s then to m/s
            
            # Calculate Reynolds number
            reynolds = (velocity * diameter) / viscosity
            
            # Calculate friction factor using Colebrook equation (approximated with Swamee-Jain)
            friction_factor = self.calculate_friction_factor(reynolds, roughness, diameter)
            
            # Calculate pressure losses
            linear_losses = friction_factor * (length / diameter) * (density * velocity ** 2) / 2
            local_losses = local_resistance * (density * velocity ** 2) / 2
            total_losses = linear_losses + local_losses
            
            # Additional losses from bends and fittings
            bend_loss_coeff = 0.3 * bends  # Typical loss coefficient per bend
            fitting_loss_coeff = 0.8 * fittings  # Typical loss coefficient per fitting
            additional_losses = (bend_loss_coeff + fitting_loss_coeff) * (density * velocity ** 2) / 2
            total_losses_with_additions = total_losses + additional_losses
            
            # Calculate flow regime
            if reynolds < 2300:
                flow_regime = "Ламинарный"
            elif reynolds < 4000:
                flow_regime = "Переходный"
            else:
                flow_regime = "Турбулентный"
            
            # Display results
            result_text = f"""ГИДРАВЛИЧЕСКИЙ РАСЧЕТ ТЕПЛОВОЙ СЕТИ

Входные параметры:
- Расход теплоносителя: {flow_rate:.2f} м³/ч
- Диаметр трубы: {diameter*1000:.1f} мм
- Длина участка: {length:.1f} м
- Шероховатость трубы: {roughness*1000:.2f} мм
- Температура теплоносителя: {temp:.1f} °C
- Количество поворотов: {bends}
- Количество арматуры: {fittings}

Результаты расчета:
- Плотность воды: {density:.2f} кг/м³
- Кинематическая вязкость: {viscosity:.2e} м²/с
- Средняя скорость: {velocity:.3f} м/с
- Число Рейнольдса: {reynolds:.0f}
- Режим течения: {flow_regime}
- Коэффициент трения: {friction_factor:.4f}

Потери давления:
- Линейные потери: {linear_losses:.2f} Па
- Местные потери: {local_losses:.2f} Па
- Потери на повороты: {bend_loss_coeff * (density * velocity ** 2) / 2:.2f} Па
- Потери на арматуру: {fitting_loss_coeff * (density * velocity ** 2) / 2:.2f} Па
- Общие потери давления: {total_losses_with_additions:.2f} Па
- Общие потери давления: {total_losses_with_additions / 1000:.2f} кПа
- Общие потери давления: {total_losses_with_additions / 10000:.2f} м.в.ст.

Дополнительная информация:
- Эквивалентная длина местных сопротивлений: {(local_resistance * diameter / friction_factor):.2f} м
- Суммарная эквивалентная длина: {length + local_resistance * diameter / friction_factor:.2f} м
"""
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result_text)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при расчете: {str(e)}")
    
    def get_water_properties(self, temp):
        """Calculate water density and kinematic viscosity based on temperature"""
        # Simplified formulas for water properties
        # Density in kg/m³
        density = 999.842594 + 6.793952e-2 * temp - 9.095290e-3 * temp**2 + 1.001685e-4 * temp**3 - 1.120083e-6 * temp**4 + 6.536332e-9 * temp**5
        
        # Dynamic viscosity in Pa·s
        dynamic_viscosity = 1.79e-3 / (1 + 0.03369 * temp + 0.000221 * temp**2)
        
        # Kinematic viscosity in m²/s
        kinematic_viscosity = dynamic_viscosity / density
        
        return density, kinematic_viscosity
    
    def calculate_friction_factor(self, reynolds, roughness, diameter):
        """Calculate friction factor using Swamee-Jain approximation of Colebrook equation"""
        if reynolds < 2300:
            # Laminar flow
            return 64 / reynolds
        else:
            # Turbulent flow - Swamee-Jain approximation
            relative_roughness = roughness / diameter
            friction_factor = 0.25 / (math.log10(
                (relative_roughness / 3.7) + (5.74 / (reynolds**0.9))
            ))**2
            return friction_factor
    
    def clear_fields(self):
        """Clear all input fields and results"""
        self.flow_rate_var.set(100.0)
        self.diameter_var.set(200.0)
        self.length_var.set(100.0)
        self.roughness_var.set(0.5)
        self.temp_var.set(95.0)
        self.local_resistance_var.set(2.0)
        self.bends_var.set(5)
        self.fittings_var.set(3)
        self.result_text.delete(1.0, tk.END)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Гидравлический расчет тепловой сети

Программа для выполнения гидравлического расчета тепловых сетей.
Рассчитывает потери давления на трение и местные сопротивления.

Версия: 1.0
Разработчик: Thermal Network Calculator
Год: 2025"""
        messagebox.showinfo("О программе", about_text)

def main():
    root = tk.Tk()
    app = ThermalNetworkCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()