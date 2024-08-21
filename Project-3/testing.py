import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class SmartIrrigationSystem:
    def __init__(self, dataset):
        self.dataset = dataset
        self.current_index = 0
        self.water_used = 0
        self.history = []

    def get_sensor_data(self):
        self.n = self.dataset['N'][self.current_index]
        self.p = self.dataset['P'][self.current_index]
        self.k = self.dataset['K'][self.current_index]
        self.temperature = self.dataset['temperature'][self.current_index]
        self.humidity = self.dataset['humidity'][self.current_index]
        self.ph = self.dataset['ph'][self.current_index]
        self.rainfall = self.dataset['rainfall'][self.current_index]
        self.current_index += 1

    def analyze_data(self):
        if self.n < 80 or self.p < 40 or self.k < 40 or self.temperature < 20 or self.temperature > 25 or self.humidity < 75 or self.ph < 6.5 or self.ph > 7.5 or self.rainfall < 200:
            return True
        return False

    def irrigate(self):
        water_amount = 50  # Adjust the water amount based on the data
        print(f"Irrigating at index {self.current_index} with {water_amount:.2f} units of water")
        self.water_used += water_amount

    def run_simulation(self):
        while self.current_index < len(self.dataset):
            self.get_sensor_data()
            if self.analyze_data():
                self.irrigate()
            
            self.history.append({
                'index': self.current_index,
                'n': self.n,
                'p': self.p,
                'k': self.k,
                'temperature': self.temperature,
                'humidity': self.humidity,
                'ph': self.ph,
                'rainfall': self.rainfall,
                'water_used': self.water_used
            })
            
            print(f"Index: {self.history[-1]['index']}")
            print(f"N: {self.n:.2f}")
            print(f"P: {self.p:.2f}")
            print(f"K: {self.k:.2f}")
            print(f"Temperature: {self.temperature:.2f}°C")
            print(f"Humidity: {self.humidity:.2f}%")
            print(f"pH: {self.ph:.2f}")
            print(f"Rainfall: {self.rainfall:.2f} mm")
            print(f"Total Water Used: {self.water_used:.2f} units")
            print("--------------------")

    def plot_data(self):
        indices = [entry['index'] for entry in self.history]
        n = [entry['n'] for entry in self.history]
        p = [entry['p'] for entry in self.history]
        k = [entry['k'] for entry in self.history]
        temperature = [entry['temperature'] for entry in self.history]
        humidity = [entry['humidity'] for entry in self.history]
        ph = [entry['ph'] for entry in self.history]
        rainfall = [entry['rainfall'] for entry in self.history]
        water_used = [entry['water_used'] for entry in self.history]

        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(4, 2, figsize=(15, 20))
        
        ax1.plot(indices, n, label='N')
        ax1.set_ylabel('N')
        ax1.set_title('Nitrogen Over Time')
        ax1.legend()

        ax2.plot(indices, p, label='P', color='red')
        ax2.set_ylabel('P')
        ax2.set_title('Phosphorus Over Time')
        ax2.legend()

        ax3.plot(indices, k, label='K', color='green')
        ax3.set_ylabel('K')
        ax3.set_title('Potassium Over Time')
        ax3.legend()

        ax4.plot(indices, temperature, label='Temperature', color='orange')
        ax4.set_ylabel('Temperature (°C)')
        ax4.set_title('Temperature Over Time')
        ax4.legend()

        ax5.plot(indices, humidity, label='Humidity', color='purple')
        ax5.set_ylabel('Humidity (%)')
        ax5.set_title('Humidity Over Time')
        ax5.legend()

        ax6.plot(indices, ph, label='pH', color='brown')
        ax6.set_ylabel('pH')
        ax6.set_title('pH Over Time')
        ax6.legend()

        ax7.plot(indices, rainfall, label='Rainfall', color='blue')
        ax7.set_ylabel('Rainfall (mm)')
        ax7.set_title('Rainfall Over Time')
        ax7.legend()

        ax8.plot(indices, water_used, label='Water Used', color='gray')
        ax8.set_xlabel('Index')
        ax8.set_ylabel('Water Used (units)')
        ax8.set_title('Cumulative Water Usage')
        ax8.legend()

        plt.tight_layout()
        plt.show()

# Load the dataset
dataset = pd.read_csv('Crop_recommendation.csv')

# Run simulation
smart_system = SmartIrrigationSystem(dataset)
smart_system.run_simulation()
smart_system.plot_data()