import sys

import h5py
import pyqtgraph as pg
import numpy as np

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from reinforcement_learning.agents.agent2d import Agent2D


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LArTPC DLP viewer")
        self.resize(900, 1000)

        self.file = h5py.File("runs/dlp_multi/job_0000/dlp.h5", "r")
        
        self.agent = Agent2D(model=None, environment=None)

        # do not assume event numbers are continuous because some events may have been dropped by the thresholding
        self.events = sorted(
            key
            for key in self.file.keys()
            if key.startswith("event_")
        )

        self.event_index = 0
        
        event_name = self.events[self.event_index]
        event = self.file[event_name]
        track_id = 0
        particle = event["particles"][track_id]
        start_mm = particle["first_step_in_crop"][:3]
        origin = event.attrs["crop_origin_mm"]
        start_voxel = np.floor((start_mm - origin) / 5.0).astype(int)
        x, y, z = start_voxel
        self.agent_positions = [
            (x, y),   # XY
            (y, z),   # YZ
            (z, x),   # ZX
        ]

        self.projections = [
            ("XY", "X", "Y"),
            ("YZ", "Y", "Z"),
            ("ZX", "Z", "X"),
        ]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.image_items = []
        self.agent_items = []

        for projection_name, axis_x, axis_y in self.projections:
            plot = pg.PlotWidget()

            plot.setTitle(f"Image - {projection_name}")
            plot.setAspectLocked(True)

            # col-major order is used to match the orientation of the image2d data
            image_item = pg.ImageItem(axisOrder="col-major")
            plot.addItem(image_item)
            
            # col-major order is used to match the orientation of the image2d data
            agent_item = pg.ImageItem(axisOrder="col-major")
            plot.addItem(agent_item)

            plot.setLabel("bottom", f"{axis_x} voxel")
            plot.setLabel("left", f"{axis_y} voxel")

            plot.setXRange(0, 256, padding=0)
            plot.setYRange(0, 256, padding=0)

            main_layout.addWidget(plot)

            self.image_items.append(image_item)
            self.agent_items.append(agent_item)
        self.move_agent_button = QPushButton("Move Agent")
        self.move_agent_button.clicked.connect(self.move_agent)
        main_layout.addWidget(self.move_agent_button)

        self.next_button = QPushButton("Next Event")
        self.next_button.clicked.connect(self.next_event)
        main_layout.addWidget(self.next_button)

        self.show_event()


    def show_event(self):
        event_name = self.events[self.event_index]

        event = self.file[event_name]

        # Shape: (3, 256, 256)
        image2d = event["image2d"][:]

        for projection_index in range(3):
            image = image2d[projection_index]

            self.image_items[projection_index].setImage(image, autoLevels=True)
            
            overlay = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

            i, j = self.agent_positions[projection_index]

            # red pixel: R, G, B, alpha
            # made slightly bigger to make it more visible
            overlay[i-1:i+2, j-1:j+2] = [255, 0, 0, 255]

            self.agent_items[projection_index].setImage(overlay, autoLevels=False)

        event_id = event.attrs["event_id"]

        self.setWindowTitle(f"LArTPC DLP viewer - {event_name} - event_id={event_id}")

    def move_agent(self):
        event_name = self.events[self.event_index]
        event = self.file[event_name]

        # Shape: (3, 256, 256)
        image2d = event["image2d"][:]
        
        for projection_index in range(3):
            i, j = self.agent_positions[projection_index]
            action = self.agent.act(image2d[projection_index][i-1:i+2, j-1:j+2])
            if action is None:
                continue
            dx, dy = action
            new_i = i + dx
            new_j = j + dy
            self.agent_positions[projection_index] = (new_i, new_j)
            print(new_i, new_j)
            
        self.show_event()

    def next_event(self):
        self.event_index += 1

        if self.event_index >= len(self.events):
            self.event_index = 0
            
        event_name = self.events[self.event_index]
        event = self.file[event_name]
        track_id = 0
        particle = event["particles"][track_id]
        start_mm = particle["first_step_in_crop"][:3]
        origin = event.attrs["crop_origin_mm"]
        start_voxel = np.floor((start_mm - origin) / 5.0).astype(int)
        x, y, z = start_voxel
        self.agent_positions = [
            (x, y),   # XY
            (y, z),   # YZ
            (z, x),   # ZX
        ]

        self.show_event()


    def closeEvent(self, event):
        self.file.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())