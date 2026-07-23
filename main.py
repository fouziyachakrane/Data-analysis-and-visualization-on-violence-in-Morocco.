import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QGraphicsDropShadowEffect, 
                              QScrollArea, QWidget, QVBoxLayout, QGridLayout, QTextEdit, QPushButton, QLabel, QComboBox, QHBoxLayout, QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from ui_interface import Ui_MainWindow
import subprocess
import io
import sys
from contextlib import redirect_stdout
import os
from PySide6.QtWebEngineWidgets import QWebEngineView
import folium
import geopandas as gpd
from PySide6.QtCore import QUrl

class MainWindow(QMainWindow):
    """
    Main application window for data visualization dashboard.
    Provides a modern, frameless interface with interactive graphs and controls.
    """
    def __init__(self):
        super().__init__()
        
        # Remove title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Apply styles to all buttons
        self.setup_button_styles()
        
        # Connect window control buttons and add tooltips
        self.ui.minimize_window_button.clicked.connect(self.showMinimized)
        self.ui.minimize_window_button.setToolTip("Minimize Window")
        self.ui.restore_widow_button.clicked.connect(self.toggle_maximize)
        self.ui.restore_widow_button.setToolTip("Maximize/Restore Window")
        self.ui.close_window_button.clicked.connect(self.close)
        self.ui.close_window_button.setToolTip("Close Window")
        
        # Variables for window dragging
        self.dragging = False
        self.drag_position = None
        
        # Make header frame handle window dragging
        self.ui.header_frame.mousePressEvent = self.mousePressEvent
        self.ui.header_frame.mouseMoveEvent = self.mouseMoveEvent
        self.ui.header_frame.mouseReleaseEvent = self.mouseReleaseEvent
        
        # Initially hide the left menu
        self.ui.left_menu_widget.hide()
        self.ui.left_menu_widget.setMinimumWidth(200)  # Set minimum width
        self.ui.left_menu_widget.setMaximumWidth(200)  # Set maximum width
        
        # Set consistent spacing for menu buttons
        menu_layout = self.ui.left_menu_widget.layout()
        if menu_layout:
            menu_layout.setSpacing(5)
            menu_layout.setContentsMargins(10, 10, 10, 10)
        
        # Setup pages
        self.setup_pages()
        
        # Connect menu button and add tooltip
        self.ui.pushButton_5.clicked.connect(self.toggle_menu)
        self.ui.pushButton_5.setToolTip("Toggle Navigation Menu")
        
        # Connecter les boutons and add tooltips
        self.ui.graphes.clicked.connect(self.show_graphs_page)
        self.ui.graphes.setToolTip("Afficher les graphiques statistiques")
        
        self.ui.moregraphes.clicked.connect(self.show_more_graphs_page)
        self.ui.moregraphes.setToolTip("Afficher l'outil de visualisation interactive")
        
        self.ui.map.clicked.connect(self.show_map)
        self.ui.map.setToolTip("Afficher la carte du Maroc")
        
        # Variables for graph management
        self.graphs_created = False
        self.current_graph_size = (8, 5)
        self.graph_titles = [
            "Distribution par lieu et activité",
            "Violence par contexte",
            "Activité par niveau scolaire",
            "Violence par âge",
            "Contexte par état civil",
            "Proportion des lieux",
            "Proportion par région",
            "Distribution des types de violence"
        ]
        self.graph_descriptions = [
            "Ce graphique montre la répartition des différentes activités selon les lieux. Il permet d'identifier où se déroulent principalement certains types d'activités.",
            "Cette visualisation présente les types de violence en fonction du contexte, permettant d'identifier les situations les plus à risque.",
            "Ce graphique illustre la distribution des activités par niveau scolaire, montrant comment les activités varient selon l'éducation.",
            "Cette analyse montre la relation entre l'âge et les types de violence, révélant les groupes d'âge les plus touchés.",
            "Ce graphique présente le contexte des incidents selon l'état civil des personnes concernées.",
            "Ce diagramme circulaire montre la répartition globale des incidents par lieu, permettant d'identifier les zones les plus touchées.",
            "Cette visualisation présente la distribution géographique des cas par région.",
            "Ce graphique présente une vue d'ensemble des différents types de violence et leur fréquence relative."
        ]  
                           
        # Create code display widget
        self.code_display = QTextEdit()
        self.code_display.setReadOnly(True)
        self.code_display.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #a9b7c6;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
        """)
        self.code_display.hide()
        self.ui.page_2.layout().addWidget(self.code_display)
        
        # Create output display widget
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
        """)
        self.output_display.hide()
        self.ui.page_2.layout().addWidget(self.output_display)
        
    def setup_button_styles(self):
        """Apply consistent styling to all buttons."""
        # Common button style
        button_style = """
            QPushButton {
                background-color: #800000;
                color: white;
                border: none;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2b2b2b;
            }
            QPushButton:pressed {
                background-color: #2b2b2b;
            }
        """
        
        # Window control buttons style
        window_control_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2b2b2b;
            }
        """
        
        # Menu button style
        menu_button_style = """
            QPushButton {
                background-color: #800000;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #800000;
            }
        """
        
        # Navigation buttons style (graphes, moregraphes)
        nav_button_style = """
            QPushButton {
                background-color: #800000;
                color: white;
                padding: 5px 15px;
                font-weight: bold;
                font-size: 15px;
                text-align: left;
                margin: 3px;
                min-width: 180px;
                max-width: 180px;
                min-height: 35px;
                max-height: 35px;
            }
            QPushButton:hover {
                background-color: #800000;
                border-color: #4b4b4b;
            }
            QPushButton:pressed {
                background-color: #1b1b1b;
                border-color: #2b2b2b;
            }
        """
        
        # Generate graph button style
        generate_button_style = """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: bold;
                font-size: 14px;
                margin: 10px 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """
        
        # Apply styles to window control buttons
        self.ui.minimize_window_button.setStyleSheet(window_control_style)
        self.ui.restore_widow_button.setStyleSheet(window_control_style)
        self.ui.close_window_button.setStyleSheet(window_control_style + """
            QPushButton:hover {
                background-color: #2b2b2b;
            }
        """)
        
        # Apply style to menu button
        self.ui.pushButton_5.setStyleSheet(menu_button_style)
        
        # Apply style to navigation buttons
        self.ui.graphes.setStyleSheet(nav_button_style)
        self.ui.moregraphes.setStyleSheet(nav_button_style)
        self.ui.map.setStyleSheet(nav_button_style)
        
        # Apply style to generate button (in interactive view)
        if hasattr(self, 'generate_button'):
            self.generate_button.setStyleSheet(generate_button_style)
            
        # Style for combo boxes
        combo_style = """
            QComboBox {
                background-color: #2b2b2b;
                color: white;
                border: 2px solid #3b3b3b;
                border-radius: 5px;
                padding: 5px;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #4b4b4b;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(:/newPrefix/icones/arrow-down.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #3b3b3b;
                selection-color: white;
                border: 1px solid #4b4b4b;
            }
        """
        
        # Apply combo box style to all combo boxes
        if hasattr(self, 'x_axis_selector'):
            self.x_axis_selector.setStyleSheet(combo_style)
            self.filter_selector.setStyleSheet(combo_style)
            self.category_selector.setStyleSheet(combo_style)
            self.graph_type_selector.setStyleSheet(combo_style)
            
        # Style for labels
        label_style = """
            QLabel {
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
            }
        """
        
        # Apply label style to all QLabels in the interactive container
        if hasattr(self, 'interactive_container'):
            for child in self.interactive_container.findChildren(QLabel):
                child.setStyleSheet(label_style)

    def setup_pages(self):
        """Configurer les différentes pages de l'interface"""
        # Page pour la carte
        self.map_page = QWidget()
        map_layout = QVBoxLayout(self.map_page)
        self.map_view = QWebEngineView()
        
        # Remove focus outline from map elements
        self.map_view.setStyleSheet("""
            QWebEngineView {
                outline: none;
                border: none;
            }
            QWebEngineView:focus {
                outline: none;
                border: none;
            }
        """)
        map_layout.addWidget(self.map_view)
        self.ui.stackedWidget.addWidget(self.map_page)
        
        # Page pour les graphes
        self.graphs_page = QWidget()
        self.grid_layout = QGridLayout(self.graphs_page)
        self.ui.stackedWidget.addWidget(self.graphs_page)
        
        # Page pour more graphes
        self.more_graphs_page = QWidget()
        self.more_graphs_layout = QVBoxLayout(self.more_graphs_page)
        self.ui.stackedWidget.addWidget(self.more_graphs_page)
        
        # Configurer la page initiale comme la carte
        self.show_map()  # Show map by default
        
    def show_map(self):
        """Affiche la carte du Maroc avec les données de violence"""
        try:
            # Vérifier si la carte est déjà chargée
            if not hasattr(self, '_map_loaded'):
                # Créer le chemin absolu pour le fichier HTML temporaire
                temp_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_map.html')
                
                # Lire les données
                geometry_data = gpd.read_file('maroc.geojson')
                violence_data = pd.read_csv('dataset.csv')
                
                # Normaliser les noms de colonnes
                violence_data.columns = violence_data.columns.str.lower()
                
                # Mapping des noms de régions
                region_mapping = {
                    "Laâyoune-Sakia Al Hamra": "Laayoune-Saguia Hamra",
                    "Rabat-Salé-Kénitra": "Rabat-Sale-Kenitra",
                    "Béni Mellal-Khénifra": "Beni Mellal-Khenifra",
                    "Ed Dakhla-Oued Ed Dahab": "Dakhla-Oued Eddahab",
                    "Tanger-Tétouan-Al Hoceima": "Tanger-Tetouan-Hoceima",
                    "Drâa-Tafilalet": "Daraa-Tafilelt",
                    "Fès-Meknès": "Fes-Meknes",
                    "Souss-Massa": "Souss Massa"
                }
                violence_data['region'] = violence_data['region'].replace(region_mapping)
                
                # Calculer les statistiques
                violence_stats = violence_data.groupby('region').agg({
                    'lieu': lambda x: f"Urbain: {round((x=='Urbain').mean()*100, 2)}%, Rurale: {round((x=='Rurale').mean()*100, 2)}%",
                    'type_violence': lambda x: x.value_counts().to_dict()
                }).reset_index()
                
                def get_color(row):
                    if isinstance(row['type_violence'], dict) and row['type_violence']:
                        max_violence = max(row['type_violence'].values())
                        if max_violence > 50:
                            return '#8B0000'  # Rouge foncé
                        elif max_violence > 20:
                            return '#FF6347'  # Rouge moyen
                        else:
                            return '#FFA07A'  # Rouge clair
                    return '#CCCCCC'  # Gris pour les régions sans données
                
                # Fusionner les données
                map_data = geometry_data.merge(violence_stats, on='region', how='left')
                map_data = gpd.GeoDataFrame(map_data)
                
                def format_popup(row):
                    lieu_stats = row['lieu'] if pd.notna(row['lieu']) else "No data"
                    type_violence = row['type_violence']

                    if isinstance(type_violence, dict):
                        type_violence_html = ''.join(f"<li>{k}: {v}</li>" for k, v in type_violence.items())
                    else:
                        type_violence_html = "<li>No data available</li>"

                    popup_html = f"""
                    <div style="border: 2px solid black; padding: 5px; border-radius: 8px;">
                        <h4>Region: {row['region']}</h4>
                        <p><b>Lieu Stats:</b> {lieu_stats}</p>
                        <p><b>Type of Violence:</b></p>
                        <ul>{type_violence_html}</ul>
                    </div>
                    """
                    return popup_html
                
                # Ajouter le contenu du popup
                map_data['popup_content'] = map_data.apply(format_popup, axis=1)
                
                # Créer la carte
                bounds = geometry_data.total_bounds
                m = folium.Map(
                    location=[31.7917, -7.0926],  # Center of Morocco
                    zoom_start=5,  # Zoomed out to show all of Morocco
                    tiles="cartodbdark_matter"  # Dark theme tiles
                )
                
                # Add custom CSS to remove focus outlines
                folium.Element("""
                    <style>
                        .leaflet-interactive {
                            outline: none !important;
                        }
                        .leaflet-interactive:focus {
                            outline: none !important;
                        }
                        path {
                            outline: none !important;
                        }
                    </style>
                """).add_to(m)
                
                # Add GeoJSON data to the map
                folium.GeoJson(
                    map_data,
                    style_function=lambda x: {
                        'fillColor': get_color(x['properties']),
                        'color': 'white',
                        'weight': 1,
                        'fillOpacity': 0.7,
                    },
                    tooltip=folium.GeoJsonTooltip(
                        fields=['region', 'lieu', 'type_violence'],
                        aliases=['Région:', 'Distribution:', 'Types de Violence:'],
                        style="""
                            background-color: #2d2d2d;
                            border: 1px solid white;
                            border-radius: 3px;
                            box-shadow: 3px 3px 10px rgba(0,0,0,0.5);
                            font-size: 14px;
                            font-weight: bold;
                            color: white;
                            padding: 10px;
                        """
                    ),
                    highlight_function=lambda x: {'weight': 3, 'fillOpacity': 0.9}
                ).add_to(m)
                
                # Add custom CSS to remove focus outline
                css = """
                <style>
                    .no-focus-outline {
                        outline: none !important;
                        -webkit-tap-highlight-color: transparent;
                    }
                    .no-focus-outline:focus {
                        outline: none !important;
                    }
                    .no-focus-outline:active {
                        outline: none !important;
                    }
                    .leaflet-interactive {
                        outline: none !important;
                    }
                </style>
                """
                m.get_root().html.add_child(folium.Element(css))
                
                # Sauvegarder la carte
                m.save(temp_html_path)
                
                # Convertir le chemin en URL compatible
                file_url = QUrl.fromLocalFile(temp_html_path)
                
                # Configurer les paramètres du WebEngineView
                self.map_view.settings().setAttribute(
                    self.map_view.settings().WebAttribute.LocalContentCanAccessRemoteUrls, 
                    True
                )
                self.map_view.settings().setAttribute(
                    self.map_view.settings().WebAttribute.LocalContentCanAccessFileUrls, 
                    True
                )
                
                # Afficher la carte dans l'interface
                self.map_view.setUrl(file_url)
                self.map_view.show()
                self._map_loaded = True
            
            # Passer à la page de la carte
            self.ui.stackedWidget.setCurrentWidget(self.map_page)
            
        except Exception as e:
            print(f"Erreur lors de l'affichage de la carte: {str(e)}")

    def show_graphs_page(self):
        """Affiche la page des graphiques statistiques"""
        self.setup_graph_page()
        self.ui.stackedWidget.setCurrentWidget(self.graphs_page)
        
    def show_more_graphs_page(self):
        """Affiche la page des graphiques interactifs"""
        try:
            # Initialize interactive page if not already done
            if not hasattr(self, '_interactive_created'):
                self.setup_interactive_page()
                self._interactive_created = True  # Mark as created
            
            # Load dataset if not already loaded
            if not hasattr(self, 'data'):
                try:
                    self.data = pd.read_csv('dataset.csv')
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", 
                        "Impossible de charger le fichier dataset.csv. Assurez-vous qu'il existe dans le répertoire.")
                    return

            # Switch to the interactive graphs page
            self.ui.stackedWidget.setCurrentWidget(self.more_graphs_page)
            
            # Clear any existing figure
            if hasattr(self, 'interactive_canvas'):
                self.interactive_canvas.figure.clear()
                self.interactive_canvas.draw()
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", 
                f"Une erreur s'est produite lors de l'affichage des graphiques interactifs: {str(e)}")
        
    def setup_pages(self):
        """Configurer les différentes pages de l'interface"""
        # Page pour la carte
        self.map_page = QWidget()
        map_layout = QVBoxLayout(self.map_page)
        self.map_view = QWebEngineView()
        
        # Remove focus outline from map elements
        self.map_view.setStyleSheet("""
            QWebEngineView {
                outline: none;
                border: none;
            }
            QWebEngineView:focus {
                outline: none;
                border: none;
            }
        """)
        map_layout.addWidget(self.map_view)
        self.ui.stackedWidget.addWidget(self.map_page)
        
        # Page pour les graphes
        self.graphs_page = QWidget()
        self.grid_layout = QGridLayout(self.graphs_page)
        self.ui.stackedWidget.addWidget(self.graphs_page)
        
        # Page pour more graphes
        self.more_graphs_page = QWidget()
        self.more_graphs_layout = QVBoxLayout(self.more_graphs_page)
        self.ui.stackedWidget.addWidget(self.more_graphs_page)
        
        # Configurer la page initiale comme la carte
        self.show_map()  # Show map by default
        
    def setup_graph_page(self):
        """Configure la page des graphiques"""
        if not self.graphs_created:
            # Create scroll area with dynamic sizing
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            
            # Create and style the container widget
            self.scroll_content = QWidget()
            self.scroll_content.setStyleSheet("background-color: white;")
            self.grid_layout = QGridLayout(self.scroll_content)
            self.grid_layout.setSpacing(20)
            self.grid_layout.setContentsMargins(20, 20, 20, 20)
            
            self.scroll_area.setWidget(self.scroll_content)
            self.graphs_page.layout().addWidget(self.scroll_area)
            
            # Configuration des graphiques
            sns.set(style="whitegrid")
            self.graphs = []  # Store graph references
            
            # Créer 8 graphiques différents
            graphs = []
            
            # 1. Lieux & Type d'activité
            fig1 = plt.figure(figsize=self.current_graph_size)
            sns.countplot(data=pd.read_csv('dataset.csv'), x='Lieu', hue='Type_activite')
            plt.title("Distribution par lieu et activité")
            canvas1 = FigureCanvas(fig1)
            canvas1.mpl_connect('button_press_event', lambda event: self.show_graph_details(0))
            graphs.append(canvas1)
            
            # 2. Contexte & Type de violence
            fig2 = plt.figure(figsize=self.current_graph_size)
            sns.countplot(data=pd.read_csv('dataset.csv'), x='Contexte', hue='Type_violence')
            plt.title("Violence par contexte")
            canvas2 = FigureCanvas(fig2)
            canvas2.mpl_connect('button_press_event', lambda event: self.show_graph_details(1))
            graphs.append(canvas2)
            
            # 3. Niveau scolaire & Type d'activité
            fig3 = plt.figure(figsize=self.current_graph_size)
            sns.countplot(data=pd.read_csv('dataset.csv'), x='Niveau_scolaire', hue='Type_activite')
            plt.title("Activité par niveau scolaire")
            canvas3 = FigureCanvas(fig3)
            canvas3.mpl_connect('button_press_event', lambda event: self.show_graph_details(2))
            graphs.append(canvas3)
            
            # 4. Age & Type de violence
            fig4 = plt.figure(figsize=self.current_graph_size)
            sns.countplot(data=pd.read_csv('dataset.csv'), x='Age', hue='Type_violence')
            plt.title("Violence par âge")
            canvas4 = FigureCanvas(fig4)
            canvas4.mpl_connect('button_press_event', lambda event: self.show_graph_details(3))
            graphs.append(canvas4)
            
            # 5. État & Contexte
            fig5 = plt.figure(figsize=self.current_graph_size)
            sns.countplot(data=pd.read_csv('dataset.csv'), x='Etat', hue='Contexte')
            plt.title("Contexte par état civil")
            canvas5 = FigureCanvas(fig5)
            canvas5.mpl_connect('button_press_event', lambda event: self.show_graph_details(4))
            graphs.append(canvas5)
            
            # 6. Proportion des lieux
            fig6 = plt.figure(figsize=self.current_graph_size)
            pd.read_csv('dataset.csv')['Lieu'].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title("Proportion des lieux")
            canvas6 = FigureCanvas(fig6)
            canvas6.mpl_connect('button_press_event', lambda event: self.show_graph_details(5))
            graphs.append(canvas6)
            
            # 7. Proportion par région
            fig7 = plt.figure(figsize=self.current_graph_size)
            pd.read_csv('dataset.csv')['Region'].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title("Proportion par région")
            canvas7 = FigureCanvas(fig7)
            canvas7.mpl_connect('button_press_event', lambda event: self.show_graph_details(6))
            graphs.append(canvas7)
            
            # 8. Types de violence
            fig8 = plt.figure(figsize=self.current_graph_size)
            sns.countplot(data=pd.read_csv('dataset.csv'), x='Type_violence')
            plt.title("Distribution des types de violence")
            canvas8 = FigureCanvas(fig8)
            canvas8.mpl_connect('button_press_event', lambda event: self.show_graph_details(7))
            graphs.append(canvas8)
            
            # Ajouter les graphiques à la grille
            for i, graph in enumerate(graphs):
                row = i // 2
                col = i % 2
                # Add the graph to the grid
                self.grid_layout.addWidget(graph, row, col)
                # Style each graph container
                graph.setMinimumSize(400, 300)
                graph.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 5px; cursor: pointer;")
            
            self.graphs = graphs
            self.graphs_created = True
            # Update layout immediately
            self.update_graph_layout()
        
        # Passer à la page des graphiques
        self.ui.stackedWidget.setCurrentWidget(self.graphs_page)

    def setup_interactive_page(self):
        """Configure la page des graphiques interactifs"""
        # Clear any existing widgets in the layout
        if hasattr(self, 'interactive_container'):
            self.interactive_container.deleteLater()
            
        # Create main container widget
        self.interactive_container = QWidget()
        self.interactive_container.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
        """)
        self.interactive_layout = QVBoxLayout(self.interactive_container)
        self.interactive_layout.setSpacing(20)
        self.interactive_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create header section with title and controls
        header_container = QWidget()
        header_container.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 15px;
                max-height: 120px;  # Reduced header height
            }
        """)
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(8)  # Reduced spacing
        header_layout.setContentsMargins(20, 10, 20, 10)  # Reduced vertical margins
        
        # Title and controls in header
        title_row = QHBoxLayout()
        
        # Title
        title_label = QLabel("Visualisation Interactive")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title_row.addWidget(title_label)
        
        # Add spacer to push controls to the right
        title_row.addStretch()
        
        # Controls row
        controls_row = QHBoxLayout()
        controls_row.setSpacing(15)
        controls_row.setAlignment(Qt.AlignCenter)  # Center the controls
        
        # Add some spacing on the left to help with centering
        controls_row.addStretch(1)
        
        # Common styles
        control_style = """
            QComboBox {
                background-color: #3d3d3d;
                color: white;
                border: 2px solid #4d4d4d;
                border-radius: 8px;
                padding: 8px;
                min-width: 180px;
                font-size: 13px;
            }
            QComboBox:hover {
                border-color: #5d5d5d;
                background-color: #454545;
            }
            QComboBox:focus {
                border-color: #007acc;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: url(:/newPrefix/icones/arrow-down.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #3d3d3d;
                color: white;
                selection-background-color: #007acc;
                selection-color: white;
                border: 1px solid #4d4d4d;
            }
        """
        
        # X-axis control group
        x_group = QWidget()
        x_layout = QVBoxLayout(x_group)
        x_label = QLabel("Variable Principale")
        x_label.setStyleSheet("color: #e0e0e0; font-size: 12px;")
        self.x_axis_selector = QComboBox()
        self.x_axis_selector.setStyleSheet(control_style)
        x_layout.addWidget(x_label)
        x_layout.addWidget(self.x_axis_selector)
        controls_row.addWidget(x_group)
        
        # Filter control group
        filter_group = QWidget()
        filter_layout = QVBoxLayout(filter_group)
        filter_label = QLabel("Filtre")
        filter_label.setStyleSheet("color: #e0e0e0; font-size: 12px;")
        self.filter_selector = QComboBox()
        self.filter_selector.setStyleSheet(control_style)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_selector)
        controls_row.addWidget(filter_group)
        
        # Category control group
        cat_group = QWidget()
        cat_layout = QVBoxLayout(cat_group)
        cat_label = QLabel("Catégorie")
        cat_label.setStyleSheet("color: #e0e0e0; font-size: 12px;")
        self.category_selector = QComboBox()
        self.category_selector.setStyleSheet(control_style)
        cat_layout.addWidget(cat_label)
        cat_layout.addWidget(self.category_selector)
        controls_row.addWidget(cat_group)
        
        # Graph type control group
        type_group = QWidget()
        type_layout = QVBoxLayout(type_group)
        type_label = QLabel("Type de Graphique")
        type_label.setStyleSheet("color: #e0e0e0; font-size: 12px;")
        self.graph_type_selector = QComboBox()
        self.graph_type_selector.addItems(["Diagramme en Barres", "Diagramme Circulaire"])
        self.graph_type_selector.setStyleSheet(control_style)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.graph_type_selector)
        controls_row.addWidget(type_group)
        
        # Generate button
        self.generate_button = QPushButton("Générer")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
                min-width: 100px;
                margin-top: 22px;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
            QPushButton:pressed {
                background-color: #005c99;
            }
        """)
        controls_row.addWidget(self.generate_button)
        
        # Add spacing on the right to help with centering
        controls_row.addStretch(1)
        
        # Add rows to header
        header_layout.addLayout(title_row)
        header_layout.addLayout(controls_row)
        
        # Add header to main layout
        self.interactive_layout.addWidget(header_container)
        
        # Create graph container
        graph_container = QWidget()
        graph_container.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 15px;
            }
        """)
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create and style the canvas with fixed size
        self.interactive_canvas = FigureCanvas(plt.figure(figsize=(8, 5), facecolor='#2d2d2d'))  # Smaller figure size
        self.interactive_canvas.setFixedSize(700, 400)  # Smaller fixed size
        self.interactive_canvas.figure.patch.set_facecolor('#2d2d2d')
        graph_layout.addWidget(self.interactive_canvas, alignment=Qt.AlignCenter)  # Center the canvas
        
        # Add graph container to main layout with stretch
        self.interactive_layout.addWidget(graph_container, stretch=1)
        
        # Add the interactive container to the page layout
        self.more_graphs_page.layout().addWidget(self.interactive_container)
        
        # Connect signals
        self.generate_button.clicked.connect(self.generate_interactive_graph)
        
        # Load data and initialize selectors
        self.data = pd.read_csv('dataset.csv')
        self.x_axis_selector.addItems(self.data.columns)
        self.filter_selector.addItems(self.data.columns)
        self.x_axis_selector.currentIndexChanged.connect(self.update_filter_options)
        self.filter_selector.currentIndexChanged.connect(self.update_category_options)
        self.update_filter_options()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update graph sizes when window is resized
        self.update_graph_layout()
        
    def update_graph_layout(self):
        if self.graphs_page.isVisible():
            # Calculate available width
            available_width = self.width()
            if self.ui.left_menu_widget.isVisible():
                available_width -= self.ui.left_menu_widget.width()
            
            # Set scroll content width
            content_width = available_width * 0.95
            self.scroll_content.setMaximumWidth(content_width)
            
            # Update grid layout spacing based on window size
            spacing = max(10, min(20, int(content_width * 0.02)))
            self.grid_layout.setSpacing(spacing)
            
            # Adjust graph sizes if they exist
            if hasattr(self, 'graphs') and self.graphs:
                for graph in self.graphs:
                    # Set minimum size based on window width
                    min_width = max(300, int(content_width * 0.4))
                    min_height = int(min_width * 0.75)
                    graph.setMinimumSize(min_width, min_height)
    
    def create_graphs(self):
        if self.graphs_created:
            return
            
        data = pd.read_csv('dataset.csv')
        
        # Configuration des graphiques
        sns.set(style="whitegrid")
        self.graphs = []  # Store graph references
        
        # Créer 8 graphiques différents
        graphs = []
        
        # 1. Lieux & Type d'activité
        fig1 = plt.figure(figsize=self.current_graph_size)
        sns.countplot(data=data, x='Lieu', hue='Type_activite')
        plt.title("Distribution par lieu et activité")
        canvas1 = FigureCanvas(fig1)
        canvas1.mpl_connect('button_press_event', lambda event: self.show_graph_details(0))
        graphs.append(canvas1)
        
        # 2. Contexte & Type de violence
        fig2 = plt.figure(figsize=self.current_graph_size)
        sns.countplot(data=data, x='Contexte', hue='Type_violence')
        plt.title("Violence par contexte")
        canvas2 = FigureCanvas(fig2)
        canvas2.mpl_connect('button_press_event', lambda event: self.show_graph_details(1))
        graphs.append(canvas2)
        
        # 3. Niveau scolaire & Type d'activité
        fig3 = plt.figure(figsize=self.current_graph_size)
        sns.countplot(data=data, x='Niveau_scolaire', hue='Type_activite')
        plt.title("Activité par niveau scolaire")
        canvas3 = FigureCanvas(fig3)
        canvas3.mpl_connect('button_press_event', lambda event: self.show_graph_details(2))
        graphs.append(canvas3)
        
        # 4. Age & Type de violence
        fig4 = plt.figure(figsize=self.current_graph_size)
        sns.countplot(data=data, x='Age', hue='Type_violence')
        plt.title("Violence par âge")
        canvas4 = FigureCanvas(fig4)
        canvas4.mpl_connect('button_press_event', lambda event: self.show_graph_details(3))
        graphs.append(canvas4)
        
        # 5. État & Contexte
        fig5 = plt.figure(figsize=self.current_graph_size)
        sns.countplot(data=data, x='Etat', hue='Contexte')
        plt.title("Contexte par état civil")
        canvas5 = FigureCanvas(fig5)
        canvas5.mpl_connect('button_press_event', lambda event: self.show_graph_details(4))
        graphs.append(canvas5)
        
        # 6. Proportion des lieux
        fig6 = plt.figure(figsize=self.current_graph_size)
        data['Lieu'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Proportion des lieux")
        canvas6 = FigureCanvas(fig6)
        canvas6.mpl_connect('button_press_event', lambda event: self.show_graph_details(5))
        graphs.append(canvas6)
        
        # 7. Proportion par région
        fig7 = plt.figure(figsize=self.current_graph_size)
        data['Region'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title("Proportion par région")
        canvas7 = FigureCanvas(fig7)
        canvas7.mpl_connect('button_press_event', lambda event: self.show_graph_details(6))
        graphs.append(canvas7)
        
        # 8. Types de violence
        fig8 = plt.figure(figsize=self.current_graph_size)
        sns.countplot(data=data, x='Type_violence')
        plt.title("Distribution des types de violence")
        canvas8 = FigureCanvas(fig8)
        canvas8.mpl_connect('button_press_event', lambda event: self.show_graph_details(7))
        graphs.append(canvas8)
        
        # Ajouter les graphiques à la grille
        for i, graph in enumerate(graphs):
            row = i // 2
            col = i % 2
            # Add the graph to the grid
            self.grid_layout.addWidget(graph, row, col)
            # Style each graph container
            graph.setMinimumSize(400, 300)
            graph.setStyleSheet("background-color: white; border: 1px solid #ddd; border-radius: 5px; cursor: pointer;")
        
        self.graphs = graphs
        self.graphs_created = True
        # Update layout immediately
        self.update_graph_layout()

    def toggle_graphs(self):
        """Toggle the visibility of the statistical graphs."""
        # Hide interactive view if visible
        self.interactive_container.hide()
        
        # Toggle main graphs visibility
        if self.graphs_page.isVisible():
            self.graphs_page.hide()
        else:
            # Hide other containers
            self.code_display.hide()
            self.output_display.hide()
            
            # Show and update graphs
            self.graphs_page.show()
            if not self.graphs_created:
                self.create_graphs()
                self.graphs_created = True
            self.update_graph_layout()

    def toggle_interactive_graphs(self):
        """Toggle the visibility of the interactive visualization."""
        # Hide main graphs if visible
        self.graphs_page.hide()
        
        # Toggle interactive view visibility
        if self.more_graphs_page.isVisible():
            self.more_graphs_page.hide()
        else:
            # Hide other containers
            self.code_display.hide()
            self.output_display.hide()
            
            # Show interactive container
            self.more_graphs_page.show()
    
    def execute_more(self):
        # Store current graph width before hiding
        if self.graphs_page.isVisible():
            self.previous_width = self.scroll_content.maximumWidth()
            
        self.ui.stackedWidget.setCurrentIndex(1)  # Go to page 2
        
        # Hide graphs and show output
        self.graphs_page.hide()
        self.output_display.show()
        self.output_display.clear()  # Clear previous output
        
        try:
            # Execute more.py and capture its output
            process = subprocess.Popen(['python', 'more.py'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    cwd=os.path.dirname(os.path.abspath(__file__)))
            
            stdout, stderr = process.communicate()
            
            # Display the output
            if stdout:
                self.output_display.append("=== Program Output ===\n")
                self.output_display.append(stdout)
            
            # Display any errors
            if stderr:
                self.output_display.append("\n=== Errors ===\n")
                self.output_display.append(stderr)
                
        except Exception as e:
            self.output_display.append(f"Error executing more.py: {str(e)}")
        
        # Add a button to go back to graphs if it doesn't exist
        if not hasattr(self, 'back_button'):
            self.back_button = QPushButton("Back to Graphs")
            self.back_button.setStyleSheet("""
                QPushButton {
                    background-color: #800000;
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #a00000;
                }
            """)
            self.back_button.clicked.connect(self.toggle_graphs)
            self.ui.page_2.layout().addWidget(self.back_button)
        
        self.back_button.show()

    def toggle_menu(self):
        """Toggle the visibility of the left menu."""
        if self.ui.left_menu_widget.isVisible():
            self.ui.left_menu_widget.hide()
        else:
            self.ui.left_menu_widget.show()
        self.update_graph_layout()

    def mousePressEvent(self, event):
        """Handle mouse press events for window dragging."""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move events for window dragging."""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events for window dragging."""
        self.dragging = False
        event.accept()
            
    def toggle_maximize(self):
        """Toggle between maximized and normal window state."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        # Update graph layout after maximize/restore
        self.update_graph_layout()
    
    def update_filter_options(self):
        """Update available filter options based on selected X-axis variable."""
        selected_x_axis = self.x_axis_selector.currentText()
        self.filter_selector.clear()
        available_filters = [col for col in self.data.columns if col != selected_x_axis]
        self.filter_selector.addItems(available_filters)
        self.update_category_options()

    def update_category_options(self):
        """Update available category options based on selected filter."""
        selected_filter = self.filter_selector.currentText()
        if selected_filter:
            unique_categories = self.data[selected_filter].dropna().unique()
            self.category_selector.clear()
            self.category_selector.addItems(map(str, unique_categories))

    def generate_interactive_graph(self):
        """Generate and display the interactive graph based on selected options."""
        try:
            # Get selected values
            x_feature = self.x_axis_selector.currentText()
            filter_feature = self.filter_selector.currentText()
            graph_type = self.graph_type_selector.currentText()
            selected_category = self.category_selector.currentText()

            # Clear previous figure
            self.interactive_canvas.figure.clf()
            ax = self.interactive_canvas.figure.subplots()
            ax.set_facecolor('#2d2d2d')
            
            # Set style for better visibility in dark theme
            plt.style.use('dark_background')
            
            if graph_type == "Diagramme en Barres":
                self.plot_interactive_bar(ax, x_feature, filter_feature)
            elif graph_type == "Diagramme Circulaire":
                self.plot_interactive_pie(ax, x_feature, filter_feature, selected_category)
            
            # Update the canvas
            self.interactive_canvas.draw()
            
        except Exception as e:
            # Show error message if something goes wrong
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Erreur")
            error_dialog.setText("Une erreur s'est produite lors de la génération du graphique")
            error_dialog.setDetailedText(str(e))
            error_dialog.exec_()

    def plot_interactive_bar(self, ax, x_feature, filter_feature):
        """Plot an interactive bar graph."""
        try:
            # Group data by the filter feature and calculate frequencies for the x feature
            filtered_data = self.data.groupby(filter_feature)[x_feature].value_counts().unstack(fill_value=0)

            # Plot each category in the filter as a separate bar group
            filtered_data.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')
            
            # Customize the plot for dark theme
            ax.set_title(f"Fréquence de {x_feature} par {filter_feature}", 
                        color='white', pad=20, fontsize=14)
            ax.set_xlabel(x_feature, color='white', labelpad=10)
            ax.set_ylabel("Fréquence", color='white', labelpad=10)
            
            # Rotate x-axis labels for better readability
            ax.tick_params(axis='both', colors='white')
            plt.xticks(rotation=45, ha='right')
            
            # Add legend with custom style
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Adjust layout to prevent label cutoff
            plt.tight_layout()
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création du graphique en barres: {str(e)}")

    def plot_interactive_pie(self, ax, x_feature, filter_feature, selected_category):
        """Plot an interactive pie chart."""
        try:
            # Filter the data for the selected category
            if selected_category:
                category_data = self.data[self.data[filter_feature] == selected_category]
                pie_data = category_data[x_feature].value_counts()

                if not pie_data.empty:
                    # Create pie chart with custom colors
                    wedges, texts, autotexts = ax.pie(pie_data, 
                                                    labels=pie_data.index,
                                                    autopct='%1.1f%%',
                                                    textprops={'color': 'white'},
                                                    colors=plt.cm.Pastel1(np.linspace(0, 1, len(pie_data))))
                    
                    # Customize the plot
                    ax.set_title(f"Répartition de {x_feature}\npour {filter_feature}: {selected_category}", 
                                color='white', pad=20, fontsize=14)
                    
                    # Add legend with custom style
                    ax.legend(wedges, pie_data.index,
                            title=x_feature,
                            loc="center left",
                            bbox_to_anchor=(1, 0, 0.5, 1))
                else:
                    ax.text(0.5, 0.5, "Aucune donnée disponible pour cette catégorie.",
                           color='white', fontsize=12, ha='center', va='center')
                
                # Adjust layout to prevent label cutoff
                plt.tight_layout()
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création du graphique circulaire: {str(e)}")

    def show_graph_details(self, graph_index):
        # Hide all graphs in the grid
        for graph in self.graphs:
            graph.hide()
        
        def create_graph(index):
            # Create a graph with adjusted size
            data = pd.read_csv('dataset.csv')
            fig = plt.figure(figsize=(7, 3.5))  # Even smaller size for better fit
            
            if index == 0:
                sns.countplot(data=data, x='Lieu', hue='Type_activite')
                plt.title("Distribution par lieu et activité", fontsize=11)
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
                if plt.legend() is not None:
                    plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
            elif index == 1:
                sns.countplot(data=data, x='Contexte', hue='Type_violence')
                plt.title("Violence par contexte", fontsize=11)
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
                if plt.legend() is not None:
                    plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
            elif index == 2:
                sns.countplot(data=data, x='Niveau_scolaire', hue='Type_activite')
                plt.title("Activité par niveau scolaire", fontsize=11)
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
                if plt.legend() is not None:
                    plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
            elif index == 3:
                sns.countplot(data=data, x='Age', hue='Type_violence')
                plt.title("Violence par âge", fontsize=11)
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
                if plt.legend() is not None:
                    plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
            elif index == 4:
                sns.countplot(data=data, x='Etat', hue='Contexte')
                plt.title("Contexte par état civil", fontsize=11)
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
                if plt.legend() is not None:
                    plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
            elif index == 5:
                data['Lieu'].value_counts().plot(kind='pie', autopct='%1.1f%%', textprops={'fontsize': 8})
                plt.title("Proportion des lieux", fontsize=11)
            elif index == 6:
                data['Region'].value_counts().plot(kind='pie', autopct='%1.1f%%', textprops={'fontsize': 8})
                plt.title("Proportion par région", fontsize=11)
            else:
                sns.countplot(data=data, x='Type_violence')
                plt.title("Distribution des types de violence", fontsize=11)
                plt.xticks(rotation=45, fontsize=8)
                plt.yticks(fontsize=8)
            
            plt.tight_layout(pad=1.0)
            return fig
        
        # Create initial graph
        current_index = graph_index
        fig = create_graph(current_index)
        canvas = FigureCanvas(fig)
        
        # Create description text with smaller font and less padding
        description_widget = QLabel(self.graph_descriptions[current_index])
        description_widget.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                color: #333;
                padding: 8px;
                border-radius: 5px;
                font-size: 11px;
                line-height: 1.2;
                margin: 5px;
                border: 1px solid #ddd;
                max-height: 80px;
            }
        """)
        description_widget.setWordWrap(True)
        description_widget.setAlignment(Qt.AlignJustify)
        
        # Create a container for the graph and description with fixed height
        container = QWidget()
        container.setFixedHeight(450)  # Set fixed height for the container
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(5)  # Reduce spacing
        container_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
        
        # Add widgets to container
        container_layout.addWidget(canvas, stretch=7)  # Give more space to the graph
        container_layout.addWidget(description_widget, stretch=2)  # Give less space to description
        
        self.grid_layout.addWidget(container, 0, 0, 4, 2)
        
        # Create navigation buttons container with reduced height
        nav_widget = QWidget()
        nav_widget.setFixedHeight(50)  # Set fixed height for navigation
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(5, 0, 5, 5)  # Reduce margins
        
        # Create navigation buttons with smaller size
        prev_button = QPushButton("← Précédent")
        next_button = QPushButton("Suivant →")
        back_button = QPushButton("Retour aux graphiques")
        
        # Style the buttons with smaller size
        button_style = """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                font-size: 12px;
                margin: 5px;
                min-width: 100px;
                max-height: 30px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """
        prev_button.setStyleSheet(button_style)
        next_button.setStyleSheet(button_style)
        back_button.setStyleSheet(button_style)
        
        # Add buttons to navigation layout
        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(back_button)
        nav_layout.addWidget(next_button)
        
        # Add navigation widget to main layout
        self.grid_layout.addWidget(nav_widget, 4, 0, 1, 2, Qt.AlignCenter)
        
        def update_nav_buttons():
            prev_button.setEnabled(current_index > 0)
            next_button.setEnabled(current_index < len(self.graph_titles) - 1)
        
        def show_prev():
            nonlocal current_index, container, canvas, description_widget
            current_index -= 1
            # Remove current container
            container.setParent(None)
            # Create and show new graph with description
            fig = create_graph(current_index)
            canvas = FigureCanvas(fig)
            description_widget = QLabel(self.graph_descriptions[current_index])
            description_widget.setStyleSheet("""
                QLabel {
                    background-color: #f5f5f5;
                    color: #333;
                    padding: 8px;
                    border-radius: 5px;
                    font-size: 11px;
                    line-height: 1.2;
                    margin: 5px;
                    border: 1px solid #ddd;
                    max-height: 80px;
                }
            """)
            description_widget.setWordWrap(True)
            description_widget.setAlignment(Qt.AlignJustify)
            
            container = QWidget()
            container.setFixedHeight(450)  # Set fixed height for the container
            container_layout = QVBoxLayout(container)
            container_layout.setSpacing(5)  # Reduce spacing
            container_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
            
            # Add widgets to container
            container_layout.addWidget(canvas, stretch=7)  # Give more space to the graph
            container_layout.addWidget(description_widget, stretch=2)  # Give less space to description
            
            self.grid_layout.addWidget(container, 0, 0, 4, 2)
            update_nav_buttons()
        
        def show_next():
            nonlocal current_index, container, canvas, description_widget
            current_index += 1
            # Remove current container
            container.setParent(None)
            # Create and show new graph with description
            fig = create_graph(current_index)
            canvas = FigureCanvas(fig)
            description_widget = QLabel(self.graph_descriptions[current_index])
            description_widget.setStyleSheet("""
                QLabel {
                    background-color: #f5f5f5;
                    color: #333;
                    padding: 8px;
                    border-radius: 5px;
                    font-size: 11px;
                    line-height: 1.2;
                    margin: 5px;
                    border: 1px solid #ddd;
                    max-height: 80px;
                }
            """)
            description_widget.setWordWrap(True)
            description_widget.setAlignment(Qt.AlignJustify)
            
            container = QWidget()
            container.setFixedHeight(450)  # Set fixed height for the container
            container_layout = QVBoxLayout(container)
            container_layout.setSpacing(5)  # Reduce spacing
            container_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins
            
            # Add widgets to container
            container_layout.addWidget(canvas, stretch=7)  # Give more space to the graph
            container_layout.addWidget(description_widget, stretch=2)  # Give less space to description
            
            self.grid_layout.addWidget(container, 0, 0, 4, 2)
            update_nav_buttons()
        
        def restore_graphs():
            # Remove the large graph and navigation
            container.setParent(None)
            nav_widget.setParent(None)
            # Show all original graphs
            for graph in self.graphs:
                graph.show()
        
        # Connect button signals
        prev_button.clicked.connect(show_prev)
        next_button.clicked.connect(show_next)
        back_button.clicked.connect(restore_graphs)
        
        # Initialize button states
        update_nav_buttons()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
