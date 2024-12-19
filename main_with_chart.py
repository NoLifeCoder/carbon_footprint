import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CarbonFootprintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carbon Footprint Monitoring Tool")
        self.root.geometry("1300x700")  # Further increased GUI size

        # Average values for each component (example values)
        self.average_energy = 1200
        self.average_water = 1500
        self.average_waste = 300

        # Input Labels and Fields
        self.createLabel("Energy Consumption (kWh):", 30, 50)
        self.energy_input = self.createEntry(250, 50)

        self.createLabel("Water Usage (liters):", 30, 100)
        self.water_input = self.createEntry(250, 100)

        self.createLabel("Waste Produced (kg):", 30, 150)
        self.waste_input = self.createEntry(250, 150)

        # Submit Button
        self.submit_btn = tk.Button(self.root, text="Generate Report", command=self.handleSubmit)
        self.submit_btn.place(x=200, y=250)

        # Result Label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left")
        self.result_label.place(x=30, y=300)

        # Pie Chart Placeholder
        self.chart = None

    def createLabel(self, text, x, y):
        label = tk.Label(self.root, text=text)
        label.place(x=x, y=y)

    def createEntry(self, x, y):
        entry = tk.Entry(self.root)
        entry.place(x=x, y=y)
        return entry

    def handleSubmit(self):
        valid = True
        try:
            energy = float(self.energy_input.get())
            self.resetColor(self.energy_input)
        except ValueError:
            self.highlightError(self.energy_input)
            valid = False

        try:
            water = float(self.water_input.get())
            self.resetColor(self.water_input)
        except ValueError:
            self.highlightError(self.water_input)
            valid = False

        try:
            waste = float(self.waste_input.get())
            self.resetColor(self.waste_input)
        except ValueError:
            self.highlightError(self.waste_input)
            valid = False

        if valid:
            self.generateReport(energy, water, waste)
            self.showPieChart(energy, water, waste)
            self.displayResult(energy, water, waste)

    def highlightError(self, widget):
        widget.configure(bg='red')

    def resetColor(self, widget):
        widget.configure(bg='white')

    def generateReport(self, energy, water, waste):
        if not os.path.exists('reports'):
            os.makedirs('reports')

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Carbon Footprint Report')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.cell(40, 10, f'Energy Consumption: {energy} kWh')
        pdf.ln(10)
        pdf.cell(40, 10, f'Water Usage: {water} liters')
        pdf.ln(10)
        pdf.cell(40, 10, f'Waste Produced: {waste} kg')
        # Adding the pie chart
        pdf.image('chart.png', x=10, y=60, w=100)
        pdf.output('reports/carbon_footprint_report.pdf')

    def showPieChart(self, energy, water, waste):
        labels = 'Energy', 'Water', 'Waste'
        sizes = [energy, water, waste]
        colors = ['#ff9999','#66b3ff','#99ff99']
        explode = (0.1, 0, 0)  # explode the 1st slice

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.savefig('chart.png')  # Save the chart as an image

        # Display the chart in the Tkinter window
        if self.chart:
            self.chart.get_tk_widget().destroy()
        self.chart = FigureCanvasTkAgg(fig1, self.root)
        self.chart.get_tk_widget().place(x=550, y=50)
        plt.close(fig1)

    def displayResult(self, energy, water, waste):
        result_text = (f"Energy Consumption: {energy} kWh\n"
                       f"- Average: {self.average_energy} kWh\n"
                       f"Water Usage: {water} liters\n"
                       f"- Average: {self.average_water} liters\n"
                       f"Waste Produced: {waste} kg\n"
                       f"- Average: {self.average_waste} kg\n\n")

        if energy > self.average_energy:
            result_text += "Your energy consumption exceeds the average family consumption.\n"
        else:
            result_text += "Your energy consumption is within the average family consumption.\n"

        if water > self.average_water:
            result_text += "Your water usage exceeds the average family usage.\n"
        else:
            result_text += "Your water usage is within the average family usage.\n"

        if waste > self.average_waste:
            result_text += "Your waste production exceeds the average family production.\n"
        else:
            result_text += "Your waste production is within the average family production.\n"

        self.result_label.config(text=result_text)

def main():
    root = tk.Tk()
    app = CarbonFootprintApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
