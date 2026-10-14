import os

# it is needed because PyVistaQt uses QtPy which is
# a compatibility layer that lets Python programs work with different Qt bindings
os.environ["QT_API"] = "pyside6"

import h5py
from PySide6.QtWidgets import (
    QHBoxLayout,
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
        self.showMaximized()

        self.file = h5py.File(self.source_file_path, "r")

        # do not assume event numbers are continuous because some events may have been dropped by the thresholding
        self.events_names = sorted(
            key for key in self.file if key.startswith("event_")
        )

        self.event_index = 0

        event_name = self.events_names[self.event_index]
        event = self.file[event_name]
        

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        central_widget.setLayout(main_layout)

        all_plots_layout = QHBoxLayout(central_widget)
        main_layout.addLayout(all_plots_layout)

        self.plot3d = Plot3D(event, parent=central_widget)

        all_plots_layout.addWidget(self.plot3d.plotter.interactor)

        right_layout = QVBoxLayout(central_widget)
        all_plots_layout.addLayout(right_layout)

        self.plots2D = []

        for projection_idx, _ in enumerate(Plot2D.PROJECTIONS):
            plot = Plot2D(event, projection_idx)
            self.plots2D.append(plot)

            right_layout.addWidget(plot.plot_widget)

        self.switch_event_layout = QHBoxLayout(central_widget)
        main_layout.addLayout(self.switch_event_layout)
        self.event_label = QPushButton(f"Event: {event_name}")
        self.prev_event_button = QPushButton("<")
        self.prev_event_button.clicked.connect(lambda: self.set_current_event(self.event_index - 1))
        main_layout.addWidget(self.prev_event_button)
        self.next_event_button = QPushButton(">")
        self.next_event_button.clicked.connect(lambda: self.set_current_event(self.event_index + 1))
        self.switch_event_layout.addWidget(self.event_label)
        self.switch_event_layout.addWidget(self.prev_event_button)
        self.switch_event_layout.addWidget(self.next_event_button)


        self.plot3d.show()
        for plot in self.plots2D:
            plot.show_image()

    def set_current_event(self, idx):
        self.event_index = idx

        if self.event_index >= len(self.events_names):
            self.event_index = len(self.events_names) - 1
        elif self.event_index < 0:
            self.event_index = 0

        event_name = self.events_names[self.event_index]
        self.event_label.setText(f"Event: {event_name}")
        event = self.file[event_name]

        for plot in self.plots2D:
            plot.event = event
            plot.show_image()
        self.plot3d.event = event
        self.plot3d.show()

    def closeEvent(self, event):
        self.file.close()
        super().closeEvent(event)
