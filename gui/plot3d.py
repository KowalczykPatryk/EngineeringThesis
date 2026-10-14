import pyvista as pv
from pyvistaqt import QtInteractor


class Plot3D:
    def __init__(self, event, parent):
        self._event = event
        
        # PyVista widget embedded inside PySide6
        # QtInteractor is a QWidget that inherits from PyVista BasePlotter and a QVTKRenderWindowInteractor
        self.plotter = QtInteractor(parent)
        # https://github.com/pyvista/pyvista/blob/release/0.49/pyvista/plotting/plotter.py#L8260-L9095
        self.plotter.add_text("3D Event Viewer", color="gray", font_size=8, position="upper_left")
        
        # Coordinate axes with numeric values
        # https://docs.pyvista.org/api/plotting/_autosummary/pyvista.renderer.show_bounds
        self.plotter.show_grid(
            xtitle="X axis",
            ytitle="Y axis",
            ztitle="Z axis",
        )

        # Small XYZ orientation indicator at the bottom left corner of the window
        self.plotter.add_axes(
            xlabel="X",
            ylabel="Y",
            zlabel="Z",
        )
        
    @property
    def event(self):
        return self._event
    
    @event.setter
    def event(self, event):
        self._event = event
        
    def show(self):
        # https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.remove_actor
        self.plotter.remove_actor("3d_vertex_cloud")
        
        self.coords = self._event["voxels/coords"][:]
        self.energy = self._event["voxels/energy"][:]
        # Converting NumPy array to PyVista point cloud
        self.cloud = pv.PolyData(self.coords.astype(float))  # PyVista expects float coordinates

        # https://docs.pyvista.org/examples/00-load/create_point_cloud
        self.cloud["energy"] = self.energy  # Adding energy as a point data array

        # Draw points
        # https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.add_mesh
        # https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.add_scalar_bar
        self.plotter.add_mesh(
            self.cloud,
            scalars="energy",
            style="points",
            name="3d_vertex_cloud",
            point_size=5,
            scalar_bar_args={
                "title": "Energy [MeV]"
                },
        )
        # Set the camera to an isometric view and reset it to fit the scene
        # The isometric view is a type of projection where the angles between the projection of the axes are equal (120 degrees)
        self.plotter.view_isometric()
        self.plotter.reset_camera()