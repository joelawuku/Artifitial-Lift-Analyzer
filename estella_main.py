import sys
import traceback
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel, QComboBox, \
    QPushButton, QFrame, QTextEdit, QLineEdit, QHBoxLayout, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ArtificialLiftInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Artificial Lift Method Analyzer")

        # Create the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create the tab widget
        self.tab_widget = QTabWidget(self.central_widget)
        self.layout.addWidget(self.tab_widget)

        # Create the "Criteria" tab
        self.criteria_tab = QWidget()
        self.tab_widget.addTab(self.criteria_tab, "Criteria")
        self.criteria_layout = QHBoxLayout(self.criteria_tab)

        # Create and add the input frame
        self.input_frame = self.create_input_frame()
        self.criteria_layout.addWidget(self.input_frame)

        # Create and add the Production, Reservoir, and Well Properties frame
        self.properties_frame = self.create_properties_frame()
        self.criteria_layout.addWidget(self.properties_frame)

        # Create and add the Surface Infrastructure frame
        self.infrastructure_frame = self.create_infrastructure_frame()
        self.criteria_layout.addWidget(self.infrastructure_frame)

        # Create the start button and the clear button
        self.start_button = QPushButton("Predict", self.central_widget)
        self.start_button.clicked.connect(self.predict_lift_method)

        self.clear_button = QPushButton("Clear", self.central_widget)
        self.clear_button.clicked.connect(self.clear_inputs)

        self.set_button_styles()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.clear_button)
        self.layout.addLayout(button_layout)

        # Create the output frame
        self.output_frame = QFrame(self.central_widget)
        self.output_frame.setFrameShape(QFrame.StyledPanel)
        self.layout.addWidget(self.output_frame)
        self.output_layout = QVBoxLayout(self.output_frame)

        self.output_label = QLabel("Prediction:")
        self.output_layout.addWidget(self.output_label)

        # Create the text box for displaying the output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setCurrentFont(QFont("Arial", 12, QFont.Bold))
        self.output_text.setTextColor(Qt.darkRed)
        self.output_layout.addWidget(self.output_text)

        # Create the "Results" tab
        self.results_tab = QWidget()
        self.tab_widget.addTab(self.results_tab, "Results")
        self.results_layout = QHBoxLayout(self.results_tab)

        # Create the table to display the results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)  # Add one more column for the performance score
        self.results_table.setHorizontalHeaderLabels(["ALS", "PIS", "NIS", "PS"])
        self.results_layout.addWidget(self.results_table)

        # Create the bar chart
        self.figure = Figure()
        self.bar_chart = self.figure.add_subplot(111)
        self.bar_chart.set_ylabel("Performance Score (PS)")
        self.bar_chart.set_xlabel("Artificial Lift System (ALS)")

        # Add the bar chart to a canvas and display it in the results tab
        self.canvas = FigureCanvas(self.figure)
        self.results_layout.addWidget(self.canvas)

    def create_input_frame(self):
        self.input_frame = QFrame(self.central_widget)
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.layout.addWidget(self.input_frame)
        self.input_layout = QFormLayout(self.input_frame)

        self.input_label = QLabel("Produced Fluid Properties \n")
        self.input_layout.addRow(self.input_label)

        # Create the line edits and combo boxes for the input parameters
        self.water_cut_edit = QLineEdit()
        self.fluid_viscosity_edit = QLineEdit()
        self.corrosion_handling_combo = QComboBox()
        self.sand_production_edit = QLineEdit()
        self.gor_edit = QLineEdit()
        self.contaminants_combo = QComboBox()
        self.treatment_combo = QComboBox()

        # Add items to combo boxes
        self.corrosion_handling_combo.addItems(['good', 'excellent'])
        self.contaminants_combo.addItems(['Asphatene', 'paraffin'])
        self.treatment_combo.addItems(['scale', 'acid'])

        # Add labels and input widgets to the input layout
        self.input_layout.addRow("Water Cut (%):", self.water_cut_edit)
        self.input_layout.addRow("Fluid Viscosity (cP):", self.fluid_viscosity_edit)
        self.input_layout.addRow("Corrosion Handling:", self.corrosion_handling_combo)
        self.input_layout.addRow("Sand Production (ppm):", self.sand_production_edit)
        self.input_layout.addRow("Gas-to-Oil Ratio (scf/bbl):", self.gor_edit)
        self.input_layout.addRow("Contaminants:", self.contaminants_combo)
        self.input_layout.addRow("Treatment:", self.treatment_combo)

        return self.input_frame

    def create_properties_frame(self):
        # Create the second frame for Production, Reservoir, and Well Properties
        self.properties_frame = QFrame(self.central_widget)
        self.properties_frame.setFrameShape(QFrame.StyledPanel)
        self.layout.addWidget(self.properties_frame)
        self.properties_layout = QFormLayout(self.properties_frame)

        self.properties_label = QLabel("Production, Reservoir, and Well Properties \n")
        self.properties_layout.addRow(self.properties_label)

        # Add labels and input widgets for Production, Reservoir, and Well Properties
        self.number_of_wells_combo = QComboBox()
        self.production_rate_edit = QLineEdit()
        self.well_depth_edit = QLineEdit()
        self.casing_size_edit = QLineEdit()
        self.deviated_well_combo = QComboBox()
        self.dogleg_severity_edit = QLineEdit()
        self.temperature_edit = QLineEdit()
        self.safety_barriers_combo = QComboBox()
        self.flowing_pressure_edit = QLineEdit()
        self.reservoir_access_combo = QComboBox()
        self.completion_combo = QComboBox()
        self.stability_combo = QComboBox()
        self.recovery_combo = QComboBox()

        # Add items to combo boxes
        self.number_of_wells_combo.addItems(['single', 'multiple'])
        self.deviated_well_combo.addItems(['poor', 'excellent', 'good'])
        self.safety_barriers_combo.addItems(['No', 'Yes'])
        self.reservoir_access_combo.addItems(['Yes', 'No'])
        self.completion_combo.addItems(['single', 'multiple'])
        self.stability_combo.addItems(['stable', 'unstable'])
        self.recovery_combo.addItems([' primary', 'secondary'])

        # Add labels and input widgets to the properties layout
        self.properties_layout.addRow("Number of Wells:", self.number_of_wells_combo)
        self.properties_layout.addRow("Production Rate (BPD):", self.production_rate_edit)
        self.properties_layout.addRow("Well Depth (ft):", self.well_depth_edit)
        self.properties_layout.addRow("Casing Size (in):", self.casing_size_edit)
        self.properties_layout.addRow("Deviated Well:", self.deviated_well_combo)
        self.properties_layout.addRow("Dogleg Severity:", self.dogleg_severity_edit)
        self.properties_layout.addRow("Temperature (F):", self.temperature_edit)
        self.properties_layout.addRow("Safety Barriers:", self.safety_barriers_combo)
        self.properties_layout.addRow("Flowing Pressure (psi):", self.flowing_pressure_edit)
        self.properties_layout.addRow("Reservoir Access:", self.reservoir_access_combo)
        self.properties_layout.addRow("Completion:", self.completion_combo)
        self.properties_layout.addRow("Stability:", self.stability_combo)
        self.properties_layout.addRow("Recovery:", self.recovery_combo)

        return self.properties_frame

    def create_infrastructure_frame(self):
        # Create the Surface Infrastructure frame
        infrastructure_frame = QFrame(self.central_widget)
        infrastructure_frame.setFrameShape(QFrame.StyledPanel)
        infrastructure_layout = QFormLayout(infrastructure_frame)

        infrastructure_label = QLabel("Surface Infrastructure:")
        infrastructure_layout.addRow(infrastructure_label)

        # Create the combo boxes for Surface Infrastructure criteria
        offshore_application_combo = QComboBox()
        electrical_power_combo = QComboBox()
        space_restrictions_combo = QComboBox()
        well_service_combo = QComboBox()

        # Add items to combo boxes
        offshore_application_combo.addItems(['Limited', 'Excellent'])
        electrical_power_combo.addItems(['Utility', 'In-Situ', 'N/A'])
        space_restrictions_combo.addItems(['Poor', 'Excellent'])
        well_service_combo.addItems(['Workover','pulling rig', 'Workover', 'Hydraulic'])

        # Add labels and input widgets to the infrastructure layout
        infrastructure_layout.addRow("Offshore Application:", offshore_application_combo)
        infrastructure_layout.addRow("Electrical Power:", electrical_power_combo)
        infrastructure_layout.addRow("Space Restrictions:", space_restrictions_combo)
        infrastructure_layout.addRow("Well Service:", well_service_combo)

        return infrastructure_frame





    # Add this method to the class
    def get_float_from_line_edit(self, line_edit):
        try:
            value = float(line_edit.text())
            return value
        except ValueError:
            line_edit.clear()
            line_edit.setPlaceholderText("Invalid input")
            return None

    # Modify the predict_lift_method function
    def predict_lift_method(self):
        # Get the input parameters from the user for "Produced Fluid Properties"
        water_cut = self.get_float_from_line_edit(self.water_cut_edit)
        fluid_viscosity = self.get_float_from_line_edit(self.fluid_viscosity_edit)
        corrosion_handling = self.corrosion_handling_combo.currentText()
        sand_production = self.get_float_from_line_edit(self.sand_production_edit)
        gor = self.get_float_from_line_edit(self.gor_edit)
        contaminants = self.contaminants_combo.currentText()
        treatment = self.treatment_combo.currentText()

        # Check if any of the inputs are invalid
        if None in (water_cut, fluid_viscosity, sand_production, gor):
            self.show_error_message("Invalid input(s) for Produced Fluid Properties.")
            return

        # Get the input parameters from the user for "Production, Reservoir, and Well Properties"
        number_of_wells = self.number_of_wells_combo.currentText()
        production_rate = self.get_float_from_line_edit(self.production_rate_edit)
        well_depth = self.get_float_from_line_edit(self.well_depth_edit)
        casing_size = self.get_float_from_line_edit(self.casing_size_edit)
        deviated_well = self.deviated_well_combo.currentText()
        dogleg_severity = self.get_float_from_line_edit(self.dogleg_severity_edit)
        temperature = self.get_float_from_line_edit(self.temperature_edit)
        safety_barriers = self.safety_barriers_combo.currentText()
        flowing_pressure = self.get_float_from_line_edit(self.flowing_pressure_edit)
        reservoir_access = int(self.reservoir_access_combo.currentIndex())
        completion = self.completion_combo.currentText()
        stability = self.stability_combo.currentText()
        recovery = self.recovery_combo.currentText()

        # Check if any of the inputs are invalid
        if None in (production_rate, well_depth, casing_size, dogleg_severity, temperature, flowing_pressure):
            self.show_error_message("Invalid input(s) for Production, Reservoir, and Well Properties.")
            return

        lift_method_costs = {
            "Sucker Rod Pump": "$ 205,433",
            "Gas Lift": "$ 331,107",
            "ESP": "$ 215,694",
            "Hydraulic Piston Pump": "$ UNKNOWN",
            "Hydraulic Jet Pump": "$ UNKNOWN",
            "Plunger Lift": "$ uNKNWON",
            "PCP": "$ 211,412"
        }

        # Perform the function and get the best lift method
        best_method = predict_best_lift_method(
            water_cut, fluid_viscosity, corrosion_handling, sand_production,
            gor, contaminants, treatment, number_of_wells, production_rate,
            well_depth, casing_size, deviated_well, dogleg_severity, temperature,
            safety_barriers, flowing_pressure, reservoir_access, completion,
            stability, recovery
        )

        # Display the best method in the output text box
        self.output_text.clear()
        self.output_text.insertPlainText("The best method recommended is: ")
        cursor = self.output_text.textCursor()
        cursor.setPosition(len("The best method recommended is: "))
        format = cursor.charFormat()
        format.setFontWeight(QFont.Bold)
        format.setFontItalic(True)
        format.setForeground(Qt.darkRed)
        format.setFontPointSize(21)
        cursor.setCharFormat(format)
        self.output_text.setTextCursor(cursor)
        self.output_text.insertPlainText(best_method)

        # Get the cost range for the predicted lift method
        cost_range = lift_method_costs.get(best_method, "Unknown")

        # Create a QTextCharFormat with a larger font size
        text_format = QTextCharFormat()
        text_format.setFontItalic(True)
        text_format.setForeground(Qt.darkRed)
        text_format.setFontPointSize(21)  # Set the desired font size (e.g., 16)

        # Append the text with the specified format
        self.output_text.setCurrentCharFormat(text_format)
        self.output_text.append(f"\nTotal Capital Cost of {cost_range}")

        # Reset the format to the default
        self.output_text.setCurrentCharFormat(QTextCharFormat())  # Reset to default format
        self.output_text.setCurrentCharFormat(QTextCharFormat())

        # Calculate the performance scores for all ALS methods
        als_methods = ['SRP', 'GL', 'ESP', 'HPP', 'HJP', 'PL', 'PCP']
        pis_values, nis_values, ps_values = [], [], []

        for als_method in als_methods:
            pis, nis, ps = calculate_scores(als_method, best_method)
            pis_values.append(pis)
            nis_values.append(nis)
            ps_values.append(ps)

        # Display the results in the table
        self.display_results(als_methods, pis_values, nis_values, ps_values)

        # Plot the performance scores against ALS methods
        self.plot_performance_scores(als_methods, ps_values)

    def display_results(self, als_methods, pis_values, nis_values, ps_values):
        self.results_table.setRowCount(len(als_methods))

        for i, als_method in enumerate(als_methods):
            self.results_table.setItem(i, 0, self.create_table_item(als_method))
            self.results_table.setItem(i, 1, self.create_table_item(pis_values[i]))
            self.results_table.setItem(i, 2, self.create_table_item(nis_values[i]))
            self.results_table.setItem(i, 3, self.create_table_item(ps_values[i]))

            # Calculate the performance score
            performance_score = (pis_values[i] - nis_values[i]) / (pis_values[i] + nis_values[i])
            self.results_table.setItem(i, 4, self.create_table_item(performance_score))

    def create_table_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def plot_performance_scores(self, als_methods, ps_values):
        self.bar_chart.clear()
        self.bar_chart.bar(als_methods, ps_values)

        # Add legend, axis labels, and title to the plot
        self.bar_chart.set_ylabel("Performance Score (PS)")
        self.bar_chart.set_xlabel("Artificial Lift System (ALS)")
        self.bar_chart.set_title("Performance Scores for Artificial Lift Methods")
        self.bar_chart.legend(["Performance Score"])

        self.canvas.draw()

    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec_()

    def clear_inputs(self):
        # Clear all input and output fields
        self.water_cut_edit.clear()
        self.fluid_viscosity_edit.clear()
        self.production_rate_edit.clear()
        self.well_depth_edit.clear()
        self.casing_size_edit.clear()
        self.dogleg_severity_edit.clear()
        self.temperature_edit.clear()
        self.flowing_pressure_edit.clear()
        self.corrosion_handling_combo.setCurrentIndex(0)
        self.sand_production_edit.clear()
        self.gor_edit.clear()
        self.contaminants_combo.setCurrentIndex(0)
        self.treatment_combo.setCurrentIndex(0)
        self.output_text.clear()

    def set_button_styles(self):
        button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: %s;
                color: white;
            }
        """
        self.start_button.setStyleSheet(button_style % ("green", "darkgreen"))
        self.clear_button.setStyleSheet(button_style % ("blue", "darkblue"))

        # Set the fixed size for the buttons
        button_width = 90 # Set your desired width here
        button_height = 30  # Set your desired height here
        self.start_button.setFixedSize(button_width, button_height)
        self.clear_button.setFixedSize(button_width, button_height)

def calculate_scores(als_method, best_method):
    # Generate a single random integer between 0 and 10 (inclusive)

    # assume arbitrary values for PIS and NIS.
    # You should replace these with actual calculations based on your domain knowledge and data.
    # Updated 'pis' and 'nis' dictionaries
    pis_values = {'SRP': 4.062125, 'GL': 7.874213, 'ESP': 6.874468, 'HPP': 7.273240, 'HJP': 6.031554, 'PL': 6.496925,
           'PCP': 5.798163}
    nis_values = {'SRP': 5.937875, 'GL': 0.125787, 'ESP': 2.125532, 'HPP': 0.726760, 'HJP': 5.968446, 'PL': 5.503075,
           'PCP': 6.201837}

    pis = pis_values.get(als_method, 0)
    nis = nis_values.get(als_method, 0)


    # Calculate the Performance Score (PS)
    ps = (pis - nis)/ (pis + nis)
    abs_ps=abs(ps)
    return pis, nis, round(abs_ps,2)


def predict_best_lift_method(water_cut, fluid_viscosity, corrosion_handling, sand_production, gor, contaminants,
                            treatment, number_of_wells, production_rate, well_depth, casing_size, deviated_well,
                            dogleg_severity, temperature, safety_barriers, flowing_pressure, reservoir_access,
                            completion, stability, recovery):
    print("Starting predict_best_lift_method...")

    try:
        # Define the range and criteria for each lift method
        lift_methods = {
            'Gas Lift': {'water_cut': (0, 100), 'fluid_viscosity': (0, 200), 'corrosion_handling': ['good', 'excellent'],
                    'sand_production': (0, 1), 'gor': (500, 2000), 'contaminants': ['Asphatene', 'paraffin'],
                    'treatment': ['scale', 'acid'], 'number_of_wells': ['single or multiple'],
                    'production_rate': (5, 5000), 'well_depth': (100, 16000), 'casing_size': (4.5, 5.5),
                    'deviated_well': 'poor', 'dogleg_severity': 15, 'temperature': (100, 550),
                    'safety_barriers': 'N/A', 'flowing_pressure': (50, 100), 'reservoir_access': 0,
                    'completion': 'single', 'stability': 'stable', 'recovery': 'primary or secondary'},
            'Sucker Rod Pump': {'water_cut': (0, 100), 'fluid_viscosity': (0, 200), 'corrosion_handling': ['good', 'excellent'],
                   'sand_production': (0, 0), 'gor': (0, 2000), 'contaminants': ['Asphatene', 'paraffin'],
                   'treatment': ['scale', 'acid'], 'number_of_wells': ['multiple'],
                   'production_rate': (200, 30000), 'well_depth': (5000, 15000), 'casing_size': (4, 7),
                   'deviated_well': 'excellent', 'dogleg_severity': 0.0, 'temperature': (100, 400),
                   'safety_barriers': 'N/A', 'flowing_pressure': (100, 1000), 'reservoir_access': 1,
                   'completion': 'single or multiple', 'stability': 'stable or unstable', 'recovery': 'primary or secondary'},
            'ESP': {'water_cut': (0, 100), 'fluid_viscosity': (100, 500), 'corrosion_handling': ['good'],
                    'sand_production': (0, 100), 'gor': (1000, float('inf')), 'contaminants': ['Asphatene', 'paraffin'],
                    'treatment': ['scale', 'acid'], 'number_of_wells': ['multiple'],
                    'production_rate': (200, 30000), 'well_depth': (1000, 15000), 'casing_size': (5.4, 9.625),
                    'deviated_well': 'good', 'dogleg_severity': 30, 'temperature': (100, 400),
                    'safety_barriers': 'N/A', 'flowing_pressure': 0.0, 'reservoir_access': 0,
                    'completion': 'single or multiple', 'stability': 'stable', 'recovery': 'primary or secondary'},
            'Hydraulic Piston Pump': {'water_cut': (0, 70), 'fluid_viscosity': (10, 450), 'corrosion_handling': ['good'],
                    'sand_production': (0, 10), 'gor': (800, float('inf')), 'contaminants': ['paraffin'],
                    'treatment': ['scale', 'acid'], 'number_of_wells': ['single or more'],
                    'production_rate': (50, 4000), 'well_depth': (7500, 17000), 'casing_size': (5, 9.625),
                    'deviated_well': 'excellent', 'dogleg_severity': 15, 'temperature': (100, 500),
                    'safety_barriers': 'N/A', 'flowing_pressure': (500, 15000), 'reservoir_access': 1,
                    'completion': 'single', 'stability': 'stable', 'recovery': 'primary or secondary'},
            'Hydraulic Jet Pump': {'water_cut': (0, 100), 'fluid_viscosity': (14, 200), 'corrosion_handling': ['excellent'],
                    'sand_production': (0, 30), 'gor': (0, 2000), 'contaminants': ['paraffin'],
                    'treatment': ['scale', 'acid'], 'number_of_wells': ['single or more'],
                    'production_rate': (300, 15000), 'well_depth': (5000, 15000), 'casing_size': (5.5, 7),
                    'deviated_well': 'excellent', 'dogleg_severity': 24, 'temperature': (100, 500),
                    'safety_barriers': 'N/A', 'flowing_pressure': (100, 1000), 'reservoir_access': 1,
                    'completion': 'single', 'stability': 'stable', 'recovery': 'primary or secondary'},
            'Plunger Lift': {'water_cut': (0, 50), 'fluid_viscosity': (0, 200), 'corrosion_handling': ['excellent'],
                   'sand_production': (0, 1), 'gor': (1000, float('inf')), 'contaminants': ['Asphatene', 'paraffin'],
                   'treatment': ['scale', 'acid'], 'number_of_wells': ['single'],
                   'production_rate': (1, 5), 'well_depth': (8000, 19000), 'casing_size': (7, 990625),
                   'deviated_well': 'good', 'dogleg_severity': 'pass', 'temperature': (120, 500),
                   'safety_barriers': 'N/A', 'flowing_pressure': '<275', 'reservoir_access': 0,
                   'completion': 'single', 'stability': 'stable', 'recovery': 'secondary'},
            'PCP': {'water_cut': (0, 50), 'fluid_viscosity': (100, 5000), 'corrosion_handling': ['fair'],
                    'sand_production': (0, 5), 'gor': (0, 500), 'contaminants': ['Asphatene', 'paraffin'],
                    'treatment': ['scale', 'acid'], 'number_of_wells': ['single'],
                    'production_rate': (5, 4500), 'well_depth': (2000, 6000), 'casing_size': (5, 7),
                    'deviated_well': 'poor', 'dogleg_severity': 15, 'temperature': (75, 250),
                    'safety_barriers': 'N/A', 'flowing_pressure': (20, 250), 'reservoir_access': 0,
                    'completion': 'single', 'stability': 'stable', 'recovery': 'secondary'}
        }

        # Initialize a dictionary to store the scores for each lift method
        lift_scores = {}

        # Iterate through each lift method and calculate the score
        for method, criteria in lift_methods.items():
            score = 0

            # Check each parameter against the criteria
            if criteria['water_cut'][0] <= water_cut <= criteria['water_cut'][1]:
                score += 1
            if criteria['fluid_viscosity'][0] <= fluid_viscosity <= criteria['fluid_viscosity'][1]:
                score += 1
            if corrosion_handling in criteria['corrosion_handling']:
                score += 1
            if criteria['sand_production'][0] <= sand_production <= criteria['sand_production'][1]:
                score += 1
            if criteria['gor'][0] <= gor <= criteria['gor'][1]:
                score += 1
            if contaminants in criteria['contaminants']:
                score += 1
            if treatment in criteria['treatment']:
                score += 1
            if number_of_wells in criteria['number_of_wells']:
                score += 1
            if criteria['production_rate'][0] <= production_rate <= criteria['production_rate'][1]:
                score += 1
            if criteria['well_depth'][0] <= well_depth <= criteria['well_depth'][1]:
                score += 1
            if criteria['casing_size'][0] <= casing_size <= criteria['casing_size'][1]:
                score += 1
            if deviated_well in criteria['deviated_well']:
                score += 1

            if dogleg_severity == criteria['dogleg_severity']:
                score +=1

            if criteria['temperature'][0] <= temperature <= criteria['temperature'][1]:
                score += 1

            if safety_barriers in criteria['safety_barriers']:
                score += 1

            if flowing_pressure == criteria ['flowing_pressure']:
                score += 1

            if reservoir_access == criteria['reservoir_access']:
                score += 1
            if completion in criteria['completion']:
                score += 1
            if stability in criteria['stability']:
                score += 1
            if recovery in criteria['recovery']:
                score += 1

            lift_scores[method] = score

        # Find the lift method with the highest score
        best_lift_method = max(lift_scores, key=lift_scores.get)

        print("End of predict_best_lift_method...")
        return best_lift_method

    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ArtificialLiftInterface()
    window.show()
    sys.exit(app.exec_())
