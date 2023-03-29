import tkinter as tk
import numpy as np
from scipy.stats import pearsonr

class CorrelationGUI:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack()

        # Draw axes and labels
        x_axis = self.canvas.create_line(0, 250, 500, 250, width=2)
        y_axis = self.canvas.create_line(250, 0, 250, 500, width=2)
        for i in range(-10, 11):
            x_pos = 250 + i * 25
            y_pos = 250 + i * 25
            x_label = self.canvas.create_text(x_pos, 260, text=str(i), font=('Arial', 12))
            y_label = self.canvas.create_text(260, y_pos, text=str(-i), font=('Arial', 12))

        # Bind mouse events and set cursor
        self.canvas.bind('<Motion>', self.on_motion)
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        self.canvas.configure(cursor='crosshair')

        # Initialize coordinates and line ID
        self.line_id = None
        self.coords = []

        # Create label for displaying correlation
        self.label = tk.Label(self.master, text='Correlation: 0.00')
        self.label.pack()

        # Create button for calculating correlation
        self.correlation_button = tk.Button(self.master, text='Calculate Correlation',
                                             command=self.update_correlation, state=tk.DISABLED)
        self.correlation_button.pack()

        # Create button for refreshing canvas
        self.refresh_button = tk.Button(self.master, text='Refresh', command=self.refresh_canvas)
        self.refresh_button.pack()

    def on_motion(self, event):
        if self.line_id is not None:
            # Adjust the coordinates to take into account the position of the origin
            x = event.x - 250
            y = 250 - event.y

            # Add a new point to the line
            self.coords.extend([x, y])
            self.canvas.coords(self.line_id, *(c+250 if i%2==0 else 250-c for i,c in enumerate(self.coords)))

    def on_button_press(self, event):
        if self.line_id is None:
            # Adjust the coordinates to take into account the position of the origin
            x = event.x - 250
            y = 250 - event.y

            # Create a new line with the start point
            self.coords = [x, y]
            self.line_id = self.canvas.create_line(*(c+250 if i%2==0 else 250-c for i,c in enumerate(self.coords)),
                                                    *(c+250 if i%2==0 else 250-c for i,c in enumerate(self.coords)), tags='line')

    def on_button_release(self, event):
        # Enable correlation button and reset coordinates and line ID
        self.correlation_button.config(state=tk.NORMAL)
        self.coords = []
        self.line_id = None


    def refresh_canvas(self):
        # Clear the canvas and disable correlation button
        self.canvas.delete('line')
        self.canvas.delete('label')
        self.correlation_button.config(state=tk.DISABLED)

    def update_correlation(self):
        # Disable correlation button
        self.correlation_button.config(state=tk.DISABLED)

        # Get all lines on the canvas and calculate correlation
        lines = self.canvas.find_withtag('line')
        x = []
        y = []
        for line in lines:
            coords = self.canvas.coords(line)
            for i in range(0, len(coords), 2):
                x.append(coords[i] - 250)
                y.append(250 - coords[i+1])
        corr = calculate_correlation(x, y)
        self.label.config(text='Correlation: {:.2f}'.format(corr))

def calculate_correlation(x, y):
    if len(x) < 2 or len(y) < 2:
        return 0
    corr, _ = pearsonr(x, y)
    return corr

