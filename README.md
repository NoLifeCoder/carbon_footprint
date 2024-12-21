# Carbon Footprint Application

## Overview
This Carbon Footprint Application allows users to input their energy consumption, water usage, and waste production. It generates a report with suggestions on how to reduce their carbon footprint. The tool includes a graphical user interface (GUI) created using Tkinter and generates a pie chart as part of the report.

## Features
- Input fields for energy consumption, water usage, and waste production.
- Exception handling for invalid inputs with visual feedback.
- PDF report generation with a pie chart.
- Comparison with average values for each component (energy, water, waste).
- GUI messages indicating whether the user exceeds the average carbon footprint.

## Requirements
- Python 3.x
- `tkinter`
- `fpdf`
- `matplotlib`

## Installation
1. Clone the repository to your local machine.
    ```sh
    git clone https://github.com/NoLifeCoder/carbon_footprint.git
    ```
2. Navigate to the project directory.
    ```sh
    cd <project-directory>
    ```
3. Install the required Python packages.
    ```sh
    pip install fpdf matplotlib
    ```

## Running the Application
1. Open a terminal or command prompt and navigate to the project directory.
2. Run the application using Python.
    ```sh
    python main.py
    ```
3. The GUI will appear, allowing you to input your data and generate the report.

## Required Imports
The following Python packages are required for this application, it's included in the requirments.txt file:
```python
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
