from typing import Callable, Optional, Union, Dict, List, Tuple
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from struphy.geometry import base
from struphy.geometry import domains
import struphy.feec.spline_space as spl
from gvec_to_python.reader.sample_loader import SampleEnum


def test_polar_splines_3D(params, func_test=None, map_type=None, func_form=None, space_type=None, domain_enum=None, op_enum=None, eta3_slice=0.75):
    """Test constructing 3D polar splines for a non-axisymmetric GVEC equilibrium via an intermediate axisymmetric torus mapping.

    Even though it says 3D, all test functions are :math:``f(x,y)``, independent of :math:``z``.
    For scalar case, the test function is :math:``f(x,y)``.
    For vector case, the test function is :math:``f(x,y) \hat{i} + f(x,y) \hat{j} + f(x,y) \hat{k}``.

    Parameters
    ----------
    func_test : FuncTest
        An Enum of implemented test functions.
    map_type : MapType
        An Enum of implemented mapping domains.
    func_form : FuncForm
        Which differential form to display plots of spline comparisons.
    space_type : SpaceType
        An Enum of whether to plot in physical or logical space.
    domain_enum : DomainType
        An Enum for selecting analytical or numerical domain for pullback/pushforward.
    op_enum : Operation
        An Enum of whether to generate data, or plot the data.
    eta3_slice : float
        When extruding a 2D poloidal plane of a 3D toroidal spline map, which eta3 coordinate to place the cut.

    Notes
    -----
    To execute this on Windows, at the project root, enter `python`.
    Then import this test function `from struphy.tests.xx_test_polar_splines_3D import test_polar_splines_3D as test_polar`.
    Finally call `test_polar(True)`.
    """

    if func_test is None:
        func_test = FuncTest.GAUSSIANCOSINE

    if map_type is None:
        map_type = MapType.CIRCLESCALED

    if func_form is None:
        func_form = FuncForm.ZERO

    if space_type is None:
        space_type = SpaceType.PHYSICAL

    if domain_enum is None:
        domain_enum = DomainType.DISCRETE

    if op_enum is None:
        op_enum = Operation.ALL

    no_cache = False
    interactive = False
    is_2d_extrude  = 'extru2d' in map_type.name.lower()
    is_3d_cylinder = 'cyldr3d' in map_type.name.lower()
    is_3d_torus    = 'torus3d' in map_type.name.lower()

    # ============================================================
    # Imports.
    # ============================================================

    import os
    import sys
    import pickle
    import tempfile
    temp_dir = tempfile.TemporaryDirectory(prefix='STRUPHY-')
    print(f'Created temp directory at: {temp_dir.name}')

    # which diagnostics is run
    print('Run diagnostics:', sys.argv[0])

    basedir = os.path.dirname(os.path.realpath(__file__))
    # sys.path.insert(0, os.path.join(basedir, '..'))

    import matplotlib.pyplot as plt



    # ============================================================
    # Unpack STRUPHY spline configuration.
    # ============================================================

    # Create splines in STRUPHY, unrelated to splines in GVEC.
    Nel      = params['grid']['Nel']      # Number of grid cells
    p        = params['grid']['p']        # Spline degree
    nq_el    = params['grid']['nq_el']    # Element integration, quadrature points per grid cell.
    nq_pr    = params['grid']['nq_pr']    # Greville integration, quadrature points per histopolation cell (for projection).
    bc       = params['grid']['bc']       # BC in s-direction
    spl_kind = params['grid']['spl_kind'] # Spline type: True=periodic, False=clamped

    # Configure subdomain for 3D torus.
    # Especially if you can't afford to use a lot of Nel to capture all the eta3-dependence.
    # TODO: Expose this interface through `params`.
    use_subdomain = True
    # The subdomain has to be centered at eta3=0.75, otherwise one might get a negative Jacobian determinant.
    if use_subdomain and is_3d_torus:
        print('Forcing torus map to use subdomain!')
        eta3_slice = 0.0
        begin3 = 0.7
        end3 = 0.8
    elif use_subdomain and is_3d_cylinder:
        print('Forcing straightened torus map to use subdomain!')
        eta3_slice = 0.0
        begin3 = 0.7
        end3 = 0.8
    else:
        begin3 = 0.0
        end3 = 1.0



    # ============================================================
    # Define mappings F = F2 \circ F1.
    # ============================================================

    if is_input_map_spline(map_type): # Special handling for spline maps.

        # The toroidal cross section is actually on the x-z plane!
        # Therefore the y-z axes were swapped when constructing STRUPHY 3D spline from GVEC's spline x fourier mapping.
        if is_2d_extrude:
            sample_enum = map_enum_to_gvec_enum(map_type)
            F_x, F_y, F_z, gvec = get_gvec_map_extru2d(sample_enum, eta3_slice=eta3_slice)
        elif is_3d_cylinder:
            sample_enum = map_enum_to_gvec_enum(map_type)
            F_x, F_y, F_z, gvec = get_gvec_map_cyldr3d(sample_enum, eta3_offset=eta3_slice, b3=begin3, e3=end3)
        elif is_3d_torus:
            sample_enum = map_enum_to_gvec_enum(map_type)
            F_x, F_y, F_z, gvec = get_gvec_map_torus3d(sample_enum, eta3_offset=eta3_slice, b3=begin3, e3=end3)
        else:
            F_x, F_y, F_z, gvec = get_gvec_map(Nel, p, spl_kind, nq_el, nq_pr, bc)
        params['gvec'] = gvec # Pass the `gvec` object for debugging. It's not necessary.
        DOMAIN_ANALYTICAL = None

        # Origin (pole) of slice of polidal spline:
        x0, y0, z0 = F_x(0.,0.,0.5), F_y(0.,0.,0.5), F_z(0.,0.,0.5)

    else:

        DOMAIN_ANALYTICAL = map_generator(map_type)
        def F_x(eta1, eta2, eta3):
            return DOMAIN_ANALYTICAL.evaluate(eta1, eta2, eta3, 'x', squeeze_output=False)
        def F_y(eta1, eta2, eta3):
            return DOMAIN_ANALYTICAL.evaluate(eta1, eta2, eta3, 'y', squeeze_output=False)
        def F_z(eta1, eta2, eta3):
            return DOMAIN_ANALYTICAL.evaluate(eta1, eta2, eta3, 'z', squeeze_output=False)

        x0, y0, z0 = F_x(0.,0.,0.5), F_y(0.,0.,0.5), F_z(0.,0.,0.5)

    print(f'='*50)
    periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
    spl_kind[-1] = periodic_eta3
    print(f'Pole:')
    print(f'x0: {x0}')
    print(f'y0: {y0}')
    print(f'z0: {z0}')
    x0_avg = (F_x(1.,0.00,0.5) + F_x(1.,0.50,0.5)) / 2
    y0_avg = (F_y(1.,0.25,0.5) + F_y(1.,0.75,0.5)) / 2
    print(f'Average origin (assume mapping is aligned to axes):')
    print(f'x0: {x0_avg}')
    print(f'y0: {y0_avg}')
    # Assumption that the Shafranov shift always shifts to the positive directions.
    shift_x = x0 - x0_avg
    shift_y = y0 - y0_avg
    print(f'2x Shafranov shift in x: {shift_x}') # delta_x = 0.03
    print(f'2x Shafranov shift in y: {shift_y}') # delta_y = 0.02
    max_x_from_x0 = F_x(1.,0.00,0.5) - x0_avg # == 0.64
    max_y_from_y0 = F_y(1.,0.25,0.5) - y0_avg # == 1.088
    print(f'Max x from x0: {F_x(1.,0.00,0.5) - x0_avg}')
    print(f'Max y from y0: {F_y(1.,0.25,0.5) - y0_avg}')
    # Scale s.d. in z with max height of the domain.
    # If domain is cylindrical, then it is simply z_top - z_bottom.
    eta_sample = np.linspace(0,1,19)
    eta1_sam, eta2_sam, eta3_sam = np.meshgrid(eta_sample, eta_sample, eta_sample, indexing='ij', sparse=False)
    z_sample = F_z(eta1_sam, eta2_sam, eta3_sam)
    max_z = np.nanmax(z_sample)
    min_z = np.nanmin(z_sample)
    print(f'z-axis has range from {min_z:.4f} to {max_z:.4f}')
    z_height = max_z - min_z
    # Place Gaussian peak between two z-planes to be better "captured"
    if True or periodic_eta3:
        mu_z = min_z + z_height / 2
    print(f'='*50)

    def_sd_x = 0.1
    def_sd_y = 0.05
    def_sd_z = 0.075
    sd_x = def_sd_x * max_x_from_x0
    sd_y = def_sd_y * max_y_from_y0
    sd_z = def_sd_z * z_height
    # We want `sd_z` to be wide enough so that there is a gradient to another plane, without overshooting the boundary of the domain map.
    # Otherwise, the slope at the Gaussian peak, as well as far away regions, are both zero.
    # Conversely, if the center is between two z-planes, the value of the peak cannot be interpolated properly.

    if isinstance(func_test, FuncTest):

        if func_test == FuncTest.GAUSSIAN:
            trial_params = {
                'sd_x' : sd_x,
                'sd_y' : sd_y,
                'mu_x' : sd_x + x0, # Include GS-shift.
                'mu_y' : sd_y + y0, # Include GS-shift.
            }
            func, dfdx, dfdy = generate_2d_trial_func(func_test, params=trial_params)
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy)
        elif func_test == FuncTest.LINEARX:
            trial_params = {
                'mu_x' : 0. + x0,
            }
            func, dfdx, dfdy = generate_2d_trial_func(func_test, params=trial_params)
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy)
        else:
            func, dfdx, dfdy = generate_2d_trial_func(func_test, params=None)
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy)

    elif isinstance(func_test, FuncTest3D):

        if func_test == FuncTest3D.GAUSSIAN3D:
            trial_params = {
                'sd_x' : sd_x,
                'sd_y' : sd_y,
                'sd_z' : sd_z,
                'mu_x' : sd_x + x0, # Include GS-shift.
                'mu_y' : sd_y + y0, # Include GS-shift.
                'mu_z' : sd_z + z0, # `mu_z` needs to be placed near z-plane for projection to be accurate.
            }
            print('3D Gaussian plot parameters:')
            print(trial_params)
            func, dfdx, dfdy, dfdz = generate_3d_trial_func(func_test, params=trial_params)
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy, dfdz)
        else:
            func, dfdx, dfdy, dfdz = generate_3d_trial_func(func_test, params=None)
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy, dfdz)

    else:

        raise TypeError(f'Enum type of trial function not recognized. Type: {type(func_test)}. Value: {func_test}')



    # ============================================================
    # Run test cases.
    # ============================================================

    print('Begin testing 3D polar splines.')

    case_0form_args = [params, func   , dfdx   , dfdy  , F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum]
    case_1form_args = [params, func_3d, curl_3d, div_3d, F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum]
    case_2form_args = [params, func_3d, curl_3d, div_3d, F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum]
    case_3form_args = [params, func   , None   , None  , F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum]
    if isinstance(func_test, FuncTest3D):
        case_0form_args = [params, func   , dfdx   , dfdy  , F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum, dfdz]

    data_folder = f'~/struphy-cache/test_polar_spline_{func_test.name}_{map_type.name}_{func_form.name}'
    data_folder = os.path.expanduser(data_folder)
    data_filename = f'{func_test.name}_{map_type.name}_{domain_enum.name}_{space_type.name}_{func_form.name}-Form'
    data_filename += f'_{str(Nel)}_{str(p)}_{str(spl_kind)}_{str(nq_el)}_{str(nq_pr)}_{str(bc)}'
    if is_2d_extrude or is_3d_cylinder or is_3d_torus:
        data_filename += f'_eta3={eta3_slice:.4f}'
    if use_subdomain and (is_3d_cylinder or is_3d_torus):
        data_filename += f'_begin3={begin3:.4f}_end3={end3:.4f}'
    data_path = os.path.join(data_folder, f'{data_filename}.pkl')
    os.makedirs(data_folder, exist_ok=True)
    print(f'data_filename: {data_filename}')

    if func_form == FuncForm.ZERO:
        if op_enum in [Operation.WRITEONLY, Operation.ALL]:
            if no_cache:
                print('Cache will not be generated.')
                plot_data_0form = case_0form(*case_0form_args)
                print('Plot data computed.')
            elif not os.path.isfile(data_path):
                print('Cache for current configuration not found. Computing...')
                plot_data_0form = case_0form(*case_0form_args)
                with open(data_path, 'wb') as handle:
                    pickle.dump(plot_data_0form, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print('Cache generated.')
            else:
                print('Cache found for current configuration.')
                with open(data_path, 'rb') as handle:
                    plot_data_0form = pickle.load(handle)
                print('Loaded data from cache.')
            print('\n' + '='*50)
            if op_enum == Operation.WRITEONLY:
                return plot_data_0form
        if op_enum in [Operation.PLOTONLY, Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
            plot_handles_0form = plot_wrapper(*plot_data_0form, params, map_type, func_test, func_form, space_type, domain_enum, Nel, p)
            if interactive:
                ref_fun_0form = plot_controls(case_0form, case_0form_args, func_test, func_form, plot_handles_0form)
                ref_spl_0form = plot_spl_config(case_0form, case_0form_args, func_test, func_form, plot_handles_0form)
            if op_enum in [Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
                for handle in plot_handles_0form:
                    handle['fig'].savefig(get_save_path(handle['metadata']['wintitle'].replace(' ', '_') + '.png'), dpi='figure', transparent=False)
            if op_enum in [Operation.PLOTONLY, Operation.SAVEPLOT, Operation.ALL]:
                plt.show()
    elif func_form == FuncForm.ONE:
        if op_enum in [Operation.WRITEONLY, Operation.ALL]:
            if no_cache:
                print('Cache will not be generated.')
                plot_data_1form = case_1form(*case_1form_args)
                print('Plot data computed.')
            elif not os.path.isfile(data_path):
                print('Cache for current configuration not found. Computing...')
                plot_data_1form = case_1form(*case_1form_args)
                with open(data_path, 'wb') as handle:
                    pickle.dump(plot_data_1form, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print('Cache generated.')
            else:
                print('Cache found for current configuration.')
                with open(data_path, 'rb') as handle:
                    plot_data_1form = pickle.load(handle)
                print('Loaded data from cache.')
            print('\n' + '='*50)
            if op_enum == Operation.WRITEONLY:
                return plot_data_1form
        if op_enum in [Operation.PLOTONLY, Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
            plot_handles_1form = plot_wrapper(*plot_data_1form, params, map_type, func_test, func_form, space_type, domain_enum, Nel, p)
            if interactive:
                ref_fun_1form = plot_controls(case_1form, case_1form_args, func_test, func_form, plot_handles_1form)
                ref_spl_1form = plot_spl_config(case_1form, case_1form_args, func_test, func_form, plot_handles_1form)
            if op_enum in [Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
                for handle in plot_handles_1form:
                    handle['fig'].savefig(get_save_path(handle['metadata']['wintitle'].replace(' ', '_') + '.png'), dpi='figure', transparent=False)
            if op_enum in [Operation.PLOTONLY, Operation.SAVEPLOT, Operation.ALL]:
                plt.show()
    elif func_form == FuncForm.TWO:
        if op_enum in [Operation.WRITEONLY, Operation.ALL]:
            if no_cache:
                print('Cache will not be generated.')
                plot_data_2form = case_2form(*case_2form_args)
                print('Plot data computed.')
            elif not os.path.isfile(data_path):
                print('Cache for current configuration not found. Computing...')
                plot_data_2form = case_2form(*case_2form_args)
                with open(data_path, 'wb') as handle:
                    pickle.dump(plot_data_2form, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print('Cache generated.')
            else:
                print('Cache found for current configuration.')
                with open(data_path, 'rb') as handle:
                    plot_data_2form = pickle.load(handle)
                print('Loaded data from cache.')
            print('\n' + '='*50)
            if op_enum == Operation.WRITEONLY:
                return plot_data_2form
        if op_enum in [Operation.PLOTONLY, Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
            plot_handles_2form = plot_wrapper(*plot_data_2form, params, map_type, func_test, func_form, space_type, domain_enum, Nel, p)
            if interactive:
                ref_fun_2form = plot_controls(case_2form, case_2form_args, func_test, func_form, plot_handles_2form)
                ref_spl_2form = plot_spl_config(case_2form, case_2form_args, func_test, func_form, plot_handles_2form)
            if op_enum in [Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
                for handle in plot_handles_2form:
                    handle['fig'].savefig(get_save_path(handle['metadata']['wintitle'].replace(' ', '_') + '.png'), dpi='figure', transparent=False)
            if op_enum in [Operation.PLOTONLY, Operation.SAVEPLOT, Operation.ALL]:
                plt.show()
    elif func_form == FuncForm.THREE:
        if op_enum in [Operation.WRITEONLY, Operation.ALL]:
            if no_cache:
                print('Cache will not be generated.')
                plot_data_3form = case_3form(*case_3form_args)
                print('Plot data computed.')
            elif not os.path.isfile(data_path):
                print('Cache for current configuration not found. Computing...')
                plot_data_3form = case_3form(*case_3form_args)
                with open(data_path, 'wb') as handle:
                    pickle.dump(plot_data_3form, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print('Cache generated.')
            else:
                print('Cache found for current configuration.')
                with open(data_path, 'rb') as handle:
                    plot_data_3form = pickle.load(handle)
                print('Loaded data from cache.')
            print('\n' + '='*50)
            if op_enum == Operation.WRITEONLY:
                return plot_data_3form
        if op_enum in [Operation.PLOTONLY, Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
            plot_handles_3form = plot_wrapper(*plot_data_3form, params, map_type, func_test, func_form, space_type, domain_enum, Nel, p)
            if interactive:
                ref_fun_3form = plot_controls(case_3form, case_3form_args, func_test, func_form, plot_handles_3form)
                ref_spl_3form = plot_spl_config(case_3form, case_3form_args, func_test, func_form, plot_handles_3form)
            if op_enum in [Operation.SAVEONLY, Operation.SAVEPLOT, Operation.ALL]:
                for handle in plot_handles_3form:
                    handle['fig'].savefig(get_save_path(handle['metadata']['wintitle'].replace(' ', '_') + '.png'), dpi='figure', transparent=False)
            if op_enum in [Operation.PLOTONLY, Operation.SAVEPLOT, Operation.ALL]:
                plt.show()


    print('Done testing 3D polar splines.')
    print('\n' + '='*50)



from enum import Enum, unique

@unique
class FuncTest(Enum):
    """Enum for 2D trial functions f(x,y)."""
    GAUSSIAN = 1
    GAUSSIANCOSINE = 2
    SIGMOID = 3
    SINEX = 4
    CONSTANT = 5
    LINEARX = 6
    LINEARXYSUM = 7
    LINEARXYPROD = 8

@unique
class FuncTest3D(Enum):
    """Enum for 3D trial functions f(x,y,z)."""
    CONSTANT3D = 1
    GAUSSIAN3D = 2
    LINEARXYZSUM = 3

@unique
class MapType(Enum):
    """Enum for F-map functions used."""
    CIRCLEIDENTICAL = 1
    CIRCLESCALED = 2
    CIRCLESHIFTED = 3
    ELLIPSE = 4
    ELLIPSEROTATED = 5
    SHAFRANOVSHIFT = 6
    SHAFRANOVSQRT = 7
    SHAFRANOVDSHAPED = 8
    SPLINE = 9 # Deprecated.
    # Extruded 2D poloidal plane (no eta3 dependence).
    GVEC_EXTRU2D_ELLIPSTELL = 1001
    GVEC_EXTRU2D_CIRCTOK    = 1002
    GVEC_EXTRU2D_E1D6M6D6   = 1003
    GVEC_EXTRU2D_E4D6M6D6   = 1004
    GVEC_EXTRU2D_E40D5M6D6  = 1005
    # Straightened 2D poloidal plane from torus (eta3 dependence).
    GVEC_CYLDR3D_ELLIPSTELL = 2001
    GVEC_CYLDR3D_CIRCTOK    = 2002
    GVEC_CYLDR3D_E1D6M6D6   = 2003
    GVEC_CYLDR3D_E4D6M6D6   = 2004
    GVEC_CYLDR3D_E40D5M6D6  = 2005
    # Full 3D torus.
    GVEC_TORUS3D_ELLIPSTELL = 3001
    GVEC_TORUS3D_CIRCTOK    = 3002
    GVEC_TORUS3D_E1D6M6D6   = 3003
    GVEC_TORUS3D_E4D6M6D6   = 3004
    GVEC_TORUS3D_E40D5M6D6  = 3005

@unique
class SpaceType(Enum):
    """Enum for whether to plot in physical or logical space.."""
    PHYSICAL = 1
    # DISK = 2
    LOGICAL = 3

@unique
class DomainType(Enum):
    """Enum for selecting analytical or discrete domain for pullback/pushforward."""
    ANALYTICAL = 1
    DISCRETE = 2

@unique
class Comparison(Enum):
    """Enum for either plotting original or difference."""
    ORIG = 1
    DIFF = 2

@unique
class PlotTypeLeft(Enum):
    """Enum for chart type on the left hand side (original function)."""
    CONTOUR2D = 1 # contourf, 2D.
    CONTOUR3D = 2 # contourf, 3D.
    SCATTER = 3 # scatter, 3D.
    SURFACE = 4 # plot_surface, 3D.
    WIREFRAME = 5 # wireframe, 3D.
    LINE = 6 # plot, 1D.
    # Line plot works only with SpaceType.LOGICAL. Hardcoded switch in plot_wrapper(). Need to specify eta2 slice in metadata. Interactive update not supported.

@unique
class PlotTypeRight(Enum):
    """Enum for chart type on the right hand side (first derivative function)."""
    CONTOUR2D = 1 # contourf, 2D.
    CONTOUR3D = 2 # contourf, 3D.
    QUIVER2D = 3 # quiver, 2D.
    QUIVER3D = 4 # quiver, 3D.
    SURFACE = 5 # plot_surface, 3D.
    LINE = 6 # plot, 1D.
    SCATTER = 7
    # Line plot works only with SpaceType.LOGICAL. Hardcoded switch in plot_wrapper(). Need to specify eta2 slice in metadata. Interactive update not supported.

@unique
class FuncForm(Enum):
    """Enum for p-form of the test function itself.
    
    It is implied that its "derivative" is (p+1)-form according to de Rham's sequence."""
    ZERO = 10
    ONE = 11
    TWO = 12
    THREE = 13 # Only projection, no FEEC derivative.

@unique
class DiffType(Enum):
    """How to represent error from reference data."""
    DIRECT = 1
    RELATIVE = 2
    RELATIVEABSOLUTE = 3
    ABSOLUTE = 4
    LOGABSOLUTE = 5

@unique
class ErrorScope(Enum):
    """Compute error from a point, average over a local region, or globally."""
    POINT = 1
    LOCAL = 2
    GLOBAL = 3

@unique
class ErrorNorm(Enum):
    """Norm to compute error."""
    L1 = 1
    L2 = 2
    Li = 999

@unique
class Operation(Enum):
    """How to represent error from reference data."""
    WRITEONLY = 1
    PLOTONLY = 2
    SAVEONLY = 3
    SAVEPLOT = 4
    ALL = 5



def is_input_map_spline(map_enum:MapType) -> bool:
    return map_enum in [ # Special handling for spline maps.
        MapType.SPLINE,
        MapType.GVEC_EXTRU2D_ELLIPSTELL,
        MapType.GVEC_EXTRU2D_CIRCTOK,
        MapType.GVEC_EXTRU2D_E1D6M6D6,
        MapType.GVEC_EXTRU2D_E4D6M6D6,
        MapType.GVEC_EXTRU2D_E40D5M6D6,
        MapType.GVEC_CYLDR3D_ELLIPSTELL,
        MapType.GVEC_CYLDR3D_CIRCTOK,
        MapType.GVEC_CYLDR3D_E1D6M6D6,
        MapType.GVEC_CYLDR3D_E4D6M6D6,
        MapType.GVEC_CYLDR3D_E40D5M6D6,
        MapType.GVEC_TORUS3D_ELLIPSTELL,
        MapType.GVEC_TORUS3D_CIRCTOK,
        MapType.GVEC_TORUS3D_E1D6M6D6,
        MapType.GVEC_TORUS3D_E4D6M6D6,
        MapType.GVEC_TORUS3D_E40D5M6D6,
    ]



def func_2d_gaussian(mu_x:float=.1, sd_x:float=.1, mu_y:float=.1, sd_y:float=.1) -> Tuple[Callable,Callable,Callable]:
    """A 2D independent Gaussian pdf f(x,y,z) = f(x,y).

    The steepest slope is at mean = s.d.

    Parameters
    ----------
    mu_x : float
        Mean along x-direction.
    sd_x : float
        Standard deviation along x-direction.
    mu_y : float
        Mean along y-direction.
    sd_y : float
        Standard deviation along y-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) a Gaussian function and its partial derivatives (2) along x and (3) along y.
    """
    func = lambda x, y, z : 1 / (2 * np.pi * sd_x * sd_y) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2))
    dfdx = lambda x, y, z : 1 / (2 * np.pi * sd_x * sd_y) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2)) * (mu_x - x) / sd_x**2
    dfdy = lambda x, y, z : 1 / (2 * np.pi * sd_x * sd_y) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2)) * (mu_y - y) / sd_y**2
    return func, dfdx, dfdy

def func_3d_gaussian(mu_x:float=.1, sd_x:float=.1, mu_y:float=.1, sd_y:float=.1, mu_z:float=.1, sd_z:float=.1) -> Tuple[Callable,Callable,Callable,Callable]:
    """A 3D independent Gaussian pdf f(x,y,z) = f(R, Z, phi).

    The steepest slope is at mean = s.d.

    Parameters
    ----------
    mu_x : float
        Mean along x-direction.
    sd_x : float
        Standard deviation along x-direction.
    mu_y : float
        Mean along y-direction.
    sd_y : float
        Standard deviation along y-direction.
    mu_z : float
        Mean along z-direction.
    sd_z : float
        Standard deviation along z-direction.

    Returns
    -------
    tuple of callables
        A 4-tuple consisting of (1) a Gaussian function and its partial derivatives (2) along x, (3) along y, and (4) along z.
    """
    func = lambda x, y, z : 1 / (2 * np.pi)**1.5 / (sd_x * sd_y * sd_z) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2 + (z - mu_z)**2 / sd_z**2))
    dfdx = lambda x, y, z : 1 / (2 * np.pi)**1.5 / (sd_x * sd_y * sd_z) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2 + (z - mu_z)**2 / sd_z**2)) * (mu_x - x) / sd_x**2
    dfdy = lambda x, y, z : 1 / (2 * np.pi)**1.5 / (sd_x * sd_y * sd_z) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2 + (z - mu_z)**2 / sd_z**2)) * (mu_y - y) / sd_y**2
    dfdz = lambda x, y, z : 1 / (2 * np.pi)**1.5 / (sd_x * sd_y * sd_z) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2 + (z - mu_z)**2 / sd_z**2)) * (mu_z - z) / sd_z**2
    return func, dfdx, dfdy, dfdz



def func_gaussian_cosine(mu_x=1, sd_x=1, mu_y=1, sd_y=1, om_x=6.2831853, ph_x=0, om_y=6.2831853, ph_y=0):
    """A 2D independent mixed Guassian and Cosine function.

    The steepest slope is when mean = s.d. coincide with (some) zeroes of cosine.
    In particular, we want the first zero of the cosine to coincide with the s.d. of the Gaussian.

    Parameters
    ----------
    mu_x : float
        Mean along x-direction.
    sd_x : float
        Standard deviation along x-direction.
    mu_y : float
        Mean along y-direction.
    sd_y : float
        Standard deviation along y-direction.
    om_x : float
        Angular frequency along x-direction.
    ph_x : float
        Phase shift along x-direction.
    om_y : float
        Angular frequency along y-direction.
    ph_y : float
        Phase shift along y-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) the mixed Gaussian-Cosine function and its partial derivatives (2) along x and (3) along y.
    """
    import numpy as np
    func = lambda x, y, z : 1 / (2 * np.pi * sd_x * sd_y) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2)) * np.cos(om_x * x + ph_x) * np.cos(om_y * y + ph_y)
    dfdx = lambda x, y, z : 1 / (2 * np.pi * sd_x * sd_y) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2)) * np.cos(om_x * x + ph_x) * np.cos(om_y * y + ph_y) * ((mu_x - x) / sd_x**2 - om_x * np.tan(om_x * x + ph_x))
    dfdy = lambda x, y, z : 1 / (2 * np.pi * sd_x * sd_y) * np.exp(-0.5 * ((x - mu_x)**2 / sd_x**2 + (y - mu_y)**2 / sd_y**2)) * np.cos(om_x * x + ph_x) * np.cos(om_y * y + ph_y) * ((mu_y - y) / sd_y**2 - om_y * np.tan(om_y * x + ph_y))
    # Pure Cosine for testing default phase offset ph_x=(mu_x+10)*2*np.pi:
    # func = lambda x, y, z : np.cos(om_x * x + ph_x) * np.cos(om_y * y + ph_y)
    # dfdx = lambda x, y, z : - om_x * np.sin(om_x * x + ph_x) * np.cos(om_y * y + ph_y)
    # dfdy = lambda x, y, z : - om_y * np.cos(om_x * x + ph_x) * np.sin(om_y * y + ph_y)
    return func, dfdx, dfdy



def func_sineX(om_x=6.2831853, ph_x=0):
    """A sine function in x.

    The steepest slope is at the origin (or other zeros).

    Parameters
    ----------
    om_x : float
        Angular frequency along x-direction.
    ph_x : float
        Phase shift along x-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) the sine function of only x, and its partial derivatives (2) along x and (3) along y.
    """
    import numpy as np
    func = lambda x, y, z : np.sin(om_x * x + ph_x)
    dfdx = lambda x, y, z : om_x * np.cos(om_x * x + ph_x)
    dfdy = lambda x, y, z : np.zeros_like(x)
    return func, dfdx, dfdy



def func_sigmoid(L=1, mu_x=0, k_x=1, mu_y=0, k_y=1):
    """A 2D independent generalized logistic cdf.

    The steepest slope is at mean = 0.

    Parameters
    ----------
    L : float
        Maximum value of the logistic function.
    mu_x : float
        Mean along x-direction.
    k_x : float
        Steepnesss of the slope along x-direction.
    mu_y : float
        Mean along y-direction.
    k_y : float
        Steepnesss of the slope along y-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) a generalized logistic function and its partial derivatives (2) along x and (3) along y.
    """
    import numpy as np
    func = lambda x, y, z : L / (1 + np.exp(-k_x * (x - mu_x))) / (1 + np.exp(-k_y * (y - mu_y)))
    dfdx = lambda x, y, z : k_x * func(x, y, z) * (1 - 1 / (1 + np.exp(-k_x * (x - mu_x))))
    dfdy = lambda x, y, z : k_y * func(x, y, z) * (1 - 1 / (1 + np.exp(-k_y * (y - mu_y))))
    return func, dfdx, dfdy



def func_3d_constant(c:float=1.) -> Tuple[Callable,Callable,Callable,Callable]:
    """A constant function: f(x,y,z) = c.

    Parameters
    ----------
    c : float
        Constant value of the function.

    Returns
    -------
    tuple of callables
        A 4-tuple consisting of (1) a constant function and its partial derivatives (2) along x, (3) along y, and (4) along z.
    """
    ones = lambda x, y, z : np.ones_like(x) * np.ones_like(y) * np.ones_like(z)
    func = lambda x, y, z : c * ones(x, y, z)
    dfdx = lambda x, y, z : 0 * ones(x, y, z)
    dfdy = lambda x, y, z : 0 * ones(x, y, z)
    dfdz = lambda x, y, z : 0 * ones(x, y, z)
    return func, dfdx, dfdy, dfdz



def func_linearX(mu_x:float=.1):
    """A linear function in x: f(x) = x.

    Parameters
    ----------
    mu_x : float
        Mean along x-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) a linear function in only x, and its partial derivatives (2) along x and (3) along y.
    """
    import numpy as np
    func = lambda x, y, z : x - mu_x
    dfdx = lambda x, y, z : np.ones_like(x)
    dfdy = lambda x, y, z : np.zeros_like(x)
    return func, dfdx, dfdy



def func_linearXYsum(mu_x:float=.1, mu_y:float=.1):
    """A linear function in x and y: f(x,y) = x + y.

    Parameters
    ----------
    mu_x : float
        Mean along x-direction.
    mu_y : float
        Mean along y-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) a linear function in x and y, and its partial derivatives (2) along x and (3) along y.
    """
    import numpy as np
    func = lambda x, y, z : (x - mu_x) + (y - mu_y)
    dfdx = lambda x, y, z : np.ones_like(x)
    dfdy = lambda x, y, z : np.ones_like(y)
    return func, dfdx, dfdy



def func_3d_linearXYZsum(mu_x:float=.1, mu_y:float=.1, mu_z:float=.1):
    """A linear function in x, y, and z: f(x,y,z) = x + y + z.

    The idea is that its curl will be (1 - 1) = 0 in all vector components.
    This is to show discretization error.

    Parameters
    ----------
    mu_x : float
        Mean along x-direction.
    mu_y : float
        Mean along y-direction.
    mu_z : float
        Mean along z-direction.

    Returns
    -------
    tuple of callables
        A 4-tuple consisting of (1) a linear function in x, y, and z, and its partial derivatives (2) along x, (3) along y, and (4) along z.
    """
    import numpy as np
    func = lambda x, y, z : (x - mu_x) + (y - mu_y) + (z - mu_z)
    dfdx = lambda x, y, z : np.ones_like(x)
    dfdy = lambda x, y, z : np.ones_like(y)
    dfdz = lambda x, y, z : np.ones_like(z)
    return func, dfdx, dfdy, dfdz



def func_linearXYprod(mu_x:float=.1, mu_y:float=.1):
    """A linear function in x and y: f(x,y) = x * y.

    Parameters
    ----------
    mu_x : float
        Mean along x-direction.
    mu_y : float
        Mean along y-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) a linear function in x and y, and its partial derivatives (2) along x and (3) along y.
    """
    import numpy as np
    func = lambda x, y, z : (x - mu_x) * (y - mu_y)
    dfdx = lambda x, y, z : y - mu_y
    dfdy = lambda x, y, z : x - mu_x
    return func, dfdx, dfdy



def func_3d_wrapper(func:Callable, dfdx:Callable, dfdy:Callable, dfdz:Optional[Callable]=None):
    """Create a vector-valued function, where all components are identical.

    The input is given by one of the provided trial functions.

    Parameters
    ----------
    func : callable
        One of the provided trial functions `func_...`.
    dfdx : callable
        Partial derivative of `func` w.r.t. x-direction.
    dfdy : callable
        Partial derivative of `func` w.r.t. y-direction.
    dfdz : callable
        Partial derivative of `func` w.r.t. z-direction.

    Returns
    -------
    tuple of callables
        A 3-tuple consisting of (1) a vector-valued function (2) its curl and (3) its divergence.

    Notes
    -----
    If input function does not have z-dependence:
    .. math::

        \vec{f}(x,y)               & = f(x,y) \hat{i} + f(x,y) \hat{j} + f(x,y) \hat{k} \\
        \nabla \times \vec{f}(x,y) & = (\pdv{f(x,y)}{y} - 0) \hat{i} + (0 - \pdv{f(x,y)}{x}) \hat{j} + (\pdv{f(x,y)}{y} - \pdv{f(x,y)}{x}) \hat{k} \\
        \nabla \cdot \vec{f}(x,y)  & = \pdv{f(x,y)}{x} + \pdv{f(x,y)}{y} + 0

    Else:
    .. math::

        \vec{f}(x,y,z)               & = f_x(x,y,z) \hat{i} + f_y(x,y,z) \hat{j} + f_z(x,y,z) \hat{k} \\
        \nabla \times \vec{f}(x,y,z) & = (\pdv{f_z(x,y,z)}{y} - \pdv{f_y(x,y,z)}{z}) \hat{i} + (\pdv{f_x(x,y,z)}{z} - \pdv{f_z(x,y,z)}{x}) \hat{j} + (\pdv{f_x(x,y,z)}{y} - \pdv{f_y(x,y,z)}{x}) \hat{k} \\
        \nabla \cdot \vec{f}(x,y,z)  & = \pdv{f_x(x,y,z)}{x} + \pdv{f_y(x,y,z)}{y} + \pdv{f_z(x,y,z)}{z}
    """
    # func_3d = [lambda x, y, z : func(x, y, z), lambda x, y, z : func(x, y, z), lambda x, y, z : func(x, y, z)]
    # curl_3d = [lambda x, y, z : np.zeros_like(x), lambda x, y, z : np.zeros_like(x), lambda x, y, z : dfdy(x, y, z) - dfdx(x, y, z)]
    if dfdz is None:
        func_3d = lambda x, y, z : np.array([func(x, y, z), func(x, y, z), func(x, y, z)])
        curl_3d = lambda x, y, z : np.array([dfdy(x, y, z), - dfdx(x, y, z), dfdx(x, y, z) - dfdy(x, y, z)])
        div_3d  = lambda x, y, z : dfdx(x, y, z) + dfdy(x, y, z)
    else:
        func_3d = lambda x, y, z : np.array([func(x, y, z), func(x, y, z), func(x, y, z)])
        curl_3d = lambda x, y, z : np.array([dfdy(x, y, z) - dfdz(x, y, z), dfdz(x, y, z) - dfdx(x, y, z), dfdx(x, y, z) - dfdy(x, y, z)])
        div_3d  = lambda x, y, z : dfdx(x, y, z) + dfdy(x, y, z) + dfdz(x, y, z)
    return func_3d, curl_3d, div_3d



def generate_2d_trial_func(func_test:FuncTest=FuncTest.GAUSSIAN, params:Optional[Dict]=None):

    # ============================================================
    # Trial functions.
    # ============================================================

    # TODO: take care of boundary conditions, shifts, etc. (-> define proper function)
    # The Gaussian should be shifted away from (0,0), 
    # otherwise its derivative at the pole is analytically zero, 
    # and would not be of interest to us,
    # because we want to test C1 continuity.
    # A jump is expected in TENSOR_SPACE.

    # Basic Gaussian implementation tests.
    from scipy.integrate import dblquad
    standard_normal, _, _ = func_2d_gaussian(0,1,0,1)
    print(f'Check maximum of 2D standard normal (== 1/(sqrt(2pi))**2?) {standard_normal(0,0,0):.8f} == {1 / 2 / np.pi:.8f}?')
    # integration_test = dblquad(lambda x, y : standard_normal(x, y, 0), -np.inf, np.inf, -np.inf, np.inf)
    # print(f'Check integrating 2D Gaussian (== 1?): {integration_test}')

    # Test case 1: 2D Gaussian
    if func_test == FuncTest.GAUSSIAN:

        if params is not None:
            mu_x = params['mu_x']
            mu_y = params['mu_y']
            sd_x = params['sd_x']
            sd_y = params['sd_y']
        else: # Default.
            sd_x = 0.1
            sd_y = 0.05
            mu_x = sd_x + 10
            mu_y = sd_y

        func, dfdx, dfdy = func_2d_gaussian(mu_x=mu_x, sd_x=sd_x, mu_y=mu_y, sd_y=sd_y)

    # Test case 2: Mixed Gaussian and cosine.
    elif func_test == FuncTest.GAUSSIANCOSINE:

        if params is not None:
            mu_x = params['mu_x']
            mu_y = params['mu_y']
            sd_x = params['sd_x']
            sd_y = params['sd_y']
            om_x = params['om_x']
            om_y = params['om_y']
            ph_x = params['ph_x']
            ph_y = params['ph_y']
        else: # Default.
            sd_x = 0.1
            sd_y = 0.05
            mu_x = sd_x + 10
            mu_y = sd_y
            v_x = 1
            v_y = 1
            om_x = 2 * np.pi * v_x / (4 * sd_x) # Steepest gradient.
            om_y = 2 * np.pi * v_y / (4 * sd_y) # Steepest gradient.
            # om_x = 2 * np.pi
            # om_y = 2 * np.pi
            ph_x = 2 * np.pi * (mu_x)
            ph_y = 2 * np.pi * (mu_y)

        func, dfdx, dfdy = func_gaussian_cosine(mu_x=mu_x, sd_x=sd_x, mu_y=mu_y, sd_y=sd_y, om_x=om_x, ph_x=ph_x, om_y=om_y, ph_y=ph_y)

    # Test case 3: Sine in x-direction.
    elif func_test == FuncTest.SINEX:

        if params is not None:
            om_x = params['om_x']
            ph_x = params['ph_x']
        else: # Default.
            om_x = 2 * np.pi
            ph_x = 2 * np.pi * 10

        func, dfdx, dfdy = func_sineX(om_x=om_x, ph_x=ph_x)

    # Test case 4: Logistic function.
    elif func_test == FuncTest.SIGMOID:

        if params is not None:
            mu_x = params['mu_x']
            mu_y = params['mu_y']
            k_x = params['k_x']
            k_y = params['k_y']
        else: # Default.
            mu_x = 0.0 + 10
            mu_y = 0.0
            k_x = 100
            k_y = 100

        func, dfdx, dfdy = func_sigmoid(L=1, mu_x=mu_x, k_x=k_x, mu_y=mu_y, k_y=k_y)

    # Test case 5: Constant function in x.
    elif func_test == FuncTest.CONSTANT:

        if params is not None:
            c = params['c']
        else: # Default.
            c = 1.

        func, dfdx, dfdy, _ = func_3d_constant(c=c)

    # Test case 6: Linear function in x.
    elif func_test == FuncTest.LINEARX:

        if params is not None:
            mu_x = params['mu_x']
        else: # Default.
            mu_x = 0. + 10

        func, dfdx, dfdy = func_linearX(mu_x=mu_x)

    # Test case 7: Linear function f(x,y) = x + y.
    elif func_test == FuncTest.LINEARXYSUM:

        if params is not None:
            mu_x = params['mu_x']
            mu_y = params['mu_y']
        else: # Default.
            mu_x = 0. + 10
            mu_y = 0.

        func, dfdx, dfdy = func_linearXYsum(mu_x=mu_x, mu_y=mu_y)

    # Test case 8: Linear function f(x,y) = x * y
    elif func_test == FuncTest.LINEARXYPROD:

        if params is not None:
            mu_x = params['mu_x']
            mu_y = params['mu_y']
        else: # Default.
            mu_x = 0. + 10
            mu_y = 0.

        func, dfdx, dfdy = func_linearXYprod(mu_x=mu_x, mu_y=mu_y)

    else:

        raise NotImplementedError(f'Test case {func_test.name} not implemented.')

    # # Shifted Gaussian.
    # shift_x = 0.02 + 10
    # shift_y = 0.04
    # hw = 0.16
    # func = lambda x, y, z : np.exp(-((x - shift_x)**2 + (y - shift_y)**2) / hw**2)

    # # Gradient to the "test function".
    # dfdx = lambda x, y, z : np.exp(-((x - shift_x)**2 + (y - shift_y)**2) / hw**2) * (- 2 * (x - shift_x) / hw**2)
    # dfdy = lambda x, y, z : np.exp(-((x - shift_x)**2 + (y - shift_y)**2) / hw**2) * (- 2 * (y - shift_y) / hw**2)

    # # Shifted sin/cos.
    # shift_x = 0.5 + 10
    # shift_y = 0.5
    # k_x = 2 * np.pi
    # k_y = 2 * np.pi

    # func = lambda x, y, z : np.sin(k_x * (x - shift_x)) * np.cos(k_y * (y - shift_y))

    # # Gradient to the "test function".
    # dfdx = lambda x, y, z :   k_x * np.cos(k_x * (x - shift_x)) * np.cos(k_y * (y - shift_y))
    # dfdy = lambda x, y, z : - k_y * np.sin(k_x * (x - shift_x)) * np.sin(k_y * (y - shift_y))

    # # Rotated sin/cos.
    # shift_x = 0.02 + 10
    # shift_y = 0.1
    # k_x = 2 * np.pi * 0.23 * 2
    # k_y = 2 * np.pi * 0.13 * 2

    # func = lambda x, y, z : np.sin(k_x * (x - shift_x + y)) * np.cos(k_y * (y - shift_y - x))

    # # Gradient to the "test function".
    # dfdx = lambda x, y, z :   k_x * np.cos(k_x * (x - shift_x + y)) * np.cos(k_y * (y - shift_y - x)) + k_y * np.sin(k_x * (x - shift_x + y)) * np.sin(k_y * (y - shift_y - x))
    # dfdy = lambda x, y, z : - k_y * np.sin(k_x * (x - shift_x + y)) * np.sin(k_y * (y - shift_y - x)) + k_x * np.cos(k_x * (x - shift_x + y)) * np.cos(k_y * (y - shift_y - x))

    return func, dfdx, dfdy



def generate_3d_trial_func(func_test:FuncTest3D=FuncTest3D.GAUSSIAN3D, params:Optional[Dict]=None):

    # ============================================================
    # Trial functions.
    # ============================================================

    # Basic Gaussian implementation tests.
    from scipy.integrate import dblquad, tplquad
    standard_normal, _, _, _ = func_3d_gaussian(0,1,0,1,0,1)
    print(f'Check maximum of 3D standard normal (== 1/(sqrt(2pi))^3?) {standard_normal(0,0,0):.8f} == {1 / (2 * np.pi)**(3/2):.8f}?')
    # integration_test = tplquad(lambda x, y, z : standard_normal(x, y, z), -np.inf, np.inf, -np.inf, np.inf, -np.inf, np.inf)
    # print(f'Check integrating 3D Gaussian (== 1?): {integration_test}')

    # Test case 1: Constant function in x.
    if func_test == FuncTest3D.CONSTANT3D:

        if params is not None:
            c = params['c']
        else: # Default.
            c = 1.

        func, dfdx, dfdy, dfdz = func_3d_constant(c=c)

    # Test case 2: 3D Gaussian
    elif func_test == FuncTest3D.GAUSSIAN3D:

        if params is not None:
            mu_x = params['mu_x']
            mu_y = params['mu_y']
            mu_z = params['mu_z']
            sd_x = params['sd_x']
            sd_y = params['sd_y']
            sd_z = params['sd_z']
        else: # Default.
            sd_x = 0.1
            sd_y = 0.05
            sd_z = 0.15
            mu_x = sd_x + 10
            mu_y = sd_y
            mu_z = sd_z

        func, dfdx, dfdy, dfdz = func_3d_gaussian(mu_x=mu_x, sd_x=sd_x, mu_y=mu_y, sd_y=sd_y, mu_z=mu_z, sd_z=sd_z)

    # Test case 3: Linear function f(x,y,z) = x + y + z.
    elif func_test == FuncTest3D.LINEARXYZSUM:

        if params is not None:
            mu_x = params['mu_x']
            mu_y = params['mu_y']
            mu_z = params['mu_z']
        else: # Default.
            mu_x = 0. + 10
            mu_y = 0.
            mu_z = 0.

        func, dfdx, dfdy, dfdz = func_3d_linearXYZsum(mu_x=mu_x, mu_y=mu_y, mu_z=mu_z)

    else:

        raise NotImplementedError(f'Test case {func_test.name} not implemented.')

    return func, dfdx, dfdy, dfdz



def map_generator(map_type:MapType, DOMAIN_F:Optional[base.Domain]=None, params:Optional[Dict]=None, verbose:bool=False):

    if map_type == MapType.CIRCLEIDENTICAL: # Unit disc centered at (10,0).

        dom_type = 'HollowCylinder'
        if verbose: print('Running test case 01: Identity map == F1 (unit circle).')
        if params is None: 
            dom_params = {'a1': .0, 'a2': 1., 'R0': 10.}

    elif map_type == MapType.CIRCLESCALED: # Circle scaled to radius = 0.5.

        dom_type = 'HollowCylinder'
        if verbose: print('Running test case 02: Scaled circle.')
        if params is None:
            dom_params = {'a1': .0, 'a2': 0.5, 'R0': 10.}

    elif map_type == MapType.CIRCLESHIFTED: # Unit disc shifted to 10.005 instead of 10.

        dom_type = 'HollowCylinder'
        if verbose: print('Running test case 03: Circular with x-axis offset.')
        if params is None:
            dom_params = {'a1': .0, 'a2': 1., 'R0': 10.005}

    elif map_type == MapType.ELLIPSE: # Ellipse centered at (10,0), with major and minor radii 1 and 0.5 respectively.

        dom_type = 'EllipticCylinder'
        if verbose: print('Running test case 04: Ellipse.')
        if params is None:
            dom_params = {'cx': 10., 'cy': 0., 'cz': 0., 'rx': 1., 'ry': 0.5, 'Lz': 10.}

    elif map_type == MapType.ELLIPSEROTATED: # Ellipse centered at (10,0), with major and minor radii 1 and 0.5 respectively, rotated 30 degrees.

        dom_type = 'RotatedEllipticCylinder'
        if verbose: print('Running test case 05: Rotated ellipse.')
        if params is None:
            dom_params = {'cx': 10., 'cy': 0., 'cz': 0., 'rx': 1., 'ry': 0.5, 'Lz': 10., 'theta': 30/360}

    elif map_type == MapType.SHAFRANOVSHIFT: # Unit disc centered at (10,0), with a Shafranov shift delta of 0.1.

        dom_type = 'ShafranovShiftCylinder'
        if verbose: print('Running test case 06: Circular map with Shafranov shift.')
        if params is None:
            dom_params = {'cx': 10., 'cy': 0., 'cz': 0., 'rx': 1., 'ry': 1., 'Lz': 10., 'delta': 0.1}

    elif map_type == MapType.SHAFRANOVSQRT: # Unit disc centered at (10,0), with a Shafranov shift delta of 0.01.

        dom_type = 'ShafranovSqrtCylinder'
        if verbose: print('Running test case 07: Circular map with Shafranov shift, but with square root dependence on eta1, instead of square.')
        if params is None:
            dom_params = {'cx': 10., 'cy': 0., 'cz': 0., 'rx': 1., 'ry': 1., 'Lz': 10., 'delta': 0.01}

    elif map_type == MapType.SHAFRANOVDSHAPED: # D-shaped map with Shafranov shift, centered at (10,0), as described by Cerfon and Freiberg (doi: 10.1063/1.3328818).

        dom_type = 'ShafranovDshapedCylinder'
        if verbose: print('Running test case 08: D-shaped map with Shafranov shift, as described by Cerfon and Freiberg (doi: 10.1063/1.3328818).')
        if params is None:
            dom_params = {
                'x0': 10. - 2., 'y0': 0., 'z0': 0., # Coordinate origin.
                'R0': 2.,
                'Lz': 10.,
                'delta_x': 0.03, 'delta_y': 0.02, # Grad-Shafranov shift: Artificially added asymmetry.
                'delta_gs': 0.33, # Delta = sin(alpha), triangularity. Shift of high point.
                'epsilon_gs': 0.32, # Inverse aspect ratio a/R0.
                'kappa_gs': 1.7, # Ellipticity (elongation).
            }

    elif is_input_map_spline(map_type):

        if verbose: print('Running test case 09: Generic spline map.')

    else:

        raise NotImplementedError(f'Map {map_type.name} not implemented.')

    if DOMAIN_F is None:
        domain_class = getattr(domains, dom_type)
        DOMAIN_F = domain_class(dom_params)

    return DOMAIN_F



def get_F1_polar_space(Nel, p, spaces_FEM):
    """Instantiate polar spline space from F1 square-to-disk map."""

    # Map F1: Canonical disk.
    domain_class = getattr(domains, 'HollowCylinder')
    DOMAIN_F1 = domain_class({'a1': .0, 'a2': 1., 'R0': 10.})

    def F1_x(eta1, eta2, eta3):
        return DOMAIN_F1.evaluate(eta1, eta2, eta3, 'x', squeeze_output=False)
    def F1_y(eta1, eta2, eta3):
        return DOMAIN_F1.evaluate(eta1, eta2, eta3, 'y', squeeze_output=False)
    def F1_z(eta1, eta2, eta3):
        return DOMAIN_F1.evaluate(eta1, eta2, eta3, 'z', squeeze_output=False)

    # This is handled separately from `Tensor_spline_space`'s periodicity!
    spl_kind_mapping_F1 = [False, True, DOMAIN_F1._periodic_eta3]
    cx_F1, cy_F1, cz_F1 = dom.interp_mapping(Nel, p, spl_kind_mapping_F1, F1_x, F1_y, F1_z)
    e3x = int((cx_F1.shape[-1] - p[-1]) / 2 + p[-1])
    e3y = int((cy_F1.shape[-1] - p[-1]) / 2 + p[-1])
    POLAR_SPACE_F1 = spl.Tensor_spline_space(spaces_FEM, ck=1, cx=cx_F1[:, :, e3x], cy=cy_F1[:, :, e3y])
    POLAR_SPACE_F1.set_projectors('general')

    return POLAR_SPACE_F1



def discretize_all(params, F_x, F_y, F_z, periodic_eta3):
    """Construct tensor product and polar splines, discrete F and analytical F1 domains."""

    import struphy.geometry.domain_3d as dom
    import struphy.feec.spline_space as spl

    import os
    import h5py
    import tempfile
    temp_dir = tempfile.TemporaryDirectory(prefix='STRUPHY-')
    print(f'Created temp directory at: {temp_dir.name}')



    # ============================================================
    # Configure STRUPHY splines.
    # ============================================================

    # Create splines in STRUPHY, unrelated to splines in GVEC.
    Nel      = params['grid']['Nel']      # Number of grid cells
    p        = params['grid']['p']        # Spline degree
    nq_el    = params['grid']['nq_el']    # Element integration, quadrature points for spline evaluation.
    nq_pr    = params['grid']['nq_pr']    # Greville integration, quadrature points for projection.
    bc       = params['grid']['bc']       # BC in s-direction
    spl_kind = params['grid']['spl_kind'] # Spline type: True=periodic, False=clamped

    # Override spline periodicity.
    # Spline space must be periodic in the 3rd direction, but the domain itself might not be periodic.
    # We "hack" this by obtaining spline coefficients from `interp_mapping` rather than Pi_0 projection.
    spl_kind_FEEC = [False, True, True]



    # ============================================================
    # Create FEM space and setup projectors.
    # ============================================================

    # 1D B-spline spline spaces for finite elements.
    spaces_FEM = [spl.Spline_space_1d(Nel_i, p_i, spl_kind_i, nq_el_i) for Nel_i, p_i, spl_kind_i, nq_el_i in zip(Nel, p, spl_kind_FEEC, nq_el)]
    [space.set_projectors(nq=nq) for space, nq in zip(spaces_FEM, nq_pr) if not hasattr(space, 'projectors')]

    # 3D tensor-product B-spline space for finite elements.
    # Independent of Domain.
    TENSOR_SPACE = spl.Tensor_spline_space(spaces_FEM, ck=-1)
    if not hasattr(TENSOR_SPACE, 'projectors'):
        TENSOR_SPACE.set_projectors('general') # def set_projectors(self, which='tensor'). Use 'general' for polar splines.
    print('Tensor space and projector set up done.')



    # ============================================================
    # Evaluate cx, cy coefficients for initializing polar splines.
    # ============================================================

    # To obtain 2D coefficients, eta3 must be an optional parameter for the map itself (e.g. F_x).
    # But since we are using a Domain object, eta3 isn't optional in Domain.evaluate().

    # `eta3` may or may not be periodic. e.g. In a full torus, vs a cylinder or a slice of the torus.
    # Check if f(eta3=0) == f(eta3=1)?
    # periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
    spl_kind_mapping_F = [False, True, periodic_eta3]
    cx_F, cy_F, cz_F = dom.interp_mapping(Nel, p, spl_kind_mapping_F, F_x, F_y, F_z)
    print(f'Shape of coefficients: cx {cx_F.shape} cy {cy_F.shape} cz {cz_F.shape}')

    # Doesn't exist in general 3D case!
    e3x = int((cx_F.shape[-1] - p[-1]) / 2 + p[-1])
    e3y = int((cy_F.shape[-1] - p[-1]) / 2 + p[-1])
    POLAR_SPACE_F = spl.Tensor_spline_space(spaces_FEM, ck=1, cx=cx_F[:, :, e3x], cy=cy_F[:, :, e3y])
    POLAR_SPACE_F.set_projectors('general')

    # Obtain polar spline space from F1 map.
    POLAR_SPACE_F1 = get_F1_polar_space(Nel, p, spaces_FEM)



    # ============================================================
    # Discretize input map into spline domain.
    # ============================================================

    spline_coeffs_file = os.path.join(temp_dir.name, 'spline_coeffs.hdf5')

    with h5py.File(spline_coeffs_file, 'w') as handle:
        handle['cx'] = cx_F
        handle['cy'] = cy_F
        handle['cz'] = cz_F
        handle.attrs['whatis'] = '3D spline coefficients constructed from domain map.'

    params_map = {
        'file': spline_coeffs_file,
        'Nel': Nel,
        'p': p,
        'spl_kind': spl_kind_mapping_F
    }

    DOMAIN_F = dom.Domain('spline', params_map=params_map)
    print('Discretized map into spline domain.')

    temp_dir.cleanup()
    print('Removed temp directory.')

    return DOMAIN_F, TENSOR_SPACE, POLAR_SPACE_F, POLAR_SPACE_F1



def verify_periodic_eta3(F_x, F_y, F_z):
    """Check whether the mapping is periodic in eta3, by randomly sampling 20 x 20 points in eta1 and eta2.
    """

    eta1_range   = np.random.random(20)
    eta2_range   = np.random.random(20)
    eta3_range_0 = np.array([0.])
    eta3_range_1 = np.array([1.])
    eta1_0, eta2_0, eta3_0 = np.meshgrid(eta1_range, eta2_range, eta3_range_0, indexing='ij', sparse=False)
    eta1_1, eta2_1, eta3_1 = np.meshgrid(eta1_range, eta2_range, eta3_range_1, indexing='ij', sparse=False)

    periodic_in_x = np.allclose(F_x(eta1_0, eta2_0, eta3_0), F_x(eta1_1, eta2_1, eta3_1))
    periodic_in_y = np.allclose(F_y(eta1_0, eta2_0, eta3_0), F_y(eta1_1, eta2_1, eta3_1))
    periodic_in_z = np.allclose(F_z(eta1_0, eta2_0, eta3_0), F_z(eta1_1, eta2_1, eta3_1))
    periodic = periodic_in_x and periodic_in_y and periodic_in_z
    print(f'Mapping is periodic in x? {periodic_in_x} y? {periodic_in_y} z? {periodic_in_z}')
    print(f'Mapping is {"" if periodic else "not "}periodic.')

    return periodic



def case_0form(params, func   , dfdx   , dfdy  , F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum, dfdz=None):

    import numpy as np

    print('Running test: 0-form and its gradient.')



    # ============================================================
    # Discretize domain map and construct splines.
    # ============================================================

    if DOMAIN_ANALYTICAL is not None:
        periodic_eta3 = DOMAIN_ANALYTICAL._periodic_eta3
    elif is_input_map_spline(map_type):
        periodic_eta3 = params['grid']['spl_kind'][-1] # Slice of GVEC in a cylinder, or a full 3D GVEC torus map.
        # Override default.
        if 'extru2d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'cyldr3d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'torus3d' in map_type.name.lower():
            # Can be True or False. True if it really is a full torus. False if it is a "periodic" slice.
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        else:
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)

    DOMAIN_F, TENSOR_SPACE, POLAR_SPACE_F, POLAR_SPACE_F1 = discretize_all(params, F_x, F_y, F_z, periodic_eta3)

    # Whether to replace discrete domain with its analytical source.
    if domain_enum == DomainType.ANALYTICAL:
        if is_input_map_spline(map_type):
            raise ValueError(f'Input {map_type.name} is already a discrete map. There is no analytical counterpart.')
        else:
            DOMAIN_F = DOMAIN_ANALYTICAL
            print(f'Replaced numerical DOMAIN_F with analytical one for map {map_type.name},')



    # ============================================================
    # Evaluation.
    # ============================================================

    # Use F for pullback!!!
    def fun_L_0(eta1, eta2, eta3):
        # Change back to analytical.
        return DOMAIN_F.pull(func, eta1, eta2, eta3, kind_fun='0_form', squeeze_output=False)

    # For comparing analytical derivative:
    if dfdz is None:
        print('Input function is only f(x,y).')
        grad_3d = [dfdx, dfdy, lambda x, y, z: np.zeros_like(x) + np.zeros_like(y) + np.zeros_like(z)]
    else:
        print('Input function is f(x,y,z).')
        grad_3d = [dfdx, dfdy, dfdz]
    def fun_L_1_1(eta1, eta2, eta3):
        return DOMAIN_F.pull(grad_3d, eta1, eta2, eta3, kind_fun='1_form_1', flat_eval=False, squeeze_output=False)
    def fun_L_1_2(eta1, eta2, eta3):
        return DOMAIN_F.pull(grad_3d, eta1, eta2, eta3, kind_fun='1_form_2', flat_eval=False, squeeze_output=False)
    def fun_L_1_3(eta1, eta2, eta3):
        return DOMAIN_F.pull(grad_3d, eta1, eta2, eta3, kind_fun='1_form_3', flat_eval=False, squeeze_output=False)
    fun_L_1 = [fun_L_1_1, fun_L_1_2, fun_L_1_3]

    proj_tensor_0form   = TENSOR_SPACE.projectors.pi_0(fun_L_0)
    proj_polar_F_0form  = POLAR_SPACE_F.projectors.pi_0(fun_L_0)
    proj_polar_F1_0form = POLAR_SPACE_F1.projectors.pi_0(fun_L_0)
    print(f'Shape of proj_tensor_0form   : {proj_tensor_0form.shape}')
    print(f'Shape of proj_polar_F_0form  : {proj_polar_F_0form.shape}')
    print(f'Shape of proj_polar_F1_0form : {proj_polar_F1_0form.shape}')

    # f[form]_[component]_[spline] are coefficients cijk.
    f0_ten    = TENSOR_SPACE.extract_0(proj_tensor_0form)
    f0_pol_F  = POLAR_SPACE_F.extract_0(proj_polar_F_0form)
    f0_pol_F1 = POLAR_SPACE_F1.extract_0(proj_polar_F1_0form)

    # Apply discrete gradient -> 1-form. Are all 3 components continuous when pushed forward?
    proj_tensor_1form   = TENSOR_SPACE.G.dot(proj_tensor_0form) # Or f0_ten. Unused because the shapes are identical.
    proj_polar_F_1form  = POLAR_SPACE_F.G.dot(proj_polar_F_0form)
    proj_polar_F1_1form = POLAR_SPACE_F1.G.dot(proj_polar_F1_0form)

    # f[form]_[component]_[spline] are coefficients cijk.
    f1_1_ten   , f1_2_ten   , f1_3_ten    = TENSOR_SPACE.extract_1(proj_tensor_1form)
    f1_1_pol_F , f1_2_pol_F , f1_3_pol_F  = POLAR_SPACE_F.extract_1(proj_polar_F_1form)
    f1_1_pol_F1, f1_2_pol_F1, f1_3_pol_F1 = POLAR_SPACE_F1.extract_1(proj_polar_F1_1form)

    # Grid for plotting.
    if 'use_el_b' in params['plot'] and params['plot']['use_el_b']:
        # Evaluate at element boundaries:
        eta1_range = TENSOR_SPACE.spaces[0].el_b
        eta2_range = TENSOR_SPACE.spaces[1].el_b
        eta3_range = TENSOR_SPACE.spaces[2].el_b
    elif 'eta_range' not in params['plot']:
        # Default:
        lim_s = 1
        num_s_log = 5
        eta1_range = np.concatenate((np.logspace(-num_s_log, -2, num_s_log*3-1), np.linspace(1e-2, lim_s, 101-num_s_log*3)[1:]))
        # eta1_range = np.linspace(1e-4, lim_s, 101)
        eta2_range = np.linspace(0, 1, 101)
        eta3_range = np.linspace(0, 1, 3)
    else:
        eta1_range = params['plot']['eta_range'][0]
        eta2_range = params['plot']['eta_range'][1]
        eta3_range = params['plot']['eta_range'][2]
    # print(f'eta1_range {eta1_range}')
    # print(f'eta2_range {eta2_range}')
    # print(f'eta3_range {eta3_range}')

    eta1, eta2, eta3 = np.meshgrid(eta1_range, eta2_range, eta3_range, indexing='ij', sparse=False)

    # Sanity check: If Jacobian determinant becomes negative somehow.
    det_df = DOMAIN_F.evaluate(eta1, eta2, eta3, 'det_df')
    print(f'Minimum value of Jacobian determinant: {np.min(det_df)}')
    if np.min(det_df) < -1e-5:
        raise ArithmeticError(f'Jacobian determinant must be non-negative, but we found minimum det_df={np.min(det_df)}!')

    # Evaluate test function.
    evaled_0_tensor   = TENSOR_SPACE.evaluate_NNN(eta1, eta2, eta3, f0_ten)
    evaled_0_polar_F  = POLAR_SPACE_F.evaluate_NNN(eta1, eta2, eta3, f0_pol_F)
    evaled_0_polar_F1 = POLAR_SPACE_F1.evaluate_NNN(eta1, eta2, eta3, f0_pol_F1)

    # Evaluate derivative.
    evaled_1_1_tensor   = TENSOR_SPACE.evaluate_DNN(eta1, eta2, eta3, f1_1_ten)
    evaled_1_1_polar_F  = POLAR_SPACE_F.evaluate_DNN(eta1, eta2, eta3, f1_1_pol_F)
    evaled_1_1_polar_F1 = POLAR_SPACE_F1.evaluate_DNN(eta1, eta2, eta3, f1_1_pol_F1)

    evaled_1_2_tensor   = TENSOR_SPACE.evaluate_NDN(eta1, eta2, eta3, f1_2_ten)
    evaled_1_2_polar_F  = POLAR_SPACE_F.evaluate_NDN(eta1, eta2, eta3, f1_2_pol_F)
    evaled_1_2_polar_F1 = POLAR_SPACE_F1.evaluate_NDN(eta1, eta2, eta3, f1_2_pol_F1)

    evaled_1_3_tensor   = TENSOR_SPACE.evaluate_NND(eta1, eta2, eta3, f1_3_ten)
    evaled_1_3_polar_F  = POLAR_SPACE_F.evaluate_NND(eta1, eta2, eta3, f1_3_pol_F)
    evaled_1_3_polar_F1 = POLAR_SPACE_F1.evaluate_NND(eta1, eta2, eta3, f1_3_pol_F1)

    evaled_1_tensor   = np.array([evaled_1_1_tensor  , evaled_1_2_tensor  , evaled_1_3_tensor  ])
    evaled_1_polar_F  = np.array([evaled_1_1_polar_F , evaled_1_2_polar_F , evaled_1_3_polar_F ])
    evaled_1_polar_F1 = np.array([evaled_1_1_polar_F1, evaled_1_2_polar_F1, evaled_1_3_polar_F1])



    # Positions of element boundaries.
    el_b_eta1, el_b_eta2, el_b_eta3 = np.meshgrid(TENSOR_SPACE.spaces[0].el_b, TENSOR_SPACE.spaces[1].el_b, TENSOR_SPACE.spaces[2].el_b, indexing='ij', sparse=False)
    xs = F_x(el_b_eta1, el_b_eta2, el_b_eta3)
    ys = F_y(el_b_eta1, el_b_eta2, el_b_eta3)
    zs = F_z(el_b_eta1, el_b_eta2, el_b_eta3)
    # Position of the pole.
    x0 = F_x(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    y0 = F_y(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    z0 = F_z(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    print(f'Origin of the (transformed) pole:')
    print(f'x0: {x0}')
    print(f'y0: {y0}')
    print(f'z0: {z0}')
    # Positions of the plotting grid.
    x = F_x(eta1, eta2, eta3)
    y = F_y(eta1, eta2, eta3)
    z = F_z(eta1, eta2, eta3)
    # Analytical evaluation of the trial function.
    orig_func = func(x, y, z)
    orig_grad = np.array([grad_i(x, y, z) for grad_i in grad_3d])


    # Short-circuit computation if we are plotting in logical space.
    if space_type == SpaceType.LOGICAL:

        orig_func = fun_L_0(eta1, eta2, eta3)
        orig_grad = np.array([fun_L_1_i(eta1, eta2, eta3) for fun_L_1_i in fun_L_1])

        print(f'Max |orig_func|          : {np.max(np.abs(orig_func))}')
        print(f'Max |pulled_F_0_tensor|  : {np.max(np.abs(evaled_0_tensor))}')
        print(f'Max |pulled_F_0_polar_F| : {np.max(np.abs(evaled_0_polar_F))}')
        print(f'Max |pulled_F_0_polar_F1|: {np.max(np.abs(evaled_0_polar_F1))}')
        print(f'Min |orig_func|          : {np.min(np.abs(orig_func))}')
        print(f'Min |pulled_F_0_tensor|  : {np.min(np.abs(evaled_0_tensor))}')
        print(f'Min |pulled_F_0_polar_F| : {np.min(np.abs(evaled_0_polar_F))}')
        print(f'Min |pulled_F_0_polar_F1|: {np.min(np.abs(evaled_0_polar_F1))}')

        return (eta1, eta2, eta3, np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5, el_b_eta1, el_b_eta2, el_b_eta3, det_df, 
        orig_func, evaled_0_tensor, evaled_0_polar_F, evaled_0_polar_F1, 
        orig_grad, evaled_1_tensor, evaled_1_polar_F, evaled_1_polar_F1)



    # Push to physical domain.
    pushed_F_0_tensor   = DOMAIN_F.push(evaled_0_tensor, eta1, eta2, eta3, kind_fun='0_form', squeeze_output=False)
    pushed_F_0_polar_F  = DOMAIN_F.push(evaled_0_polar_F, eta1, eta2, eta3, kind_fun='0_form', squeeze_output=False)
    pushed_F_0_polar_F1 = DOMAIN_F.push(evaled_0_polar_F1, eta1, eta2, eta3, kind_fun='0_form', squeeze_output=False)

    print(f'Max |orig_func|          : {np.max(np.abs(orig_func))}')
    print(f'Max |pushed_F_0_tensor|  : {np.max(np.abs(pushed_F_0_tensor))}')
    print(f'Max |pushed_F_0_polar_F| : {np.max(np.abs(pushed_F_0_polar_F))}')
    print(f'Max |pushed_F_0_polar_F1|: {np.max(np.abs(pushed_F_0_polar_F1))}')

    print(f'Min |orig_func|          : {np.min(np.abs(orig_func))}')
    print(f'Min |pushed_F_0_tensor|  : {np.min(np.abs(pushed_F_0_tensor))}')
    print(f'Min |pushed_F_0_polar_F| : {np.min(np.abs(pushed_F_0_polar_F))}')
    print(f'Min |pushed_F_0_polar_F1|: {np.min(np.abs(pushed_F_0_polar_F1))}')

    pushed_F_1_1_tensor   = DOMAIN_F.push(evaled_1_tensor, eta1, eta2, eta3, kind_fun='1_form_1', squeeze_output=False)
    pushed_F_1_1_polar_F  = DOMAIN_F.push(evaled_1_polar_F, eta1, eta2, eta3, kind_fun='1_form_1', squeeze_output=False)
    pushed_F_1_1_polar_F1 = DOMAIN_F.push(evaled_1_polar_F1, eta1, eta2, eta3, kind_fun='1_form_1', squeeze_output=False)

    pushed_F_1_2_tensor   = DOMAIN_F.push(evaled_1_tensor, eta1, eta2, eta3, kind_fun='1_form_2', squeeze_output=False)
    pushed_F_1_2_polar_F  = DOMAIN_F.push(evaled_1_polar_F, eta1, eta2, eta3, kind_fun='1_form_2', squeeze_output=False)
    pushed_F_1_2_polar_F1 = DOMAIN_F.push(evaled_1_polar_F1, eta1, eta2, eta3, kind_fun='1_form_2', squeeze_output=False)

    pushed_F_1_3_tensor   = DOMAIN_F.push(evaled_1_tensor, eta1, eta2, eta3, kind_fun='1_form_3', squeeze_output=False)
    pushed_F_1_3_polar_F  = DOMAIN_F.push(evaled_1_polar_F, eta1, eta2, eta3, kind_fun='1_form_3', squeeze_output=False)
    pushed_F_1_3_polar_F1 = DOMAIN_F.push(evaled_1_polar_F1, eta1, eta2, eta3, kind_fun='1_form_3', squeeze_output=False)

    pushed_F_1_tensor   = np.array([pushed_F_1_1_tensor  , pushed_F_1_2_tensor  , pushed_F_1_3_tensor  ])
    pushed_F_1_polar_F  = np.array([pushed_F_1_1_polar_F , pushed_F_1_2_polar_F , pushed_F_1_3_polar_F ])
    pushed_F_1_polar_F1 = np.array([pushed_F_1_1_polar_F1, pushed_F_1_2_polar_F1, pushed_F_1_3_polar_F1])

    print(f'Max |orig_grad|          : {np.max(np.abs(orig_grad))}')
    print(f'Max |pushed_F_1_tensor|  : {np.max(np.abs(pushed_F_1_tensor))}')
    print(f'Max |pushed_F_1_polar_F| : {np.max(np.abs(pushed_F_1_polar_F))}')
    print(f'Max |pushed_F_1_polar_F1|: {np.max(np.abs(pushed_F_1_polar_F1))}')

    print(f'Min |orig_grad|          : {np.min(np.abs(orig_grad))}')
    print(f'Min |pushed_F_1_tensor|  : {np.min(np.abs(pushed_F_1_tensor))}')
    print(f'Min |pushed_F_1_polar_F| : {np.min(np.abs(pushed_F_1_polar_F))}')
    print(f'Min |pushed_F_1_polar_F1|: {np.min(np.abs(pushed_F_1_polar_F1))}')



    print(f'Is pushed tensor equivalent to the original function? {np.allclose(orig_func, pushed_F_0_tensor)}')
    print(f'Is pushed polar_F equivalent to the original function? {np.allclose(orig_func, pushed_F_0_polar_F)}')
    print(f'Is pushed polar_F1 equivalent to the original function? {np.allclose(orig_func, pushed_F_0_polar_F1)}')
    print(f'Is pushed tensor equivalent to pushed polar_F? {np.allclose(pushed_F_0_tensor, pushed_F_0_polar_F)}')
    print(f'Shape of orig_func           : {orig_func.shape}')
    print(f'Shape of pushed_F_0_tensor   : {pushed_F_0_tensor.shape}')
    print(f'Shape of pushed_F_0_polar_F  : {pushed_F_0_polar_F.shape}')
    print(f'Shape of pushed_F_0_polar_F1 : {pushed_F_0_polar_F1.shape}')
    print(f'Shape of orig_grad           : {orig_grad.shape}')
    print(f'Shape of pushed_F_1_tensor   : {pushed_F_1_tensor.shape}')
    print(f'Shape of pushed_F_1_polar_F  : {pushed_F_1_polar_F.shape}')
    print(f'Shape of pushed_F_1_polar_F1 : {pushed_F_1_polar_F1.shape}')
    # print(orig_func-pushed_tensor)

    return (x, y, z, x0, y0, z0, xs, ys, zs, det_df, 
    orig_func, pushed_F_0_tensor, pushed_F_0_polar_F, pushed_F_0_polar_F1, 
    orig_grad, pushed_F_1_tensor, pushed_F_1_polar_F, pushed_F_1_polar_F1)



def case_1form(params, func_3d, curl_3d, div_3d, F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum):

    import numpy as np

    print('Running test: 1-form and its curl.')



    # ============================================================
    # Discretize domain map and construct splines.
    # ============================================================

    if DOMAIN_ANALYTICAL is not None:
        periodic_eta3 = DOMAIN_ANALYTICAL._periodic_eta3
    elif is_input_map_spline(map_type):
        periodic_eta3 = params['grid']['spl_kind'][-1] # Slice of GVEC in a cylinder, or a full 3D GVEC torus map.
        # Override default.
        if 'extru2d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'cyldr3d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'torus3d' in map_type.name.lower():
            # Can be True or False. True if it really is a full torus. False if it is a "periodic" slice.
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        else:
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)

    DOMAIN_F, TENSOR_SPACE, POLAR_SPACE_F, POLAR_SPACE_F1 = discretize_all(params, F_x, F_y, F_z, periodic_eta3)

    # Whether to replace discrete domain with its analytical source.
    if domain_enum == DomainType.ANALYTICAL:
        if is_input_map_spline(map_type):
            raise ValueError(f'Input {map_type.name} is already a discrete map. There is no analytical counterpart.')
        else:
            DOMAIN_F = DOMAIN_ANALYTICAL
            print(f'Replaced numerical DOMAIN_F with analytical one for map {map_type.name},')



    # ============================================================
    # Evaluation.
    # ============================================================

    # Use F for pullback!!!
    def fun_L_1_1(eta1, eta2, eta3):
        return DOMAIN_F.pull(func_3d, eta1, eta2, eta3, kind_fun='1_form_1', flat_eval=False, squeeze_output=False)
    def fun_L_1_2(eta1, eta2, eta3):
        return DOMAIN_F.pull(func_3d, eta1, eta2, eta3, kind_fun='1_form_2', flat_eval=False, squeeze_output=False)
    def fun_L_1_3(eta1, eta2, eta3):
        return DOMAIN_F.pull(func_3d, eta1, eta2, eta3, kind_fun='1_form_3', flat_eval=False, squeeze_output=False)
    fun_L_1 = [fun_L_1_1, fun_L_1_2, fun_L_1_3]

    # For comparing analytical derivative:
    def fun_L_2_1(eta1, eta2, eta3):
        return DOMAIN_F.pull(curl_3d, eta1, eta2, eta3, kind_fun='2_form_1', flat_eval=False, squeeze_output=False)
    def fun_L_2_2(eta1, eta2, eta3):
        return DOMAIN_F.pull(curl_3d, eta1, eta2, eta3, kind_fun='2_form_2', flat_eval=False, squeeze_output=False)
    def fun_L_2_3(eta1, eta2, eta3):
        return DOMAIN_F.pull(curl_3d, eta1, eta2, eta3, kind_fun='2_form_3', flat_eval=False, squeeze_output=False)
    fun_L_2 = [fun_L_2_1, fun_L_2_2, fun_L_2_3]

    proj_tensor_1form   = TENSOR_SPACE.projectors.pi_1(fun_L_1)
    proj_polar_F_1form  = POLAR_SPACE_F.projectors.pi_1(fun_L_1)
    proj_polar_F1_1form = POLAR_SPACE_F1.projectors.pi_1(fun_L_1)
    print(f'Shape of proj_tensor_1form   : {proj_tensor_1form.shape}')
    print(f'Shape of proj_polar_F_1form  : {proj_polar_F_1form.shape}')
    print(f'Shape of proj_polar_F1_1form : {proj_polar_F1_1form.shape}')

    # f[form]_[component]_[spline] are coefficients cijk.
    f1_1_ten   , f1_2_ten   , f1_3_ten    = TENSOR_SPACE.extract_1(proj_tensor_1form)
    f1_1_pol_F , f1_2_pol_F , f1_3_pol_F  = POLAR_SPACE_F.extract_1(proj_polar_F_1form)
    f1_1_pol_F1, f1_2_pol_F1, f1_3_pol_F1 = POLAR_SPACE_F1.extract_1(proj_polar_F1_1form)

    # Apply discrete curl -> 2-form. Are all 3 components continuous when pushed forward?
    proj_tensor_2form   = TENSOR_SPACE.C.dot(proj_tensor_1form)
    proj_polar_F_2form  = POLAR_SPACE_F.C.dot(proj_polar_F_1form)
    proj_polar_F1_2form = POLAR_SPACE_F1.C.dot(proj_polar_F1_1form)

    # f[form]_[component]_[spline] are coefficients cijk.
    f2_1_ten   , f2_2_ten   , f2_3_ten    = TENSOR_SPACE.extract_2(proj_tensor_2form)
    f2_1_pol_F , f2_2_pol_F , f2_3_pol_F  = POLAR_SPACE_F.extract_2(proj_polar_F_2form)
    f2_1_pol_F1, f2_2_pol_F1, f2_3_pol_F1 = POLAR_SPACE_F1.extract_2(proj_polar_F1_2form)

    # Grid for plotting.
    if 'use_el_b' in params['plot'] and params['plot']['use_el_b']:
        # Evaluate at element boundaries:
        eta1_range = TENSOR_SPACE.spaces[0].el_b
        eta2_range = TENSOR_SPACE.spaces[1].el_b
        eta3_range = TENSOR_SPACE.spaces[2].el_b
    elif 'eta_range' not in params['plot']:
        # Default:
        lim_s = 1
        num_s_log = 5
        eta1_range = np.concatenate((np.logspace(-num_s_log, -2, num_s_log*3-1), np.linspace(1e-2, lim_s, 101-num_s_log*3)[1:]))
        # eta1_range = np.linspace(1e-4, lim_s, 101)
        eta2_range = np.linspace(0, 1, 101)
        eta3_range = np.linspace(0, 1, 3)
    else:
        eta1_range = params['plot']['eta_range'][0]
        eta2_range = params['plot']['eta_range'][1]
        eta3_range = params['plot']['eta_range'][2]
    # print(f'eta1_range {eta1_range}')
    # print(f'eta2_range {eta2_range}')
    # print(f'eta3_range {eta3_range}')

    eta1, eta2, eta3 = np.meshgrid(eta1_range, eta2_range, eta3_range, indexing='ij', sparse=False)

    # Sanity check: If Jacobian determinant becomes negative somehow.
    det_df = DOMAIN_F.evaluate(eta1, eta2, eta3, 'det_df')
    print(f'Minimum value of Jacobian determinant: {np.min(det_df)}')
    if np.min(det_df) < -1e-5:
        raise ArithmeticError(f'Jacobian determinant must be non-negative, but we found minimum det_df={np.min(det_df)}!')

    # Evaluate test function.
    evaled_1_1_tensor   = TENSOR_SPACE.evaluate_DNN(eta1, eta2, eta3, f1_1_ten)
    evaled_1_1_polar_F  = POLAR_SPACE_F.evaluate_DNN(eta1, eta2, eta3, f1_1_pol_F)
    evaled_1_1_polar_F1 = POLAR_SPACE_F1.evaluate_DNN(eta1, eta2, eta3, f1_1_pol_F1)

    evaled_1_2_tensor   = TENSOR_SPACE.evaluate_NDN(eta1, eta2, eta3, f1_2_ten)
    evaled_1_2_polar_F  = POLAR_SPACE_F.evaluate_NDN(eta1, eta2, eta3, f1_2_pol_F)
    evaled_1_2_polar_F1 = POLAR_SPACE_F1.evaluate_NDN(eta1, eta2, eta3, f1_2_pol_F1)

    evaled_1_3_tensor   = TENSOR_SPACE.evaluate_NND(eta1, eta2, eta3, f1_3_ten)
    evaled_1_3_polar_F  = POLAR_SPACE_F.evaluate_NND(eta1, eta2, eta3, f1_3_pol_F)
    evaled_1_3_polar_F1 = POLAR_SPACE_F1.evaluate_NND(eta1, eta2, eta3, f1_3_pol_F1)

    evaled_1_tensor   = np.array([evaled_1_1_tensor  , evaled_1_2_tensor  , evaled_1_3_tensor  ])
    evaled_1_polar_F  = np.array([evaled_1_1_polar_F , evaled_1_2_polar_F , evaled_1_3_polar_F ])
    evaled_1_polar_F1 = np.array([evaled_1_1_polar_F1, evaled_1_2_polar_F1, evaled_1_3_polar_F1])

    # Evaluate derivative.
    evaled_2_1_tensor   = TENSOR_SPACE.evaluate_NDD(eta1, eta2, eta3, f2_1_ten)
    evaled_2_1_polar_F  = POLAR_SPACE_F.evaluate_NDD(eta1, eta2, eta3, f2_1_pol_F)
    evaled_2_1_polar_F1 = POLAR_SPACE_F1.evaluate_NDD(eta1, eta2, eta3, f2_1_pol_F1)

    evaled_2_2_tensor   = TENSOR_SPACE.evaluate_DND(eta1, eta2, eta3, f2_2_ten)
    evaled_2_2_polar_F  = POLAR_SPACE_F.evaluate_DND(eta1, eta2, eta3, f2_2_pol_F)
    evaled_2_2_polar_F1 = POLAR_SPACE_F1.evaluate_DND(eta1, eta2, eta3, f2_2_pol_F1)

    evaled_2_3_tensor   = TENSOR_SPACE.evaluate_DDN(eta1, eta2, eta3, f2_3_ten)
    evaled_2_3_polar_F  = POLAR_SPACE_F.evaluate_DDN(eta1, eta2, eta3, f2_3_pol_F)
    evaled_2_3_polar_F1 = POLAR_SPACE_F1.evaluate_DDN(eta1, eta2, eta3, f2_3_pol_F1)

    evaled_2_tensor   = np.array([evaled_2_1_tensor  , evaled_2_2_tensor  , evaled_2_3_tensor  ])
    evaled_2_polar_F  = np.array([evaled_2_1_polar_F , evaled_2_2_polar_F , evaled_2_3_polar_F ])
    evaled_2_polar_F1 = np.array([evaled_2_1_polar_F1, evaled_2_2_polar_F1, evaled_2_3_polar_F1])



    # Positions of element boundaries.
    el_b_eta1, el_b_eta2, el_b_eta3 = np.meshgrid(TENSOR_SPACE.spaces[0].el_b, TENSOR_SPACE.spaces[1].el_b, TENSOR_SPACE.spaces[2].el_b, indexing='ij', sparse=False)
    xs = F_x(el_b_eta1, el_b_eta2, el_b_eta3)
    ys = F_y(el_b_eta1, el_b_eta2, el_b_eta3)
    zs = F_z(el_b_eta1, el_b_eta2, el_b_eta3)
    # Position of the pole.
    x0 = F_x(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    y0 = F_y(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    z0 = F_z(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    print(f'Origin of the (transformed) pole:')
    print(f'x0: {x0}')
    print(f'y0: {y0}')
    print(f'z0: {z0}')
    # Positions of the plotting grid.
    x = F_x(eta1, eta2, eta3)
    y = F_y(eta1, eta2, eta3)
    z = F_z(eta1, eta2, eta3)
    # Analytical evaluation of the trial function.
    orig_func = func_3d(x, y, z)
    orig_curl = curl_3d(x, y, z)

    # Short-circuit computation if we are plotting in logical space.
    if space_type == SpaceType.LOGICAL:
        orig_func = np.array([fun_L_1_i(eta1, eta2, eta3) for fun_L_1_i in fun_L_1])
        orig_curl = np.array([fun_L_2_i(eta1, eta2, eta3) for fun_L_2_i in fun_L_2])
        return (eta1, eta2, eta3, np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5, el_b_eta1, el_b_eta2, el_b_eta3, det_df, 
        orig_func, evaled_1_tensor, evaled_1_polar_F, evaled_1_polar_F1, 
        orig_curl, evaled_2_tensor, evaled_2_polar_F, evaled_2_polar_F1)



    # Push to physical domain.
    pushed_F_1_1_tensor   = DOMAIN_F.push(evaled_1_tensor, eta1, eta2, eta3, kind_fun='1_form_1', squeeze_output=False)
    pushed_F_1_1_polar_F  = DOMAIN_F.push(evaled_1_polar_F, eta1, eta2, eta3, kind_fun='1_form_1', squeeze_output=False)
    pushed_F_1_1_polar_F1 = DOMAIN_F.push(evaled_1_polar_F1, eta1, eta2, eta3, kind_fun='1_form_1', squeeze_output=False)

    pushed_F_1_2_tensor   = DOMAIN_F.push(evaled_1_tensor, eta1, eta2, eta3, kind_fun='1_form_2', squeeze_output=False)
    pushed_F_1_2_polar_F  = DOMAIN_F.push(evaled_1_polar_F, eta1, eta2, eta3, kind_fun='1_form_2', squeeze_output=False)
    pushed_F_1_2_polar_F1 = DOMAIN_F.push(evaled_1_polar_F1, eta1, eta2, eta3, kind_fun='1_form_2', squeeze_output=False)

    pushed_F_1_3_tensor   = DOMAIN_F.push(evaled_1_tensor, eta1, eta2, eta3, kind_fun='1_form_3', squeeze_output=False)
    pushed_F_1_3_polar_F  = DOMAIN_F.push(evaled_1_polar_F, eta1, eta2, eta3, kind_fun='1_form_3', squeeze_output=False)
    pushed_F_1_3_polar_F1 = DOMAIN_F.push(evaled_1_polar_F1, eta1, eta2, eta3, kind_fun='1_form_3', squeeze_output=False)

    pushed_F_1_tensor   = np.array([pushed_F_1_1_tensor  , pushed_F_1_2_tensor  , pushed_F_1_3_tensor  ])
    pushed_F_1_polar_F  = np.array([pushed_F_1_1_polar_F , pushed_F_1_2_polar_F , pushed_F_1_3_polar_F ])
    pushed_F_1_polar_F1 = np.array([pushed_F_1_1_polar_F1, pushed_F_1_2_polar_F1, pushed_F_1_3_polar_F1])

    print(f'Max |orig_func|          : {np.max(np.abs(orig_func))}')
    print(f'Max |pushed_F_1_tensor|  : {np.max(np.abs(pushed_F_1_tensor))}')
    print(f'Max |pushed_F_1_polar_F| : {np.max(np.abs(pushed_F_1_polar_F))}')
    print(f'Max |pushed_F_1_polar_F1|: {np.max(np.abs(pushed_F_1_polar_F1))}')

    print(f'Min |orig_func|          : {np.min(np.abs(orig_func))}')
    print(f'Min |pushed_F_1_tensor|  : {np.min(np.abs(pushed_F_1_tensor))}')
    print(f'Min |pushed_F_1_polar_F| : {np.min(np.abs(pushed_F_1_polar_F))}')
    print(f'Min |pushed_F_1_polar_F1|: {np.min(np.abs(pushed_F_1_polar_F1))}')

    pushed_F_2_1_tensor   = DOMAIN_F.push(evaled_2_tensor, eta1, eta2, eta3, kind_fun='2_form_1', squeeze_output=False)
    pushed_F_2_1_polar_F  = DOMAIN_F.push(evaled_2_polar_F, eta1, eta2, eta3, kind_fun='2_form_1', squeeze_output=False)
    pushed_F_2_1_polar_F1 = DOMAIN_F.push(evaled_2_polar_F1, eta1, eta2, eta3, kind_fun='2_form_1', squeeze_output=False)

    pushed_F_2_2_tensor   = DOMAIN_F.push(evaled_2_tensor, eta1, eta2, eta3, kind_fun='2_form_2', squeeze_output=False)
    pushed_F_2_2_polar_F  = DOMAIN_F.push(evaled_2_polar_F, eta1, eta2, eta3, kind_fun='2_form_2', squeeze_output=False)
    pushed_F_2_2_polar_F1 = DOMAIN_F.push(evaled_2_polar_F1, eta1, eta2, eta3, kind_fun='2_form_2', squeeze_output=False)

    pushed_F_2_3_tensor   = DOMAIN_F.push(evaled_2_tensor, eta1, eta2, eta3, kind_fun='2_form_3', squeeze_output=False)
    pushed_F_2_3_polar_F  = DOMAIN_F.push(evaled_2_polar_F, eta1, eta2, eta3, kind_fun='2_form_3', squeeze_output=False)
    pushed_F_2_3_polar_F1 = DOMAIN_F.push(evaled_2_polar_F1, eta1, eta2, eta3, kind_fun='2_form_3', squeeze_output=False)

    pushed_F_2_tensor   = np.array([pushed_F_2_1_tensor  , pushed_F_2_2_tensor  , pushed_F_2_3_tensor  ])
    pushed_F_2_polar_F  = np.array([pushed_F_2_1_polar_F , pushed_F_2_2_polar_F , pushed_F_2_3_polar_F ])
    pushed_F_2_polar_F1 = np.array([pushed_F_2_1_polar_F1, pushed_F_2_2_polar_F1, pushed_F_2_3_polar_F1])

    print(f'Max |orig_curl|          : {np.max(np.abs(orig_curl))}')
    print(f'Max |pushed_F_2_tensor|  : {np.max(np.abs(pushed_F_2_tensor))}')
    print(f'Max |pushed_F_2_polar_F| : {np.max(np.abs(pushed_F_2_polar_F))}')
    print(f'Max |pushed_F_2_polar_F1|: {np.max(np.abs(pushed_F_2_polar_F1))}')

    print(f'Min |orig_curl|          : {np.min(np.abs(orig_curl))}')
    print(f'Min |pushed_F_2_tensor|  : {np.min(np.abs(pushed_F_2_tensor))}')
    print(f'Min |pushed_F_2_polar_F| : {np.min(np.abs(pushed_F_2_polar_F))}')
    print(f'Min |pushed_F_2_polar_F1|: {np.min(np.abs(pushed_F_2_polar_F1))}')



    print(f'Is pushed tensor equivalent to the original function? {np.allclose(orig_func, pushed_F_1_tensor)}')
    print(f'Is pushed polar_F equivalent to the original function? {np.allclose(orig_func, pushed_F_1_polar_F)}')
    print(f'Is pushed polar_F1 equivalent to the original function? {np.allclose(orig_func, pushed_F_1_polar_F1)}')
    print(f'Is pushed tensor equivalent to pushed polar_F? {np.allclose(pushed_F_1_tensor, pushed_F_1_polar_F)}')
    print(f'Shape of orig_func           : {orig_func.shape}')
    print(f'Shape of orig_curl           : {orig_curl.shape}')
    print(f'Shape of pushed_F_1_tensor   : {pushed_F_1_tensor.shape}')
    print(f'Shape of pushed_F_1_polar_F  : {pushed_F_1_polar_F.shape}')
    print(f'Shape of pushed_F_1_polar_F1 : {pushed_F_1_polar_F1.shape}')
    # print(orig_func-pushed_tensor)

    return (x, y, z, x0, y0, z0, xs, ys, zs, det_df, 
    orig_func, pushed_F_1_tensor, pushed_F_1_polar_F, pushed_F_1_polar_F1, 
    orig_curl, pushed_F_2_tensor, pushed_F_2_polar_F, pushed_F_2_polar_F1)



def case_2form(params, func_3d, curl_3d, div_3d, F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum):

    import numpy as np

    print('Running test: 2-form and its divergence.')



    # ============================================================
    # Discretize domain map and construct splines.
    # ============================================================

    if DOMAIN_ANALYTICAL is not None:
        periodic_eta3 = DOMAIN_ANALYTICAL._periodic_eta3
    elif is_input_map_spline(map_type):
        periodic_eta3 = params['grid']['spl_kind'][-1] # Slice of GVEC in a cylinder, or a full 3D GVEC torus map.
        # Override default.
        if 'extru2d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'cyldr3d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'torus3d' in map_type.name.lower():
            # Can be True or False. True if it really is a full torus. False if it is a "periodic" slice.
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        else:
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)

    DOMAIN_F, TENSOR_SPACE, POLAR_SPACE_F, POLAR_SPACE_F1 = discretize_all(params, F_x, F_y, F_z, periodic_eta3)

    # Whether to replace discrete domain with its analytical source.
    if domain_enum == DomainType.ANALYTICAL:
        if is_input_map_spline(map_type):
            raise ValueError(f'Input {map_type.name} is already a discrete map. There is no analytical counterpart.')
        else:
            DOMAIN_F = DOMAIN_ANALYTICAL
            print(f'Replaced numerical DOMAIN_F with analytical one for map {map_type.name},')



    # ============================================================
    # Evaluation.
    # ============================================================

    # Use F for pullback!!!
    def fun_L_2_1(eta1, eta2, eta3):
        return DOMAIN_F.pull(func_3d, eta1, eta2, eta3, kind_fun='2_form_1', flat_eval=False, squeeze_output=False)
    def fun_L_2_2(eta1, eta2, eta3):
        return DOMAIN_F.pull(func_3d, eta1, eta2, eta3, kind_fun='2_form_2', flat_eval=False, squeeze_output=False)
    def fun_L_2_3(eta1, eta2, eta3):
        return DOMAIN_F.pull(func_3d, eta1, eta2, eta3, kind_fun='2_form_3', flat_eval=False, squeeze_output=False)
    fun_L_2 = [fun_L_2_1, fun_L_2_2, fun_L_2_3]

    # For comparing analytical derivative:
    def fun_L_3(eta1, eta2, eta3):
        return DOMAIN_F.pull(div_3d, eta1, eta2, eta3, kind_fun='3_form', flat_eval=False, squeeze_output=False)

    proj_tensor_2form   = TENSOR_SPACE.projectors.pi_2(fun_L_2)
    proj_polar_F_2form  = POLAR_SPACE_F.projectors.pi_2(fun_L_2)
    proj_polar_F1_2form = POLAR_SPACE_F1.projectors.pi_2(fun_L_2)
    print(f'Shape of proj_tensor_2form   : {proj_tensor_2form.shape}')
    print(f'Shape of proj_polar_F_2form  : {proj_polar_F_2form.shape}')
    print(f'Shape of proj_polar_F1_2form : {proj_polar_F1_2form.shape}')

    # f[form]_[component]_[spline] are coefficients cijk.
    f2_1_ten   , f2_2_ten   , f2_3_ten    = TENSOR_SPACE.extract_2(proj_tensor_2form)
    f2_1_pol_F , f2_2_pol_F , f2_3_pol_F  = POLAR_SPACE_F.extract_2(proj_polar_F_2form)
    f2_1_pol_F1, f2_2_pol_F1, f2_3_pol_F1 = POLAR_SPACE_F1.extract_2(proj_polar_F1_2form)

    # Apply discrete divergence -> 3-form. Are all 3 components continuous when pushed forward?
    proj_tensor_3form   = TENSOR_SPACE.D.dot(proj_tensor_2form)
    proj_polar_F_3form  = POLAR_SPACE_F.D.dot(proj_polar_F_2form)
    proj_polar_F1_3form = POLAR_SPACE_F1.D.dot(proj_polar_F1_2form)

    # f[form]_[component]_[spline] are coefficients cijk.
    f3_ten    = TENSOR_SPACE.extract_3(proj_tensor_3form)
    f3_pol_F  = POLAR_SPACE_F.extract_3(proj_polar_F_3form)
    f3_pol_F1 = POLAR_SPACE_F1.extract_3(proj_polar_F1_3form)

    # Grid for plotting.
    if 'use_el_b' in params['plot'] and params['plot']['use_el_b']:
        # Evaluate at element boundaries:
        eta1_range = TENSOR_SPACE.spaces[0].el_b
        eta2_range = TENSOR_SPACE.spaces[1].el_b
        eta3_range = TENSOR_SPACE.spaces[2].el_b
    elif 'eta_range' not in params['plot']:
        # Default:
        lim_s = 1
        num_s_log = 5
        eta1_range = np.concatenate((np.logspace(-num_s_log, -2, num_s_log*3-1), np.linspace(1e-2, lim_s, 101-num_s_log*3)[1:]))
        # eta1_range = np.linspace(1e-4, lim_s, 101)
        eta2_range = np.linspace(0, 1, 101)
        eta3_range = np.linspace(0, 1, 3)
    else:
        eta1_range = params['plot']['eta_range'][0]
        eta2_range = params['plot']['eta_range'][1]
        eta3_range = params['plot']['eta_range'][2]
    # print(f'eta1_range {eta1_range}')
    # print(f'eta2_range {eta2_range}')
    # print(f'eta3_range {eta3_range}')

    eta1, eta2, eta3 = np.meshgrid(eta1_range, eta2_range, eta3_range, indexing='ij', sparse=False)

    # Sanity check: If Jacobian determinant becomes negative somehow.
    det_df = DOMAIN_F.evaluate(eta1, eta2, eta3, 'det_df')
    print(f'Minimum value of Jacobian determinant: {np.min(det_df)}')
    if np.min(det_df) < -1e-5:
        raise ArithmeticError(f'Jacobian determinant must be non-negative, but we found minimum det_df={np.min(det_df)}!')

    # Evaluate test function.
    evaled_2_1_tensor   = TENSOR_SPACE.evaluate_NDD(eta1, eta2, eta3, f2_1_ten)
    evaled_2_1_polar_F  = POLAR_SPACE_F.evaluate_NDD(eta1, eta2, eta3, f2_1_pol_F)
    evaled_2_1_polar_F1 = POLAR_SPACE_F1.evaluate_NDD(eta1, eta2, eta3, f2_1_pol_F1)

    evaled_2_2_tensor   = TENSOR_SPACE.evaluate_DND(eta1, eta2, eta3, f2_2_ten)
    evaled_2_2_polar_F  = POLAR_SPACE_F.evaluate_DND(eta1, eta2, eta3, f2_2_pol_F)
    evaled_2_2_polar_F1 = POLAR_SPACE_F1.evaluate_DND(eta1, eta2, eta3, f2_2_pol_F1)

    evaled_2_3_tensor   = TENSOR_SPACE.evaluate_DDN(eta1, eta2, eta3, f2_3_ten)
    evaled_2_3_polar_F  = POLAR_SPACE_F.evaluate_DDN(eta1, eta2, eta3, f2_3_pol_F)
    evaled_2_3_polar_F1 = POLAR_SPACE_F1.evaluate_DDN(eta1, eta2, eta3, f2_3_pol_F1)

    evaled_2_tensor   = np.array([evaled_2_1_tensor  , evaled_2_2_tensor  , evaled_2_3_tensor  ])
    evaled_2_polar_F  = np.array([evaled_2_1_polar_F , evaled_2_2_polar_F , evaled_2_3_polar_F ])
    evaled_2_polar_F1 = np.array([evaled_2_1_polar_F1, evaled_2_2_polar_F1, evaled_2_3_polar_F1])

    # Evaluate derivative.
    evaled_3_tensor   = TENSOR_SPACE.evaluate_DDD(eta1, eta2, eta3, f3_ten)
    evaled_3_polar_F  = POLAR_SPACE_F.evaluate_DDD(eta1, eta2, eta3, f3_pol_F)
    evaled_3_polar_F1 = POLAR_SPACE_F1.evaluate_DDD(eta1, eta2, eta3, f3_pol_F1)



    # Positions of element boundaries.
    el_b_eta1, el_b_eta2, el_b_eta3 = np.meshgrid(TENSOR_SPACE.spaces[0].el_b, TENSOR_SPACE.spaces[1].el_b, TENSOR_SPACE.spaces[2].el_b, indexing='ij', sparse=False)
    xs = F_x(el_b_eta1, el_b_eta2, el_b_eta3)
    ys = F_y(el_b_eta1, el_b_eta2, el_b_eta3)
    zs = F_z(el_b_eta1, el_b_eta2, el_b_eta3)
    # Position of the pole.
    x0 = F_x(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    y0 = F_y(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    z0 = F_z(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    print(f'Origin of the (transformed) pole:')
    print(f'x0: {x0}')
    print(f'y0: {y0}')
    print(f'z0: {z0}')
    # Positions of the plotting grid.
    x = F_x(eta1, eta2, eta3)
    y = F_y(eta1, eta2, eta3)
    z = F_z(eta1, eta2, eta3)
    # Analytical evaluation of the trial function.
    orig_func = func_3d(x, y, z)
    orig_div  = div_3d(x, y, z)

    # Short-circuit computation if we are plotting in logical space.
    if space_type == SpaceType.LOGICAL:
        orig_func = np.array([fun_L_2_i(eta1, eta2, eta3) for fun_L_2_i in fun_L_2])
        orig_div  = fun_L_3(eta1, eta2, eta3)
        return (eta1, eta2, eta3, np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5, el_b_eta1, el_b_eta2, el_b_eta3, det_df, 
        orig_func, evaled_2_tensor, evaled_2_polar_F, evaled_2_polar_F1, 
        orig_div , evaled_3_tensor, evaled_3_polar_F, evaled_3_polar_F1)



    # Push to physical domain.
    pushed_F_2_1_tensor   = DOMAIN_F.push(evaled_2_tensor, eta1, eta2, eta3, kind_fun='2_form_1', squeeze_output=False)
    pushed_F_2_1_polar_F  = DOMAIN_F.push(evaled_2_polar_F, eta1, eta2, eta3, kind_fun='2_form_1', squeeze_output=False)
    pushed_F_2_1_polar_F1 = DOMAIN_F.push(evaled_2_polar_F1, eta1, eta2, eta3, kind_fun='2_form_1', squeeze_output=False)

    pushed_F_2_2_tensor   = DOMAIN_F.push(evaled_2_tensor, eta1, eta2, eta3, kind_fun='2_form_2', squeeze_output=False)
    pushed_F_2_2_polar_F  = DOMAIN_F.push(evaled_2_polar_F, eta1, eta2, eta3, kind_fun='2_form_2', squeeze_output=False)
    pushed_F_2_2_polar_F1 = DOMAIN_F.push(evaled_2_polar_F1, eta1, eta2, eta3, kind_fun='2_form_2', squeeze_output=False)

    pushed_F_2_3_tensor   = DOMAIN_F.push(evaled_2_tensor, eta1, eta2, eta3, kind_fun='2_form_3', squeeze_output=False)
    pushed_F_2_3_polar_F  = DOMAIN_F.push(evaled_2_polar_F, eta1, eta2, eta3, kind_fun='2_form_3', squeeze_output=False)
    pushed_F_2_3_polar_F1 = DOMAIN_F.push(evaled_2_polar_F1, eta1, eta2, eta3, kind_fun='2_form_3', squeeze_output=False)

    pushed_F_2_tensor   = np.array([pushed_F_2_1_tensor  , pushed_F_2_2_tensor  , pushed_F_2_3_tensor  ])
    pushed_F_2_polar_F  = np.array([pushed_F_2_1_polar_F , pushed_F_2_2_polar_F , pushed_F_2_3_polar_F ])
    pushed_F_2_polar_F1 = np.array([pushed_F_2_1_polar_F1, pushed_F_2_2_polar_F1, pushed_F_2_3_polar_F1])

    print(f'Max |orig_func|          : {np.max(np.abs(orig_func))}')
    print(f'Max |pushed_F_2_tensor|  : {np.max(np.abs(pushed_F_2_tensor))}')
    print(f'Max |pushed_F_2_polar_F| : {np.max(np.abs(pushed_F_2_polar_F))}')
    print(f'Max |pushed_F_2_polar_F1|: {np.max(np.abs(pushed_F_2_polar_F1))}')

    print(f'Min |orig_func|          : {np.min(np.abs(orig_func))}')
    print(f'Min |pushed_F_2_tensor|  : {np.min(np.abs(pushed_F_2_tensor))}')
    print(f'Min |pushed_F_2_polar_F| : {np.min(np.abs(pushed_F_2_polar_F))}')
    print(f'Min |pushed_F_2_polar_F1|: {np.min(np.abs(pushed_F_2_polar_F1))}')

    pushed_F_3_tensor   = DOMAIN_F.push(evaled_3_tensor, eta1, eta2, eta3, kind_fun='3_form', squeeze_output=False)
    pushed_F_3_polar_F  = DOMAIN_F.push(evaled_3_polar_F, eta1, eta2, eta3, kind_fun='3_form', squeeze_output=False)
    pushed_F_3_polar_F1 = DOMAIN_F.push(evaled_3_polar_F1, eta1, eta2, eta3, kind_fun='3_form', squeeze_output=False)

    print(f'Max |orig_div|           : {np.max(np.abs(orig_div))}')
    print(f'Max |pushed_F_3_tensor|  : {np.max(np.abs(pushed_F_3_tensor))}')
    print(f'Max |pushed_F_3_polar_F| : {np.max(np.abs(pushed_F_3_polar_F))}')
    print(f'Max |pushed_F_3_polar_F1|: {np.max(np.abs(pushed_F_3_polar_F1))}')

    print(f'Min |orig_div|           : {np.min(np.abs(orig_div))}')
    print(f'Min |pushed_F_3_tensor|  : {np.min(np.abs(pushed_F_3_tensor))}')
    print(f'Min |pushed_F_3_polar_F| : {np.min(np.abs(pushed_F_3_polar_F))}')
    print(f'Min |pushed_F_3_polar_F1|: {np.min(np.abs(pushed_F_3_polar_F1))}')



    print(f'Is pushed tensor equivalent to the original function? {np.allclose(orig_func, pushed_F_2_tensor)}')
    print(f'Is pushed polar_F equivalent to the original function? {np.allclose(orig_func, pushed_F_2_polar_F)}')
    print(f'Is pushed polar_F1 equivalent to the original function? {np.allclose(orig_func, pushed_F_2_polar_F1)}')
    print(f'Is pushed tensor equivalent to pushed polar_F? {np.allclose(pushed_F_2_tensor, pushed_F_2_polar_F)}')
    print(f'Shape of orig_func           : {orig_func.shape}')
    print(f'Shape of orig_div            : {orig_div.shape}')
    print(f'Shape of pushed_F_2_tensor   : {pushed_F_2_tensor.shape}')
    print(f'Shape of pushed_F_2_polar_F  : {pushed_F_2_polar_F.shape}')
    print(f'Shape of pushed_F_2_polar_F1 : {pushed_F_2_polar_F1.shape}')
    # print(orig_func-pushed_tensor)

    return (x, y, z, x0, y0, z0, xs, ys, zs, det_df, 
    orig_func, pushed_F_2_tensor, pushed_F_2_polar_F, pushed_F_2_polar_F1, 
    orig_div , pushed_F_3_tensor, pushed_F_3_polar_F, pushed_F_3_polar_F1)



def case_3form(params, func   , curl_3d, div_3d, F_x, F_y, F_z, DOMAIN_ANALYTICAL, map_type, space_type, domain_enum):

    import numpy as np

    print('Running test: 3-form projection only.')



    # ============================================================
    # Discretize domain map and construct splines.
    # ============================================================

    if DOMAIN_ANALYTICAL is not None:
        periodic_eta3 = DOMAIN_ANALYTICAL._periodic_eta3
    elif is_input_map_spline(map_type):
        periodic_eta3 = params['grid']['spl_kind'][-1] # Slice of GVEC in a cylinder, or a full 3D GVEC torus map.
        # Override default.
        if 'extru2d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'cyldr3d' in map_type.name.lower():
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        elif 'torus3d' in map_type.name.lower():
            # Can be True or False. True if it really is a full torus. False if it is a "periodic" slice.
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)
        else:
            periodic_eta3 = verify_periodic_eta3(F_x, F_y, F_z)

    DOMAIN_F, TENSOR_SPACE, POLAR_SPACE_F, POLAR_SPACE_F1 = discretize_all(params, F_x, F_y, F_z, periodic_eta3)

    # Whether to replace discrete domain with its analytical source.
    if domain_enum == DomainType.ANALYTICAL:
        if is_input_map_spline(map_type):
            raise ValueError(f'Input {map_type.name} is already a discrete map. There is no analytical counterpart.')
        else:
            DOMAIN_F = DOMAIN_ANALYTICAL
            print(f'Replaced numerical DOMAIN_F with analytical one for map {map_type.name},')



    # ============================================================
    # Evaluation.
    # ============================================================

    # Use F for pullback!!!
    def fun_L_3(eta1, eta2, eta3):
        return DOMAIN_F.pull(func, eta1, eta2, eta3, kind_fun='3_form', flat_eval=False, squeeze_output=False)

    proj_tensor_3form   = TENSOR_SPACE.projectors.pi_3(fun_L_3)
    proj_polar_F_3form  = POLAR_SPACE_F.projectors.pi_3(fun_L_3)
    proj_polar_F1_3form = POLAR_SPACE_F1.projectors.pi_3(fun_L_3)
    print(f'Shape of proj_tensor_3form   : {proj_tensor_3form.shape}')
    print(f'Shape of proj_polar_F_3form  : {proj_polar_F_3form.shape}')
    print(f'Shape of proj_polar_F1_3form : {proj_polar_F1_3form.shape}')

    # f[form]_[component]_[spline] are coefficients cijk.
    f3_ten    = TENSOR_SPACE.extract_3(proj_tensor_3form)
    f3_pol_F  = POLAR_SPACE_F.extract_3(proj_polar_F_3form)
    f3_pol_F1 = POLAR_SPACE_F1.extract_3(proj_polar_F1_3form)

    # Grid for plotting.
    if 'use_el_b' in params['plot'] and params['plot']['use_el_b']:
        # Evaluate at element boundaries:
        eta1_range = TENSOR_SPACE.spaces[0].el_b
        eta2_range = TENSOR_SPACE.spaces[1].el_b
        eta3_range = TENSOR_SPACE.spaces[2].el_b
    elif 'eta_range' not in params['plot']:
        # Default:
        lim_s = 1
        num_s_log = 5
        eta1_range = np.concatenate((np.logspace(-num_s_log, -2, num_s_log*3-1), np.linspace(1e-2, lim_s, 101-num_s_log*3)[1:]))
        # eta1_range = np.linspace(1e-4, lim_s, 101)
        eta2_range = np.linspace(0, 1, 101)
        eta3_range = np.linspace(0, 1, 3)
    else:
        eta1_range = params['plot']['eta_range'][0]
        eta2_range = params['plot']['eta_range'][1]
        eta3_range = params['plot']['eta_range'][2]
    # print(f'eta1_range {eta1_range}')
    # print(f'eta2_range {eta2_range}')
    # print(f'eta3_range {eta3_range}')

    eta1, eta2, eta3 = np.meshgrid(eta1_range, eta2_range, eta3_range, indexing='ij', sparse=False)

    # Sanity check: If Jacobian determinant becomes negative somehow.
    det_df = DOMAIN_F.evaluate(eta1, eta2, eta3, 'det_df')
    print(f'Minimum value of Jacobian determinant: {np.min(det_df)}')
    if np.min(det_df) < -1e-5:
        raise ArithmeticError(f'Jacobian determinant must be non-negative, but we found minimum det_df={np.min(det_df)}!')

    # Evaluate derivative.
    evaled_3_tensor   = TENSOR_SPACE.evaluate_DDD(eta1, eta2, eta3, f3_ten)
    evaled_3_polar_F  = POLAR_SPACE_F.evaluate_DDD(eta1, eta2, eta3, f3_pol_F)
    evaled_3_polar_F1 = POLAR_SPACE_F1.evaluate_DDD(eta1, eta2, eta3, f3_pol_F1)

    # Positions of element boundaries.
    el_b_eta1, el_b_eta2, el_b_eta3 = np.meshgrid(TENSOR_SPACE.spaces[0].el_b, TENSOR_SPACE.spaces[1].el_b, TENSOR_SPACE.spaces[2].el_b, indexing='ij', sparse=False)
    xs = F_x(el_b_eta1, el_b_eta2, el_b_eta3)
    ys = F_y(el_b_eta1, el_b_eta2, el_b_eta3)
    zs = F_z(el_b_eta1, el_b_eta2, el_b_eta3)
    # Position of the pole.
    x0 = F_x(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    y0 = F_y(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    z0 = F_z(np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5)
    print(f'Origin of the (transformed) pole:')
    print(f'x0: {x0}')
    print(f'y0: {y0}')
    print(f'z0: {z0}')
    # Positions of the plotting grid.
    x = F_x(eta1, eta2, eta3)
    y = F_y(eta1, eta2, eta3)
    z = F_z(eta1, eta2, eta3)
    # Analytical evaluation of the trial function.
    orig_func = func(x, y, z)

    # Short-circuit computation if we are plotting in logical space.
    if space_type == SpaceType.LOGICAL:
        orig_func = fun_L_3(eta1, eta2, eta3)
        return (eta1, eta2, eta3, np.zeros((1,1,1)), np.zeros((1,1,1)), np.zeros((1,1,1))+0.5, el_b_eta1, el_b_eta2, el_b_eta3, det_df, 
        orig_func, evaled_3_tensor, evaled_3_polar_F, evaled_3_polar_F1, 
        orig_func, evaled_3_tensor, evaled_3_polar_F, evaled_3_polar_F1)



    # Push to physical domain.
    pushed_F_3_tensor   = DOMAIN_F.push(evaled_3_tensor, eta1, eta2, eta3, kind_fun='3_form', squeeze_output=False)
    pushed_F_3_polar_F  = DOMAIN_F.push(evaled_3_polar_F, eta1, eta2, eta3, kind_fun='3_form', squeeze_output=False)
    pushed_F_3_polar_F1 = DOMAIN_F.push(evaled_3_polar_F1, eta1, eta2, eta3, kind_fun='3_form', squeeze_output=False)

    print(f'Max |orig_div|           : {np.max(np.abs(orig_func))}')
    print(f'Max |pushed_F_3_tensor|  : {np.max(np.abs(pushed_F_3_tensor))}')
    print(f'Max |pushed_F_3_polar_F| : {np.max(np.abs(pushed_F_3_polar_F))}')
    print(f'Max |pushed_F_3_polar_F1|: {np.max(np.abs(pushed_F_3_polar_F1))}')

    print(f'Min |orig_div|           : {np.min(np.abs(orig_func))}')
    print(f'Min |pushed_F_3_tensor|  : {np.min(np.abs(pushed_F_3_tensor))}')
    print(f'Min |pushed_F_3_polar_F| : {np.min(np.abs(pushed_F_3_polar_F))}')
    print(f'Min |pushed_F_3_polar_F1|: {np.min(np.abs(pushed_F_3_polar_F1))}')



    print(f'Is pushed tensor equivalent to the original function? {np.allclose(orig_func, pushed_F_3_tensor)}')
    print(f'Is pushed polar_F equivalent to the original function? {np.allclose(orig_func, pushed_F_3_polar_F)}')
    print(f'Is pushed polar_F1 equivalent to the original function? {np.allclose(orig_func, pushed_F_3_polar_F1)}')
    print(f'Is pushed tensor equivalent to pushed polar_F? {np.allclose(pushed_F_3_tensor, pushed_F_3_polar_F)}')
    print(f'Shape of orig_func           : {orig_func.shape}')
    print(f'Shape of pushed_F_3_tensor   : {pushed_F_3_tensor.shape}')
    print(f'Shape of pushed_F_3_polar_F  : {pushed_F_3_polar_F.shape}')
    print(f'Shape of pushed_F_3_polar_F1 : {pushed_F_3_polar_F1.shape}')
    # print(orig_func-pushed_tensor)

    return (x, y, z, x0, y0, z0, xs, ys, zs, det_df, 
    orig_func, pushed_F_3_tensor, pushed_F_3_polar_F, pushed_F_3_polar_F1, 
    orig_func, pushed_F_3_tensor, pushed_F_3_polar_F, pushed_F_3_polar_F1)



def map_enum_to_gvec_enum(map_enum:MapType) -> SampleEnum:
    """Identify a GVEC SampleEnum that corresponds to a given MapType.

    Parameters
    ----------
    map_enum : MapType
        Map type.

    Returns
    -------
    SampleEnum
        gvec_to_python's corresponding SampleEnum.
    """
    temp_identifier = map_enum.name.split('_')[-1]
    if temp_identifier == 'ELLIPSTELL':
        return SampleEnum.ELLIP_STELL_UPDATED
    elif temp_identifier == 'CIRCTOK':
        return SampleEnum.CIRC_TOK
    elif temp_identifier == 'E1D6M6D6':
        return SampleEnum.ELLIP_STELL_V2_E1D6_M6N6
    elif temp_identifier == 'E4D6M6D6':
        return SampleEnum.ELLIP_STELL_V2_E4D6_M6N6
    elif temp_identifier == 'E40D5M6D6':
        return SampleEnum.ELLIP_STELL_V2_E40D5_M6N6
    else:
        raise NotImplementedError(f'Unknown map type: {map_enum}.')



def get_gvec_map(Nel, p, spl_kind, nq_el, nq_pr, bc):
    """Hardcoded function to obtain GVEC from the `ellipstell` test case.

    Replace `params` inside this function to generalize it. Deprecated."""

    # ============================================================
    # Imports.
    # ============================================================

    import os
    import h5py
    import numpy as np
    import tempfile
    temp_dir = tempfile.TemporaryDirectory(prefix='STRUPHY-')
    print(f'Created temp directory at: {temp_dir.name}')

    basedir = os.path.dirname(os.path.realpath(__file__))
    # sys.path.insert(0, os.path.join(basedir, '..'))

    # Import necessary struphy.modules.
    import struphy.geometry.domain_3d as dom
    from gvec_to_python import GVEC
    from gvec_to_python.reader.gvec_reader import GVEC_Reader

    gvec_dir = os.path.abspath(os.path.join(basedir, '..', 'mhd_equil', 'gvec'))
    print(f'Path to GVEC eq    : {gvec_dir}')
    gvec_files   = [f for f in os.listdir(gvec_dir) if os.path.isfile(os.path.join(gvec_dir, f))]
    gvec_folders = [f for f in os.listdir(gvec_dir) if os.path.isdir( os.path.join(gvec_dir, f))]
    print(f'Files in GVEC eq   : {gvec_files}')
    print(f'Folders in GVEC eq : {gvec_folders}')
    print(' ')

    from struphy.fields_background.mhd_equil.gvec.interface import GVECtoSTRUPHY



    # ============================================================
    # Create fake input params.
    # ============================================================

    # Fake input params.
    params = {
        "mhd_equilibrium" : {
            "general" : {
                "type" : "gvec"
            },
            "params_gvec" : {
                "filepath" : 'struphy/mhd_equil/gvec/',
                "filename" : 'GVEC_ellipStell_profile_update_State_0000_00010000.dat', # .dat or .json
            },
        },
    }

    params['mhd_equilibrium']['params_gvec']['filepath'] = gvec_dir # Overwrite path, because this is a test file.
    params = params['mhd_equilibrium']['params_gvec']



    # ============================================================
    # Convert GVEC .dat output to .json.
    # ============================================================

    if params['filename'].endswith('.dat'):

        read_filepath = params['filepath']
        read_filename = params['filename']
        gvec_filepath = temp_dir.name
        gvec_filename = params['filename'][:-4] + '.json'
        reader = GVEC_Reader(read_filepath, read_filename, gvec_filepath, gvec_filename, with_spl_coef=True)

    elif params['filename'].endswith('.json'):

        gvec_filepath = params['filepath']
        gvec_filename = params['filename'][:-4] + '.json'



    # ============================================================
    # Load GVEC mapping.
    # ============================================================

    gvec = GVEC(gvec_filepath, gvec_filename)

    # f = gvec.mapfull.f # Full mapping, (s,u,v) to (x,y,z).
    # X = gvec.mapX.f    # Only x component of the mapping.
    # Y = gvec.mapY.f    # Only y component of the mapping.
    # Z = gvec.mapZ.f    # Only z component of the mapping.
    print('Loaded default GVEC mapping.')



    # ===============================================================
    # Map source domain
    # ===============================================================

    # Enable another layer of mapping, from STRUPHY's (eta1,eta2,eta3) to GVEC's (s,u,v).
    # bounds = [0.3,0.8,0.3,0.8,0.3,0.8]
    # bounds = {'b1': 0.3, 'e1': 0.8, 'b2': 0.3, 'e2': 0.8, 'b3': 0.3, 'e3': 0.8}
    bounds = {'b1': 0.0, 'e1': 1.0, 'b2': 0.0, 'e2': 1.0, 'b3': 0.0, 'e3': 1.0}
    SOURCE_DOMAIN = dom.Domain('cuboid', params_map=bounds)

    def s(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'x')

    def u(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'y')

    def v(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'z')

    def eta123_to_suv(eta1, eta2, eta3):
        return s(eta1, eta2, eta3), u(eta1, eta2, eta3), v(eta1, eta2, eta3)

    def f(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). All (x,y,z) components."""
        return gvec.mapfull.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3))

    # If eta3+0.25, eta1 will go from -4.7 to -3.3.
    # If eta3+0.75, eta1 will go from +3.3 to +4.7.

    # gvec.mapY.f = -R * sin(2*pi*eta3)
    # => gvec.mapY.f == R @ eta3=0.75

    def X(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only x-component."""
        return gvec.mapY.f(s(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0), u(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0), v(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0))

    def Y(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only y-component."""
        return gvec.mapZ.f(s(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0), u(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0), v(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0))

    def Z(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only z-component."""
        # return gvec.mapX.f(s(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0), u(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0), v(eta1,eta2,(np.zeros_like(eta3)+0.75)%1.0))
        return np.ones_like(eta1) * np.ones_like(eta2) * eta3
        # return v(eta1,eta2,eta3)

    # TODO: Swap Jacobian too? No. We only need Pi_0 projection to obtain spline coefficients, Jacobian is not evaluated.
    # TODO: Swap the trial function too? No.
    # TODO: Add another mapping in gvec_to_python that swaps? No. Overkill.



    # TODO: Below is not my code. It appeared during rebase.
    #       The sole purpose appears to be to initialize a `GVECtoSTRUPHY` class that is never returned/used.

    # ============================================================
    # Create FEM space and setup projectors.
    # ============================================================

    # 1d B-spline spline spaces for finite elements
    spaces_FEM = [spl.Spline_space_1d(Nel, p, spl_kind, nq_el) for Nel, p, spl_kind, nq_el in zip(Nel, p, spl_kind, nq_el)]
    # Set projectors.
    [space.set_projectors(nq=nq) for space, nq in zip(spaces_FEM, nq_pr) if not hasattr(space, 'projectors')]

    # 3d tensor-product B-spline space for finite elements
    TENSOR_SPACE = spl.Tensor_spline_space(spaces_FEM, ck=-1)
    # Set projectors.
    if not hasattr(TENSOR_SPACE, 'projectors'):
        # def set_projectors(self, which='tensor'). Use 'general' for polar splines.
        # Projectors from `Projectors_tensor_3d` class:
        TENSOR_SPACE.set_projectors('tensor') # No need to reshape into 3D with `extract_0()`.
        # Projectors from `Projectors_global_3d` class:
        # TENSOR_SPACE.set_projectors('general') # Need to reshape afterwards.
    print('Tensor space and projector set up done.')



    # ============================================================
    # Create splines (using PI_0 projector).
    # ============================================================

    # Calculate spline coefficients using PI_0 projector.
    # Projectors from `Projectors_tensor_3d` class.
    cx = TENSOR_SPACE.projectors.PI_0(X)
    cy = TENSOR_SPACE.projectors.PI_0(Y)
    cz = TENSOR_SPACE.projectors.PI_0(Z)
    # Reshape to 3D if using `pi_0()` from `Projectors_global_3d`.
    # cx = TENSOR_SPACE.projectors.pi_0(X)
    # cy = TENSOR_SPACE.projectors.pi_0(Y)
    # cz = TENSOR_SPACE.projectors.pi_0(Z)
    # cx = TENSOR_SPACE.extract_0(cx)
    # cy = TENSOR_SPACE.extract_0(cy)
    # cz = TENSOR_SPACE.extract_0(cz)

    spline_coeffs_file = os.path.join(temp_dir.name, 'spline_coeffs.hdf5')

    with h5py.File(spline_coeffs_file, 'w') as handle:
        handle['cx'] = cx
        handle['cy'] = cy
        handle['cz'] = cz
        handle.attrs['whatis'] = 'These are 3D spline coefficients constructed from GVEC mapping.'

    params_map = {
        'file': spline_coeffs_file,
        'Nel': Nel,
        'p': p,
        'spl_kind': spl_kind,
    }

    DOMAIN = dom.Domain('spline', params_map=params_map)
    print('Computed spline coefficients.')

    # Actual initialization.
    # Wouldn't work in this test file, because the axes are swapped.
    EQ_MHD = GVECtoSTRUPHY(params, DOMAIN, TENSOR_SPACE, SOURCE_DOMAIN)
    print('Initialized the `GVECtoSTRUPHY` class.')



    temp_dir.cleanup()
    print('Removed temp directory.')

    return X, Y, Z, gvec



def get_gvec_map_extru2d(sample_enum:SampleEnum, eta3_slice:float):
    """Extrude a slice of a sample GVEC equilibrium's toroidal map into a cylinder.

    Parameters
    ----------
    sample_enum : SampleEnum
        Which sample GVEC equilibrium to load.
    eta3_slice : float
        Which poloidal plane along eta3 direction to cut out as 2D and extrude into a 3D cylindrical object.

    Returns
    -------
    4-tuple
        Mapping functions in X, Y, Z, and a GVEC object."""

    # ============================================================
    # Imports.
    # ============================================================

    import os
    import numpy as np
    import tempfile
    temp_dir = tempfile.TemporaryDirectory(prefix='STRUPHY-')
    print(f'Created temp directory at: {temp_dir.name}')

    # basedir = os.path.dirname(os.path.realpath(__file__))
    basedir = os.path.abspath('')
    # sys.path.insert(0, os.path.join(basedir, '..'))

    # Import necessary struphy.modules.
    import struphy.geometry.domain_3d as dom
    from gvec_to_python.reader.sample_loader import SampleEnum, SampleEquilibrium



    # ============================================================
    # Load GVEC mapping.
    # ============================================================

    # New mechanism, using sample within `gvec_to_python` repo:
    user_path = os.path.join(basedir, 'gvec_to_python')
    sample_equilibrium = SampleEquilibrium(sample_enum, user_path=user_path)
    gvec = sample_equilibrium.get_gvec_object()

    # If user-provided equilibrium:
    # gvec = SampleEquilibrium.get_user_gvec_object(filepath, filename)

    print('Loaded default GVEC mapping.')



    # ===============================================================
    # Map source domain
    # ===============================================================

    # Enable another layer of mapping, from STRUPHY's (eta1,eta2,eta3) to GVEC's (s,u,v).
    # bounds = [0.3,0.8,0.3,0.8,0.3,0.8]
    # bounds = {'b1': 0.3, 'e1': 0.8, 'b2': 0.3, 'e2': 0.8, 'b3': 0.3, 'e3': 0.8}
    bounds = {'b1': 0.0, 'e1': 1.0, 'b2': 0.0, 'e2': 1.0, 'b3': 0.0, 'e3': 1.0}
    SOURCE_DOMAIN = dom.Domain('cuboid', params_map=bounds)

    def s(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'x')

    def u(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'y')

    def v(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'z')

    # gvec.mapY.f = -R * sin(2*pi*eta3)
    # => gvec.mapY.f == R @ eta3=0.75

    def X(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only x-component."""
        eta3 = (np.zeros_like(eta3) + eta3_slice) % 1.0
        return gvec.mapR.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3))

    def Y(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only y-component."""
        eta3 = (np.zeros_like(eta3) + eta3_slice) % 1.0
        return gvec.mapZ.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3))

    def Z(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only z-component."""
        return np.ones_like(eta1) * np.ones_like(eta2) * eta3

    temp_dir.cleanup()
    print('Removed temp directory.')

    return X, Y, Z, gvec



def get_gvec_map_cyldr3d(sample_enum:SampleEnum, eta3_offset:float, b3:float=0.0, e3:float=1.0):
    """Straighten a sample GVEC equilibrium's toroidal map into a cylindrical map.

    Parameters
    ----------
    sample_enum : SampleEnum
        Which sample GVEC equilibrium to load.
    eta3_offset : float
        Whether to offset eta3 coordinates to start at another poloidal plane.

    Returns
    -------
    4-tuple
        Mapping functions in X, Y, Z, and a GVEC object."""

    # ============================================================
    # Imports.
    # ============================================================

    import os
    import numpy as np
    import tempfile
    temp_dir = tempfile.TemporaryDirectory(prefix='STRUPHY-')
    print(f'Created temp directory at: {temp_dir.name}')

    # basedir = os.path.dirname(os.path.realpath(__file__))
    basedir = os.path.abspath('')
    # sys.path.insert(0, os.path.join(basedir, '..'))

    # Import necessary struphy.modules.
    import struphy.geometry.domain_3d as dom
    from gvec_to_python.reader.sample_loader import SampleEnum, SampleEquilibrium



    # ============================================================
    # Load GVEC mapping.
    # ============================================================

    # New mechanism, using sample within `gvec_to_python` repo:
    user_path = os.path.join(basedir, 'gvec_to_python')
    sample_equilibrium = SampleEquilibrium(sample_enum, user_path=user_path)
    gvec = sample_equilibrium.get_gvec_object()

    # If user-provided equilibrium:
    # gvec = SampleEquilibrium.get_user_gvec_object(filepath, filename)

    print('Loaded default GVEC mapping.')



    # ===============================================================
    # Map source domain
    # ===============================================================

    # Enable another layer of mapping, from STRUPHY's (eta1,eta2,eta3) to GVEC's (s,u,v).
    # bounds = [0.3,0.8,0.3,0.8,0.3,0.8]
    # bounds = {'b1': 0.3, 'e1': 0.8, 'b2': 0.3, 'e2': 0.8, 'b3': 0.3, 'e3': 0.8}
    # bounds = {'b1': 0.0, 'e1': 1.0, 'b2': 0.0, 'e2': 1.0, 'b3': 0.0, 'e3': 1.0}
    bounds = {'b1': 0.0, 'e1': 1.0, 'b2': 0.0, 'e2': 1.0, 'b3': b3, 'e3': e3}
    SOURCE_DOMAIN = dom.Domain('cuboid', params_map=bounds)

    def s(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'x')

    def u(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'y')

    def v(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'z')

    # gvec.mapY.f = -R * sin(2*pi*eta3)
    # => gvec.mapY.f == R @ eta3=0.75

    def X(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only x-component."""
        if isinstance(eta1, float):
            eta1 = np.array([eta1])
        if isinstance(eta2, float):
            eta2 = np.array([eta2])
        if isinstance(eta3, float):
            eta3 = np.array([eta3])
        if (eta3 + eta3_offset != 1.0).all():
            # Otherwise `verify_periodic_eta3` will report a false periodicity.
            eta3 = (eta3 + eta3_offset) % 1.0
        return gvec.mapR.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3))

    def Y(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only y-component."""
        if isinstance(eta1, float):
            eta1 = np.array([eta1])
        if isinstance(eta2, float):
            eta2 = np.array([eta2])
        if isinstance(eta3, float):
            eta3 = np.array([eta3])
        if (eta3 + eta3_offset != 1.0).all():
            # Otherwise `verify_periodic_eta3` will report a false periodicity.
            eta3 = (eta3 + eta3_offset) % 1.0
        return gvec.mapZ.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3))

    def Z(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only z-component."""
        return np.ones_like(eta1) * np.ones_like(eta2) * eta3

    temp_dir.cleanup()
    print('Removed temp directory.')

    return X, Y, Z, gvec



def get_gvec_map_torus3d(sample_enum:SampleEnum, eta3_offset:float, b3:float=0.0, e3:float=1.0):
    """Load a sample GVEC equilibrium contained inside the `gvec_to_python` repository.

    Parameters
    ----------
    sample_enum : SampleEnum
        Which sample GVEC equilibrium to load.
    eta3_offset : float
        Whether to offset eta3 coordinates to start at another poloidal plane.

    Returns
    -------
    4-tuple
        Mapping functions in X, Y, Z, and a GVEC object."""

    # ============================================================
    # Imports.
    # ============================================================

    import os
    import tempfile
    temp_dir = tempfile.TemporaryDirectory(prefix='STRUPHY-')
    print(f'Created temp directory at: {temp_dir.name}')

    # basedir = os.path.dirname(os.path.realpath(__file__))
    basedir = os.path.abspath('')
    # sys.path.insert(0, os.path.join(basedir, '..'))

    # Import necessary struphy.modules.
    import struphy.geometry.domain_3d as dom
    from gvec_to_python.reader.sample_loader import SampleEnum, SampleEquilibrium



    # ============================================================
    # Load GVEC mapping.
    # ============================================================

    # New mechanism, using sample within `gvec_to_python` repo:
    user_path = os.path.join(basedir, 'gvec_to_python')
    sample_equilibrium = SampleEquilibrium(sample_enum, user_path=user_path)
    gvec = sample_equilibrium.get_gvec_object()

    # If user-provided equilibrium:
    # gvec = SampleEquilibrium.get_user_gvec_object(filepath, filename)

    print('Loaded default GVEC mapping.')



    # ===============================================================
    # Map source domain
    # ===============================================================

    # Enable another layer of mapping, from STRUPHY's (eta1,eta2,eta3) to GVEC's (s,u,v).
    # bounds = [0.3,0.8,0.3,0.8,0.3,0.8]
    # bounds = {'b1': 0.3, 'e1': 0.8, 'b2': 0.3, 'e2': 0.8, 'b3': 0.3, 'e3': 0.8}
    # bounds = {'b1': 0.0, 'e1': 1.0, 'b2': 0.0, 'e2': 1.0, 'b3': 0.0, 'e3': 1.0}
    bounds = {'b1': 0.0, 'e1': 1.0, 'b2': 0.0, 'e2': 1.0, 'b3': b3, 'e3': e3}
    SOURCE_DOMAIN = dom.Domain('cuboid', params_map=bounds)

    def s(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'x')

    def u(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'y')

    def v(eta1, eta2, eta3):
        return SOURCE_DOMAIN.evaluate(eta1, eta2, eta3, 'z')

    # gvec.mapY.f = -R * sin(2*pi*eta3)
    # => gvec.mapY.f == R @ eta3=0.75

    def X(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only x-component."""
        if isinstance(eta1, float):
            eta1 = np.array([eta1])
        if isinstance(eta2, float):
            eta2 = np.array([eta2])
        if isinstance(eta3, float):
            eta3 = np.array([eta3])
        # eta10 = np.zeros_like(eta1)
        # eta20 = np.zeros_like(eta2)
        # eta30 = np.zeros_like(eta3) + eta3_offset
        # eta3 = (np.zeros_like(eta3) + eta3_offset) % 1.0
        if (eta3 + eta3_offset != 1.0).all():
            # Otherwise `verify_periodic_eta3` will report a false periodicity.
            eta3 = (eta3 + eta3_offset) % 1.0
        return gvec.mapY.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3)) # - gvec.mapY.f(s(eta10,eta20,eta30), u(eta10,eta20,eta30), v(eta10,eta20,eta30))

    def Y(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only y-component."""
        if isinstance(eta1, float):
            eta1 = np.array([eta1])
        if isinstance(eta2, float):
            eta2 = np.array([eta2])
        if isinstance(eta3, float):
            eta3 = np.array([eta3])
        # eta10 = np.zeros_like(eta1)
        # eta20 = np.zeros_like(eta2)
        # eta30 = np.zeros_like(eta3) + eta3_offset
        # eta3 = (np.zeros_like(eta3) + eta3_offset) % 1.0
        if (eta3 + eta3_offset != 1.0).all():
            # Otherwise `verify_periodic_eta3` will report a false periodicity.
            eta3 = (eta3 + eta3_offset) % 1.0
        return gvec.mapZ.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3)) # - gvec.mapZ.f(s(eta10,eta20,eta30), u(eta10,eta20,eta30), v(eta10,eta20,eta30))

    def Z(eta1, eta2, eta3):
        """Mapping that goes from (eta1,eta2,eta3) to (s,u,v) then to (x,y,z). Only z-component."""
        if isinstance(eta1, float):
            eta1 = np.array([eta1])
        if isinstance(eta2, float):
            eta2 = np.array([eta2])
        if isinstance(eta3, float):
            eta3 = np.array([eta3])
        # eta10 = np.zeros_like(eta1)
        # eta20 = np.zeros_like(eta2)
        # eta30 = np.zeros_like(eta3) + eta3_offset
        # eta3 = (np.zeros_like(eta3) + eta3_offset) % 1.0
        if (eta3 + eta3_offset != 1.0).all():
            # Otherwise `verify_periodic_eta3` will report a false periodicity.
            eta3 = (eta3 + eta3_offset) % 1.0
        return gvec.mapX.f(s(eta1,eta2,eta3), u(eta1,eta2,eta3), v(eta1,eta2,eta3)) # - gvec.mapX.f(s(eta10,eta20,eta30), u(eta10,eta20,eta30), v(eta10,eta20,eta30))

    temp_dir.cleanup()
    print('Removed temp directory.')

    return X, Y, Z, gvec



def compute_error(numerical:List, analytical:np.ndarray, eta2_pos:int, eta2_neg:int=None, eta3:int=0, normalize:bool=True, norm_enum:ErrorNorm=ErrorNorm.Li, scope_enum:ErrorScope=ErrorScope.LOCAL, scope_ratio:Tuple[float,float]=(0,0.05)):
    """Compute error along eta1, for a fixed value (index) of eta2 and eta3.

    Parameters
    ----------
    numerical : List of np.ndarray
        List of evaluated results for error computation. A list of 3D arrays or 4D ones with 3x 3D components.
    analytical : np.ndarray
        Reference "ground truth" solution for error compuation.
    eta2_pos : int
        An *index* of the input arrays, along a line in eta1 in the eta2 direction to evaluate the error.
        Can be obtained from `compute_eta2_cross_section()`.
        If not given, the entire ring of eta2 values will be included in error computation.
    eta2_neg : int
        An *index* that corresponds to `eta2 + 0.5`, which is on the opposite side of the eta2 line across pole at eta1=0.
        If not given, this other half of the eta2 line will be omitted.
    eta3 : int
        An *index* of the input arrays where a slice at eta3 is taken out for error evaluation.
        Note that this is an index, not a coordinate.
    normalize : bool
        Whether to normalize all errors, using the respective norms, on the entire reference array.
        Recommend leave it as `True` to return relative errors.
    norm_enum : ErrorNorm
        Which norm is used for error calculation.
    scope_enum : ErrorScope
        From where along eta1 is the error computed from.
        It can be a point that is closest to the pole, or a region of points around the pole, or globally throughout the eta2 line.
    scope_ratio : tuple of 2 float
        If `scope_enum` is LOCAL, what ratio along the eta2 line is used for evaluation.
        This applies to array index, not the actual eta1 values.

    Returns
    -------
    error : float
        Computed scalar error.
    """

    err = []

    eta2_ring = eta2_pos is None and eta2_neg is None
    if eta2_pos is None and eta2_neg is not None:
        raise ValueError(f'Incorrect input. `eta2_pos` cannot be `None` while `eta2_neg` is not `None`.')

    if analytical.ndim == 3:
        pass
    elif analytical.ndim == 4 and analytical.shape[0] == 3:
        pass
    else:
        raise ValueError(f'Input dimension not recognized. Shape: {analytical.shape}')

    if isinstance(scope_ratio, float):
        scope_ratio = (0, scope_ratio)

    if scope_enum == ErrorScope.POINT:
        eta1L = 0
        eta1R = 1
    elif scope_enum == ErrorScope.LOCAL:
        if analytical.ndim == 3:
            eta1L = int(scope_ratio[0] * analytical.shape[0])
            eta1R = int(scope_ratio[1] * analytical.shape[0])
            if scope_ratio[0] == 0.:
                eta1L = 0
            if scope_ratio[1] == 1.:
                eta1R = analytical.shape[0]
        elif analytical.ndim == 4 and analytical.shape[0] == 3:
            eta1L = int(scope_ratio[0] * analytical.shape[1])
            eta1R = int(scope_ratio[1] * analytical.shape[1])
            if scope_ratio[0] == 0.:
                eta1L = 0
            if scope_ratio[1] == 1.:
                eta1R = analytical.shape[1]
    elif scope_enum == ErrorScope.GLOBAL:
        if analytical.ndim == 3:
            eta1L = 0
            eta1R = analytical.shape[0]
        elif analytical.ndim == 4 and analytical.shape[0] == 3:
            eta1L = 0
            eta1R = analytical.shape[1]

    if norm_enum == ErrorNorm.L1: # Median absolute.

        if analytical.ndim == 3:
            for data in numerical:
                if eta2_ring:
                    err.append(
                        np.nanmedian(np.abs(data[eta1L:eta1R,:,eta3] - analytical[eta1L:eta1R,:,eta3]), axis=(0,1))
                    )
                elif eta2_neg is None:
                    err.append(
                        np.nanmedian(np.abs(data[eta1L:eta1R,eta2_pos,eta3] - analytical[eta1L:eta1R,eta2_pos,eta3]), axis=0)
                    )
                else:
                    err.append(
                        np.nanmedian(np.concatenate((
                            np.abs(data[eta1L:eta1R,eta2_pos,eta3] - analytical[eta1L:eta1R,eta2_pos,eta3]),
                            np.abs(data[eta1L:eta1R,eta2_neg,eta3] - analytical[eta1L:eta1R,eta2_neg,eta3])
                        )), axis=0)
                    )
        elif analytical.ndim == 4 and analytical.shape[0] == 3:
            for data in numerical:
                if eta2_ring:
                    err.append(
                        np.nanmedian(np.abs(data[:,eta1L:eta1R,:,eta3] - analytical[:,eta1L:eta1R,:,eta3]), axis=(1,2))
                    )
                elif eta2_neg is None:
                    err.append(
                        np.nanmedian(np.abs(data[:,eta1L:eta1R,eta2_pos,eta3] - analytical[:,eta1L:eta1R,eta2_pos,eta3]), axis=1)
                    )
                else:
                    err.append(
                        np.nanmedian(np.hstack((
                            np.abs(data[:,eta1L:eta1R,eta2_pos,eta3] - analytical[:,eta1L:eta1R,eta2_pos,eta3]),
                            np.abs(data[:,eta1L:eta1R,eta2_neg,eta3] - analytical[:,eta1L:eta1R,eta2_neg,eta3])
                        )), axis=1)
                    )

    elif norm_enum == ErrorNorm.L2: # Root mean square.

        if analytical.ndim == 3:
            for data in numerical:
                if eta2_ring:
                    err.append(
                        np.sqrt(np.nanmean(np.square(data[eta1L:eta1R,:,eta3] - analytical[eta1L:eta1R,:,eta3]), axis=(0,1)))
                    )
                elif eta2_neg is None:
                    err.append(
                        np.sqrt(np.nanmean(np.square(data[eta1L:eta1R,eta2_pos,eta3] - analytical[eta1L:eta1R,eta2_pos,eta3]), axis=0))
                    )
                else:
                    err.append(
                        np.sqrt(np.nanmean(np.concatenate((
                            np.square(data[eta1L:eta1R,eta2_pos,eta3] - analytical[eta1L:eta1R,eta2_pos,eta3]),
                            np.square(data[eta1L:eta1R,eta2_neg,eta3] - analytical[eta1L:eta1R,eta2_neg,eta3])
                        )), axis=0))
                    )
        elif analytical.ndim == 4 and analytical.shape[0] == 3:
            for data in numerical:
                if eta2_ring:
                    err.append(
                        np.sqrt(np.nanmean(np.square(data[:,eta1L:eta1R,:,eta3] - analytical[:,eta1L:eta1R,:,eta3]), axis=(1,2)))
                    )
                elif eta2_neg is None:
                    err.append(
                        np.sqrt(np.nanmean(np.square(data[:,eta1L:eta1R,eta2_pos,eta3] - analytical[:,eta1L:eta1R,eta2_pos,eta3]), axis=1))
                    )
                else:
                    err.append(
                        np.sqrt(np.nanmean(np.hstack((
                            np.square(data[:,eta1L:eta1R,eta2_pos,eta3] - analytical[:,eta1L:eta1R,eta2_pos,eta3]),
                            np.square(data[:,eta1L:eta1R,eta2_neg,eta3] - analytical[:,eta1L:eta1R,eta2_neg,eta3])
                        )), axis=1))
                    )

    elif norm_enum == ErrorNorm.Li: # Max absolute.

        if analytical.ndim == 3:
            for data in numerical:
                if eta2_ring:
                    err.append(
                        np.nanmax(np.abs(data[eta1L:eta1R,:,eta3] - analytical[eta1L:eta1R,:,eta3]), axis=(0,1))
                    )
                elif eta2_neg is None:
                    err.append(
                        np.nanmax(np.abs(data[eta1L:eta1R,eta2_pos,eta3] - analytical[eta1L:eta1R,eta2_pos,eta3]), axis=0)
                    )
                else:
                    err.append(
                        np.nanmax(np.concatenate((
                            np.abs(data[eta1L:eta1R,eta2_pos,eta3] - analytical[eta1L:eta1R,eta2_pos,eta3]),
                            np.abs(data[eta1L:eta1R,eta2_neg,eta3] - analytical[eta1L:eta1R,eta2_neg,eta3])
                        )), axis=0)
                    )
        elif analytical.ndim == 4 and analytical.shape[0] == 3:
            for data in numerical:
                if eta2_ring:
                    err.append(
                        np.nanmax(np.abs(data[:,eta1L:eta1R,:,eta3] - analytical[:,eta1L:eta1R,:,eta3]), axis=(1,2))
                    )
                elif eta2_neg is None:
                    err.append(
                        np.nanmax(np.abs(data[:,eta1L:eta1R,eta2_pos,eta3] - analytical[:,eta1L:eta1R,eta2_pos,eta3]), axis=1)
                    )
                else:
                    err.append(
                        np.nanmax(np.hstack((
                            np.abs(data[:,eta1L:eta1R,eta2_pos,eta3] - analytical[:,eta1L:eta1R,eta2_pos,eta3]),
                            np.abs(data[:,eta1L:eta1R,eta2_neg,eta3] - analytical[:,eta1L:eta1R,eta2_neg,eta3])
                        )), axis=1)
                    )

    else:
        raise NotImplementedError(f'Norm {norm_enum.name} not implemented.')

    if normalize:
        err = np.array(err)
        if norm_enum == ErrorNorm.L1: # Median absolute.
            err = err / np.nanmedian(np.abs(analytical))
        elif norm_enum == ErrorNorm.L2: # Root mean square.
            err = err / np.sqrt(np.nanmean(np.square(analytical)))
        elif norm_enum == ErrorNorm.Li: # Max absolute.
            err = err / np.nanmax(np.abs(analytical))
        else:
            raise NotImplementedError(f'Norm {norm_enum.name} not implemented.')
    else:
        err = np.array(err)

    if analytical.ndim == 3:
        assert err.ndim == 1
    elif analytical.ndim == 4 and analytical.shape[0] == 3:
        assert err.ndim == 2
        assert err.shape[1] == 3

    return err



def get_diff(numerical, analytical, diff_type:DiffType=DiffType.RELATIVE):

    if diff_type == DiffType.DIRECT:
        return numerical - analytical
    elif diff_type == DiffType.RELATIVE:
        return (numerical - analytical) / np.mean(np.abs(analytical))
    elif diff_type == DiffType.RELATIVEABSOLUTE:
        return np.abs(numerical - analytical) / np.mean(np.abs(analytical))
    elif diff_type == DiffType.ABSOLUTE:
        return np.abs(numerical - analytical)
    elif diff_type == DiffType.LOGABSOLUTE:
        return np.log(np.abs(numerical - analytical))
    else:
        raise NotImplementedError(f'Diff type {diff_type.name} not implemented.')


def gdr(numerical, analytical):
    """Alias for get_diff(), computed with relative error."""
    return get_diff(numerical, analytical, DiffType.RELATIVE)


def gdra(numerical, analytical):
    """Alias for get_diff(), computed with relative absolute error."""
    return get_diff(numerical, analytical, DiffType.RELATIVEABSOLUTE)



def plot_wrapper(x, y, z, x0, y0, z0, xs, ys, zs, det_df, 
    f_exact, f_ten_F, f_pol_F, f_pol_F1, 
    df_exact, df_ten_F, df_pol_F, df_pol_F1, 
    params, map_enum, func_enum, form_enum, space_enum, domain_enum, Nel, p):
    """(x,y,z) are (eta1,eta2,eta3) when plotting in logical domain!"""

    import copy
    import numpy as np

    plot_handles = []

    # An ugly hardcoded switch to turn on 1D line plots.
    line_plot = True

    Nel_str = str(Nel).replace(' ', '')
    p_str   = str(p).replace(' ', '')

    metadata_base = {
        'mapping': map_enum,
        'function': func_enum,
        'func_form': form_enum,
        'space_enum': space_enum,
        'origin': [x0, y0, z0,],
        'el_b': [xs, ys, zs,],
        'axlim': (1 if line_plot else 0.2) if space_enum == SpaceType.LOGICAL else 0.02,
        'wintitle': f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-i (Original)',
        'suptitle': f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-i (Original)',
        'comptype': Comparison.ORIG,
        'refcolor': True, # Use reference solution to scale plots.
        'colscale': 1,    # Factor to scale up/down the max/min of the plot's color code.
        'collevel': 20,   # Number of color levels on a contour plot.
        'unlink': False,  # Set color and z-axis limits individually.
        'norm_dist': True, # Normalize line plots versus L2 physical distance between two plot points.
        'share_plot': True, # Overlay line plots on the same figure.
        'lplot': PlotTypeLeft.LINE if line_plot else PlotTypeLeft.CONTOUR2D,
        'lxlabel': '$x$' if space_enum == SpaceType.PHYSICAL else '$\eta^1$',
        'lylabel': '$y$' if space_enum == SpaceType.PHYSICAL else '$\eta^2$',
        # 'lzlabel': '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$',
        # 'lzlabel': '$f(x,y)$',
        # 'lzlabeld': '$f(x,y) - \hat{f}(x,y)$',
        'rplot': PlotTypeRight.LINE if line_plot else PlotTypeRight.CONTOUR2D,
        'rxlabel': '$x$' if space_enum == SpaceType.PHYSICAL else '$\eta^1$',
        'rylabel': '$y$' if space_enum == SpaceType.PHYSICAL else '$\eta^2$',
        # 'rzlabel': '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$',
        # 'rzlabel': '$\\nabla f(x,y)$',
        # 'rzlabeld': '$\\nabla f(x,y) - \\nabla \hat{f}(x,y)$',
        'show_el_b': False,
        'show_pole': True,
        'show_grid': False,
        # For line plot:
        'eta2_cut' : 2, # Index of eta2_range array for the slice.
        'eta3_cut' : int(f_exact.shape[-1] / 2), # Which cross section along eta3 to plot. eta3's size should better be odd...
    }



    if form_enum == FuncForm.ZERO:

        # LHS: Original 0-form function.
        # RHS: 1-form gradient, only x component, because y is identical and z is zero.
        # Figure 1: Actual value, full range.
        # Figure 2: Actual value, zoomed.
        # Figure 3: Relative difference, zoomed.
        # Figure 4: Pure element boundaries.
        # Figure 5: Pure plotting grid.

        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-1 Surface Plot'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-1 Surface Plot (LHS: $\hat{{f}}^{{\,0}}$, RHS: $[\hat{{\\nabla}} \hat{{f}}^{{\,0}}]_1 = \hat{{f}}^{{\,1}}_1$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['colscale'] = 1
        metadata['axlim'] = 1
        metadata['lplot'] = PlotTypeLeft.SURFACE
        metadata['lplot'] = PlotTypeLeft.SCATTER
        metadata['rplot'] = PlotTypeRight.SURFACE
        metadata['rplot'] = PlotTypeRight.SCATTER
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,0}$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \hat{f}^{\,0}]_1$'
        metadata['show_el_b'] = False
        if metadata['lplot'] == PlotTypeLeft.SCATTER:
            metadata['lclabel'] = metadata['lzlabel']
            metadata['lzlabel'] = '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$'
        if metadata['rplot'] == PlotTypeRight.SCATTER:
            metadata['rclabel'] = metadata['rzlabel']
            metadata['rzlabel'] = '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[0], df_ten_F[0], df_pol_F[0], df_pol_F1[0])
        plot_handles.append(handle)

        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-2 Surface Plot'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-2 Surface Plot (LHS: $\hat{{f}}^{{\,0}}$, RHS: $[\hat{{\\nabla}} \hat{{f}}^{{\,0}}]_2 = \hat{{f}}^{{\,1}}_2$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['colscale'] = 1
        metadata['axlim'] = 1
        metadata['lplot'] = PlotTypeLeft.SURFACE
        metadata['lplot'] = PlotTypeLeft.SCATTER
        metadata['rplot'] = PlotTypeRight.SURFACE
        metadata['rplot'] = PlotTypeRight.SCATTER
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,0}$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \hat{f}^{\,0}]_2$'
        metadata['show_el_b'] = False
        if metadata['lplot'] == PlotTypeLeft.SCATTER:
            metadata['lclabel'] = metadata['lzlabel']
            metadata['lzlabel'] = '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$'
        if metadata['rplot'] == PlotTypeRight.SCATTER:
            metadata['rclabel'] = metadata['rzlabel']
            metadata['rzlabel'] = '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[1], df_ten_F[1], df_pol_F[1], df_pol_F1[1])
        plot_handles.append(handle)

        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-3 Surface Plot'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-3 Surface Plot (LHS: $\hat{{f}}^{{\,0}}$, RHS: $[\hat{{\\nabla}} \hat{{f}}^{{\,0}}]_3 = \hat{{f}}^{{\,1}}_3$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['colscale'] = 1
        metadata['axlim'] = 1
        metadata['lplot'] = PlotTypeLeft.SURFACE
        metadata['lplot'] = PlotTypeLeft.SCATTER
        metadata['rplot'] = PlotTypeRight.SURFACE
        metadata['rplot'] = PlotTypeRight.SCATTER
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,0}$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \hat{f}^{\,0}]_3$'
        metadata['show_el_b'] = False
        if metadata['lplot'] == PlotTypeLeft.SCATTER:
            metadata['lclabel'] = metadata['lzlabel']
            metadata['lzlabel'] = '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$'
        if metadata['rplot'] == PlotTypeRight.SCATTER:
            metadata['rclabel'] = metadata['rzlabel']
            metadata['rzlabel'] = '$z$' if space_enum == SpaceType.PHYSICAL else '$\eta^3$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[2], df_ten_F[2], df_pol_F[2], df_pol_F1[2])
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-1 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-1 Original (LHS: $\hat{{f}}^{{\,0}}$, RHS: $[\hat{{\\nabla}} \hat{{f}}^{{\,0}}]_1 = \hat{{f}}^{{\,1}}_1$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,0}$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \hat{f}^{\,0}]_1$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[0], df_ten_F[0], df_pol_F[0], df_pol_F1[0])
        plot_handles.append(handle)


        # metadata = copy.deepcopy(metadata_base)
        # metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-1 Diff'
        # metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-1 Diff (LHS: $\hat{{f}}^{{\,0}}$, RHS: $[\hat{{\\nabla}} \hat{{f}}^{{\,0}}]_1 = \hat{{f}}^{{\,1}}_1$)'
        # metadata['comptype'] = Comparison.DIFF
        # metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,0}$'
        # metadata['rzlabel'] = '$[\hat{\\nabla} \hat{f}^{\,0}]_1$'
        # metadata['lzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        # metadata['rzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        # handle = plot_comparison(metadata, params, x, y, z, 
        #  f_exact   , gdra( f_ten_F   ,  f_exact   ), gdra( f_pol_F   ,  f_exact   ), gdra( f_pol_F1   ,  f_exact   ), 
        # df_exact[0], gdra(df_ten_F[0], df_exact[0]), gdra(df_pol_F[0], df_exact[0]), gdra(df_pol_F1[0], df_exact[0]))
        # plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-2 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-2 Original (LHS: $\hat{{f}}^{{\,0}}$, RHS: $[\hat{{\\nabla}} \hat{{f}}^{{\,0}}]_2 = \hat{{f}}^{{\,1}}_2$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,0}$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \hat{f}^{\,0}]_2$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[1], df_ten_F[1], df_pol_F[1], df_pol_F1[1])
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-3 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-3 Original (LHS: $\hat{{f}}^{{\,0}}$, RHS: $[\hat{{\\nabla}} \hat{{f}}^{{\,0}}]_3 = \hat{{f}}^{{\,1}}_3$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,0}$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \hat{f}^{\,0}]_3$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[2], df_ten_F[2], df_pol_F[2], df_pol_F1[2])
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {map_enum.name} Plotting grid'
        metadata['suptitle'] = f'Polar Spline Comparison {map_enum.name} Plotting grid'
        metadata['comptype'] = Comparison.ORIG
        metadata['colscale'] = 1
        metadata['axlim'] = 1
        metadata['unlink'] = True
        metadata['lplot'] = PlotTypeLeft.WIREFRAME
        metadata['rplot'] = PlotTypeRight.SURFACE
        metadata['lzlabel'] = ''
        metadata['rzlabel'] = ''
        metadata['show_el_b'] = False
        metadata['show_grid'] = True
        handle = plot_comparison(metadata, params, x, y, z, 
        np.zeros_like(x), np.zeros_like(x), np.zeros_like(x), np.zeros_like(x), 
        np.zeros_like(x), np.zeros_like(x), np.zeros_like(x), np.zeros_like(x))
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {map_enum.name} Element boundaries'
        metadata['suptitle'] = f'Polar Spline Comparison {map_enum.name} Element boundaries'
        metadata['comptype'] = Comparison.ORIG
        metadata['colscale'] = 1
        metadata['axlim'] = 1
        metadata['unlink'] = True
        metadata['lplot'] = PlotTypeLeft.WIREFRAME
        metadata['rplot'] = PlotTypeRight.SURFACE
        metadata['lzlabel'] = ''
        metadata['rzlabel'] = ''
        metadata['show_el_b'] = True
        metadata['show_grid'] = False
        handle = plot_comparison(metadata, params, xs, ys, zs, 
        np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs), 
        np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs))
        plot_handles.append(handle)



    elif form_enum == FuncForm.ONE:

        # LHS: Original 1-form function, only x-component because all directions are identical.
        # RHS: 2-form curl, only z component because x and y are zero.
        # Figure 1: Actual value, zoomed.
        # Figure 2: Relative difference, zoomed.

        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-1 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-1 Original (LHS: $\hat{{f}}^{{\,1}}_1$, RHS: $[\hat{{\\nabla}} \\times \hat{{f}}^{{\,1}}]_1 = \hat{{f}}^{{\,2}}_1$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$\hat{f}^{\,1}_1$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \\times \hat{f}^{\,1}]_1 = \hat{f}^{\,2}_1$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[0],  f_ten_F[0],  f_pol_F[0],  f_pol_F1[0], 
        df_exact[0], df_ten_F[0], df_pol_F[0], df_pol_F1[0])
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-1 Diff'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-1 Diff (LHS: $\hat{{f}}^{{\,1}}_1$, RHS: $[\hat{{\\nabla}} \\times \hat{{f}}^{{\,1}}]_1 = \hat{{f}}^{{\,2}}_1$)'
        metadata['comptype'] = Comparison.DIFF
        metadata['lzlabel'] = '$\hat{f}^{\,1}_1$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \\times \hat{f}^{\,1}]_1 = \hat{f}^{\,2}_1$'
        metadata['lzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        metadata['rzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[0], gdra( f_ten_F[0],  f_exact[0]), gdra( f_pol_F[0],  f_exact[0]), gdra( f_pol_F1[0],  f_exact[0]), 
        df_exact[0], gdra(df_ten_F[0], df_exact[0]), gdra(df_pol_F[0], df_exact[0]), gdra(df_pol_F1[0], df_exact[0]))
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-2 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-2 Original (LHS: $\hat{{f}}^{{\,1}}_2$, RHS: $[\hat{{\\nabla}} \\times \hat{{f}}^{{\,1}}]_2 = \hat{{f}}^{{\,2}}_2$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$\hat{f}^{\,1}_2$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \\times \hat{f}^{\,1}]_2 = \hat{f}^{\,2}_2$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[1],  f_ten_F[1],  f_pol_F[1],  f_pol_F1[1], 
        df_exact[1], df_ten_F[1], df_pol_F[1], df_pol_F1[1])
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-2 Diff'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-2 Diff (LHS: $\hat{{f}}^{{\,1}}_2$, RHS: $[\hat{{\\nabla}} \\times \hat{{f}}^{{\,1}}]_2 = \hat{{f}}^{{\,2}}_2$)'
        metadata['comptype'] = Comparison.DIFF
        metadata['lzlabel'] = '$\hat{f}^{\,1}_2$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \\times \hat{f}^{\,1}]_2 = \hat{f}^{\,2}_2$'
        metadata['lzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        metadata['rzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[1], gdra( f_ten_F[1],  f_exact[1]), gdra( f_pol_F[1],  f_exact[1]), gdra( f_pol_F1[1],  f_exact[1]), 
        df_exact[1], gdra(df_ten_F[1], df_exact[1]), gdra(df_pol_F[1], df_exact[1]), gdra(df_pol_F1[1], df_exact[1]))
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-3 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-3 Original (LHS: $\hat{{f}}^{{\,1}}_3$, RHS: $[\hat{{\\nabla}} \\times \hat{{f}}^{{\,1}}]_3 = \hat{{f}}^{{\,2}}_3$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$\hat{f}^{\,1}_3$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \\times \hat{f}^{\,1}]_3 = \hat{f}^{\,2}_3$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[2],  f_ten_F[2],  f_pol_F[2],  f_pol_F1[2], 
        df_exact[2], df_ten_F[2], df_pol_F[2], df_pol_F1[2])
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-3 Diff'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-3 Diff (LHS: $\hat{{f}}^{{\,1}}_3$, RHS: $[\hat{{\\nabla}} \\times \hat{{f}}^{{\,1}}]_3 = \hat{{f}}^{{\,2}}_3$)'
        metadata['comptype'] = Comparison.DIFF
        metadata['lzlabel'] = '$\hat{f}^{\,1}_3$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \\times \hat{f}^{\,1}]_3 = \hat{f}^{\,2}_3$'
        metadata['lzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        metadata['rzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[2], gdra( f_ten_F[2],  f_exact[2]), gdra( f_pol_F[2],  f_exact[2]), gdra( f_pol_F1[2],  f_exact[2]), 
        df_exact[2], gdra(df_ten_F[2], df_exact[2]), gdra(df_pol_F[2], df_exact[2]), gdra(df_pol_F1[2], df_exact[2]))
        plot_handles.append(handle)



    elif form_enum == FuncForm.TWO:

        # LHS: Original 2-form function, only x-component because all directions are identical.
        # RHS: 3-form div.
        # Figure 1: Actual value, zoomed.
        # Figure 2: Relative difference, zoomed.

        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-1 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-1 Original (LHS: $\hat{{f}}^{{\,2}}_1$, RHS: $[\hat{{\\nabla}} \cdot \hat{{f}}^{{\,2}}] = \hat{{f}}^{{\,3}}$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$\hat{f}^{\,2}_1$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \cdot \hat{f}^{\,2}] = \hat{f}^{\,3}$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[0],  f_ten_F[0],  f_pol_F[0],  f_pol_F1[0], 
        df_exact   , df_ten_F   , df_pol_F   , df_pol_F1   )
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-1 Diff'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-1 Diff (LHS: $\hat{{f}}^{{\,2}}_1$, RHS: $[\hat{{\\nabla}} \cdot \hat{{f}}^{{\,2}}] = \hat{{f}}^{{\,3}}$)'
        metadata['comptype'] = Comparison.DIFF
        metadata['lzlabel'] = '$\hat{f}^{\,2}_1$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \cdot \hat{f}^{\,2}] = \hat{f}^{\,3}$'
        metadata['lzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        metadata['rzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[0], gdra( f_ten_F[0],  f_exact[0]), gdra( f_pol_F[0],  f_exact[0]), gdra( f_pol_F1[0],  f_exact[0]), 
        df_exact   , gdra(df_ten_F   , df_exact   ), gdra(df_pol_F   , df_exact   ), gdra(df_pol_F1   , df_exact   ))
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-2 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-2 Original (LHS: $\hat{{f}}^{{\,2}}_2$, RHS: $[\hat{{\\nabla}} \cdot \hat{{f}}^{{\,2}}] = \hat{{f}}^{{\,3}}$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$\hat{f}^{\,2}_2$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \cdot \hat{f}^{\,2}] = \hat{f}^{\,3}$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[1],  f_ten_F[1],  f_pol_F[1],  f_pol_F1[1], 
        df_exact   , df_ten_F   , df_pol_F   , df_pol_F1   )
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-2 Diff'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-2 Diff (LHS: $\hat{{f}}^{{\,2}}_2$, RHS: $[\hat{{\\nabla}} \cdot \hat{{f}}^{{\,2}}] = \hat{{f}}^{{\,3}}$)'
        metadata['comptype'] = Comparison.DIFF
        metadata['lzlabel'] = '$\hat{f}^{\,2}_2$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \cdot \hat{f}^{\,2}] = \hat{f}^{\,3}$'
        metadata['lzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        metadata['rzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[1], gdra( f_ten_F[1],  f_exact[1]), gdra( f_pol_F[1],  f_exact[1]), gdra( f_pol_F1[1],  f_exact[1]), 
        df_exact   , gdra(df_ten_F   , df_exact   ), gdra(df_pol_F   , df_exact   ), gdra(df_pol_F1   , df_exact   ))
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-3 Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-3 Original (LHS: $\hat{{f}}^{{\,2}}_3$, RHS: $[\hat{{\\nabla}} \cdot \hat{{f}}^{{\,2}}] = \hat{{f}}^{{\,3}}$)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$\hat{f}^{\,2}_3$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \cdot \hat{f}^{\,2}] = \hat{f}^{\,3}$'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[2],  f_ten_F[2],  f_pol_F[2],  f_pol_F1[2], 
        df_exact   , df_ten_F   , df_pol_F   , df_pol_F1   )
        plot_handles.append(handle)


        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form-3 Diff'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form-3 Diff (LHS: $\hat{{f}}^{{\,2}}_3$, RHS: $[\hat{{\\nabla}} \cdot \hat{{f}}^{{\,2}}] = \hat{{f}}^{{\,3}}$)'
        metadata['comptype'] = Comparison.DIFF
        metadata['lzlabel'] = '$\hat{f}^{\,2}_3$'
        metadata['rzlabel'] = '$[\hat{\\nabla} \cdot \hat{f}^{\,2}] = \hat{f}^{\,3}$'
        metadata['lzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        metadata['rzlabeld'] = 'Point-wise error, normalized by $L^\infty$ norm'
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact[2], gdra( f_ten_F[2],  f_exact[2]), gdra( f_pol_F[2],  f_exact[2]), gdra( f_pol_F1[2],  f_exact[2]), 
        df_exact   , gdra(df_ten_F   , df_exact   ), gdra(df_pol_F   , df_exact   ), gdra(df_pol_F1   , df_exact   ))
        plot_handles.append(handle)



    elif form_enum == FuncForm.THREE:

        # LHS: Original 3-form function.
        # RHS: Empty space.
        # Figure 1: Actual value, surface plot.
        # Figure 2: Actual value, line plot.

        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form Surface Plot'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form Surface Plot (LHS: $\hat{{f}}^{{\,3}}$, RHS: N/A)'
        metadata['comptype'] = Comparison.ORIG
        metadata['colscale'] = 1
        metadata['axlim'] = 1
        metadata['lplot'] = PlotTypeLeft.SURFACE
        metadata['rplot'] = PlotTypeRight.SURFACE
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,3}$'
        metadata['rzlabel'] = ''
        metadata['show_el_b'] = False
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1)
        plot_handles.append(handle)

        metadata = copy.deepcopy(metadata_base)
        metadata['wintitle'] = f'Polar Spline Comparison {func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {Nel_str} {p_str} {form_enum.name}-form Original'
        metadata['suptitle'] =                         f'{func_enum.name} {map_enum.name} {domain_enum.name} {space_enum.name} {form_enum.name}-form Original (LHS: $\hat{{f}}^{{\,3}}$, RHS: N/A)'
        metadata['comptype'] = Comparison.ORIG
        metadata['lzlabel'] = '$f(x,y)=\hat{f}^{\,3}$'
        metadata['rzlabel'] = ''
        handle = plot_comparison(metadata, params, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1)
        plot_handles.append(handle)



    else:

        raise NotImplementedError(f'FuncForm {form_enum.name} not recognized.')



    update_fig_suptitle(plot_handles, Nel, p)



    return plot_handles



def plot_comparison(metadata, params, eta1, eta2, eta3, 
f_exact, f_ten_F, f_pol_F, f_pol_F1, 
df_exact, df_ten_F, df_pol_F, df_pol_F1):
    """Draw and compare tensor product splines and polar splines.

    While the inputs are called (eta1,eta2,eta3), they can also be Cartesian (x,y,z).
    Expects 3D input with useless z-component, effectively 2D, on axisymmetric maps."""

    print('='*50)
    print('Started plot_comparison().')

    import numpy             as np
    import matplotlib.pyplot as plt
    import matplotlib.tri    as tri
    import matplotlib.ticker as ticker

    space_enum = metadata['space_enum']
    func_form = metadata['func_form']
    map_enum = metadata['mapping']
    levels = metadata['collevel']
    axlim = metadata['axlim']
    e3 = metadata['eta3_cut']
    print(f'Graphs will be plotted at eta3 index {e3}.')
    print(f'This corresponds to z or eta3 = {eta3[0,0,e3]}.')
    if not params['plot']['use_el_b']:
        print(f"We are currently plotting at eta3={params['plot']['eta_range'][-1][e3]}")

    # Special handling axis labels for 1D line plots.
    if metadata['lplot'] in [PlotTypeLeft.LINE]:
        metadata['lylabel'] = metadata['lzlabel']
    if metadata['rplot'] in [PlotTypeRight.LINE]:
        metadata['rylabel'] = metadata['rzlabel']

    if metadata['comptype'] == Comparison.ORIG:
        print('Comparison type: Original values.')
        lmin = np.nanmin([
            np.nanmin(f_exact),
            np.nanmin(f_ten_F),
            np.nanmin(f_pol_F),
            np.nanmin(f_pol_F1),
        ])
        lmax = np.nanmax([
            np.nanmax(f_exact),
            np.nanmax(f_ten_F),
            np.nanmax(f_pol_F),
            np.nanmax(f_pol_F1),
        ])
        rmin = np.nanmin([
            np.nanmin(df_exact),
            np.nanmin(df_ten_F),
            np.nanmin(df_pol_F),
            np.nanmin(df_pol_F1),
        ])
        rmax = np.nanmax([
            np.nanmax(df_exact),
            np.nanmax(df_ten_F),
            np.nanmax(df_pol_F),
            np.nanmax(df_pol_F1),
        ])
        if metadata['refcolor']:
            print('Scale with reference solution.')
            lmin = np.nanmin(f_exact)
            lmax = np.nanmax(f_exact)
            rmin = np.nanmin(df_exact)
            rmax = np.nanmax(df_exact)
    else:
        print('Comparison type: Errors.')
        lmin = np.nanmin([
            np.nanmin(f_ten_F),
            np.nanmin(f_pol_F),
            np.nanmin(f_pol_F1),
        ])
        lmax = np.nanmax([
            np.nanmax(f_ten_F),
            np.nanmax(f_pol_F),
            np.nanmax(f_pol_F1),
        ])
        rmin = np.nanmin([
            np.nanmin(df_ten_F),
            np.nanmin(df_pol_F),
            np.nanmin(df_pol_F1),
        ])
        rmax = np.nanmax([
            np.nanmax(df_ten_F),
            np.nanmax(df_pol_F),
            np.nanmax(df_pol_F1),
        ])

    # Because np.log(0)!
    if np.isneginf(lmin):
        print('Overwritten infinite lmin.')
        lmin = -10000
    if np.isneginf(rmin):
        print('Overwritten infinite rmin.')
        rmin = -10000
    if np.isposinf(lmax):
        print('Overwritten infinite lmax.')
        lmax = 10000
    if np.isposinf(rmax):
        print('Overwritten infinite rmax.')
        rmax = 10000

    if metadata['colscale'] != 1:
        lrange = lmax - lmin
        rrange = rmax - rmin
        lmid = (lmax + lmin) / 2
        rmid = (rmax + rmin) / 2
        lrange_new = lrange * metadata['colscale']
        rrange_new = rrange * metadata['colscale']
        lmin = lmid - lrange_new / 2
        lmax = lmid + lrange_new / 2
        rmin = rmid - rrange_new / 2
        rmax = rmid + rrange_new / 2

    if metadata['unlink']:
        lmin=None
        lmax=None
        rmin=None
        rmax=None

    # Hardcode relative error:
    if metadata['comptype'] == Comparison.DIFF:
        print('Plot range overridden for relative absolute error.')
        lmin=0
        lmax=1
        rmin=0
        rmax=1

    print(f'lmin: {lmin}')
    print(f'lmax: {lmax}')
    print(f'rmin: {rmin}')
    print(f'rmax: {rmax}')

    # Plot settings.
    row = 2
    col = 4
    dpi = 100
    lbl_size = 12
    width, height = (1920 / dpi, 1200 / dpi)
    fig = plt.figure(figsize=(width,height), dpi=dpi)
    gs  = fig.add_gridspec(row, col, width_ratios=[1,1]*2)
    fig.canvas.manager.set_window_title(metadata['wintitle'])
    fig.suptitle(metadata['suptitle'] + '\n', y=0.98)

    l_is_3d = metadata['lplot'] in [PlotTypeLeft.CONTOUR3D, PlotTypeLeft.SCATTER, PlotTypeLeft.SURFACE, PlotTypeLeft.WIREFRAME]
    r_is_3d = metadata['rplot'] in [PlotTypeRight.CONTOUR3D, PlotTypeRight.SCATTER, PlotTypeRight.QUIVER3D, PlotTypeRight.SURFACE]

    if l_is_3d:
        lax1 = fig.add_subplot(gs[0, 0], projection='3d')
        lax2 = fig.add_subplot(gs[0, 1], projection='3d')
        lax3 = fig.add_subplot(gs[1, 0], projection='3d')
        lax4 = fig.add_subplot(gs[1, 1], projection='3d')
    else:
        lax1 = fig.add_subplot(gs[0, 0])
        lax2 = fig.add_subplot(gs[0, 1])
        lax3 = fig.add_subplot(gs[1, 0])
        lax4 = fig.add_subplot(gs[1, 1])
    if r_is_3d:
        print('Plot is 3D')
        rax1 = fig.add_subplot(gs[0, 2], projection='3d')
        rax2 = fig.add_subplot(gs[0, 3], projection='3d')
        rax3 = fig.add_subplot(gs[1, 2], projection='3d')
        rax4 = fig.add_subplot(gs[1, 3], projection='3d')
    else:
        rax1 = fig.add_subplot(gs[0, 2])
        rax2 = fig.add_subplot(gs[0, 3])
        rax3 = fig.add_subplot(gs[1, 2])
        rax4 = fig.add_subplot(gs[1, 3])
    laxes = [lax1, lax2, lax3, lax4]
    raxes = [rax1, rax2, rax3, rax4]

    for idx, ax in enumerate(laxes):
        ax.xaxis.get_major_locator().set_params(integer=True)
        ax.yaxis.get_major_locator().set_params(integer=True)
        # ax.zaxis.get_major_locator().set_params(integer=True)
        ax.ticklabel_format(useOffset=False)
        ax.tick_params(axis='both', which='major', labelsize=lbl_size)
        # ax.tick_params(axis='both', which='minor', labelsize=lbl_size)
        ax.set_xlabel(metadata['lxlabel'])
        ax.set_ylabel(metadata['lylabel'])
        if l_is_3d:
            if not metadata['unlink'] and metadata['lplot'] != PlotTypeLeft.SCATTER:
                ax.set_zlim(lmin, lmax)
            if metadata['comptype'] == Comparison.ORIG:
                ax.set_zlabel(metadata['lzlabel'])
            else:
                if idx == 0:
                    ax.set_zlabel(metadata['lzlabel'])
                else:
                    ax.set_zlabel(metadata['lzlabeld'])
            ax.set_aspect('auto', adjustable='box')
        elif metadata['lplot'] == PlotTypeLeft.LINE:
            pass
        else:
            ax.set_aspect('equal', adjustable='box')

    for idx, ax in enumerate(raxes):
        ax.xaxis.get_major_locator().set_params(integer=True)
        ax.yaxis.get_major_locator().set_params(integer=True)
        # ax.zaxis.get_major_locator().set_params(integer=True)
        ax.ticklabel_format(useOffset=False)
        ax.tick_params(axis='both', which='major', labelsize=lbl_size)
        # ax.tick_params(axis='both', which='minor', labelsize=lbl_size)
        ax.set_xlabel(metadata['rxlabel'])
        ax.set_ylabel(metadata['rylabel'])
        if r_is_3d:
            if not metadata['unlink'] and metadata['rplot'] != PlotTypeRight.SCATTER:
                ax.set_zlim(rmin, rmax)
            if metadata['comptype'] == Comparison.ORIG:
                ax.set_zlabel(metadata['rzlabel'])
            else:
                if idx == 0:
                    ax.set_zlabel(metadata['rzlabel'])
                else:
                    ax.set_zlabel(metadata['rzlabeld'])
            ax.set_aspect('auto', adjustable='box')
        elif metadata['rplot'] == PlotTypeRight.LINE:
            pass
        else:
            ax.set_aspect('equal', adjustable='box')

    push_pull = 'pushed'
    if space_enum == SpaceType.LOGICAL:
        push_pull = 'pulled'
    lax1.set_title((metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']) + f' analytical')
    lax2.set_title((metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']) + f' {push_pull}, on tensor F')
    lax3.set_title((metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']) + f' {push_pull}, on polar F')
    lax4.set_title((metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']) + f' {push_pull}, on polar F1')

    if metadata['rplot'] in [PlotTypeRight.QUIVER2D, PlotTypeRight.QUIVER3D]:
        rax1.set_title('Derivative $\\nabla f(x,y)$')
        rax2.set_title('$\\nabla f(x,y)$ on tensor F')
        rax3.set_title('$\\nabla f(x,y)$ on polar F')
        rax4.set_title('$\\nabla f(x,y)$ on polar F1')

    rax1.set_title((metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']) + f' analytical')
    rax2.set_title((metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']) + f' {push_pull}, on tensor F')
    rax3.set_title((metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']) + f' {push_pull}, on polar F')
    rax4.set_title((metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']) + f' {push_pull}, on polar F1')



    # ============================================================
    # Four original functions on the left.
    # ============================================================

    cmap = plt.cm.get_cmap("viridis").copy()
    cmap.set_over('white')
    cmap.set_under('black')
    if metadata['lplot'] in [PlotTypeLeft.CONTOUR2D, PlotTypeLeft.CONTOUR3D]:
        if metadata['comptype'] == Comparison.ORIG:
            limg1 = lax1.contourf(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
        else:
            limg1 = lax1.contourf(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(np.nanmin(f_exact[:,:,e3]),np.nanmax(f_exact[:,:,e3]),levels), vmin=np.nanmin(f_exact[:,:,e3]), vmax=np.nanmax(f_exact[:,:,e3]))
        limg2 = lax2.contourf(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
        limg3 = lax3.contourf(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
        limg4 = lax4.contourf(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
    elif metadata['lplot'] == PlotTypeLeft.SURFACE:
        limg1 = lax1.plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
        limg2 = lax2.plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
        limg3 = lax3.plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
        limg4 = lax4.plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
    elif metadata['lplot'] == PlotTypeLeft.WIREFRAME:
        # The element boundaries have a different shape than the plotting grid.
        # We cannot use the plotting grid indexing directly!
        # # e3 = int(eta1.shape[-1]/2) # If 3D torus.
        # e3 = 0 # If 3D cylinder.
        limg1 = lax1.plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3])
        limg2 = lax2.plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3])
        limg3 = lax3.plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3])
        limg4 = lax4.plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3])
    elif metadata['lplot'] == PlotTypeLeft.SCATTER:
        # Use Scatter plot for 2D data:
        # limg1 = lax1.scatter(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], c=f_exact[:,:,e3], cmap=plt.cm.viridis, marker='.')
        # limg2 = lax2.scatter(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3], c=f_ten_F[:,:,e3], cmap=plt.cm.viridis, marker='.')
        # limg3 = lax3.scatter(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3], c=f_pol_F[:,:,e3], cmap=plt.cm.viridis, marker='.')
        # limg4 = lax4.scatter(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3], c=f_pol_F1[:,:,e3], cmap=plt.cm.viridis, marker='.')
        # When the function is dependent on eta3 as well (3D).
        # print(np.sqrt(eta1**2+eta2**2) / np.max(np.sqrt(eta1**2+eta2**2)))
        # print(np.abs(f_exact) / np.max(np.abs(f_exact)))
        limg1 = lax1.scatter(eta1, eta2, eta3, c=f_exact,  cmap=plt.cm.viridis, marker='.', alpha=0.1)
        limg2 = lax2.scatter(eta1, eta2, eta3, c=f_ten_F,  cmap=plt.cm.viridis, marker='.', alpha=0.1)
        limg3 = lax3.scatter(eta1, eta2, eta3, c=f_pol_F,  cmap=plt.cm.viridis, marker='.', alpha=0.1)
        limg4 = lax4.scatter(eta1, eta2, eta3, c=f_pol_F1, cmap=plt.cm.viridis, marker='.', alpha=0.1)
    elif metadata['lplot'] == PlotTypeLeft.LINE:
        prop_cycle = plt.rcParams['axes.prop_cycle']
        colcyl = prop_cycle.by_key()['color']
        # print(f'eta1.shape {eta1.shape}')
        # print(f'eta1.shape[1] {eta1.shape[1]}')
        eta2_pos = metadata['eta2_cut']
        eta2_neg = (eta2_pos + int(eta1.shape[1] / 2)) % eta1.shape[1]
        # print(f'eta2_pos {eta2_pos}')
        # print(f'eta2_neg {eta2_neg}')
        # print(f'z or eta2[0,eta2_pos,e3]  {eta2[0,eta2_pos,e3]}')
        # print(f'z or eta2[0,eta2_neg,e3]  {eta2[0,eta2_neg,e3]}')
        # print(f'z or eta2[10,eta2_pos,e3] {eta2[10,eta2_pos,e3]}')
        # print(f'z or eta2[10,eta2_neg,e3] {eta2[10,eta2_neg,e3]}')
        if space_enum == SpaceType.PHYSICAL and metadata['norm_dist']:
            # Normalize line plots versus L2 physical distance between two plot points.
            x1_pos = eta1[:,eta2_pos,e3]
            x2_pos = eta2[:,eta2_pos,e3]
            x3_pos = eta3[:,eta2_pos,e3]
            x1_neg = eta1[:,eta2_neg,e3]
            x2_neg = eta2[:,eta2_neg,e3]
            x3_neg = eta3[:,eta2_neg,e3]
            x0 = (x1_pos[0] + x1_neg[0]) / 2
            y0 = (x2_pos[0] + x2_neg[0]) / 2
            z0 = (x3_pos[0] + x3_neg[0]) / 2
            pos = np.zeros_like(x1_pos)
            neg = np.zeros_like(x1_neg)
            for i in range(len(pos)):
                if i == 0:
                    pos[i] = np.sqrt((x1_pos[i] - x0)**2 + (x2_pos[i] - y0)**2 + (x3_pos[i] - z0)**2)
                    neg[i] = np.sqrt((x1_neg[i] - x0)**2 + (x2_neg[i] - y0)**2 + (x3_neg[i] - z0)**2)
                else:
                    pos[i] = pos[i-1] + np.sqrt((x1_pos[i] - x1_pos[i-1])**2 + (x2_pos[i] - x2_pos[i-1])**2 + (x3_pos[i] - x3_pos[i-1])**2)
                    neg[i] = neg[i-1] + np.sqrt((x1_neg[i] - x1_neg[i-1])**2 + (x2_neg[i] - x2_neg[i-1])**2 + (x3_neg[i] - x3_neg[i-1])**2)
            neg = -neg[::-1]
        elif space_enum == SpaceType.LOGICAL:
            pos = eta1[:,eta2_pos,e3]
            neg = -eta1[::-1,eta2_neg,e3]
        else:
            raise NotImplementedError('Line plot at current configuration not implemented.')

        if metadata['share_plot']:
            limg1 = lax1.plot(pos, f_exact[ :,eta2_pos,e3],    c=colcyl[0], alpha=0.8, lw=2, marker='+', ms=8,  mfc='none', mew=1, label=f'Reference (Max: {     np.max(np.abs(f_exact)):.4e})')
            limg2 = lax1.plot(pos, f_ten_F[ :,eta2_pos,e3],    c=colcyl[1], alpha=0.8, lw=2, marker='o', ms=14, mfc='none', mew=1, label=f'Tensor $F$   (Max: {  np.max(np.abs(f_ten_F)):.4e})')
            limg3 = lax1.plot(pos, f_pol_F[ :,eta2_pos,e3],    c=colcyl[2], alpha=0.8, lw=2, marker='s', ms=8,  mfc='none', mew=1, label=f'Polar $F$      (Max: {np.max(np.abs(f_pol_F)):.4e})')
            limg4 = lax1.plot(pos, f_pol_F1[:,eta2_pos,e3],    c=colcyl[6], alpha=0.8, lw=2, marker='x', ms=8,  mfc='none', mew=1, label=f'Polar $F_1$    (Max: {np.max(np.abs(f_pol_F1)):.4e})')
            limg1 = lax1.plot(neg, f_exact[ ::-1,eta2_neg,e3], c=colcyl[0], alpha=0.8, lw=2, marker='+', ms=8,  mfc='none', mew=1, label=f'Reference (Max: {     np.max(np.abs(f_exact)):.4e})')
            limg2 = lax1.plot(neg, f_ten_F[ ::-1,eta2_neg,e3], c=colcyl[1], alpha=0.8, lw=2, marker='o', ms=14, mfc='none', mew=1, label=f'Tensor $F$   (Max: {  np.max(np.abs(f_ten_F)):.4e})')
            limg3 = lax1.plot(neg, f_pol_F[ ::-1,eta2_neg,e3], c=colcyl[2], alpha=0.8, lw=2, marker='s', ms=8,  mfc='none', mew=1, label=f'Polar $F$      (Max: {np.max(np.abs(f_pol_F)):.4e})')
            limg4 = lax1.plot(neg, f_pol_F1[::-1,eta2_neg,e3], c=colcyl[6], alpha=0.8, lw=2, marker='x', ms=8,  mfc='none', mew=1, label=f'Polar $F_1$    (Max: {np.max(np.abs(f_pol_F1)):.4e})')
        else:
            limg1 = lax1.plot(pos, f_exact[ :,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            limg2 = lax2.plot(pos, f_ten_F[ :,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            limg3 = lax3.plot(pos, f_pol_F[ :,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            limg4 = lax4.plot(pos, f_pol_F1[:,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            limg1 = lax1.plot(neg, f_exact[ ::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
            limg2 = lax2.plot(neg, f_ten_F[ ::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
            limg3 = lax3.plot(neg, f_pol_F[ ::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
            limg4 = lax4.plot(neg, f_pol_F1[::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
        if not metadata['norm_dist'] or metadata['share_plot']:
            # unique_legends(lax1)
            # unique_legends(lax2)
            # unique_legends(lax3)
            # unique_legends(lax4)
            pass
        if metadata['share_plot'] and metadata['comptype'] == Comparison.DIFF:
            for line in lax1.get_lines():
                if 'Reference' in line.get_label():
                    lax1.lines.remove(line)



    l_is_contour = metadata['lplot'] in [PlotTypeLeft.CONTOUR2D, PlotTypeLeft.CONTOUR3D]
    if metadata['lplot'] not in [PlotTypeLeft.WIREFRAME, PlotTypeLeft.LINE]:
        if metadata['comptype'] == Comparison.ORIG:
            lcbar1 = fig.colorbar(limg1, ax=lax1, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']))
            lcbar2 = fig.colorbar(limg2, ax=lax2, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']))
            lcbar3 = fig.colorbar(limg3, ax=lax3, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']))
            lcbar4 = fig.colorbar(limg4, ax=lax4, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabel'] if 'lclabel' not in metadata else metadata['lclabel']))
        else:
            lcbar1 = fig.colorbar(limg1, ax=lax1, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabel']  if 'lclabel'  not in metadata else metadata['lclabel']))
            lcbar2 = fig.colorbar(limg2, ax=lax2, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabeld'] if 'lclabeld' not in metadata else metadata['lclabeld']))
            lcbar3 = fig.colorbar(limg3, ax=lax3, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabeld'] if 'lclabeld' not in metadata else metadata['lclabeld']))
            lcbar4 = fig.colorbar(limg4, ax=lax4, shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=(metadata['lzlabeld'] if 'lclabeld' not in metadata else metadata['lclabeld']))

    limgs = [limg1, limg2, limg3, limg4]
    if metadata['lplot'] not in [PlotTypeLeft.WIREFRAME, PlotTypeLeft.LINE]:
        lcbars = [lcbar1, lcbar2, lcbar3, lcbar4]
        for cbar in lcbars:
            # cbar.ax.locator_params(nbins=3)
            cbar.ax.tick_params(labelsize=lbl_size)
            cbar.locator = ticker.LinearLocator(5)
            cbar.update_ticks()
    else:
        lcbars = None



    # ============================================================
    # Four derivatives on the right.
    # ============================================================

    if func_form == FuncForm.ZERO:

        # LHS: Original 0-form function.
        # RHS: 1-form gradient, only x component, because y is identical and z is zero.
        # Figure 1: Actual value.
        # Figure 2: Difference.
        df_mag = np.sqrt(2 * df_ten_F**2)

    elif func_form == FuncForm.ONE:

        # LHS: Original 1-form function, only x-component because all directions are identical.
        # RHS: 2-form curl, only z component because x and y are zero.
        # Figure 1: Actual value.
        # Figure 2: Difference.
        df_mag = np.sqrt(3 * df_ten_F**2)

    elif func_form == FuncForm.TWO:

        # LHS: Original 2-form function, only x-component because all directions are identical.
        # RHS: 3-form div.
        # Figure 1: Actual value.
        # Figure 2: Difference.
        df_mag = np.sqrt(3 * df_ten_F**2)

    elif func_form == FuncForm.THREE:

        # LHS: Original 3-form function.
        # RHS: None.
        # Figure 1: Actual value.
        # Figure 2: Difference.
        df_mag = np.sqrt(2 * df_ten_F**2)

    else:

        raise NotImplementedError(f'FuncForm {func_form.name} not recognized.')

    # df_mag = np.sqrt(df_ten_F[0]**2 + df_ten_F[1]**2 + df_ten_F[2]**2)
    print('df_mag.shape', df_mag.shape)
    print('Max |df|:', np.max(df_mag))
    print('Min |df|:', np.min(df_mag))

    # Flatten and normalize.
    if r_is_3d:
        c = (df_mag.ravel() - df_mag.min()) / df_mag.ptp()
    else:
        c = (df_mag[:,:,e3].ravel() - df_mag[:,:,e3].min()) / df_mag[:,:,e3].ptp()
    # print('c.shape', c.shape)
    # Repeat for each body line and two head lines in a quiver.
    c = np.concatenate((c, np.repeat(c, 2)))
    # print('c.shape', c.shape)
    # Colormap.
    c = plt.cm.viridis(c)
    # print('c.shape', c.shape)



    cmap = plt.cm.get_cmap("viridis").copy()
    cmap.set_over('white')
    cmap.set_under('black')
    if metadata['rplot'] in [PlotTypeRight.CONTOUR2D, PlotTypeRight.CONTOUR3D]:
        if metadata['comptype'] == Comparison.ORIG:
            rimg1 = rax1.contourf(eta1[:,:,e3], eta2[:,:,e3], df_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
        else:
            rimg1 = rax1.contourf(eta1[:,:,e3], eta2[:,:,e3], df_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(np.nanmin(df_exact[:,:,e3]),np.nanmax(df_exact[:,:,e3]),levels), vmin=np.nanmin(df_exact[:,:,e3]), vmax=np.nanmax(df_exact[:,:,e3]))
        rimg2 = rax2.contourf(eta1[:,:,e3], eta2[:,:,e3], df_ten_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
        rimg3 = rax3.contourf(eta1[:,:,e3], eta2[:,:,e3], df_pol_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
        rimg4 = rax4.contourf(eta1[:,:,e3], eta2[:,:,e3], df_pol_F1[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
    elif metadata['rplot'] == PlotTypeRight.SURFACE:
        rimg1 = rax1.plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_exact[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
        rimg2 = rax2.plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_ten_F[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
        rimg3 = rax3.plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_pol_F[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
        rimg4 = rax4.plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_pol_F1[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
    elif metadata['rplot'] == PlotTypeRight.SCATTER:
        # Use Scatter plot for 2D data:
        # rimg1 = rax1.scatter(eta1[:,:,e3], eta2[:,:,e3], df_exact[:,:,e3],  c=df_exact[:,:,e3],  cmap=plt.cm.viridis, marker='.')
        # rimg2 = rax2.scatter(eta1[:,:,e3], eta2[:,:,e3], df_ten_F[:,:,e3],  c=df_ten_F[:,:,e3],  cmap=plt.cm.viridis, marker='.')
        # rimg3 = rax3.scatter(eta1[:,:,e3], eta2[:,:,e3], df_pol_F[:,:,e3],  c=df_pol_F[:,:,e3],  cmap=plt.cm.viridis, marker='.')
        # rimg4 = rax4.scatter(eta1[:,:,e3], eta2[:,:,e3], df_pol_F1[:,:,e3], c=df_pol_F1[:,:,e3], cmap=plt.cm.viridis, marker='.')
        # When the function is dependent on eta3 as well (3D).
        rimg1 = rax1.scatter(eta1, eta2, eta3, c=df_exact,  cmap=plt.cm.viridis, marker='.', alpha=0.1)
        rimg2 = rax2.scatter(eta1, eta2, eta3, c=df_ten_F,  cmap=plt.cm.viridis, marker='.', alpha=0.1)
        rimg3 = rax3.scatter(eta1, eta2, eta3, c=df_pol_F,  cmap=plt.cm.viridis, marker='.', alpha=0.1)
        rimg4 = rax4.scatter(eta1, eta2, eta3, c=df_pol_F1, cmap=plt.cm.viridis, marker='.', alpha=0.1)
    elif metadata['rplot'] == PlotTypeRight.QUIVER2D:
        scale = 500
        metadata['rzlabel'] = metadata['rzlabel'] + f' Scale: {1/scale}'
        rimg1 = rax1.quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_exact[0,:,:,e3].flatten(), df_exact[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimg2 = rax2.quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_ten_F[0,:,:,e3].flatten(), df_ten_F[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimg3 = rax3.quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_pol_F[0,:,:,e3].flatten(), df_pol_F[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimg4 = rax4.quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_pol_F1[0,:,:,e3].flatten(), df_pol_F1[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimg1.set_array(df_mag[:,:,e3].flatten())
        rimg2.set_array(df_mag[:,:,e3].flatten())
        rimg3.set_array(df_mag[:,:,e3].flatten())
        rimg4.set_array(df_mag[:,:,e3].flatten())
        rimg1.set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
        rimg2.set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
        rimg3.set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
        rimg4.set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
    elif metadata['rplot'] == PlotTypeRight.QUIVER3D:
        scale = 500
        metadata['rzlabel'] = metadata['rzlabel'] + f' Scale: {1/scale}'
        rimg1 = rax1.quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_exact[0].flatten(), df_exact[1].flatten(), df_exact[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimg2 = rax2.quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_ten_F[0].flatten(), df_ten_F[1].flatten(), df_ten_F[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimg3 = rax3.quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_pol_F[0].flatten(), df_pol_F[1].flatten(), df_pol_F[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimg4 = rax4.quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_pol_F1[0].flatten(), df_pol_F1[1].flatten(), df_pol_F1[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimg1.set_array(df_mag.flatten())
        rimg2.set_array(df_mag.flatten())
        rimg3.set_array(df_mag.flatten())
        rimg4.set_array(df_mag.flatten())
        rimg1.set_clim(np.min(df_mag), np.max(df_mag))
        rimg2.set_clim(np.min(df_mag), np.max(df_mag))
        rimg3.set_clim(np.min(df_mag), np.max(df_mag))
        rimg4.set_clim(np.min(df_mag), np.max(df_mag))
    elif metadata['rplot'] == PlotTypeRight.LINE:
        prop_cycle = plt.rcParams['axes.prop_cycle']
        colcyl = prop_cycle.by_key()['color']
        # print(f'eta1.shape {eta1.shape}')
        # print(f'eta1.shape[1] {eta1.shape[1]}')
        eta2_pos = metadata['eta2_cut']
        eta2_neg = (eta2_pos + int(eta1.shape[1] / 2)) % eta1.shape[1]
        # print(f'eta2_pos {eta2_pos}')
        # print(f'eta2_neg {eta2_neg}')
        # print(f'z or eta2[0,eta2_pos,e3]  {eta2[0,eta2_pos,e3]}')
        # print(f'z or eta2[0,eta2_neg,e3]  {eta2[0,eta2_neg,e3]}')
        # print(f'z or eta2[10,eta2_pos,e3] {eta2[10,eta2_pos,e3]}')
        # print(f'z or eta2[10,eta2_neg,e3] {eta2[10,eta2_neg,e3]}')
        if space_enum == SpaceType.PHYSICAL and metadata['norm_dist']:
            # Normalize line plots versus L2 physical distance between two plot points.
            x1_pos = eta1[:,eta2_pos,e3]
            x2_pos = eta2[:,eta2_pos,e3]
            x3_pos = eta3[:,eta2_pos,e3]
            x1_neg = eta1[:,eta2_neg,e3]
            x2_neg = eta2[:,eta2_neg,e3]
            x3_neg = eta3[:,eta2_neg,e3]
            x0 = (x1_pos[0] + x1_neg[0]) / 2
            y0 = (x2_pos[0] + x2_neg[0]) / 2
            z0 = (x3_pos[0] + x3_neg[0]) / 2
            pos = np.zeros_like(x1_pos)
            neg = np.zeros_like(x1_neg)
            for i in range(len(pos)):
                if i == 0:
                    pos[i] = np.sqrt((x1_pos[i] - x0)**2 + (x2_pos[i] - y0)**2 + (x3_pos[i] - z0)**2)
                    neg[i] = np.sqrt((x1_neg[i] - x0)**2 + (x2_neg[i] - y0)**2 + (x3_neg[i] - z0)**2)
                else:
                    pos[i] = pos[i-1] + np.sqrt((x1_pos[i] - x1_pos[i-1])**2 + (x2_pos[i] - x2_pos[i-1])**2 + (x3_pos[i] - x3_pos[i-1])**2)
                    neg[i] = neg[i-1] + np.sqrt((x1_neg[i] - x1_neg[i-1])**2 + (x2_neg[i] - x2_neg[i-1])**2 + (x3_neg[i] - x3_neg[i-1])**2)
            neg = -neg[::-1]
        elif space_enum == SpaceType.LOGICAL:
            pos = eta1[:,eta2_pos,e3]
            neg = -eta1[::-1,eta2_neg,e3]
        else:
            raise NotImplementedError('Line plot at current configuration not implemented.')

        if metadata['share_plot']:
            rimg1 = rax1.plot(pos, df_exact[ :,eta2_pos,e3],    c=colcyl[0], alpha=0.8, marker='+', ms=8,  mfc='none', mew=1, label=f'Reference (Max: {     np.max(np.abs(df_exact)):.4e})')
            rimg2 = rax1.plot(pos, df_ten_F[ :,eta2_pos,e3],    c=colcyl[1], alpha=0.8, marker='o', ms=14, mfc='none', mew=1, label=f'Tensor $F$   (Max: {  np.max(np.abs(df_ten_F)):.4e})')
            rimg3 = rax1.plot(pos, df_pol_F[ :,eta2_pos,e3],    c=colcyl[2], alpha=0.8, marker='s', ms=8,  mfc='none', mew=1, label=f'Polar $F$      (Max: {np.max(np.abs(df_pol_F)):.4e})')
            rimg4 = rax1.plot(pos, df_pol_F1[:,eta2_pos,e3],    c=colcyl[6], alpha=0.8, marker='x', ms=8,  mfc='none', mew=1, label=f'Polar $F_1$    (Max: {np.max(np.abs(df_pol_F1)):.4e})')
            rimg1 = rax1.plot(neg, df_exact[ ::-1,eta2_neg,e3], c=colcyl[0], alpha=0.8, marker='+', ms=8,  mfc='none', mew=1, label=f'Reference (Max: {     np.max(np.abs(df_exact)):.4e})')
            rimg2 = rax1.plot(neg, df_ten_F[ ::-1,eta2_neg,e3], c=colcyl[1], alpha=0.8, marker='o', ms=14, mfc='none', mew=1, label=f'Tensor $F$   (Max: {  np.max(np.abs(df_ten_F)):.4e})')
            rimg3 = rax1.plot(neg, df_pol_F[ ::-1,eta2_neg,e3], c=colcyl[2], alpha=0.8, marker='s', ms=8,  mfc='none', mew=1, label=f'Polar $F$      (Max: {np.max(np.abs(df_pol_F)):.4e})')
            rimg4 = rax1.plot(neg, df_pol_F1[::-1,eta2_neg,e3], c=colcyl[6], alpha=0.8, marker='x', ms=8,  mfc='none', mew=1, label=f'Polar $F_1$    (Max: {np.max(np.abs(df_pol_F1)):.4e})')
        else:
            rimg1 = rax1.plot(pos, df_exact[ :,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            rimg2 = rax2.plot(pos, df_ten_F[ :,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            rimg3 = rax3.plot(pos, df_pol_F[ :,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            rimg4 = rax4.plot(pos, df_pol_F1[:,eta2_pos,e3],    c=colcyl[0], marker='.', label=f'$\eta_2$: {eta2[0,eta2_pos,e3]:.2f}')
            rimg1 = rax1.plot(neg, df_exact[ ::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
            rimg2 = rax2.plot(neg, df_ten_F[ ::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
            rimg3 = rax3.plot(neg, df_pol_F[ ::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
            rimg4 = rax4.plot(neg, df_pol_F1[::-1,eta2_neg,e3], c=colcyl[1], marker='.', label=f'$\eta_2$: {eta2[0,eta2_neg,e3]:.2f}')
        if not metadata['norm_dist'] or metadata['share_plot']:
            # unique_legends(rax1)
            # unique_legends(rax2)
            # unique_legends(rax3)
            # unique_legends(rax4)
            pass
        if metadata['share_plot'] and metadata['comptype'] == Comparison.DIFF:
            for line in rax1.get_lines():
                if 'Reference' in line.get_label():
                    rax1.lines.remove(line)



    r_is_contour = metadata['rplot'] in [PlotTypeRight.CONTOUR2D, PlotTypeRight.CONTOUR3D]
    if metadata['rplot'] not in [PlotTypeRight.LINE]:
        if metadata['comptype'] == Comparison.ORIG:
            rcbar1 = fig.colorbar(rimg1, ax=rax1, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']))
            rcbar2 = fig.colorbar(rimg2, ax=rax2, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']))
            rcbar3 = fig.colorbar(rimg3, ax=rax3, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']))
            rcbar4 = fig.colorbar(rimg4, ax=rax4, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabel'] if 'rclabel' not in metadata else metadata['rclabel']))
        else:
            rcbar1 = fig.colorbar(rimg1, ax=rax1, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabel'] if  'rclabel'  not in metadata else metadata['rclabel']))
            rcbar2 = fig.colorbar(rimg2, ax=rax2, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabeld'] if 'rclabeld' not in metadata else metadata['rclabeld']))
            rcbar3 = fig.colorbar(rimg3, ax=rax3, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabeld'] if 'rclabeld' not in metadata else metadata['rclabeld']))
            rcbar4 = fig.colorbar(rimg4, ax=rax4, shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=(metadata['rzlabeld'] if 'rclabeld' not in metadata else metadata['rclabeld']))
    rimgs = [rimg1, rimg2, rimg3, rimg4]
    if metadata['rplot'] not in [PlotTypeRight.LINE]:
        rcbars = [rcbar1, rcbar2, rcbar3, rcbar4]
        for cbar in rcbars:
            # cbar.ax.locator_params(nbins=3)
            cbar.ax.tick_params(labelsize=lbl_size)
            cbar.locator = ticker.LinearLocator(5)
            cbar.update_ticks()
    else:
        rcbars = None



    # Mark position on mapping pole.
    show_el_b = metadata['show_el_b']
    show_pole = metadata['show_pole']
    show_grid = metadata['show_grid']
    origin = metadata['origin']
    el_b = metadata['el_b']
    lpoles = []
    lgrids = []
    lel_bs = []
    for idx, ax in enumerate(laxes):
        if metadata['lplot'] == PlotTypeLeft.LINE and space_enum == SpaceType.PHYSICAL and metadata['norm_dist']:
            # axlim = 0.02
            # ax.set_xlim(np.min(neg) * axlim, np.max(pos) * axlim)
            ax.set_xlim(np.min(neg), np.max(pos))
            ax.set_ylim(lmin, lmax)
            ax.set_xlabel('Arc length')
        elif metadata['lplot'] == PlotTypeLeft.LINE and space_enum == SpaceType.LOGICAL:
            ax.set_xlim(origin[0] - axlim, origin[0] + axlim)
            ax.set_ylim(lmin, lmax)
        elif space_enum == SpaceType.LOGICAL:
            ax.set_xlim(origin[0], origin[0] + axlim)
            ax.set_ylim(origin[1], origin[1] + axlim)
        elif is_input_map_spline(map_enum):
            ax.set_xlim(origin[0] - axlim*1.2, origin[0] + axlim*1.2)
            ax.set_ylim(origin[1] - axlim*1.2, origin[1] + axlim*1.2)
            # ax.set_zlim(origin[2] - axlim*1.2, origin[2] + axlim*1.2)
        else:
            ax.set_xlim(origin[0] - axlim, origin[0] + axlim)
            ax.set_ylim(origin[1] - axlim, origin[1] + axlim)
        # Custom override:
        if metadata['lplot'] == PlotTypeLeft.SCATTER:
            ax.set_xlim(None, None)
            ax.set_ylim(None, None)
            ax.set_zlim(None, None)
        pole = None
        grid = None
        spce = None
        if l_is_3d:
            if show_grid:
                grid = ax.scatter(     eta1,      eta2,      eta3, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                print('Me Me Me!!!')
                spce = ax.scatter(  el_b[0],el_b[1],        el_b[2],         marker='x', facecolors='navy',         alpha=0.1, label='el_b')
                ax.scatter( el_b[0][-1,:,:],el_b[1][-1,:,:],el_b[2][-1,:,:], marker='X', facecolors='navy', edgecolors='navy',         alpha=0.2, label='none', s=64, lw=1)
                ax.scatter( el_b[0][ 0,:,:],el_b[1][ 0,:,:],el_b[2][ 0,:,:], marker='o', facecolors='red',  edgecolors='red',          alpha=1.0, label='none', s=96, lw=2)
            if show_pole:
                pole = ax.scatter(origin[0], origin[1], origin[2], marker='o', facecolors='none', edgecolors='red',  label='Pole', s=128, lw=3)
        elif metadata['lplot'] == PlotTypeLeft.LINE:
            if show_pole:
                pole = ax.axvline(0, ls='dashed', color='red', alpha=0.5, label='Pole')
            # ax.legend()
            unique_legends(ax)
        else:
            if show_grid:
                grid = ax.scatter(     eta1,      eta2,       100, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                spce = ax.scatter(  el_b[0],   el_b[1],       100, marker='x', facecolors='navy',         alpha=0.1, label='el_b')
            if show_pole:
                pole = ax.scatter(origin[0], origin[1],       100, marker='o', facecolors='none', edgecolors='red',  label='Pole', s=64, lw=3)
        # `None` is appended regardless, to ensure `zip()` works on plot update.
        lpoles.append(pole)
        lgrids.append(grid)
        lel_bs.append(spce)
    rpoles = []
    rgrids = []
    rel_bs = []
    for idx, ax in enumerate(raxes):
        if metadata['rplot'] == PlotTypeRight.LINE and space_enum == SpaceType.PHYSICAL and metadata['norm_dist']:
            # axlim = 0.02
            # ax.set_xlim(np.min(neg) * axlim, np.max(pos) * axlim)
            ax.set_xlim(np.min(neg), np.max(pos))
            ax.set_ylim(rmin, rmax)
            ax.set_xlabel('Arc length')
        elif metadata['rplot'] == PlotTypeRight.LINE and space_enum == SpaceType.LOGICAL:
            ax.set_xlim(origin[0] - axlim, origin[0] + axlim)
            ax.set_ylim(rmin, rmax)
        elif space_enum == SpaceType.LOGICAL:
            ax.set_xlim(origin[0], origin[0] + axlim)
            ax.set_ylim(origin[1], origin[1] + axlim)
        elif is_input_map_spline(map_enum):
            ax.set_xlim(origin[0] - axlim*1.2, origin[0] + axlim*1.2)
            ax.set_ylim(origin[1] - axlim*1.2, origin[1] + axlim*1.2)
            # ax.set_zlim(origin[2] - axlim*1.2, origin[2] + axlim*1.2)
        else:
            ax.set_xlim(origin[0] - axlim, origin[0] + axlim)
            ax.set_ylim(origin[1] - axlim, origin[1] + axlim)
        # Custom override:
        if metadata['rplot'] == PlotTypeRight.SCATTER:
            ax.set_xlim(None, None)
            ax.set_ylim(None, None)
            ax.set_zlim(None, None)
        pole = None
        grid = None
        spce = None
        if r_is_3d:
            if show_grid:
                grid = ax.scatter(     eta1,      eta2,      eta3, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                spce = ax.scatter(  el_b[0],   el_b[1],   el_b[2], marker='x', facecolors='navy',         alpha=0.1, label='el_b')
            if show_pole:
                pole = ax.scatter(origin[0], origin[1], origin[2], marker='o', facecolors='none', edgecolors='red',  label='Pole', s=64, lw=3)
        elif metadata['rplot'] == PlotTypeRight.LINE:
            if show_pole:
                pole = ax.axvline(0, ls='dashed', color='red', alpha=0.5, label='Pole')
            # ax.legend()
            unique_legends(ax)
        else:
            if show_grid:
                grid = ax.scatter(     eta1,      eta2,       100, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                spce = ax.scatter(  el_b[0],   el_b[1],       100, marker='x', facecolors='navy',         alpha=0.1, label='el_b')
            if show_pole:
                pole = ax.scatter(origin[0], origin[1],       100, marker='o', facecolors='none', edgecolors='red',  label='Pole', s=64, lw=3)
        # `None` is appended regardless, to ensure `zip()` works on plot update.
        rpoles.append(pole)
        rgrids.append(grid)
        rel_bs.append(spce)



    # Remove unnecessary subplots, and resize.
    gs = GridSpec(1,2)
    if metadata['lplot'] == PlotTypeLeft.LINE and metadata['share_plot']:
        fig.delaxes(lax2)
        fig.delaxes(lax3)
        fig.delaxes(lax4)
        lax1.set_title(lax1.get_title().replace(' analytical', ''))
        # lax1.change_geometry(1,2,1) # Deprecated.
        lax1.set_position(gs[0].get_position(fig))
        lax1.set_subplotspec(gs[0])
        autoscale_y(lax1, ignore_labels=['Tensor $F$'])
        if metadata['comptype'] == Comparison.DIFF:
            autoscale_y(lax1, ignore_labels=['Reference', 'Tensor $F$'])
    if metadata['rplot'] == PlotTypeRight.LINE and metadata['share_plot']:
        fig.delaxes(rax2)
        fig.delaxes(rax3)
        fig.delaxes(rax4)
        rax1.set_title(rax1.get_title().replace(' analytical', ''))
        # rax1.change_geometry(1,2,2) # Deprecated.
        rax1.set_position(gs[1].get_position(fig))
        rax1.set_subplotspec(gs[1])
        autoscale_y(rax1, ignore_labels=['Tensor $F$'])
        if metadata['comptype'] == Comparison.DIFF:
            autoscale_y(rax1, ignore_labels=['Reference', 'Tensor $F$'])

    # if metadata['lplot'] == PlotTypeLeft.WIREFRAME:
    #     fig.delaxes(lax2)
    #     fig.delaxes(lax3)
    #     fig.delaxes(lax4)
    #     lax1.set_title(lax1.get_title().replace(' analytical', ''))
    #     # lax1.change_geometry(1,2,1) # Deprecated.
    #     lax1.set_position(gs[0].get_position(fig))
    #     lax1.set_subplotspec(gs[0])
    #     # lax1.view_init(azim=270, elev=0)
    #     # autoscale_y(lax1, ignore_labels=['Tensor $F$'])
    #     # if metadata['comptype'] == Comparison.DIFF:
    #     #     autoscale_y(lax1, ignore_labels=['Reference', 'Tensor $F$'])
    # if metadata['rplot'] == PlotTypeRight.SURFACE:
    #     fig.delaxes(rax1)
    #     fig.delaxes(rax2)
    #     fig.delaxes(rax3)
    #     fig.delaxes(rax4)

    if metadata['rplot'] == PlotTypeRight.LINE and metadata['share_plot'] and func_form == FuncForm.THREE:
        fig.delaxes(rax1)
    elif func_form == FuncForm.THREE:
        fig.delaxes(rax1)
        fig.delaxes(rax2)
        fig.delaxes(rax3)
        fig.delaxes(rax4)



    # ============================================================
    # Show the figure.
    # ============================================================

    # print('Before `tight_layout()`   | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))
    fig.tight_layout()
    # print('After `tight_layout()`    | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))
    fig.subplots_adjust(hspace=fig.subplotpars.hspace * 1.2, wspace=fig.subplotpars.wspace * .9)
    # print('After `subplots_adjust()` | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))



    print('Completed plot_comparison().')
    print('='*50)

    return {
        'fig': fig,
        'laxes': laxes,
        'raxes': raxes,
        'limgs': limgs,
        'rimgs': rimgs,
        'lcbars': lcbars,
        'rcbars': rcbars,
        'lpoles': lpoles,
        'rpoles': rpoles,
        'lgrids': lgrids,
        'rgrids': rgrids,
        'lel_bs': lel_bs,
        'rel_bs': rel_bs,
        'params': params,
        'metadata': metadata,
    }



def plot_updater(plot_handles, x, y, z, x0, y0, z0, xs, ys, zs, 
f_exact, f_ten_F, f_pol_F, f_pol_F1, 
df_exact, df_ten_F, df_pol_F, df_pol_F1):

    import numpy as np
    import matplotlib.pyplot as plt

    import copy
    metadata = plot_handles[0]['metadata']
    func_form = metadata['func_form']

    # Update metadata.
    for plot in plot_handles:
        if 'metadata' in plot:
            plot['metadata']['origin'] = [x0, y0, z0,]
            plot['metadata']['el_b'] = [xs, ys, zs,]

    if func_form == FuncForm.ZERO:

        # LHS: Original 0-form function.
        # RHS: 1-form gradient, only x component, because y is identical and z is zero.
        # Figure 1: Actual value, full range.
        # Figure 2: Actual value, zoomed.
        # Figure 3: Relative difference, zoomed.
        # Figure 4: Pure element boundaries.
        # Figure 5: Pure plotting grid.

        handle = plot_handles[0]
        plot_update(handle, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[0], df_ten_F[0], df_pol_F[0], df_pol_F1[0])

        handle = plot_handles[1]
        plot_update(handle, x, y, z, 
         f_exact   ,  f_ten_F   ,  f_pol_F   ,  f_pol_F1   , 
        df_exact[0], df_ten_F[0], df_pol_F[0], df_pol_F1[0])

        handle = plot_handles[2]
        plot_update(handle, x, y, z, 
         f_exact   , gdra( f_ten_F   ,  f_exact   ), gdra( f_pol_F   ,  f_exact   ), gdra( f_pol_F1   ,  f_exact   ), 
        df_exact[0], gdra(df_ten_F[0], df_exact[0]), gdra(df_pol_F[0], df_exact[0]), gdra(df_pol_F1[0], df_exact[0]))

        handle = plot_handles[3]
        plot_update(handle, x, y, z, 
        np.zeros_like(x), np.zeros_like(x), np.zeros_like(x), np.zeros_like(x), 
        np.zeros_like(x), np.zeros_like(x), np.zeros_like(x), np.zeros_like(x))

        handle = plot_handles[4]
        plot_update(handle, xs, ys, zs, 
        np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs), 
        np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs), np.zeros_like(xs))



    elif func_form == FuncForm.ONE:

        # LHS: Original 1-form function, only x-component because all directions are identical.
        # RHS: 2-form curl, only z component because x and y are zero.
        # Figure 1: Actual value, zoomed.
        # Figure 2: Relative difference, zoomed.

        handle = plot_handles[0]
        plot_update(handle, x, y, z, 
         f_exact[0],  f_ten_F[0],  f_pol_F[0],  f_pol_F1[0], 
        df_exact[0], df_ten_F[0], df_pol_F[0], df_pol_F1[0])

        handle = plot_handles[1]
        plot_update(handle, x, y, z, 
         f_exact[0], gdra( f_ten_F[0],  f_exact[0]), gdra( f_pol_F[0],  f_exact[0]), gdra( f_pol_F1[0],  f_exact[0]), 
        df_exact[0], gdra(df_ten_F[0], df_exact[0]), gdra(df_pol_F[0], df_exact[0]), gdra(df_pol_F1[0], df_exact[0]))

        handle = plot_handles[2]
        plot_update(handle, x, y, z, 
         f_exact[1],  f_ten_F[1],  f_pol_F[1],  f_pol_F1[1], 
        df_exact[1], df_ten_F[1], df_pol_F[1], df_pol_F1[1])

        handle = plot_handles[3]
        plot_update(handle, x, y, z, 
         f_exact[1], gdra( f_ten_F[1],  f_exact[1]), gdra( f_pol_F[1],  f_exact[1]), gdra( f_pol_F1[1],  f_exact[1]), 
        df_exact[1], gdra(df_ten_F[1], df_exact[1]), gdra(df_pol_F[1], df_exact[1]), gdra(df_pol_F1[1], df_exact[1]))

        handle = plot_handles[4]
        plot_update(handle, x, y, z, 
         f_exact[2],  f_ten_F[2],  f_pol_F[2],  f_pol_F1[2], 
        df_exact[2], df_ten_F[2], df_pol_F[2], df_pol_F1[2])

        handle = plot_handles[5]
        plot_update(handle, x, y, z, 
         f_exact[2], gdra( f_ten_F[2],  f_exact[2]), gdra( f_pol_F[2],  f_exact[2]), gdra( f_pol_F1[2],  f_exact[2]), 
        df_exact[2], gdra(df_ten_F[2], df_exact[2]), gdra(df_pol_F[2], df_exact[2]), gdra(df_pol_F1[2], df_exact[2]))



    elif func_form == FuncForm.TWO:

        # LHS: Original 2-form function, only x-component because all directions are identical.
        # RHS: 3-form div.
        # Figure 1: Actual value, zoomed.
        # Figure 2: Relative difference, zoomed.

        handle = plot_handles[0]
        plot_update(handle, x, y, z, 
         f_exact[0],  f_ten_F[0],  f_pol_F[0],  f_pol_F1[0], 
        df_exact   , df_ten_F   , df_pol_F   , df_pol_F1   )

        handle = plot_handles[1]
        plot_update(handle, x, y, z, 
         f_exact[0], gdra( f_ten_F[0],  f_exact[0]), gdra( f_pol_F[0],  f_exact[0]), gdra( f_pol_F1[0],  f_exact[0]), 
        df_exact   , gdra(df_ten_F   , df_exact   ), gdra(df_pol_F   , df_exact   ), gdra(df_pol_F1   , df_exact   ))

        handle = plot_handles[2]
        plot_update(handle, x, y, z, 
         f_exact[1],  f_ten_F[1],  f_pol_F[1],  f_pol_F1[1], 
        df_exact   , df_ten_F   , df_pol_F   , df_pol_F1   )

        handle = plot_handles[3]
        plot_update(handle, x, y, z, 
         f_exact[1], gdra( f_ten_F[1],  f_exact[1]), gdra( f_pol_F[1],  f_exact[1]), gdra( f_pol_F1[1],  f_exact[1]), 
        df_exact   , gdra(df_ten_F   , df_exact   ), gdra(df_pol_F   , df_exact   ), gdra(df_pol_F1   , df_exact   ))

        handle = plot_handles[4]
        plot_update(handle, x, y, z, 
         f_exact[2],  f_ten_F[2],  f_pol_F[2],  f_pol_F1[2], 
        df_exact   , df_ten_F   , df_pol_F   , df_pol_F1   )

        handle = plot_handles[5]
        plot_update(handle, x, y, z, 
         f_exact[2], gdra( f_ten_F[2],  f_exact[2]), gdra( f_pol_F[2],  f_exact[2]), gdra( f_pol_F1[2],  f_exact[2]), 
        df_exact   , gdra(df_ten_F   , df_exact   ), gdra(df_pol_F   , df_exact   ), gdra(df_pol_F1   , df_exact   ))



    else:

        raise NotImplementedError(f'FuncForm {func_form.name} not recognized.')



    return plot_handles



def plot_update(handle, eta1, eta2, eta3, 
f_exact, f_ten_F, f_pol_F, f_pol_F1, 
df_exact, df_ten_F, df_pol_F, df_pol_F1):

    print('='*50)
    print('Started plot_update().')

    import numpy             as np
    import matplotlib.pyplot as plt
    import matplotlib.tri    as tri
    import matplotlib.ticker as ticker

    # `handle` is a dict that looks like this:
    # handle == {
    #     'fig': fig,
    #     'laxes': laxes,
    #     'raxes': raxes,
    #     'limgs': limgs,
    #     'rimgs': rimgs,
    #     'lcbars': lcbars,
    #     'rcbars': rcbars,
    #     'metadata': metadata,
    # }
    fig = handle['fig']
    laxes = handle['laxes']
    raxes = handle['raxes']
    limgs = handle['limgs']
    rimgs = handle['rimgs']
    lcbars = handle['lcbars']
    rcbars = handle['rcbars']
    lpoles = handle['lpoles']
    rpoles = handle['rpoles']
    lgrids = handle['lgrids']
    rgrids = handle['rgrids']
    lel_bs = handle['lel_bs']
    rel_bs = handle['rel_bs']
    metadata = handle['metadata']
    space_enum = metadata['space_enum']
    func_form = metadata['func_form']
    levels = metadata['collevel']
    axlim = metadata['axlim']
    e3 = metadata['eta3_cut']
    print(f'Graphs will be plotted at eta3 index {e3}.')
    print(f'This corresponds to z or eta3 = {eta3[0,0,e3]}.')
    lbl_size = 12

    print(f'Updating plot {metadata["suptitle"]}')

    print(f'type(laxes[0]): {type(laxes[0])}')
    print(f'type(limgs[0]): {type(limgs[0])}')

    if metadata['comptype'] == Comparison.ORIG:
        print('Comparison type: Original values.')
        lmin = np.nanmin([
            np.nanmin(f_exact),
            np.nanmin(f_ten_F),
            np.nanmin(f_pol_F),
            np.nanmin(f_pol_F1),
        ])
        lmax = np.nanmax([
            np.nanmax(f_exact),
            np.nanmax(f_ten_F),
            np.nanmax(f_pol_F),
            np.nanmax(f_pol_F1),
        ])
        rmin = np.nanmin([
            np.nanmin(df_exact),
            np.nanmin(df_ten_F),
            np.nanmin(df_pol_F),
            np.nanmin(df_pol_F1),
        ])
        rmax = np.nanmax([
            np.nanmax(df_exact),
            np.nanmax(df_ten_F),
            np.nanmax(df_pol_F),
            np.nanmax(df_pol_F1),
        ])
        if metadata['refcolor']:
            print('Scale with reference solution.')
            lmin = np.nanmin(f_exact)
            lmax = np.nanmax(f_exact)
            rmin = np.nanmin(df_exact)
            rmax = np.nanmax(df_exact)
    else:
        print('Comparison type: Errors.')
        lmin = np.nanmin([
            np.nanmin(f_ten_F),
            np.nanmin(f_pol_F),
            np.nanmin(f_pol_F1),
        ])
        lmax = np.nanmax([
            np.nanmax(f_ten_F),
            np.nanmax(f_pol_F),
            np.nanmax(f_pol_F1),
        ])
        rmin = np.nanmin([
            np.nanmin(df_ten_F),
            np.nanmin(df_pol_F),
            np.nanmin(df_pol_F1),
        ])
        rmax = np.nanmax([
            np.nanmax(df_ten_F),
            np.nanmax(df_pol_F),
            np.nanmax(df_pol_F1),
        ])

    if metadata['colscale'] != 1:
        lrange = lmax - lmin
        rrange = rmax - rmin
        lmid = (lmax + lmin) / 2
        rmid = (rmax + rmin) / 2
        lrange_new = lrange * metadata['colscale']
        rrange_new = rrange * metadata['colscale']
        lmin = lmid - lrange_new / 2
        lmax = lmid + lrange_new / 2
        rmin = rmid - rrange_new / 2
        rmax = rmid + rrange_new / 2

    if metadata['unlink']:
        lmin=None
        lmax=None
        rmin=None
        rmax=None

    # Hardcode relative error:
    if metadata['comptype'] == Comparison.DIFF:
        lmin=0
        lmax=1
        rmin=0
        rmax=1

    print(f'lmin: {lmin}')
    print(f'lmax: {lmax}')
    print(f'rmin: {rmin}')
    print(f'rmax: {rmax}')

    l_is_3d = metadata['lplot'] in [PlotTypeLeft.CONTOUR3D, PlotTypeLeft.SCATTER, PlotTypeLeft.SURFACE, PlotTypeLeft.WIREFRAME]
    r_is_3d = metadata['rplot'] in [PlotTypeRight.CONTOUR3D, PlotTypeRight.QUIVER3D, PlotTypeRight.SURFACE]



    # ============================================================
    # Four original functions on the left.
    # ============================================================

    cmap = plt.cm.get_cmap("viridis").copy()
    cmap.set_over('white')
    cmap.set_under('black')
    if metadata['lplot'] in [PlotTypeLeft.CONTOUR2D, PlotTypeLeft.CONTOUR3D]:
        for img in limgs:
            for c in img.collections:
                c.remove() # Remove only the contours, leave the rest intact.
        if metadata['comptype'] == Comparison.ORIG:
            limgs[0] = laxes[0].contourf(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
            limgs[0].set_clim(lmin, lmax)
        else:
            limgs[0] = laxes[0].contourf(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(np.nanmin(f_exact[:,:,e3]),np.nanmax(f_exact[:,:,e3]),levels), vmin=np.nanmin(f_exact[:,:,e3]), vmax=np.nanmax(f_exact[:,:,e3]))
        limgs[1] = laxes[1].contourf(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
        limgs[2] = laxes[2].contourf(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
        limgs[3] = laxes[3].contourf(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(lmin,lmax,levels), vmin=lmin, vmax=lmax)
        limgs[1].set_clim(lmin, lmax)
        limgs[2].set_clim(lmin, lmax)
        limgs[3].set_clim(lmin, lmax)
        # limgs[0].cmap.set_over('white')
        # limgs[1].cmap.set_over('white')
        # limgs[2].cmap.set_over('white')
        # limgs[3].cmap.set_over('white')
        # limgs[0].cmap.set_under('black')
        # limgs[1].cmap.set_under('black')
        # limgs[2].cmap.set_under('black')
        # limgs[3].cmap.set_under('black')
        # limgs[0].changed()
        # limgs[1].changed()
        # limgs[2].changed()
        # limgs[3].changed()
    elif metadata['lplot'] == PlotTypeLeft.SURFACE:
        # for img in limgs:
        #     img.remove()
        for ax, img in zip(laxes, limgs):
            ax.collections.remove(img)
        limgs[0] = laxes[0].plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
        limgs[1] = laxes[1].plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
        limgs[2] = laxes[2].plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
        limgs[3] = laxes[3].plot_surface(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3], vmin=lmin, vmax=lmax, cmap=plt.cm.viridis)
    elif metadata['lplot'] == PlotTypeLeft.WIREFRAME:
        for ax, img in zip(laxes, limgs):
            ax.collections.remove(img)
        # for img in limgs:
        #     img.remove()
        limgs[0] = laxes[0].plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3])
        limgs[1] = laxes[1].plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3])
        limgs[2] = laxes[2].plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3])
        limgs[3] = laxes[3].plot_wireframe(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3])
    elif metadata['lplot'] == PlotTypeLeft.SCATTER:
        for ax, img in zip(laxes, limgs):
            ax.collections.remove(img)
        # limgs[0]._offsets3d = (eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3])
        # Use Scatter plot for 2D data:
        limgs[0] = laxes[0].scatter(eta1[:,:,e3], eta2[:,:,e3], f_exact[:,:,e3], c=f_exact[:,:,e3], cmap=plt.cm.viridis, marker='.')
        limgs[1] = laxes[1].scatter(eta1[:,:,e3], eta2[:,:,e3], f_ten_F[:,:,e3], c=f_ten_F[:,:,e3], cmap=plt.cm.viridis, marker='.')
        limgs[2] = laxes[2].scatter(eta1[:,:,e3], eta2[:,:,e3], f_pol_F[:,:,e3], c=f_pol_F[:,:,e3], cmap=plt.cm.viridis, marker='.')
        limgs[3] = laxes[3].scatter(eta1[:,:,e3], eta2[:,:,e3], f_pol_F1[:,:,e3], c=f_pol_F1[:,:,e3], cmap=plt.cm.viridis, marker='.')
        # When the function is dependent on eta3 as well (3D).
        # limgs[0] = laxes[1].scatter(eta1, eta2, eta3, c=f_exact, cmap=plt.cm.viridis, marker='.')
        # limgs[1] = laxes[2].scatter(eta1, eta2, eta3, c=f_ten_F, cmap=plt.cm.viridis, marker='.')
        # limgs[2] = laxes[3].scatter(eta1, eta2, eta3, c=f_pol_F, cmap=plt.cm.viridis, marker='.')
        # limgs[3] = laxes[4].scatter(eta1, eta2, eta3, c=f_pol_F1, cmap=plt.cm.viridis, marker='.')



    # TODO: Bug: Colorbar only updates with scatter plot but not the others (surface, contourf).
    l_is_contour = metadata['lplot'] in [PlotTypeLeft.CONTOUR2D, PlotTypeLeft.CONTOUR3D]
    if metadata['lplot'] != PlotTypeLeft.WIREFRAME:
        try:
            for i in range(4):
                # lcbars[i].set_clim(lmin, lmax)
                # limgs[i].colorbar = lcbars[i]
                # limgs[i].colorbar_cid = limgs[i].callbacks.connect('changed', lcbars[i].update_normal)
                # limgs[i].changed()
                # lcbars[i].update_normal(limgs[i])
                # lcbars[i].update_ticks()
                # lcbars[i].draw_all()
                lcbars[i].remove()
                if metadata['comptype'] == Comparison.ORIG:
                    lcbars[i] = fig.colorbar(limgs[i], ax=laxes[i], shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=metadata['lzlabel'])
                else:
                    if i == 0:
                        lcbars[i] = fig.colorbar(limgs[i], ax=laxes[i], shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=metadata['lzlabel'])
                    else:
                        lcbars[i] = fig.colorbar(limgs[i], ax=laxes[i], shrink=0.9, pad=0.15, location='bottom', drawedges=l_is_contour, extend='both', label=metadata['lzlabeld'])
            for cbar in lcbars:
                # cbar.ax.locator_params(nbins=3)
                cbar.ax.tick_params(labelsize=lbl_size)
                cbar.locator = ticker.LinearLocator(5)
                cbar.update_ticks()

        except Exception as e:
            print(e)



    # ============================================================
    # Four derivatives on the right.
    # ============================================================

    if func_form == FuncForm.ZERO:

        # LHS: Original 0-form function.
        # RHS: 1-form gradient, only x component, because y is identical and z is zero.
        # Figure 1: Actual value.
        # Figure 2: Difference.
        df_mag = np.sqrt(2 * df_ten_F**2)

    elif func_form == FuncForm.ONE:

        # LHS: Original 1-form function, only x-component because all directions are identical.
        # RHS: 2-form curl, only z component because x and y are zero.
        # Figure 1: Actual value.
        # Figure 2: Difference.
        df_mag = np.sqrt(3 * df_ten_F**2)

    elif func_form == FuncForm.TWO:

        # LHS: Original 2-form function, only x-component because all directions are identical.
        # RHS: 3-form div.
        # Figure 1: Actual value.
        # Figure 2: Difference.
        df_mag = np.sqrt(3 * df_ten_F**2)

    else:

        raise NotImplementedError(f'FuncForm {func_form.name} not recognized.')

    # df_mag = np.sqrt(df_ten_F[0]**2 + df_ten_F[1]**2 + df_ten_F[2]**2)
    print('df_mag.shape', df_mag.shape)
    print('Max |df|:', np.max(df_mag))
    print('Min |df|:', np.min(df_mag))

    # Flatten and normalize.
    if r_is_3d:
        c = (df_mag.ravel() - df_mag.min()) / df_mag.ptp()
    else:
        c = (df_mag[:,:,e3].ravel() - df_mag[:,:,e3].min()) / df_mag[:,:,e3].ptp()
    # print('c.shape', c.shape)
    # Repeat for each body line and two head lines in a quiver.
    c = np.concatenate((c, np.repeat(c, 2)))
    # print('c.shape', c.shape)
    # Colormap.
    c = plt.cm.viridis(c)
    # print('c.shape', c.shape)



    cmap = plt.cm.get_cmap("viridis").copy()
    cmap.set_over('white')
    cmap.set_under('black')
    if metadata['rplot'] in [PlotTypeRight.CONTOUR2D, PlotTypeRight.CONTOUR3D]:
        for img in rimgs:
            for c in img.collections:
                c.remove() # Remove only the contours, leave the rest intact.
        if metadata['comptype'] == Comparison.ORIG:
            rimgs[0] = raxes[0].contourf(eta1[:,:,e3], eta2[:,:,e3], df_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
            rimgs[0].set_clim(rmin, rmax)
        else:
            rimgs[0] = raxes[0].contourf(eta1[:,:,e3], eta2[:,:,e3], df_exact[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(np.nanmin(df_exact[:,:,e3]),np.nanmax(df_exact[:,:,e3]),levels), vmin=np.nanmin(df_exact[:,:,e3]), vmax=np.nanmax(df_exact[:,:,e3]))
        rimgs[1] = raxes[1].contourf(eta1[:,:,e3], eta2[:,:,e3], df_ten_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
        rimgs[2] = raxes[2].contourf(eta1[:,:,e3], eta2[:,:,e3], df_pol_F[:,:,e3],  cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
        rimgs[3] = raxes[3].contourf(eta1[:,:,e3], eta2[:,:,e3], df_pol_F1[:,:,e3], cmap=cmap, extend='both', levels=np.linspace(rmin,rmax,levels), vmin=rmin, vmax=rmax)
        rimgs[1].set_clim(rmin, rmax)
        rimgs[2].set_clim(rmin, rmax)
        rimgs[3].set_clim(rmin, rmax)
        # rimgs[0].cmap.set_over('white')
        # rimgs[1].cmap.set_over('white')
        # rimgs[2].cmap.set_over('white')
        # rimgs[3].cmap.set_over('white')
        # rimgs[0].cmap.set_under('black')
        # rimgs[1].cmap.set_under('black')
        # rimgs[2].cmap.set_under('black')
        # rimgs[3].cmap.set_under('black')
        # rimgs[0].changed()
        # rimgs[1].changed()
        # rimgs[2].changed()
        # rimgs[3].changed()
    elif metadata['rplot'] == PlotTypeRight.SURFACE:
        # for img in rimgs:
        #     img.remove()
        for ax, img in zip(raxes, rimgs):
            ax.collections.remove(img)
        rimgs[0] = raxes[0].plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_exact[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
        rimgs[1] = raxes[1].plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_ten_F[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
        rimgs[2] = raxes[2].plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_pol_F[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
        rimgs[3] = raxes[3].plot_surface(eta1[:,:,e3], eta2[:,:,e3], df_pol_F1[:,:,e3], vmin=rmin, vmax=rmax, cmap=plt.cm.viridis)
    elif metadata['rplot'] == PlotTypeRight.QUIVER2D:
        for img in rimgs:
            img.remove()
        scale = 500
        metadata['rzlabel'] = metadata['rzlabel'] + f' Scale: {1/scale}'
        rimgs[0] = raxes[0].quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_exact[0,:,:,e3].flatten(), df_exact[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimgs[1] = raxes[1].quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_ten_F[0,:,:,e3].flatten(), df_ten_F[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimgs[2] = raxes[2].quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_pol_F[0,:,:,e3].flatten(), df_pol_F[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimgs[3] = raxes[3].quiver(eta1[:,:,e3].flatten(), eta2[:,:,e3].flatten(), df_pol_F1[0,:,:,e3].flatten(), df_pol_F1[1,:,:,e3].flatten(), color=c, cmap=plt.cm.viridis, scale=scale)
        rimgs[0].set_array(df_mag[:,:,e3].flatten())
        rimgs[1].set_array(df_mag[:,:,e3].flatten())
        rimgs[2].set_array(df_mag[:,:,e3].flatten())
        rimgs[3].set_array(df_mag[:,:,e3].flatten())
        rimgs[0].set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
        rimgs[1].set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
        rimgs[2].set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
        rimgs[3].set_clim(np.min(df_mag[:,:,e3]), np.max(df_mag[:,:,e3]))
    elif metadata['rplot'] == PlotTypeRight.QUIVER3D:
        for img in rimgs:
            img.remove()
        scale = 500
        metadata['rzlabel'] = metadata['rzlabel'] + f' Scale: {1/scale}'
        rimgs[0] = raxes[0].quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_exact[0].flatten(), df_exact[1].flatten(), df_exact[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimgs[1] = raxes[1].quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_ten_F[0].flatten(), df_ten_F[1].flatten(), df_ten_F[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimgs[2] = raxes[2].quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_pol_F[0].flatten(), df_pol_F[1].flatten(), df_pol_F[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimgs[3] = raxes[3].quiver(eta1.flatten(), eta2.flatten(), eta3.flatten(), df_pol_F1[0].flatten(), df_pol_F1[1].flatten(), df_pol_F1[2].flatten(), color=c, cmap=plt.cm.viridis, length=1/scale)
        rimgs[0].set_array(df_mag.flatten())
        rimgs[1].set_array(df_mag.flatten())
        rimgs[2].set_array(df_mag.flatten())
        rimgs[3].set_array(df_mag.flatten())
        rimgs[0].set_clim(np.min(df_mag), np.max(df_mag))
        rimgs[1].set_clim(np.min(df_mag), np.max(df_mag))
        rimgs[2].set_clim(np.min(df_mag), np.max(df_mag))
        rimgs[3].set_clim(np.min(df_mag), np.max(df_mag))



    # TODO: Bug: Colorbar only updates with scatter plot but not the others (surface, contourf).
    r_is_contour = metadata['rplot'] in [PlotTypeRight.CONTOUR2D, PlotTypeRight.CONTOUR3D]
    try:
        for i in range(4):
            # rcbars[i].set_clim(rmin, rmax)
            # rimgs[i].colorbar = rcbars[i]
            # rimgs[i].colorbar_cid = rimgs[i].callbacks.connect('changed', rcbars[i].update_normal)
            # rimgs[i].changed()
            # rcbars[i].update_normal(rimgs[i])
            # rcbars[i].update_ticks()
            # rcbars[i].draw_all()
            rcbars[i].remove()
            if metadata['comptype'] == Comparison.ORIG:
                rcbars[i] = fig.colorbar(rimgs[i], ax=raxes[i], shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=metadata['rzlabel'])
            else:
                if i == 0:
                    rcbars[i] = fig.colorbar(rimgs[i], ax=raxes[i], shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=metadata['rzlabel'])
                else:
                    rcbars[i] = fig.colorbar(rimgs[i], ax=raxes[i], shrink=0.9, pad=0.15, location='bottom', drawedges=r_is_contour, extend='both', label=metadata['rzlabeld'])
        for cbar in rcbars:
            # cbar.ax.locator_params(nbins=3)
            cbar.ax.tick_params(labelsize=lbl_size)
            cbar.locator = ticker.LinearLocator(5)
            cbar.update_ticks()

    except Exception as e:
        print(e)



    # Mark position on mapping pole.
    show_el_b = metadata['show_el_b']
    show_pole = metadata['show_pole']
    show_grid = metadata['show_grid']
    origin = metadata['origin']
    el_b = metadata['el_b']
    print('='*20)
    print(f'l_is_3d? {l_is_3d} {metadata["lplot"]} {metadata["lplot"].name}')
    print(f'r_is_3d? {r_is_3d} {metadata["rplot"]} {metadata["rplot"].name}')
    print(f'show_el_b? {show_el_b}')
    print(f'show_pole? {show_pole}')
    print(f'show_grid? {show_grid}')
    print(f'Updated el_b[0].shape {el_b[0].shape}')
    print(f'Updated el_b[1].shape {el_b[1].shape}')
    print(f'Updated el_b[2].shape {el_b[2].shape}')
    print(f'Lengths of L items: {len(laxes)} {len(lpoles)} {len(lgrids)} {len(lel_bs)}')
    print(f'Lengths of R items: {len(raxes)} {len(rpoles)} {len(rgrids)} {len(rel_bs)}')

    for idx, (ax, pole, grid, spce) in enumerate(zip(laxes, lpoles, lgrids, lel_bs)):
        ax.set_xlim(origin[0] - axlim, origin[0] + axlim)
        ax.set_ylim(origin[1] - axlim, origin[1] + axlim)
        if space_enum == SpaceType.LOGICAL:
            ax.set_xlim(origin[0], origin[0] + axlim)
            ax.set_ylim(origin[1], origin[1] + axlim)
        if l_is_3d:
            if show_grid:
                ax.collections.remove(grid)
                lgrids[idx] = ax.scatter(     eta1,      eta2,      eta3, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                ax.collections.remove(spce)
                lel_bs[idx] = ax.scatter(  el_b[0],   el_b[1],   el_b[2], marker='x', facecolors='navy',         alpha=0.1, label='el_b')
                # print(f'type(lel_bs[idx]) {type(lel_bs[idx])}')
                # lel_bs[idx]._offsets3d = (  el_b[0],   el_b[1],   el_b[2])
            if show_pole:
                ax.collections.remove(pole)
                lpoles[idx] = ax.scatter(origin[0], origin[1], origin[2], marker='o', facecolors='none', edgecolors='red',  label='Pole', s=64, lw=3)
        else:
            if show_grid:
                ax.collections.remove(grid)
                lgrids[idx] = ax.scatter(     eta1,      eta2,       100, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                ax.collections.remove(spce)
                lel_bs[idx] = ax.scatter(  el_b[0],   el_b[1],       100, marker='x', facecolors='navy',         alpha=0.1, label='el_b')
            if show_pole:
                ax.collections.remove(pole)
                lpoles[idx] = ax.scatter(origin[0], origin[1],       100, marker='o', facecolors='none', edgecolors='red',  label='Pole', s=64, lw=3)

    for idx, (ax, pole, grid, spce) in enumerate(zip(raxes, rpoles, rgrids, rel_bs)):
        ax.set_xlim(origin[0] - axlim, origin[0] + axlim)
        ax.set_ylim(origin[1] - axlim, origin[1] + axlim)
        if space_enum == SpaceType.LOGICAL:
            ax.set_xlim(origin[0], origin[0] + axlim)
            ax.set_ylim(origin[1], origin[1] + axlim)
        if r_is_3d:
            if show_grid:
                ax.collections.remove(grid)
                rgrids[idx] = ax.scatter(     eta1,      eta2,      eta3, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                ax.collections.remove(spce)
                rel_bs[idx] = ax.scatter(  el_b[0],   el_b[1],   el_b[2], marker='x', facecolors='navy',         alpha=0.1, label='el_b')
                # print(f'type(rel_bs[idx]) {type(rel_bs[idx])}')
                # rel_bs[idx]._offsets3d = (  el_b[0],   el_b[1],   el_b[2])
            if show_pole:
                ax.collections.remove(pole)
                rpoles[idx] = ax.scatter(origin[0], origin[1], origin[2], marker='o', facecolors='none', edgecolors='red',  label='Pole', s=64, lw=3)
        else:
            if show_grid:
                ax.collections.remove(grid)
                rgrids[idx] = ax.scatter(     eta1,      eta2,       100, marker='+', facecolors='cyan',         alpha=0.2, label='Grid')
            if show_el_b:
                ax.collections.remove(spce)
                rel_bs[idx] = ax.scatter(  el_b[0],   el_b[1],       100, marker='x', facecolors='navy',         alpha=0.1, label='el_b')
            if show_pole:
                ax.collections.remove(pole)
                rpoles[idx] = ax.scatter(origin[0], origin[1],       100, marker='o', facecolors='none', edgecolors='red',  label='Pole', s=64, lw=3)



    # fig.canvas.draw()
    # fig.canvas.flush_events()

    fig.canvas.draw_idle()

    print('Completed plot_update().')
    print('='*50)



def plot_controls(case, case_args, func_test, func_form, plot_handles):

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Button, RadioButtons, Slider

    references = []
    case_args = case_args[1:] # Removing `params`.



    if func_test == FuncTest.GAUSSIAN:

        # Plot settings.
        row = 3
        col = 2
        dpi = 100
        width, height = (640 / dpi, 320 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('Change Plot Parameters (Gaussian)')
        fig.suptitle('Change Plot Parameters (Gaussian)')

        axis_color = 'lightgoldenrodyellow'

        # Define an axis and draw a slider.
        sd_x = 0.1
        sd_y = 0.05
        mu_x = sd_x
        mu_y = sd_y
        # mu_x_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axis_color)
        # mu_y_slider_ax = fig.add_axes([0.25, 0.10, 0.65, 0.03], facecolor=axis_color)
        mu_x_slider_ax = fig.add_subplot(gs[0, 0], facecolor=axis_color)
        mu_y_slider_ax = fig.add_subplot(gs[0, 1], facecolor=axis_color)
        sd_x_slider_ax = fig.add_subplot(gs[1, 0], facecolor=axis_color)
        sd_y_slider_ax = fig.add_subplot(gs[1, 1], facecolor=axis_color)
        mu_x_slider = Slider(mu_x_slider_ax, '$\mu_x$', -2.0, 2.0, valinit=mu_x, valfmt='%+.3f')
        mu_y_slider = Slider(mu_y_slider_ax, '$\mu_y$', -2.0, 2.0, valinit=mu_y, valfmt='%+.3f')
        sd_x_slider = Slider(sd_x_slider_ax, '$\sigma_x$', 0.001, 2.0, valinit=sd_x, valfmt='%+.3f')
        sd_y_slider = Slider(sd_y_slider_ax, '$\sigma_y$', 0.001, 2.0, valinit=sd_y, valfmt='%+.3f')
        references.append(mu_x_slider)
        references.append(mu_y_slider)
        references.append(sd_x_slider)
        references.append(sd_y_slider)

        # Define a listener for modifying the line when any slider's value changes.
        def sliders_on_changed(val):
            print(f'Updated {val}')
            func, dfdx, dfdy = generate_2d_trial_func(func_test, params={
                'mu_x': mu_x_slider.val + 10,
                'mu_y': mu_y_slider.val,
                'sd_x': sd_x_slider.val,
                'sd_y': sd_y_slider.val,
            })
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy)
            if func_form == FuncForm.ZERO:
                case_args[6] = func
                case_args[7] = dfdx
                case_args[8] = dfdy
            else:
                case_args[6] = func_3d
                case_args[7] = curl_3d
                case_args[8] = div_3d
            plot_data = case(*case_args)
            plot_updater(plot_handles, *plot_data)
            fig.canvas.draw_idle()
        for slider in references:
            slider.on_changed(sliders_on_changed)

        # Add a button for resetting the parameters.
        reset_button_ax = fig.add_subplot(gs[2, 0:2])
        reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
        references.append(reset_button)

        def reset_button_on_clicked(mouse_event):
            print('Reset!')
            mu_x_slider.reset()
            mu_y_slider.reset()
            sd_x_slider.reset()
            sd_y_slider.reset()
        reset_button.on_clicked(reset_button_on_clicked)



    elif func_test == FuncTest.GAUSSIANCOSINE:

        # Plot settings.
        row = 5
        col = 2
        dpi = 100
        width, height = (640 / dpi, 480 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('Change Plot Parameters (Gaussian-Cosine)')
        fig.suptitle('Change Plot Parameters (Gaussian-Cosine)')

        axis_color = 'lightgoldenrodyellow'

        # Define an axis and draw a slider.
        sd_x = 0.1
        sd_y = 0.05
        mu_x = sd_x
        mu_y = sd_y
        v_x = 1
        v_y = 1
        om_x = 2 * np.pi * v_x / (4 * sd_x) # Steepest gradient.
        om_y = 2 * np.pi * v_y / (4 * sd_y) # Steepest gradient.
        ph_x = 2 * np.pi * (mu_x)
        ph_y = 2 * np.pi * (mu_y)
        mu_x_slider_ax = fig.add_subplot(gs[0, 0], facecolor=axis_color)
        sd_x_slider_ax = fig.add_subplot(gs[1, 0], facecolor=axis_color)
        om_x_slider_ax = fig.add_subplot(gs[2, 0], facecolor=axis_color)
        ph_x_slider_ax = fig.add_subplot(gs[3, 0], facecolor=axis_color)
        mu_y_slider_ax = fig.add_subplot(gs[0, 1], facecolor=axis_color)
        sd_y_slider_ax = fig.add_subplot(gs[1, 1], facecolor=axis_color)
        om_y_slider_ax = fig.add_subplot(gs[2, 1], facecolor=axis_color)
        ph_y_slider_ax = fig.add_subplot(gs[3, 1], facecolor=axis_color)
        mu_x_slider = Slider(mu_x_slider_ax, '$\mu_x$', -2.0, 2.0, valinit=mu_x, valfmt='%+.3f')
        mu_y_slider = Slider(mu_y_slider_ax, '$\mu_y$', -2.0, 2.0, valinit=mu_y, valfmt='%+.3f')
        sd_x_slider = Slider(sd_x_slider_ax, '$\sigma_x$', 0.001, 2.0, valinit=sd_x, valfmt='%+.3f')
        sd_y_slider = Slider(sd_y_slider_ax, '$\sigma_y$', 0.001, 2.0, valinit=sd_y, valfmt='%+.3f')
        om_x_slider = Slider(om_x_slider_ax, '$\omega_x$', -100.0, 100.0, valinit=om_x, valfmt='%+.3f')
        om_y_slider = Slider(om_y_slider_ax, '$\omega_y$', -100.0, 100.0, valinit=om_y, valfmt='%+.3f')
        ph_x_slider = Slider(ph_x_slider_ax, '$\\varphi_x$', -10.0, 10.0, valinit=ph_x, valfmt='%+.3f')
        ph_y_slider = Slider(ph_y_slider_ax, '$\\varphi_y$', -10.0, 10.0, valinit=ph_y, valfmt='%+.3f')
        references.append(mu_x_slider)
        references.append(mu_y_slider)
        references.append(sd_x_slider)
        references.append(sd_y_slider)
        references.append(om_x_slider)
        references.append(om_y_slider)
        references.append(ph_x_slider)
        references.append(ph_y_slider)

        # Define a listener for modifying the line when any slider's value changes.
        def sliders_on_changed(val):
            print(f'Updated {val}')
            func, dfdx, dfdy = generate_2d_trial_func(func_test, params={
                'mu_x': mu_x_slider.val + 10,
                'mu_y': mu_y_slider.val,
                'sd_x': sd_x_slider.val,
                'sd_y': sd_y_slider.val,
                'om_x': om_x_slider.val,
                'om_y': om_y_slider.val,
                'ph_x': ph_x_slider.val + 10 * 2 * np.pi,
                'ph_y': ph_y_slider.val,
            })
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy)
            if func_form == FuncForm.ZERO:
                case_args[6] = func
                case_args[7] = dfdx
                case_args[8] = dfdy
            else:
                case_args[6] = func_3d
                case_args[7] = curl_3d
                case_args[8] = div_3d
            plot_data = case(*case_args)
            plot_updater(plot_handles, *plot_data)
            fig.canvas.draw_idle()
        for slider in references:
            slider.on_changed(sliders_on_changed)

        # Add a button for resetting the parameters.
        reset_button_ax = fig.add_subplot(gs[4, 0:2])
        reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
        references.append(reset_button)

        def reset_button_on_clicked(mouse_event):
            print('Reset!')
            mu_x_slider.reset()
            mu_y_slider.reset()
            sd_x_slider.reset()
            sd_y_slider.reset()
            om_x_slider.reset()
            om_y_slider.reset()
            ph_x_slider.reset()
            ph_y_slider.reset()
        reset_button.on_clicked(reset_button_on_clicked)



    elif func_test == FuncTest.SINEX:

        # Plot settings.
        row = 3
        col = 1
        dpi = 100
        width, height = (640 / dpi, 320 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('Change Plot Parameters (Sine(x))')
        fig.suptitle('Change Plot Parameters (Sine(x))')

        axis_color = 'lightgoldenrodyellow'

        # Define an axis and draw a slider.
        om_x = 2 * np.pi
        ph_x = 0
        om_x_slider_ax = fig.add_subplot(gs[0, 0], facecolor=axis_color)
        ph_x_slider_ax = fig.add_subplot(gs[1, 0], facecolor=axis_color)
        om_x_slider = Slider(om_x_slider_ax, '$\omega_x$', -100.0, 100.0, valinit=om_x, valfmt='%+.3f')
        ph_x_slider = Slider(ph_x_slider_ax, '$\\varphi_x$', -10.0, 10.0, valinit=ph_x, valfmt='%+.3f')
        references.append(om_x_slider)
        references.append(ph_x_slider)

        # Define a listener for modifying the line when any slider's value changes.
        def sliders_on_changed(val):
            print(f'Updated {val}')
            func, dfdx, dfdy = generate_2d_trial_func(func_test, params={
                'om_x': om_x_slider.val,
                'ph_x': ph_x_slider.val + 10 * 2 * np.pi,
            })
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy)
            if func_form == FuncForm.ZERO:
                case_args[6] = func
                case_args[7] = dfdx
                case_args[8] = dfdy
            else:
                case_args[6] = func_3d
                case_args[7] = curl_3d
                case_args[8] = div_3d
            plot_data = case(*case_args)
            plot_updater(plot_handles, *plot_data)
            fig.canvas.draw_idle()
        for slider in references:
            slider.on_changed(sliders_on_changed)

        # Add a button for resetting the parameters.
        reset_button_ax = fig.add_subplot(gs[2, 0])
        reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
        references.append(reset_button)

        def reset_button_on_clicked(mouse_event):
            print('Reset!')
            om_x_slider.reset()
            ph_x_slider.reset()
        reset_button.on_clicked(reset_button_on_clicked)



    elif func_test == FuncTest.SIGMOID:

        # Plot settings.
        row = 3
        col = 2
        dpi = 100
        width, height = (640 / dpi, 320 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('Change Plot Parameters (Sigmoid/Logistic)')
        fig.suptitle('Change Plot Parameters (Sigmoid/Logistic)')

        axis_color = 'lightgoldenrodyellow'

        # Define an axis and draw a slider.
        mu_x = 0.0
        mu_y = 0.0
        k_x = 100
        k_y = 100
        mu_x_slider_ax = fig.add_subplot(gs[0, 0], facecolor=axis_color)
        mu_y_slider_ax = fig.add_subplot(gs[0, 1], facecolor=axis_color)
        sd_x_slider_ax = fig.add_subplot(gs[1, 0], facecolor=axis_color)
        sd_y_slider_ax = fig.add_subplot(gs[1, 1], facecolor=axis_color)
        mu_x_slider = Slider(mu_x_slider_ax, '$\mu_x$', -2.0, 2.0, valinit=mu_x, valfmt='%+.3f')
        mu_y_slider = Slider(mu_y_slider_ax, '$\mu_y$', -2.0, 2.0, valinit=mu_y, valfmt='%+.3f')
        k_x_slider = Slider(sd_x_slider_ax, '$k_x$', 0.001, 1000, valinit=k_x, valfmt='%+.3f')
        k_y_slider = Slider(sd_y_slider_ax, '$k_y$', 0.001, 1000, valinit=k_y, valfmt='%+.3f')
        references.append(mu_x_slider)
        references.append(mu_y_slider)
        references.append(k_x_slider)
        references.append(k_y_slider)

        # Define a listener for modifying the line when any slider's value changes.
        def sliders_on_changed(val):
            print(f'Updated {val}')
            func, dfdx, dfdy = generate_2d_trial_func(func_test, params={
                'mu_x': mu_x_slider.val + 10,
                'mu_y': mu_y_slider.val,
                'k_x': k_x_slider.val,
                'k_y': k_y_slider.val,
            })
            func_3d, curl_3d, div_3d = func_3d_wrapper(func, dfdx, dfdy)
            if func_form == FuncForm.ZERO:
                case_args[6] = func
                case_args[7] = dfdx
                case_args[8] = dfdy
            else:
                case_args[6] = func_3d
                case_args[7] = curl_3d
                case_args[8] = div_3d
            plot_data = case(*case_args)
            plot_updater(plot_handles, *plot_data)
            fig.canvas.draw_idle()
        for slider in references:
            slider.on_changed(sliders_on_changed)

        # Add a button for resetting the parameters.
        reset_button_ax = fig.add_subplot(gs[2, 0:2])
        reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
        references.append(reset_button)

        def reset_button_on_clicked(mouse_event):
            print('Reset!')
            mu_x_slider.reset()
            mu_y_slider.reset()
            k_x_slider.reset()
            k_y_slider.reset()
        reset_button.on_clicked(reset_button_on_clicked)



    elif func_test == FuncTest.CONSTANT:

        # Plot settings.
        row = 3
        col = 2
        dpi = 100
        width, height = (640 / dpi, 320 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('No Configurable Plot Parameters (Constant)')
        fig.suptitle('No Configurable Plot Parameters (Constant)')



    elif func_test == FuncTest.LINEARX:

        # Plot settings.
        row = 3
        col = 2
        dpi = 100
        width, height = (640 / dpi, 320 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('No Configurable Plot Parameters (Linear X)')
        fig.suptitle('No Configurable Plot Parameters (Linear X)')



    elif func_test == FuncTest.LINEARXYSUM:

        # Plot settings.
        row = 3
        col = 2
        dpi = 100
        width, height = (640 / dpi, 320 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('No Configurable Plot Parameters (Linear XY Sum)')
        fig.suptitle('No Configurable Plot Parameters (Linear XY Sum)')



    elif func_test == FuncTest.LINEARXYPROD:

        # Plot settings.
        row = 3
        col = 2
        dpi = 100
        width, height = (640 / dpi, 320 / dpi)
        fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
        gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
        fig.canvas.manager.set_window_title('No Configurable Plot Parameters (Linear XY Product)')
        fig.suptitle('No Configurable Plot Parameters (Linear XY Product)')



    else:

        raise NotImplementedError(f'Test case {func_test.name} not implemented.')



    # print('Before `tight_layout()`   | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))
    fig.tight_layout()
    # print('After `tight_layout()`    | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))
    fig.subplots_adjust(hspace=fig.subplotpars.hspace * 0.5, wspace=fig.subplotpars.wspace * 1.2)
    # print('After `subplots_adjust()` | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))

    return references



def plot_spl_config(case, case_args, func_test, func_form, plot_handles):

    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Button, RadioButtons, Slider

    references = []
    case_args = case_args[1:] # Removing `params`.

    Nel = case_args[0]
    p = case_args[1]

    # Plot settings.
    row = 4
    col = 2
    dpi = 100
    width, height = (640 / dpi, 320 / dpi)
    fig = plt.figure(figsize=(width,height), dpi=dpi)#, constrained_layout=True)
    gs  = fig.add_gridspec(row, col)#, width_ratios=[1,1]*2)
    fig.canvas.manager.set_window_title('Change Spline Configurations')
    fig.suptitle('Change Spline Configurations')

    axis_color = 'lightgoldenrodyellow'

    Nel1_slider_ax = fig.add_subplot(gs[0, 0], facecolor=axis_color)
    Nel2_slider_ax = fig.add_subplot(gs[1, 0], facecolor=axis_color)
    Nel3_slider_ax = fig.add_subplot(gs[2, 0], facecolor=axis_color)
    deg1_slider_ax = fig.add_subplot(gs[0, 1], facecolor=axis_color)
    deg2_slider_ax = fig.add_subplot(gs[1, 1], facecolor=axis_color)
    deg3_slider_ax = fig.add_subplot(gs[2, 1], facecolor=axis_color)
    Nel1_slider = Slider(Nel1_slider_ax, '$Nel_s$'      , 3, 100, valinit=Nel[0], valfmt='%d', valstep=1)
    Nel2_slider = Slider(Nel2_slider_ax, '$Nel_\\theta$', 3, 100, valinit=Nel[1], valfmt='%d', valstep=3)
    Nel3_slider = Slider(Nel3_slider_ax, '$Nel_\zeta$'  , 3, 100, valinit=Nel[2], valfmt='%d', valstep=1)
    deg1_slider = Slider(deg1_slider_ax, '$p_s$'      , 2, 6, valinit=p[0], valfmt='%d', valstep=1)
    deg2_slider = Slider(deg2_slider_ax, '$p_\\theta$', 2, 6, valinit=p[1], valfmt='%d', valstep=1)
    deg3_slider = Slider(deg3_slider_ax, '$p_\zeta$'  , 2, 6, valinit=p[2], valfmt='%d', valstep=1)
    references.append(Nel1_slider)
    references.append(Nel2_slider)
    references.append(Nel3_slider)
    references.append(deg1_slider)
    references.append(deg2_slider)
    references.append(deg3_slider)

    # Define a listener for modifying the line when any slider's value changes.
    def sliders_on_changed(val):
        print(f'Updated {val}')
        # Nel
        case_args[0][0] = int(Nel1_slider.val)
        case_args[0][1] = int(Nel2_slider.val)
        case_args[0][2] = int(Nel3_slider.val)
        # p
        case_args[1][0] = int(deg1_slider.val)
        case_args[1][1] = int(deg2_slider.val)
        case_args[1][2] = int(deg3_slider.val)
        Nel = case_args[0]
        p = case_args[1]
        # TODO: Update DOMAIN_F in case_args, if MapType.SPLINE is used.
        plot_data = case(*case_args)
        plot_updater(plot_handles, *plot_data)
        update_fig_suptitle(plot_handles, Nel, p)
        fig.canvas.draw_idle()
    for slider in references:
        slider.on_changed(sliders_on_changed)

    # Add a button for resetting the parameters.
    reset_button_ax = fig.add_subplot(gs[3, 0:2])
    reset_button = Button(reset_button_ax, 'Reset', color=axis_color, hovercolor='0.975')
    references.append(reset_button)

    def reset_button_on_clicked(mouse_event):
        print('Reset!')
        # Reset all except the reset button itself.
        for slider in references[:-1]:
            slider.reset()
    reset_button.on_clicked(reset_button_on_clicked)



    # print('Before `tight_layout()`   | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))
    fig.tight_layout()
    # print('After `tight_layout()`    | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))
    fig.subplots_adjust(hspace=fig.subplotpars.hspace * 0.5, wspace=fig.subplotpars.wspace * 1.2)
    # print('After `subplots_adjust()` | hspace: {}; wspace: {}.'.format(fig.subplotpars.hspace, fig.subplotpars.wspace))

    return references



def update_fig_suptitle(plot_handles, Nel, p):
    for handle in plot_handles:
        fig = handle['fig']
        params = handle['params']
        metadata = handle['metadata']
        title_x1 = fig._suptitle.get_text()
        title_x2 = title_x1.split('\n')[0]
        title_x3 = title_x2 + f'\nNel: {Nel}   p: {p}'
        if 'eta2_cut' in metadata and (metadata['lplot'] == PlotTypeLeft.LINE or metadata['rplot'] == PlotTypeRight.LINE):
            eta2_range = params['plot']['eta_range'][1]
            eta2_pos = metadata['eta2_cut']
            eta2_neg = (eta2_pos + int(eta2_range.shape[0] / 2)) % eta2_range.shape[0]
            title_x3 += f'   eta2: {{{eta2_range[eta2_pos]:.2f}, {eta2_range[eta2_neg]:.2f}}}'
        if 'eta3_cut' in metadata:
            eta3_cut = params['plot']['eta_range'][2][metadata['eta3_cut']]
            title_x3 += f'   eta3: {eta3_cut:.2f}'
        print(f'Original suptitle: {title_x1}')
        print(f'First line of suptitle: {title_x2}')
        # fig.canvas.manager.set_window_title(title_x3)
        fig.suptitle(title_x3, y=0.98)
        print(f'Updated suptitle: {title_x3}')



def autoscale_y(ax, margin=0.2, ignore_labels=[], ignore_duplicates=False, maxi=2e4, mini=-2e4, force_finite=8e5):
    """Rescales the y-axis based on the data that is visible given the current xlim of the axis.

    Source: https://stackoverflow.com/questions/29461608/matplotlib-fixing-x-axis-scale-and-autoscale-y-axis

    Parameters
    ----------
    ax : Axes
        A matplotlib axes object.
    margin : float
        The fraction of the total height of the y-data to pad the upper and lower ylims.
    ignore_labels : list
        A list of axis labels that are to be ignored during autoscaling. `['Pole', 'Grid', 'el_b']` are always ignored.
    ignore_duplicates : bool
        Whether to ignore lines with identical labels.
    maxi : float
        If the data range contains y-values that exceed this number, the entire range will be ignored.
    mini : float
        If the data range contains y-values smaller than this number, the entire range will be ignored.
    force_finite : float
        Initialize the autoscale range to a finite number, instead of `np.inf` (`if force_finite is None`).
    """

    import numpy as np

    def get_bottom_top(line, local_pad=False):
        """Return the minimum and maximum y-values within the range given by `xlim`."""
        xd = line.get_xdata()
        yd = line.get_ydata()
        lo,hi = ax.get_xlim()
        y_displayed = yd[((xd>lo) & (xd<hi))]
        if local_pad: # Padding is added w.r.t each line.
            h = np.nanmax(y_displayed) - np.nanmin(y_displayed)
            bot = np.nanmin(y_displayed) - margin * h
            top = np.nanmax(y_displayed) + margin * h
        else: # Return vanilla minimum and maximum.
            bot = np.nanmin(y_displayed)
            top = np.nanmax(y_displayed)
        return bot, top

    if force_finite is None:
        bot, top = np.inf, -np.inf
    else:
        bot, top = force_finite, -force_finite

    lines = ax.get_lines()

    ignore_labels = ['Pole', 'Grid', 'el_b'] + ignore_labels # Lines to ignore when computing y-axis limits.

    for line in lines:
        if all(label not in line.get_label() for label in ignore_labels):
            if ignore_duplicates: # Don't! This will only process the `pos` part of the plot!
                ignore_labels.append(line.get_label())
            new_bot, new_top = get_bottom_top(line)
            if new_bot < mini or new_top > maxi:
                continue
            # print(f'autoscale_y(): {line.get_label(): >12} range of y-values: {new_bot}, {new_top}')
            if new_bot < bot: bot = new_bot
            if new_top > top: top = new_top

    # print(f'autoscale_y(): {"Be4 margin": >12} range of y-values: {bot}, {top}')
    h = top - bot
    bot -= margin * h / 2
    top += margin * h / 2
    # print(f'autoscale_y(): {"Final": >12} range of y-values: {bot}, {top}')
    ax.set_ylim(bot, top)



def unique_legends(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))



def multicolor_label(ax, list_of_strings, list_of_colors, axis='x', anchorpad=0, **kw):
    """Creates axes labels with multiple colors.

    Source: https://stackoverflow.com/questions/33159134/matplotlib-y-axis-label-with-multiple-colors

    Parameters
    ----------
    ax
        Specifies the axes object where the labels should be drawn
    list_of_strings : list
        A list of all of the text items
    list_of_colors : list
        A corresponding list of colors for the strings
    axis : str
        {'x', 'y', 'both'}, specifies which label(s) should be drawn
    """

    from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker

    # x-axis label
    if axis == 'x' or axis == 'both':
        boxes = [TextArea(text, textprops=dict(color=color, ha='left', va='bottom', **kw))
                 for text, color in zip(list_of_strings, list_of_colors)]
        xbox = HPacker(children=boxes, align="center", pad=0, sep=5)
        anchored_xbox = AnchoredOffsetbox(loc=3, child=xbox, pad=anchorpad, frameon=False, bbox_to_anchor=(0.2, -0.09),
                                          bbox_transform=ax.transAxes, borderpad=0.)
        ax.add_artist(anchored_xbox)

    # y-axis label
    if axis == 'y' or axis == 'both':
        boxes = [TextArea(text, textprops=dict(color=color, ha='left', va='bottom', rotation=90, **kw))
                 for text, color in zip(list_of_strings[::-1], list_of_colors)]
        ybox = VPacker(children=boxes, align="center", pad=0, sep=5)
        anchored_ybox = AnchoredOffsetbox(loc=3, child=ybox, pad=anchorpad, frameon=False, bbox_to_anchor=(-0.10, 0.2),
                                          bbox_transform=ax.transAxes, borderpad=0.)
        ax.add_artist(anchored_ybox)



def plot_ref_order(ax:matplotlib.axes.Axes, order:int, Nels, errors, c):
    """Plot reference convergence order.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to plot.
    order : int
        Reference convergence order.
    Nels : list
        List of Nel in a certain direction.
    errors : list or float
        A list of errors (y-axis of plot), or the mid-point, or any point where you want to anchor this reference plot.
    c : any
        Color of line.
    """

    mid_idx = int(len(Nels) / 2)
    mid_x   = Nels[mid_idx]
    if isinstance(errors, float):
        mid_y = errors
    else: # A 1D error array.
        mid_y = errors[mid_idx]
    intercept = np.log(mid_y) - (-order) * np.log(mid_x)
    xs = np.linspace(Nels[0], Nels[-1], 2)
    ys = np.array([np.exp(np.log(xi) * (-order) + intercept) for xi in xs])
    ax.plot(xs, ys, c=c, alpha=0.8, ls='dotted', label=f'Order {order} ref.')



def flipped_logical(form_enum: FuncForm, comp=None, is_der=False, bypass=False):
    """Return -1 if the differential form component is flipped in logical space, 1 otherwise.

    Parameters
    ----------
    form_enum : FuncForm
        Differential form.
    comp : int
        If the differential form is vector-valued, its vector component {0,1,2}. Ignored if scalar-valued.
    is_der : bool
        Convenient switch to step `form_enum` by one on the de Rham complex, if an FEEC derivative has been applied.
    bypass : bool
        Convenient switch to always return 1.

    Returns
    -------
    int
        {-1,1}, depending on if the component is flipped in logical space.
    """

    if bypass:
        return 1

    assert isinstance(form_enum, FuncForm)
    assert form_enum in [FuncForm.ZERO, FuncForm.ONE, FuncForm.TWO, FuncForm.THREE]
    if is_der:
        if form_enum == FuncForm.ZERO:
            form_enum = FuncForm.ONE
        elif form_enum == FuncForm.ONE:
            form_enum = FuncForm.TWO
        elif form_enum == FuncForm.TWO:
            form_enum = FuncForm.THREE
        else:
            assert form_enum != FuncForm.THREE
    if form_enum in [FuncForm.ONE, FuncForm.TWO]:
        assert comp in [0,1,2]

    if form_enum == FuncForm.ONE and comp == 0:
        return -1
    elif form_enum == FuncForm.TWO and comp in [1,2]:
        return -1
    elif form_enum == FuncForm.THREE:
        return -1
    else:
        return 1



def get_save_path(fname, output_path=None):
    import os
    if output_path is None:
        output_path = os.path.join(os.path.expanduser('~'), 'polar-output')
    os.makedirs(output_path, exist_ok=True)
    return os.path.join(output_path, fname)



if __name__ == "__main__":

    import copy

    # Plotting grid.
    lim_s = 1
    num_s = 101
    num_s_log = 5
    eta1_range = np.concatenate((np.logspace(-num_s_log, -2, num_s_log*3+1), np.linspace(1e-2, lim_s, num_s-num_s_log*3)[1:])) # For visualization.
    # eta1_range = np.linspace(1e-5, lim_s, num_s) # For error computation.
    eta2_range = np.linspace(0, 1, 21)
    eta3_range = np.linspace(0, 1, 7)  # Default for Gaussian f(x,y).
    # eta3_range = np.linspace(0, 1, 21) # Default for Gaussian f(x,y,z).
    # eta3_range = np.linspace(0, 1, 41) # Default for Gaussian f(x,y,z) with full 3D torus.

    params_base = {
        'grid' : {

            # Nel2 must be a multiple of 3!
            # 'Nel'     : [16*1, 18*1, 6],
            # 'Nel'     : [16*2, 18*2, 6],  # Default for Gaussian f(x,y).
            'Nel'     : [16*2, 18*1, 10], # Default for Gaussian f(x,y,z).
            # 'Nel'     : [16*2, 18*2, 40], # Default for Gaussian f(x,y,z) with full 3D torus.
            # 'Nel'     : [16*4, 18*4, 6],

            # Odd degrees will have Greville point at zero, aligning with our evaluation eta3-plane.
            # 'p'       : [2, 2, 2],
            'p'       : [3, 3, 3], # Default.
            # 'p'       : [4, 4, 4],
            # 'p'       : [5, 5, 5],

            # Element integration, quadrature points per grid cell (for spline evaluation).
            # 'nq_el'   : [2, 2, 2],
            # 'nq_el'   : [4, 4, 4],
            'nq_el'   : [6, 6, 6], # Default.
            # 'nq_el'   : [8, 8, 8],

            # Greville integration, quadrature points per histopolation cell (for projection).
            # 'nq_pr'   : [2, 2, 2],
            # 'nq_pr'   : [4, 4, 4],
            'nq_pr'   : [6, 6, 6], # Default.
            # 'nq_pr'   : [8, 8, 8],

            # BC in s-direction.
            # This is the default within STRUPHY anyway, and is therefore unused.
            'bc'      : ['f', 'f'],

            # `spl_kind`, especially the last component, will be overridden / ignored within the code, and instead, inferred.
            # This is because periodicity of the mapping != periodicity of the trial function.
            'spl_kind': [False, True, False], # Spline type: True=periodic, False=clamped
            # 'spl_kind': [False, True, True ], # For full 3D torus.

        },
        'plot' : {
            'use_el_b' : False,
            'eta_range' : [eta1_range, eta2_range, eta3_range],
        },
    }
    params = copy.deepcopy(params_base)



    op_enum = Operation.ALL
    space_enum = SpaceType.PHYSICAL
    # space_enum = SpaceType.LOGICAL
    domain_enum = DomainType.DISCRETE

    # # Go through all trial functions.
    # for func_test in FuncTest:
    #     test_polar_splines_3D(params, func_test=func_test,         map_type=MapType.CIRCLEIDENTICAL, func_form=FuncForm.ZERO, space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)

    # Go through all domain maps, focusing on the 3rd component of curled 1-form, and divergence of 2-form.
    # for map_type in MapType:
    #     for space_enum in SpaceType:
    #         for domain_enum in DomainType:
    #             for func_form in FuncForm:
    #                 test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=map_type, func_form=func_form, space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)

    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.CIRCLEIDENTICAL,  func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.CIRCLEIDENTICAL,  func_form=FuncForm.ONE,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.CIRCLEIDENTICAL,  func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.CIRCLEIDENTICAL,  func_form=FuncForm.THREE, space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.CIRCLESCALED,     func_form=FuncForm.ONE,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.CIRCLESCALED,     func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.CIRCLESHIFTED,    func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.ELLIPSE,          func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.ELLIPSEROTATED,   func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SHAFRANOVSHIFT,   func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SHAFRANOVSQRT,    func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SHAFRANOVSQRT,    func_form=FuncForm.ONE,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SHAFRANOVSQRT,    func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SHAFRANOVDSHAPED, func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.SINEX,    map_type=MapType.SPLINE,           func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.LINEARX,  map_type=MapType.SPLINE,           func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SPLINE,           func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SPLINE,           func_form=FuncForm.ONE,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest.GAUSSIAN, map_type=MapType.SPLINE,           func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)

    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.SHAFRANOVDSHAPED, func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.SHAFRANOVDSHAPED, func_form=FuncForm.ONE,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.SHAFRANOVDSHAPED, func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.SHAFRANOVDSHAPED, func_form=FuncForm.THREE, space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum)

    eta3_slice = 0.75
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_EXTRU2D_ELLIPSTELL, func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_EXTRU2D_E1D6M6D6,   func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_EXTRU2D_E4D6M6D6,   func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_EXTRU2D_E40D5M6D6,  func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_EXTRU2D_CIRCTOK,    func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)

    eta3_slice = 0.75
    # test_polar_splines_3D(params, func_test=FuncTest3D.CONSTANT3D, map_type=MapType.GVEC_CYLDR3D_E4D6M6D6,   func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_CYLDR3D_E4D6M6D6,   func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_CYLDR3D_E4D6M6D6,   func_form=FuncForm.ONE,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_CYLDR3D_E4D6M6D6,   func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_CYLDR3D_E4D6M6D6,   func_form=FuncForm.THREE, space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)

    eta3_slice = 0.75
    # test_polar_splines_3D(params, func_test=FuncTest3D.CONSTANT3D, map_type=MapType.GVEC_TORUS3D_E4D6M6D6,   func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_TORUS3D_E4D6M6D6,   func_form=FuncForm.ZERO,  space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_TORUS3D_E4D6M6D6,   func_form=FuncForm.ONE,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_TORUS3D_E4D6M6D6,   func_form=FuncForm.TWO,   space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)
    # test_polar_splines_3D(params, func_test=FuncTest3D.GAUSSIAN3D, map_type=MapType.GVEC_TORUS3D_E4D6M6D6,   func_form=FuncForm.THREE, space_type=space_enum, domain_enum=domain_enum, op_enum=op_enum, eta3_slice=eta3_slice)

    print('='*20 + ' The End ' + '='*20)
