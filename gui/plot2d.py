import numpy as np
import pyqtgraph as pg
from reinforcement_learning.agents.agent2d import Agent2D

class Plot2D:
    PROJECTIONS = (
            ("XY", "X", "Y"),
            ("YZ", "Y", "Z"),
            ("ZX", "Z", "X"),
        )
    def __init__(self, event, projection_idx):
        self._event = event
        self.projection_idx = projection_idx
        self.projection_name = self.PROJECTIONS[projection_idx][0]
        self.axis_1 = self.PROJECTIONS[projection_idx][1]
        self.axis_2 = self.PROJECTIONS[projection_idx][2]
                
        self.plot_widget = pg.PlotWidget()

        self.plot_widget.setTitle(f"Image - {self.projection_name}")
        self.plot_widget.setAspectLocked(True)

        # col-major order is used to match the orientation of the image2d data
        self.image_item = pg.ImageItem(axisOrder="col-major")
        self.plot_widget.addItem(self.image_item)

        # col-major order is used to match the orientation of the image2d data
        self.agents_item = pg.ImageItem(axisOrder="col-major")
        self.plot_widget.addItem(self.agents_item)

        self.plot_widget.setLabel("bottom", f"{self.axis_1} pixels")
        self.plot_widget.setLabel("left", f"{self.axis_2} pixels")

        self.plot_widget.setXRange(0, 256, padding=0)
        self.plot_widget.setYRange(0, 256, padding=0)
        
        self.agents = []
        for _ in range(len([particle for particle in self._event["particles"] if particle["is_primary"]])):
            self.agents.append(Agent2D(model=None, environment=None))
        
    def axis_label_to_idx(self, axis_label):
        if axis_label == "X":
            return 0
        elif axis_label == "Y":
            return 1
        elif axis_label == "Z":
            return 2
        else:
            raise ValueError("Invalid axis label")

    @property
    def event(self):
        return self._event
    
    @event.setter
    def event(self, event):
        self._event = event
        
    def show_image(self):
        
        # Shape: (3, 256, 256)
        images2d = self._event["image2d"][:]

        self.image = images2d[self.projection_idx]
        self.image_item.setImage(self.image, autoLevels=True)
        self.update_agents_image()
        
    def move_agents(self):
        # Shape: (3, 256, 256)
        images2d = self._event["image2d"][:]

        for idx, (i, j) in enumerate(self.agents_positions):
            action = self.agents[idx].act(
                images2d[self.projection_idx][i - 1 : i + 2, j - 1 : j + 2]
            )
            if action is None:
                return
            dx, dy = action
            new_i = i + dx
            new_j = j + dy
            self.agents_positions[idx] = (new_i, new_j)
            print(new_i, new_j)

        self.update_agents_image()
        
    def update_agents_image(self):
                
        self.agents_positions = []
        for track_id in range(len(self._event["particles"])):
            particle = self._event["particles"][track_id]
            if not particle["is_primary"]:
                continue
            start_mm = particle["first_step_in_crop"][:3]
            origin = self._event.attrs["crop_origin_mm"]
            start_voxel = np.floor((start_mm - origin) / 5.0).astype(int)
            self.agents_positions.append(
                (start_voxel[self.axis_label_to_idx(self.axis_1)], start_voxel[self.axis_label_to_idx(self.axis_2)])
            )
            
        overlay = np.zeros((self.image.shape[0], self.image.shape[1], 4), dtype=np.uint8)

        for i, j in self.agents_positions:
            # red pixel: R, G, B, alpha
            # made slightly bigger to make it more visible
            overlay[i - 1 : i + 2, j - 1 : j + 2] = [255, 0, 0, 255]

        self.agents_item.setImage(overlay, autoLevels=False)
