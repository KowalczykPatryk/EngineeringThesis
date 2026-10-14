'''
This module contains the main window of the application.
Layout of the application is visualized in the APP_LAYOUT.md file.
'''

import h5py
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.plot2d import Plot2D
from gui.plot3d import Plot3D


class MainWindow(QMainWindow):
    def __init__(self, source_file_path, window_title):
        super().__init__()
        self.source_file_path = source_file_path

        self.setWindowTitle(window_title)

        self.file = h5py.File(self.source_file_path, "r")

        # I do not assume event numbers are continuous because some events may have been dropped by the thresholding
        self.events_names = sorted(
            key for key in self.file if key.startswith("event_")
        )
        
        self.events_numbers = [key.split("_")[1] for key in self.events_names]

        self.event_index = 0

        event_name = self.events_names[self.event_index]
        event = self.file[event_name]
        

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.l0 = QVBoxLayout()
        self.l0.setObjectName("l0")
        self.central_widget.setLayout(self.l0)

        self.l1 = QHBoxLayout()
        self.l1.setObjectName("l1")
        self.l0.addLayout(self.l1)
        
        self.l5 = QVBoxLayout()
        self.l5.setObjectName("l5")
        self.l1.addLayout(self.l5)

        self.plot3d = Plot3D(event, parent=self.central_widget)

        self.l5.addWidget(self.plot3d.plotter.interactor)

        self.l2 = QVBoxLayout()
        self.l1.addLayout(self.l2)
        self.l1.addStretch(1)

        self.plots2D = []

        for projection_idx, _ in enumerate(Plot2D.PROJECTIONS):
            plot = Plot2D(event, projection_idx)
            self.plots2D.append(plot)

            self.l2.addWidget(plot.plot_widget)

        self.l3 = QVBoxLayout()
        self.l3.setObjectName("l3")
        self.l0.addLayout(self.l3)
        self.event_label = QLabel("Event No.")
        self.event_label.setObjectName("event_label")
        self.l6 = QHBoxLayout()
        self.l6.setObjectName("l6")
        # adding stretchable space before and after the label to center it in the layout
        self.l6.addStretch(1)
        self.l6.addWidget(self.event_label)
        self.l6.addStretch(1)
        self.l3.addLayout(self.l6)

        self.l4 = QHBoxLayout()
        self.l4.setObjectName("l4")
        self.l3.addLayout(self.l4)
        self.prev_event_button = QPushButton("<")
        self.prev_event_button.setObjectName("prev_event_button")
        self.prev_event_button.clicked.connect(lambda: self.set_current_event(self.event_index - 1))
        self.combo_box = QComboBox()
        self.combo_box.setObjectName("combo_box")
        self.combo_box.addItems(self.events_numbers)
        # make the combo box editable because without it setMaxVisibleItems() does not work
        self.combo_box.setEditable(True)
        self.combo_box.setMaxVisibleItems(7)
        # make line edit read-only because I don't want free-form typing
        self.combo_box.lineEdit().setReadOnly(True)
        self.combo_box.currentIndexChanged.connect(lambda: self.set_current_event(self.combo_box.currentIndex()))
        self.next_event_button = QPushButton(">")
        self.next_event_button.setObjectName("next_event_button")
        self.next_event_button.clicked.connect(lambda: self.set_current_event(self.event_index + 1))
        self.l4.addStretch(1)
        self.l4.addWidget(self.prev_event_button)
        self.l4.addWidget(self.combo_box)
        self.l4.addWidget(self.next_event_button)
        self.l4.addStretch(1)

        self.plot3d.show()
        for plot in self.plots2D:
            plot.show_image()

    def set_current_event(self, idx):
        self.event_index = idx

        if self.event_index >= len(self.events_names):
            self.event_index = len(self.events_names) - 1
        elif self.event_index < 0:
            self.event_index = 0
            
        self.combo_box.setCurrentIndex(self.event_index)

        event_name = self.events_names[self.event_index]
        event = self.file[event_name]

        for plot in self.plots2D:
            plot.event = event
            plot.show_image()
        self.plot3d.event = event
        self.plot3d.show()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.plot3d.plotter.setMinimumWidth(event.size().width() // 2)

    def closeEvent(self, event):
        self.file.close()
        super().closeEvent(event)
