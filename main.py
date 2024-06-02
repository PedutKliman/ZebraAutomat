import tkinter as tk
import random

def initialize_matrix():
    """
    Initialize Matrix:
    Create an 80x80 matrix with random binary values (0 or 1).

    Returns:
    matrix (list of lists): An 80x80 matrix with random binary values.
    """
    matrix = []
    for _ in range(80):
        row = [random.randint(0, 1) for _ in range(80)]
        matrix.append(row)
    return matrix

class AutomatonGUI(tk.Tk):
    """
    Automaton GUI:
    Represents the graphical user interface for the cellular automaton simulation.

    Attributes:
    canvas (tk.Canvas): The canvas widget for displaying the matrix.
    matrix (list of lists): The current state of the cellular automaton.
    running (bool): Flag indicating whether the simulation is running.
    iteration (int): Current iteration/generation of the simulation.
    cell_width (int): Width of each cell in pixels.
    cell_height (int): Height of each cell in pixels.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the GUI:
        Setup the GUI components and initial state of the simulation.
        """
        super().__init__(*args, **kwargs)

        # Create canvas for displaying the matrix
        self.canvas = tk.Canvas(self, width=640, height=640, bg="white")
        self.canvas.pack()

        # Initialize matrix and simulation parameters
        self.matrix = initialize_matrix()
        self.running = False
        self.iteration = 0

        # Define cell dimensions
        self.cell_width = 640 // 80
        self.cell_height = 640 // 80

        # Draw initial matrix
        self.draw_matrix()
        print("hahah")
        # Create buttons and labels
        self.button_start = tk.Button(self, text="Start", command=self.start_simulation)
        self.button_start.pack()

        self.button_stop = tk.Button(self, text="Stop", command=self.stop_simulation)
        self.button_stop.pack()

        self.label_iterations = tk.Label(self, text=f"Generations: {self.iteration}")
        self.label_iterations.pack()

        self.label_zebra_score = tk.Label(self, text="Zebra Score: 0")
        self.label_zebra_score.pack()

    def draw_matrix(self):
        """
        Draw Matrix:
        Draw the current state of the matrix on the canvas.
        """
        self.canvas.delete("cells")
        for y in range(80):
            for x in range(80):
                x_left = x * self.cell_width
                x_right = x_left + self.cell_width
                y_up = y * self.cell_height
                y_down = y_up + self.cell_height
                if self.matrix[y][x] == 1:
                    self.canvas.create_rectangle(x_left, y_up, x_right, y_down, fill="black", tags="cells")
                else:
                    self.canvas.create_rectangle(x_left, y_up, x_right, y_down, fill="white", outline="gray",
                                                 tags="cells")

    def start_simulation(self):
        """
        Start Simulation:
        Begin running the cellular automaton simulation.
        """
        if not self.running:
            self.running = True
            self.run_simulation()

    def stop_simulation(self):
        """
        Stop Simulation:
        Stop the currently running simulation.
        """
        self.running = False

    def run_simulation(self):
        """
        Run Simulation:
        Execute one step of the cellular automaton simulation.
        """
        if self.running:
            new_matrix = []
            for y in range(80):
                new_row = []
                for x in range(80):
                    z = self.get_new_state(x, y)
                    new_row.append(z)
                new_matrix.append(new_row)
            self.matrix = new_matrix
            self.iteration += 1
            self.label_iterations.config(text=f"Generations: {self.iteration}")
            self.draw_matrix()
            zebra_score = self.calculate_zebra_score()
            self.label_zebra_score.config(text=f"Zebra Score: {zebra_score:.2f}")
            self.after(300, self.run_simulation)

    def get_new_state(self, x, y):
        """
        Get New State:
        Calculate the new state of a cell based on its neighbors.

        Args:
        x (int): X-coordinate of the cell.
        y (int): Y-coordinate of the cell.

        Returns:
        int: The new state of the cell (0 or 1).
        """
        left = (x - 1) % 80
        right = (x + 1) % 80
        up = (y - 1) % 80
        down = (y + 1) % 80
        # sides
        if self.matrix[y][right] == 0 and self.matrix[y][left] == 0:
            return 1
        elif self.matrix[y][right] == 1 and self.matrix[y][left] == 1:
            return 0
        #up and down
        elif self.matrix[up][x] == 1 and self.matrix[down][x] == 1:
            return 1
        elif self.matrix[up][x] == 0 and self.matrix[down][x] == 0:
             return 0
        #slants
        elif self.matrix[down][right] == 0 and self.matrix[up][left] == 0:
            return 1
        elif self.matrix[down][right] == 1 and self.matrix[up][left] == 1:
            return 0
        elif self.matrix[up][right] == 0 and self.matrix[down][left] == 0:
            return 1
        elif self.matrix[up][right] == 1 and self.matrix[down][left] == 1:
            return 0
        else:
            return random.randint(0, 1)

    def calculate_zebra_score(self):
        """
        Calculate Zebra Score:
        Calculate the zebra score of the current matrix.

        Returns:
        float: The calculated zebra score.
        """
        continuity_score = 0
        alternation_score = 0
        for x in range(80):
            count_row = 0
            count_col = 0
            for y in range(80):
                left = (x - 1) % 80
                right = (x + 1) % 80
                up = (y - 1) % 80
                down = (y + 1) % 80
                #calculate per row
                if self.matrix[y][x] != self.matrix[y][left] and self.matrix[y][x] != self.matrix[y][right]:
                    count_row += 1
                #calculate per column
                if self.matrix[y][x] == self.matrix[down][x] and self.matrix[y][x] == self.matrix[up][x]:
                    count_col += 1
            continuity_score += count_col / 80
            alternation_score += count_row / 80
        alternation_score /= 79
        continuity_score /= 80
        zebra_score = (continuity_score + 2*alternation_score) / 3
        return zebra_score

if __name__ == "__main__":
    app = AutomatonGUI()
    app.mainloop()