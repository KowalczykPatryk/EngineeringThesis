import pyvista as pv
from pyvistaqt import QtInteractor


class Plot3D:
    def __init__(self, event, parent):
        self._event = event
        
        # PyVista widget embedded inside PySide6
        # QtInteractor is a QWidget that inherits from PyVista BasePlotter and a QVTKRenderWindowInteractor
        self.plotter = QtInteractor(parent)
        
    @property
    def event(self):
        return self._event
    
    @event.setter
    def event(self, event):
        self._event = event
        
    def show(self):
        self.plotter.clear()
        coords = self._event["voxels/coords"][:]
        energy = self._event["voxels/energy"][:]
        # Converting NumPy array to PyVista point cloud
        cloud = pv.PolyData(coords.astype(float))  # PyVista expects float coordinates

        # https://docs.pyvista.org/examples/00-load/create_point_cloud
        cloud["energy"] = energy  # Adding energy as a point data array

        # Draw points
        # https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.add_mesh
        # https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotter.add_scalar_bar
        self.plotter.add_mesh(
            cloud,
            scalars="energy",
            style="points",
            point_size=5,
            scalar_bar_args={
                "title": "Energy [MeV]"
                },
        )

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

        # Set the camera to an isometric view and reset it to fit the scene
        # The isometric view is a type of projection where the angles between the projection of the axes are equal (120 degrees)
        self.plotter.view_isometric()
        self.plotter.reset_camera()