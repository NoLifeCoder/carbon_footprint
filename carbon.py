import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CarbonFootprintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carbon Footprint Application")
        self.root.geometry("1700x800")

        self.average_values = {
            "electricity": 1100,
            "natural_gas": 800,
            "fuel": 300,
            "waste": 50,
            "business_km": 5000,
            "fuel_efficiency": 9
        }

        # Create input and graph frames
        self.create_input_frame()
        self.create_graph_tabs()

   ## this methode to create input component
    def create_input_frame(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.inputs = {}

        # Input fields (2 per row)
        self.create_input_row("Electricity Bill (euros/month):", "electricity", 0, 0)
        self.create_input_row("Natural Gas Bill (euros/month):", "natural_gas", 0, 1)
        self.create_input_row("Transportation Fuel Bill (euros/month):", "fuel", 1, 0)
        self.create_input_row("Waste (kg/month):", "waste", 1, 1)
        self.create_input_row("Recycled/Composted Waste (%):", "recycled", 2, 0)
        self.create_input_row("Business Travel Distance (km/year):", "business_km", 2, 1)
        self.create_input_row("Vehicle Fuel Efficiency (L/100km):", "fuel_efficiency", 3, 0)

        # Submit Button, this will generate a PDF report, in the reports folder
        self.submit_btn = tk.Button(self.input_frame, text="Generate PDF Report", command=self.handle_submit)
        self.submit_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Result Label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), justify="left")
        self.result_label.pack(pady=10)

    def create_input_row(self, label_text, key, row, column):
        frame = tk.Frame(self.input_frame)
        frame.grid(row=row, column=column, padx=10, pady=5, sticky="w")

        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)
        self.inputs[key] = entry

    def create_graph_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        # Bar Graph Tab
        self.bar_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.bar_tab, text="Bar Graph")

        # Pie Chart Tab
        self.pie_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.pie_tab, text="Pie Chart")

        self.tab_control.pack(fill=tk.BOTH, expand=True)

    def handle_submit(self):
        try:
            data = {key: float(entry.get()) for key, entry in self.inputs.items()}
            self.validate_inputs(data)
            self.calculate_emissions(data)
            self.generate_report(data)
            self.update_graphs(data)
            self.display_results(data)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")

    def validate_inputs(self, data):
        if any(value < 0 for value in data.values()):
            raise ValueError("Inputs must be non-negative.")
    ##Calculate CO2 emissions based on inputs."""
    def calculate_emissions(self, data):
       
        data["electricity_emissions"] = data["electricity"] * 12 * 0.0005
        data["natural_gas_emissions"] = data["natural_gas"] * 12 * 0.0053
        data["fuel_emissions"] = data["fuel"] * 12 * 2.32
        data["waste_emissions"] = data["waste"] * 12 * (0.57 - data["recycled"] / 100)
        data["business_travel_emissions"] = data["business_km"] * (1 / data["fuel_efficiency"]) * 2.31

    def generate_report(self, data):
        """Generate a PDF report."""
        if not os.path.exists('reports'):
            os.makedirs('reports')

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Carbon Footprint Report')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)

        for key in ["electricity", "natural_gas", "fuel", "waste", "business_km"]:
            pdf.cell(40, 10, f"{key.replace('_', ' ').capitalize()} Consumption: {data[key]}")
            pdf.ln(10)

        pdf.cell(40, 10, f"Total Emissions (kgCO2): {sum([data[k] for k in data if '_emissions' in k]):.2f}")
        pdf.output('reports/carbon_footprint_report.pdf')

    def update_graphs(self, data):
        """Update the graphs in the tabs."""
        self.show_bar_graph(data)
        self.show_pie_chart(data)

    def show_bar_graph(self, data):
        """Show a bar graph comparing consumed and average values."""
        labels = ["Electricity", "Natural Gas", "Fuel", "Waste", "Business Travel"]
        consumed = [data["electricity"], data["natural_gas"], data["fuel"], data["waste"], data["business_km"]]
        average = [self.average_values["electricity"], self.average_values["natural_gas"], 
                   self.average_values["fuel"], self.average_values["waste"], self.average_values["business_km"]]

        fig, ax = plt.subplots()
        x = range(len(labels))
        ax.bar(x, consumed, width=0.4, label='Consumed', align='center')
        ax.bar([i + 0.4 for i in x], average, width=0.4, label='Average', align='center')

        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")
        ax.set_title("Consumed vs Average")
        ax.set_xticks([i + 0.2 for i in x])
        ax.set_xticklabels(labels)
        ax.legend()

        for widget in self.bar_tab.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, self.bar_tab)
        canvas.get_tk_widget().pack()
        plt.close(fig)

    def show_pie_chart(self, data):
        """Show a pie chart of consumed values."""
        labels = ["Electricity", "Natural Gas", "Fuel", "Waste", "Business Travel"]
        sizes = [data["electricity_emissions"], data["natural_gas_emissions"], data["fuel_emissions"], 
                 data["waste_emissions"], data["business_travel_emissions"]]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        for widget in self.pie_tab.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, self.pie_tab)
        canvas.get_tk_widget().pack()
        plt.close(fig)

    def display_results(self, data):
        result_text = "Carbon Footprint Results:\n\n"

        for key in ["electricity", "natural_gas", "fuel", "waste", "business_km"]:
            avg = self.average_values[key]
            value = data[key]
            emissions_key = f"{key}_emissions"
            emissions = data[emissions_key]
            result_text += (f"{key.replace('_', ' ').capitalize()}:\n"
                            f" - Consumed: {value}\n"
                            f" - Average: {avg}\n"
                            f" - Emissions (kgCO2): {emissions:.2f}\n")
            if value > avg:
                result_text += f"   * Your {key.replace('_', ' ')} exceeds the average.\n"
            else:
                result_text += f"   * Your {key.replace('_', ' ')} is within the average.\n"
            result_text += "\n"

        total_emissions = sum([data[k] for k in data if "_emissions" in k])
        result_text += f"Total Emissions (kgCO2): {total_emissions:.2f}\n"

        self.result_label.config(text=result_text)

def main():
    root = tk.Tk()
    app = CarbonFootprintApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
