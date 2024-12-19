import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os

class CarbonFootprintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carbon Footprint Monitoring Tool")
        self.root.geometry("500x400")

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
        # Suggestions can be added here
        pdf.output('reports/carbon_footprint_report.pdf')

def main():
    root = tk.Tk()
    app = CarbonFootprintApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
