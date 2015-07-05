from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
from openmoc.options import Options
from cells import *

###############################################################################
#######################   Main Simulation Parameters   ########################
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
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating Takeda core...')

c = core
v = void
a = control_rod
r = reflector

lattice = Lattice(name='4x4 lattice')
lattice.setWidth(width_x=5.0/refines, width_y=5.0/refines, width_z=5.0/refines)
template = [[[r, r, r, r, r],
             [r, r, r, r, r],
             [r, r, r, r, r],
             [r, r, r, r, r],
             [r, r, r, v, r]],
            [[r, r, r, r, r],
             [r, r, r, r, r],
             [r, r, r, r, r],
             [r, r, r, r, r],
             [r, r, r, v, r]],
            [[r, r, r, r, r],
             [r, r, r, r, r],
             [c, c, c, r, r],
             [c, c, c, r, r],
             [c, c, c, v, r]],
            [[r, r, r, r, r],
             [r, r, r, r, r],
             [c, c, c, r, r],
             [c, c, c, r, r],
             [c, c, c, v, r]],
            [[r, r, r, r, r],
             [r, r, r, r, r],
             [c, c, c, r, r],
             [c, c, c, r, r],
             [c, c, c, v, r]]]

# refine lattice
template_refined = [[ []*5 ]*5 ]*5
for k in range(5):
  for j in range(5):
    a = template[k][j]
    template_refined[k][j] = sum([[a[i]]*refines for i in range(len(a))], [])

lattice.setUniverses3D(template_refined)
root_cell.setFill(lattice)


###############################################################################
##########################     Creating Cmfd mesh    ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating Cmfd mesh...')

cmfd = Cmfd()
cmfd.setMOCRelaxationFactor(1.0)
cmfd.setSORRelaxationFactor(1.5)
cmfd.setOpticallyThick(True)
cmfd.setLatticeStructure(5, 5, 5)
cmfd.setKNearest(1)


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
geometry.setRootUniverse(root_universe)
geometry.setCmfd(cmfd)
geometry.initializeFlatSourceRegions()


###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

quad = EqualAnglePolarQuad()
quad.setNumPolarAngles(num_polar)

track_generator = TrackGenerator(geometry, num_azim, num_polar, azim_spacing,
                                 polar_spacing)
track_generator.setQuadrature(quad)
track_generator.setNumThreads(num_threads)
track_generator.generateTracks()


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = CPUSolver(track_generator)
solver.setConvergenceThreshold(tolerance)
solver.setNumThreads(num_threads)
solver.computeEigenvalue(max_iters)
solver.printTimerReport()


###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

plotter.plot_materials(geometry, gridsize=500, plane='xy')
plotter.plot_materials(geometry, gridsize=500, plane='xz', offset=-10.0)
plotter.plot_materials(geometry, gridsize=500, plane='yz')
plotter.plot_cells(geometry, gridsize=500)
plotter.plot_flat_source_regions(geometry, gridsize=500, plane='xy')
plotter.plot_flat_source_regions(geometry, gridsize=500, plane='xz')
plotter.plot_flat_source_regions(geometry, gridsize=500, plane='yz')
plotter.plot_spatial_fluxes(solver, energy_groups=[1,2],
                            gridsize=500, plane='xy', offset=0.)
plotter.plot_spatial_fluxes(solver, energy_groups=[1,2],
                            gridsize=500, plane='xz', offset=0.)
plotter.plot_spatial_fluxes(solver, energy_groups=[1,2],
                            gridsize=500, plane='yz', offset=0.)


log.py_printf('TITLE', 'Finished')
