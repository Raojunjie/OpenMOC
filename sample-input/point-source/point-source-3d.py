import openmoc
import openmoc.log as log
import openmoc.plotter as plotter
from openmoc.options import Options
from geometry import geometry

###############################################################################
#                          Main Simulation Parameters
###############################################################################

options = Options()

num_threads = options.getNumThreads()
azim_spacing = options.getAzimSpacing()
num_azim = options.getNumAzimAngles()
polar_spacing = options.getPolarSpacing()
num_polar = options.getNumPolarAngles()
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()


###############################################################################
#                          Creating the TrackGenerator
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = openmoc.TrackGenerator(geometry, num_azim, num_polar,
                                         azim_spacing, polar_spacing)
track_generator.setNumThreads(num_threads)
track_generator.generateTracks()


###############################################################################
#                            Running a Simulation
###############################################################################

solver = openmoc.CPUSolver(track_generator)
solver.setNumThreads(num_threads)
solver.setConvergenceThreshold(tolerance)
solver.setFixedSourceByCell(source_cell, 1, 1.0)
solver.computeSource(max_iters)
solver.printTimerReport()


###############################################################################
#                             Generating Plots
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

plotter.plot_materials(geometry, gridsize=250)
plotter.plot_cells(geometry, gridsize=250)
plotter.plot_flat_source_regions(geometry, gridsize=250)
plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')
