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
                
        pg.setConfigOption("background", "w")
        self.plot_widget = pg.PlotWidget()


        self.plot_widget.setTitle(f"Image - {self.projection_name}")
        #self.plot_widget.setAspectLocked(True)

        # col-major order is used to match the orientation of the image2d data
        self.image_item = pg.ImageItem(axisOrder="col-major")
        # https://github.com/pyqtgraph/pyqtgraph/tree/master/pyqtgraph/colors/maps
        # https://pyqtgraph.readthedocs.io/en/latest/api_reference/colormap.html#pyqtgraph.colormap.get
        viridis = pg.colormap.get("viridis")
        self.image_item.setColorMap(viridis)
        self.plot_widget.addItem(self.image_item)
        
        # https://pyqtgraph.readthedocs.io/en/latest/api_reference/colormap.html#pyqtgraph.ColorMap.getLookupTable
        viridis_lut = viridis.getLookupTable(
            # from 0.0 to 1.0 means sample all of the colormap, from start to stop
            start=0.0, # which part of the colormap is sampled (start)
            stop=1.0, # which part of the colormap is sampled (stop)
            nPts=255,
            alpha=True,
        )

        # shape means for each of the nPts, we have 4 values (RGBA)
        colors_lut = np.empty((256, 4), dtype=np.ubyte)

        colors_lut[0] = [255, 255, 255, 255]  # opaque white for background
        colors_lut[1:] = viridis_lut
        
        positions = np.linspace(0.0, 1.0, 256)

        # https://pyqtgraph.readthedocs.io/en/latest/api_reference/colormap.html#pyqtgraph.ColorMap
        # In this case, we are creating a custom colormap that starts with opaque white for the background and then transitions to the viridis colormap for the rest of the values
        self.custom_cmap = pg.ColorMap(
            positions,
            colors_lut,
        )
        
        # dividing colors by 256 was chosen randomly and could be any relatively big number

        self.image_item.setColorMap(self.custom_cmap)
        
        # https://pyqtgraph.readthedocs.io/en/latest/api_reference/graphicsItems/plotitem.html
        # https://pyqtgraph.readthedocs.io/en/latest/api_reference/graphicsItems/colorbaritem.html#pyqtgraph.ColorBarItem
        self.color_bar = self.plot_widget.getPlotItem().addColorBar(
            self.image_item,
            colorMap=self.custom_cmap,
            label="Energy [MeV]",
            width=15,
            interactive=False,
        )

        # col-major order is used to match the orientation of the image2d data
        self.agents_item = pg.ImageItem(axisOrder="col-major")
        self.plot_widget.addItem(self.agents_item)

        self.plot_widget.setLabel("bottom", f"{self.axis_1} axis")
        self.plot_widget.setLabel("left", f"{self.axis_2} axis")
        
        plot_item = self.plot_widget.getPlotItem()
        view_box = plot_item.getViewBox()       
        view_box.setRange(
            xRange=(0, 256),
            yRange=(0, 256),
            padding=0,
        )
        
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
        
        self.color_bar.setLevels(values=(0, self.image.max() / 100))  # The image is divided by 100 to match the scale of 3D plot and true energy values
        
        # The image is divided by 100 to match the scale of 3D plot and true energy values
        self.image_item.setImage(self.image / 100, autoLevels=True)
        
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
        
    def make_view_box_square(self):
        plot_item = self.plot_widget.getPlotItem()
        view_box = plot_item.getViewBox()
        layout = plot_item.layout

        # size = min(view_box.width(), view_box.height())

        # # ViewBox is in row 2, column 1
        # layout.setColumnFixedWidth(1, size)
        # layout.setRowFixedHeight(2, size)

        # layout.invalidate()
        # layout.activate()

        # self.plot_widget.setFixedWidth(
        #     plot_item.width()
        # )

        # let the ViewBox row consume available vertical space.
        layout.setRowStretchFactor(2, 1)

        layout.invalidate()
        layout.activate()

        size = view_box.height()

        layout.setColumnFixedWidth(1, size)

        layout.invalidate()
        layout.activate()
        
        self.plot_widget.setFixedWidth(
            plot_item.width()
        )
        
