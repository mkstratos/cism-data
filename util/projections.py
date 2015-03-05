import os
import scipy
import pyproj

from util import speak

class DataGrid():
    """A class to hold data grids.
    """
    
    def make_grid(self):
        """A way to make a basic grid from x,y data.
        """
        self.y_grid, self.x_grid = scipy.meshgrid(self.y[:], self.x[:], indexing='ij')


def greenland(args, lc_bamber, base):
    """The projections and tranformation grids for Greenland.
    """
    proj_epsg3413 = pyproj.Proj('+proj=stere +lat_ts=70.0 +lat_0=90 +lon_0=-45.0 +k_0=1.0 +x_0=0.0 +y_0=0.0 +ellps=WGS84 +units=m')
        # InSAR data in this projections

    # EIGEN-GL04C referenced data:
    #----------------------------
    # unfortunately, bed, surface, and thickness data is referenced to 
    # EIGEN-GL04C which doesn't exist in proj4. However, EGM2008 should
    # be within ~1m everywhere (and within 10-20 cm in most places) so 
    # we use the egm08 projection which is available in proj4
    path_bamber = os.path.dirname(lc_bamber)
    if not ( os.path.exists(path_bamber+'/egm08_25.gtx') ):
        raise Exception("No "+path_bamber+"/egm08_25.gtx ! Get it here: http://download.osgeo.org/proj/vdatum/egm08_25/egm08_25.gtx") 
    
    #NOTE: Bamber projection appears to not actually have any fasle northings or eastings. 
    #proj_eigen_gl04c = pyproj.Proj('+proj=stere +lat_ts=71.0 +lat_0=90 +lon_0=321.0 +k_0=1.0 +x_0=800000.0 +y_0=3400000.0 +geoidgrids='+path_bamber+'/egm08_25.gtx')
    proj_eigen_gl04c = pyproj.Proj('+proj=stere +lat_ts=71.0 +lat_0=90 +lon_0=321.0 +k_0=1.0 +geoidgrids='+path_bamber+'/egm08_25.gtx')

    # transform meshes. 
    speak.verbose(args,"   Creating the transform meshes: base Bamber grid to EPSG-3413.")

    trans = DataGrid()
    trans.ny = base.ny
    trans.nx = base.nx

    trans.x_grid, trans.y_grid = pyproj.transform(proj_eigen_gl04c, proj_epsg3413, base.x_grid.flatten(), base.y_grid.flatten())
    trans.y_grid = trans.y_grid.reshape((base.ny,base.nx))
    trans.x_grid = trans.x_grid.reshape((base.ny,base.nx))

    return (trans, proj_epsg3413, proj_eigen_gl04c)
