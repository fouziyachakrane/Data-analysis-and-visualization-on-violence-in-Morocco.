import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Define classes representing each column in the dataset
class Lieu:
    """Represents a location in the dataset."""
    def __init__(self, type_lieu):
        self.type_lieu = type_lieu

    def __str__(self):
        return f"Lieu: {self.type_lieu}"

class Region:
    """Represents a geographical region in the dataset."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Region: {self.name}"

class Age:
    """Represents an age range in the dataset."""
    def __init__(self, range):
        self.range = range

    def __str__(self):
        return f"Age: {self.range}"

class Etat:
    """Represents marital status in the dataset."""
    def __init__(self, marital_status):
        self.marital_status = marital_status

    def __str__(self):
        return f"Etat: {self.marital_status}"

class TypeActivite:
    """Represents type of activity in the dataset."""
    def __init__(self, activity_type):
        self.activity_type = activity_type

    def __str__(self):
        return f"TypeActivite: {self.activity_type}"

class Contexte:
    """Represents context information in the dataset."""
    def __init__(self, context):
        self.context = context

    def __str__(self):
        return f"Contexte: {self.context}"

class TypeViolence:
    """Represents type of violence in the dataset."""
    def __init__(self, violence_type):
        self.violence_type = violence_type

    def __str__(self):
        return f"TypeViolence: {self.violence_type}"

class NiveauScolaire:
    """Represents educational level in the dataset."""
    def __init__(self, education_level):
        self.education_level = education_level

    def __str__(self):
        return f"NiveauScolaire: {self.education_level}"

class DataVisualizationApp(QMainWindow):
    """
    Interactive data visualization application for analyzing violence-related data.
    Provides dynamic filtering and multiple visualization options.
    """
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        """Initialize the user interface with all necessary components."""
        self.setWindowTitle("Visualisation des Données sur la Violence")
        self.setGeometry(200, 200, 600, 500)

        # Central widget setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Dropdowns setup
        filter_layout = QHBoxLayout()

        # X-axis selector
        self.x_axis_selector = QComboBox()
        self.x_axis_selector.addItems(self.data.columns)
        self.x_axis_selector.setToolTip("Sélectionnez la variable pour l'axe X")
        self.x_axis_selector.currentIndexChanged.connect(self.update_filter_options)
        filter_layout.addWidget(QLabel("categorie1 :"))
        filter_layout.addWidget(self.x_axis_selector)

        # Filter selector
        self.filter_selector = QComboBox()
        self.filter_selector.addItems(self.data.columns)
        self.filter_selector.setToolTip("Sélectionnez une variable pour filtrer les données")
        self.filter_selector.currentIndexChanged.connect(self.update_category_options)
        filter_layout.addWidget(QLabel("categorie2 :"))
        filter_layout.addWidget(self.filter_selector)

        # Category selector
        self.category_selector = QComboBox()
        self.category_selector.setToolTip("Sélectionnez une valeur spécifique pour le filtre")
        filter_layout.addWidget(QLabel("Sélectionnez une catégorie :"))
        filter_layout.addWidget(self.category_selector)

        # Graph type selector
        self.graph_type_selector = QComboBox()
        self.graph_type_selector.addItems(["Bar", "Pie"])
        self.graph_type_selector.setToolTip("Choisissez le type de graphique à afficher")
        filter_layout.addWidget(QLabel("Type de Graphe :"))
        filter_layout.addWidget(self.graph_type_selector)

        layout.addLayout(filter_layout)

        # Plot button
        self.plot_button = QPushButton("Générer le Graphique")
        self.plot_button.setToolTip("Cliquez pour générer le graphique avec les paramètres sélectionnés")
        self.plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(self.plot_button)

        # Matplotlib canvas
        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

    def update_filter_options(self):
        """Update available filter options based on selected X-axis variable."""
        selected_x_axis = self.x_axis_selector.currentText()
        self.filter_selector.clear()
        available_filters = [col for col in self.data.columns if col != selected_x_axis]
        self.filter_selector.addItems(available_filters)
        self.update_category_options()  # Update categories when filter changes

    def update_category_options(self):
        """Update available category options based on selected filter."""
        selected_filter = self.filter_selector.currentText()
        if selected_filter:
            unique_categories = self.data[selected_filter].dropna().unique()
            self.category_selector.clear()
            self.category_selector.addItems(map(str, unique_categories))

    def plot_graph(self):
        """Generate and display the graph based on selected options."""
        x_feature = self.x_axis_selector.currentText()
        filter_feature = self.filter_selector.currentText()
        graph_type = self.graph_type_selector.currentText()
        selected_category = self.category_selector.currentText()

        # Clear previous plots
        self.canvas.figure.clf()
        ax = self.canvas.figure.subplots()

        if graph_type == "Bar":
            self.plot_bar_graph(ax, x_feature, filter_feature)
        elif graph_type == "Pie":
            self.plot_pie_chart(ax, x_feature, filter_feature, selected_category)

        self.canvas.draw()

    def plot_bar_graph(self, ax, x_feature, filter_feature):
        """Plot a bar graph for the selected features."""
        # Group data by the filter feature and calculate frequencies for the x feature
        filtered_data = self.data.groupby(filter_feature)[x_feature].value_counts().unstack(fill_value=0)

        # Plot each category in the filter as a separate bar group
        filtered_data.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')

        ax.set_title(f"Fréquence de {x_feature} par {filter_feature}", fontsize=14)
        ax.set_xlabel(x_feature, fontsize=12)
        ax.set_ylabel("Fréquence", fontsize=12)
        ax.tick_params(axis='x', rotation=45)

    def plot_pie_chart(self, ax, x_feature, filter_feature, selected_category):
        """Plot a pie chart for the selected features and category."""
        # Filter the data for the selected category
        if selected_category:
            category_data = self.data[self.data[filter_feature] == selected_category]
            pie_data = category_data[x_feature].value_counts()

            if not pie_data.empty:
                pie_data.plot(kind='pie', ax=ax, autopct='%1.1f%%', colormap='viridis')
                ax.set_title(f"Répartition de {x_feature} pour {selected_category}", fontsize=14)
                ax.set_ylabel("")  # Remove default ylabel for aesthetics
            else:
                ax.text(0.5, 0.5, "Aucune donnée disponible pour cette catégorie.", 
                        fontsize=12, ha='center', va='center')

# Main application
if __name__ == "__main__":
    # Charger le dataset

    df = pd.read_csv("dataset.csv")

    app = QApplication(sys.argv)
    window = DataVisualizationApp(df)
    window.show()
    sys.exit(app.exec())
