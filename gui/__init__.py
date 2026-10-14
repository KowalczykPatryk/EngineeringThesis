import os

import pyvista as pv

# it is needed because PyVistaQt uses QtPy which is
# a compatibility layer that lets Python programs work with different Qt bindings
os.environ["QT_API"] = "pyside6"

# https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotting.themes._colorbarconfig
# https://docs.pyvista.org/api/plotting/_autosummary/pyvista.plotting.themes.theme
pv.global_theme.colorbar_orientation = "vertical"
pv.global_theme.colorbar_vertical.width = 0.05
pv.global_theme.colorbar_vertical.height = 0.5
pv.global_theme.colorbar_vertical.position_x = 0.92
pv.global_theme.font.size = 10
pv.global_theme.font.label_size = 10
pv.global_theme.font.title_size = 12