# Licensed under a 3-clause BSD style license - see LICENSE

# Standard Library
from collections import Iterable
import re
import io 
import os

# 3rd Party
import numpy as np
import pandas as pd
import pandas.core
#vector quantization
import scipy.cluster.vq as vq

# Internal
from latbin.point_information import PointInformation
from latbin._six import isstr, pickle, range


__all__ = ["Lattice","ZLattice","DLattice","ALattice", "PointCloud",
           "generate_lattice","CompositeLattice","load_lattice","save_lattice"]

# ########################################################################### #

def load_lattice (filepath):
    """ Load a lattice from file
    
    Parameters
    ----------
    filepath : string, ends in '.lat'
        Gives the path to the save file

    Returns
    -------
    lattice : `latbin.Lattice` subclass

    """    
    return pickle.load(io.open(filepath,'r'))
    
def save_lattice (lattice,filepath,clobber=True):   
    """ Save a lattice to file
    
    Parameters
    ----------
    lattice : `latbin.Lattice` subclass
    filepath : string, ends in '.lat'
        Gives the path to the save file
    clobber : boolean
        If True and filepath is an existing file then it will be overwritten

    """
    if not filepath.count(".lat"):
        filepath += ".lat"
    if os.path.isfile(filepath):
        if clobber:
            os.remove(filepath)
        else:            
            raise IOError("File exists '{}'".format(filepath))
    if not isinstance(lattice,Lattice):
        raise TypeError("lattice must be a Lattice subclass")
    pickle.dump(lattice,io.open(filepath,'w'))  

pass
# ########################################################################### #

class LatticeImplementationError (NotImplementedError):
    """ This error is designed for lattice methods which have not been 
    implemented
    """
    pass

class Lattice (object):
    """ The abstract lattice class.
    
    If :math:`a_1,...,a_1` are linearly independent vectors in *m*-dimensional 
    real Euclidean space :math:`R^m` with :math:`m \geq n`, the set of all vectors
    
    .. math::
    
        x = u_n a_n + .... + u_n a_n
        
    where :math:`u_1,...,u_{n}` are arbitrary integers, is called an 
    *n*-dimensional *lattice* :math:`\Lambda`. [Conway1982]_
     
    """
    def __init__(self, ndim, origin, scale, rotation):
        """
        The abstract lattice class
        
        Parameters
        ----------
        ndim : integer
            The number of lattice dimensions
        origin : None or array-like of floats ndim long
            Gives the origin of the lattice
        scale : None, float, or array-like of floats ndim long
            Sets the scaling for which a spacing of 1 in lattice corresponds in 
            data space. None is assumed scaling of 1. A float will be cast to 
            all the dimensions. An array will be used to scale each dimension
            independently.
        rotation : array, shape=(ndim,ndim)
            Not currently implemented
        """        
        if ndim <= 0:
            raise ValueError("ndim must be > 0")
        self.ndim = ndim
        
        if origin is None:
            origin = np.zeros(ndim,dtype=float)
        self.origin = np.asarray(origin,dtype=float)
        if len(self.origin) != ndim or self.origin.ndim != 1:
            raise ValueError("origin must be a float vector of length={}".format(ndim))
        
        if scale is None:
            scale = np.ones(ndim,dtype=float)
        if isinstance(scale,Iterable):
            self.scale = np.asarray(scale,dtype=float)
        else:
            self.scale = np.ones(ndim,dtype=float)*scale
        if len(self.scale) != ndim or self.scale.ndim != 1:
            raise ValueError("scale must be a float or a float vector of length={}".format(ndim))
        
        if rotation is None:
            self.rotation = None
        else:
            self.rotation = np.asarray(rotation)
     
    def __delattr__ (self,attrib):
        """ del self.attrib ! not mutable """
        if hasattr(self, attrib):
            msg = "'{}' attribute is immutable in '{}'".format(attrib,repr(self))
        else:
            msg = "'{}' not an attribute of '{}'".format(attrib,repr(self))
        raise AttributeError(msg)  
    
    def __eq__ (self,other):
        """ self==other """
        if not type(other) == type(self):
            return False
        if other.ndim != self.ndim:
            return False
        if np.all(other.origin != self.origin):
            return False
        if np.all(other.scale != self.scale):
            return False
        return True
    
    def __ne__ (self,other):
        """ self!=other """
        equals = self.__eq__(other)
        return not equals
    
    def __setattr__ (self,attrib,value):
        """ self.attrib = value ! not mutable """
        if hasattr(self,attrib):
            msg = "'{}' attribute is immutable in '{}'".format(attrib,repr(self))
            raise AttributeError(msg)
        else:
            object.__setattr__(self,attrib,value)
    
    def __setitem__ (self,index,value):
        """ self[i]=value ! not mutable """
        raise TypeError("'{}' does not support item assignment".format(repr(self)))
    
    def bin(self, data, bin_cols=None, bin_prefix="q"):
        """bin a set of points into the Voronoi cells of this lattice
        
        This uses the `quantize` method to map the data points onto lattice
        coordinates. The mapped data points are gathered up based on the 
        the lattice coordinate representations.
        
        Parameters
        ----------
        data : ndarray, shape=(M,N)
            the data to bin 
            the length of the second dimension must match self.ndim
        bin_cols : list
            the indexes of the columns to be used in order to bin the data
        bin_prefix: string
            prefix for the lattice quantization columns used to bin on.
            
        Returns
        -------
        bin_nums: pandas.groupby
            
        """
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(np.asarray(data))
        if bin_cols == None:
            bin_cols = data.columns[:self.ndim]
        if len(bin_cols) != self.ndim:
            raise ValueError("bin_cols isn't long enough")
        #quantize
        q_pts = self.quantize(data[bin_cols].values)
        # make the quantized result a pandas data frame
        q_dict = {}
        for q_col_idx in range(q_pts.shape[1]):
            q_dict["%s_%d" % (bin_prefix, q_col_idx)] = q_pts[:, q_col_idx]
        q_df = pd.DataFrame(data=q_dict, index=data.index)
        joint_df = pd.concat([data, q_df], axis=1)
        grouped_df = joint_df.groupby(by=list(q_dict.keys()))
        return grouped_df
    
    def data_to_lattice_space (self,data_coords):
        """Transforms from the data coordinates to the internal lattice coordinates
        
        The internal representations of a particular lattice can have multiple
        representations. We've pick a particular one for this lattice and this
        function maps your data space to those coordinates.
        
        
        Parameters
        ----------
        data_coords: ndarray shape = (npoints, ndims)  or (ndims,)
            The points in data coordinates
        
        Returns
        -------
        lattice_coords : ndarray, shape=(npoints,*)
            The lattice representations of each data point
        
        """
        data_coords = np.asarray(data_coords)
        
        if data_coords.shape[-1] != self.ndim:
            raise ValueError("lattice_coords must be ndim={}".format(self.ndim))
        
        if data_coords.ndim == 1:
            dc = data_coords.reshape((1,)+data_coords.shape)
            lattice_coords = (dc-self.origin)/self.scale
        else:
            lattice_coords = (data_coords-self.origin)/self.scale
        
        return lattice_coords        
    
    def histogram(self, *args, **kwargs):
        return self.bin(*args, **kwargs).size()
    
    def lattice_to_data_space (self, lattice_coords):
        """Transforms from the internal lattice coordinates to the original 
        data coordinates.
        
        The internal representations of a particular lattice can have multiple
        representations. We've pick a particular one for this lattice and this
        function maps from those coordinates to your data space  
        
        Parameters
        ----------
        lattice_coords: ndarray, shape = (n_points, n_dims)  or (n_dims,)
        
        """
        lattice_coords = np.asarray(lattice_coords)
        
        if lattice_coords.shape[-1] != self.ndim:
            raise ValueError("lattice_coords must be ndim={}".format(self.ndim))
        
        if lattice_coords.ndim == 1:
            lc = lattice_coords.reshape((1,)+lattice_coords.shape)
            data_coords = self.scale*lc+self.origin
        else:
            data_coords = self.scale*lattice_coords+self.origin
        
        return data_coords        
    
    def minimal_vectors(self):
        """return a complete list of minimal norm of the vectors
        with minimal non-zero norm in the lattice.
        """
        raise NotImplementedError("Not implemented for this Lattice type.")
    
    @property
    def norm(self):
        raise NotImplementedError("Not implemented for this Lattice type")
    
    def quantize(self, points):
        """Takes points in the data space and quantizes to this lattice. 
        
        This takes the data and uses particular algorithms described in
        [Conway83]_ to take the data and quantize to the lattice points. Each 
        data point is mapped to the closest lattice point. This function 
        returns the lattice point in the space where the lattice can be 
        uniquely and easily represented.
        
        Parameters
        ----------
        points : ndarray, shape=(npoints,ndim)
        
        Returns
        -------
        representations : ndarray, shape=(npoints,*)
            These are the internal representations of lattice points for each
            data point which was given
        
        """
        raise LatticeImplementationError("Lattice isn't meant to be used this way see the generate_lattice helper function")
    
    def representation_to_centers(self, representations):
        """Takes internal lattice representations and returns corresponding data
        centers.
        
        The internal representations of a particular lattice can have multiple
        representations. We've pick a particular one for this lattice and this
        function maps the lattice point representations to the data space.
                
        Parameters
        ----------
        representations : ndarray, shape=(npoints,*)
        
        Returns
        -------
        centers : ndarray, shape=(npoints,ndim)
        
        """
        raise NotImplementedError("Lattice isn't meant to be used this way see the generate_lattice helper function")
            
class PointCloud (Lattice):
    """A representation of a finite set of points. While Technically not a 
    Lattice in the mathematical sense it implements the same API
    
    The quantization is done using scipy.cluster.vq algorithm.
    """
    
    def __init__ (self, point_coordinates, force_unique=True):
        """
        Parameters
        ---------
        point_coordinates : ndarray, size=(npoints , ndims) 
        force_unique : boolean
            Force the point coordinates to be unique
        
        """
        # check as an array
        points = np.asarray(point_coordinates)
        # if 1 dimensional add a dimension to
        if points.ndim == 1:
            points = points.reshape((len(points),1))
        # If you force unqiue data points
        if force_unique:
            unique = list({tuple(pt) for pt in points})
            points = np.array(unique)
        # sort the data points down the first axis
        points = np.sort(points)
        
        Lattice.__init__(self,points.shape[-1],origin=None,
                         scale=None,rotation=None)
        self.points = points
        object.__delattr__(self,'origin')
        object.__delattr__(self,'scale')
        object.__delattr__(self,'rotation')
    
    def data_to_lattice_space(self, data_coords):
        # TODO: This is very slow and memory intensive, need a better way!
        lattice_coords = []        
        for point in data_coords:
            lattice_coords.append(self.index(point))
        return np.array(lattice_coords).reshape((len(lattice_coords),1))
    
    data_to_lattice_space.__doc__ = Lattice.data_to_lattice_space.__doc__
   
    def lattice_to_data_space(self, lattice_coords):
        return self.points[np.asarray(lattice_coords,dtype=int)]
    
    lattice_to_data_space.__doc__ = Lattice.lattice_to_data_space.__doc__
    
    def quantize (self, points):
        """ Takes points and returns point set representation
        
        Parameters
        ----------
        points : ndarray, size=(n_points , n_dims)
            array of points to quantize
        
        Returns
        -------
        reps : list, length M
            a list of representations for each point in pts
            
        """
        vqres = vq.vq(np.asarray(points), self.points)        
        reps = vqres[0]
        if reps.ndim == 1:
            reps = reps.reshape((len(reps),1))
        return reps
        
    def count (self,point):
        """ Count number of times a point appears in self.points
        
        Parameters
        ----------
        points : ndarray
            Point in self.points
        
        Returns
        -------
        count : integer
            Number of times the point appears in lattice
        
        """
        check_pt = tuple(point)
        count = 0
        for pt in self.points:
            if tuple(pt) == check_pt:
                count += 1
        return count
    
    def index (self,point):
        """ Count number of times a point appears in self.points
        
        Parameters
        ----------
        points : ndarray
            Point in self.points
        
        Returns
        -------
        index : integer
            The first index where the point is found
        
        Raises
        ------
        ValueError : if point is not in PointCloud
        
        """
        check_pt = tuple(point)
        for i,pt in enumerate(self.points):
            if tuple(pt) == check_pt:
                return i
        raise ValueError("'{}' not in PointCloud".format(pt))
    
    def __eq__(self, other):
        """ self==other """
        is_equal = Lattice.__eq__(self, other)        
        if not is_equal:
            return False
        if not np.all(self.points == other.points):
            return False
        return True
      
class ZLattice (Lattice):
    """ The Z lattice is composed of n-dimensional integers. This is most 
    classically thought of as square binning.  
    
    """    
    def __init__ (self, ndim, origin=None, scale=None, rotation=None):
        Lattice.__init__(self, ndim, origin, scale, rotation)
    
    __init__.__doc__ = Lattice.__init__.__doc__

    def representation_to_centers(self, representations):
        return self.lattice_to_data_space(representations)
    
    representation_to_centers.__doc__ = Lattice.representation_to_centers.__doc__
    
    def minimal_vectors(self):
        out_vecs = np.empty((2*self.ndim, self.ndim), dtype=int)
        out_vecs[:self.ndim] = np.eye(self.ndim)
        out_vecs[self.ndim:] = -np.eye(self.ndim)
        return out_vecs
    
    minimal_vectors.__doc__ = Lattice.minimal_vectors.__doc__
    
    @property
    def norm(self):
        return 1.0
    
    def quantize (self,points):
        lspace_pts = self.data_to_lattice_space(points)
        return np.around(lspace_pts).astype(int)

    quantize.__doc__ = Lattice.quantize.__doc__

class DLattice (Lattice):
    """ The D lattice consists of integer coordinates with an even sum.
    """
    
    def __init__ (self, ndim, origin=None, scale=None, rotation=None):
        Lattice.__init__(self, ndim, origin, scale, rotation)
    
    __init__.__doc__ = Lattice.__init__.__doc__
    
    def minimal_vectors(self):
        out_vecs = []
        for i in range(self.ndim):
            for j in range(i, self.ndim):
                cvec = np.zeros(self.ndim, dtype=int)
                cvec[i] += 1
                cvec[j] += 1
                out_vecs.append(cvec)
                out_vecs.append(-cvec)
                if not i == j:
                    ncvec = cvec.copy()
                    ncvec[i] = -1
                    out_vecs.append(ncvec)
                    out_vecs.append(-ncvec)
        return np.array(out_vecs)
    
    minimal_vectors.__doc__ = Lattice.minimal_vectors.__doc__
    
    @property
    def norm(self):
        return np.sqrt(2.0)
    
    def quantize(self, points):
        lspace_pts = self.data_to_lattice_space(points)
        rounded_pts = np.around(lspace_pts)
        csum = np.sum(rounded_pts, axis=-1)
        cdiff = lspace_pts - rounded_pts
        abs_cdiff = np.abs(cdiff)
        delta_max_idxs = np.argmax(np.abs(cdiff), axis=-1)
        quantized_repr = np.array(rounded_pts, dtype=int)
        for i in range(len(quantized_repr)):
            if csum[i] % 2 == 1:
                max_idx = delta_max_idxs[i]
                if cdiff[i, max_idx] < 0:
                    #we rounded up round down instead
                    quantized_repr[i, max_idx] -= 1
                else:
                    quantized_repr[i, max_idx] += 1
        return quantized_repr
    
    quantize.__doc__ = Lattice.quantize.__doc__            
    
    def representation_to_centers(self, representations):
        return self.lattice_to_data_space(representations)
    
    representation_to_centers.__doc__ = Lattice.representation_to_centers.__doc__

class ALattice (Lattice):
    """The A Lattice consists of points $(x_{0},x_{1},\cdots,x_{n})$ having integer
    coordinates that sum to zero. $A_{2}$ is equivalent to the familiar 
    two-dimensional hexagonal (honeycomb) lattice.
    """
    def __init__ (self, ndim, origin=None, scale=None, rotation=None):
        Lattice.__init__(self, ndim, origin, scale, rotation)
        #set up a rotation matrix into the lattice coordinate space
        rot = np.zeros((ndim, ndim+1))
        for dim_idx in range(ndim):
            rot[dim_idx, :dim_idx+1] = 1
            rot[dim_idx, dim_idx+1] = -(dim_idx + 1)
        self._rot = rot/np.sqrt(np.sum(rot**2, axis=-1)).reshape((-1, 1))
        self._rot_inv = np.linalg.pinv(self._rot)
    
    __init__.__doc__ = Lattice.__init__.__doc__
    
    def data_to_lattice_space(self, points):
        points = super(ALattice, self).data_to_lattice_space(points)
        return np.dot(points, self._rot)
    
    data_to_lattice_space.__doc__ = Lattice.data_to_lattice_space.__doc__
    
    def lattice_to_data_space(self, points):
        unrot = np.dot(points, self._rot_inv)
        return super(ALattice, self).lattice_to_data_space(unrot)
    
    lattice_to_data_space.__doc__ = Lattice.lattice_to_data_space.__doc__
    
    def minimal_vectors(self, space="lattice"):
        out_vecs = np.zeros((self.ndim*(self.ndim+1), self.ndim+1), dtype=int)
        out_idx = 0
        for i in range(self.ndim+1):
            for j in range(self.ndim+1):
                if i == j:
                    continue
                out_vecs[out_idx, i] = 1
                out_vecs[out_idx, j] = -1
                out_idx +=1
        return out_vecs
    
    minimal_vectors.__doc__ = Lattice.minimal_vectors.__doc__
    
    @property
    def norm(self):
        return np.sqrt(2)
    
    def quantize(self, points):
        # take points to lattice space
        lspace_pts = self.data_to_lattice_space(points)
        lspace_dim = lspace_pts.shape[-1]
        # round to nearest integer
        rounded_pts = np.around(lspace_pts).astype(int)
        # calculate the deficiency in the rounding
        deficiency = np.sum(rounded_pts, axis=-1)
        cdiff = lspace_pts - rounded_pts
        permutations = np.argsort(cdiff,axis=-1)
        quantized_repr = rounded_pts
        
        for i in range(len(quantized_repr)):
            cdeff = deficiency[i]
            if cdeff == 0:
                continue
            elif cdeff > 0:
                for j in range(cdeff):
                    perm_idx = permutations[i, j]
                    quantized_repr[i, perm_idx] -= 1
            elif cdeff < 0:
                for j in range(-cdeff):
                    perm_idx = permutations[i, -1-j]
                    quantized_repr[i, perm_idx] += 1
        return quantized_repr
      
    quantize.__doc__ = Lattice.quantize.__doc__
    
    def representation_to_centers(self, representations):
        return self.lattice_to_data_space(representations)
    
    representation_to_centers.__doc__ = Lattice.representation_to_centers.__doc__

lattice_types = {'z':ZLattice,
                'd':DLattice,
                'a':ALattice,
                }

class CompositeLattice (Lattice):
    """ This lattice is composed of a list of separate lattices
    
    """
    
    def __init__ (self, lattices, column_idx=None, origin=None, scale=None, rotation=None):
        """Create a composite of lattices
        
        A composite lattice contains several lattices stacked together. For 
        example if you have 10 dimensions and you want to break some of them
        up you could make a composite lattice A2,A2,Z4,D2 whose total ndim 
        equals the number of dimensions. 
        
        Parameters
        ----------
        lattices : string or list of lattices
            The lattices must be a either ZLattice, DLattice, or ALattice
            the total dimension is assumed from the sum of each lattice dimension. 
            Optionally, you can give a string for lattices such as "a2,z2,d3" which 
            becomes [ALattice(2), ZLattice(2), DLattice(3)] with total dimension 7
        column_idx : list of integer lists
            Maps data columns to specific lattices. See Note 1
        origin : array-like
        scale : array-like
        rotation : array-like
            *Currently not implemented*
        
        Notes
        -----
        __1.__ column_idx maps data columns to specific lattices. Say you have a 
        composite lattice consisting of A2, Z2 and D3 and data which has the shape
        (1000,10). Because the composite is only dimension 7 you can only bin
        in 7 of the 10 data dimensions. You can specify which 7 columns are mapped
        to which lattices. Continuing the example, say [0,1] columns to A2, [2,5] 
        to Z2, and 6,7,9 to D3 then you would give:
        
        column_idx = [[0,1],
                      [2,5],
                      [6,7,9]]
        
        The i-th element of column_idx corresponds to the i-th lattice of lattices
        and it's length equals the value of lattice.ndim
        
        You can use `None` in column_idx once to create a default lattice for 
        columns to be placed in. Say data is (1000,5) and composite lattice is 
        (A2,Z3). If you wanted the [2,4] columns in A2 and all the others in Z 
        then you can use:
        
        column_idx = [[2,4], = [[2,4],
                      None]     [0,1,3]]
        
        
        """
        
        # get lattices
        if isstr(lattices):
            lat_dims = []
            lattice_structs = []
            for latstr in lattices.split(","):
                search_result = re.search("([a,d,z]).*(\d)",latstr.lower())
                if search_result is None:
                    raise ValueError("Couldn't parse lattice {} from lattices string".format(latstr))
                lat_type = search_result.groups()[0]
                try:
                    lat_dim = int(search_result.groups()[1])
                except ValueError:
                    raise ValueError("Must give letter then dimension")
                lat_dims.append(lat_dim)
                lattice_structs.append(lattice_types[lat_type](lat_dim))
            self.lat_dims = lat_dims
            self.lattices = lattice_structs
        else:
            self.lat_dims = [lat.ndim for lat in lattices]
            self.lattices = lattices 

        ndim = np.sum(self.lat_dims)        
        
        # get the index mapping
        if column_idx is None:
            current_i = 0
            column_idx = []
            for ldim in self.lat_dims:
                column_idx.append(list(range(current_i,current_i+ldim)))
                current_i += ldim
            
        column_idx = list(column_idx)
        if len(column_idx) != len(self.lattices):
            raise ValueError("column_idx must have the same length as given lattices")

        used_idxs = set()            
        none_idx = -1
        for i,row in enumerate(column_idx):
            if row is None:
                if none_idx >= 0:
                    raise ValueError("can only have one None (aka default) in column_idx")
                none_idx = i
                continue
            
            if len(row) != self.lat_dims[i]:
                raise ValueError("the number of indicies in column_idx[i]={} must match lattice dimension = {} ".format(len(row),self.lat_dims[i]))
            
            used_idxs = used_idxs.union(set(map(int,row)))
        
        if none_idx >= 0:
            unused_idxs = set(range(ndim)) - used_idxs
            if len(unused_idxs) != self.lat_dims[none_idx]:
                raise ValueError("number of unused indicies does not match default lattice dimension")
            column_idx[none_idx] = sorted(list(unused_idxs))

        for i,idx in enumerate(column_idx):
            column_idx[i] = np.asarray(idx,dtype=int)

        self.column_idx = column_idx
        Lattice.__init__(self,ndim,origin,scale,rotation)

    def lattice_to_data_space(self, lattice_coords):
        return Lattice.lattice_to_data_space(self, lattice_coords)
    
    lattice_to_data_space.__doc__ = Lattice.lattice_to_data_space.__doc__
    
    def data_to_lattice_space(self, data_coords):        
        lattice_coords_list = []
        arrays = self.map_data_to_lattice(data_coords)  
        lat_coords_list = [self.lattices[i].data_to_lattice_space(arrays[i]) for i in range(len(arrays))]
        return Lattice.data_to_lattice_space(self, data_coords)

    data_to_lattice_space.__doc__ = Lattice.data_to_lattice_space.__doc__

    def quantize(self, points): 
        #    return ndarray shape (npts,self.ndim)
        LatticeImplementationError("can't yet quantize composite lattices")

    quantize.__doc__ = Lattice.quantize.__doc__
    
    def representation_to_centers(self, representations):
        LatticeImplementationError()
        Lattice.representation_to_centers(self, representations)

    representation_to_centers.__doc__ = Lattice.representation_to_centers.__doc__

    def map_data_to_lattice (self,points):
        """still beta"""
        arrays = [points[:,idx] for idx in self.column_idx]
        return arrays

    def __eq__ (self,other):
        """ self == other """
        if not isinstance(other, CompositeLattice):
            return False
        if not len(self.lattices) == len(other.lattices):
            return False
        if self.lat_dims != other.lat_dims:
            return False
        #print(self.column_idx)
        #print(other.column_idx)
        for ci1, ci2 in zip(self.column_idx, other.column_idx):
            if not np.all(ci1 == ci2):
                return False
        for i,lat in enumerate(self.lattices):
            if lat != other.lattices[i]:
                return False 
        return True          
                     
pass
# ########################################################################### #

def generate_lattice (ndim, origin=None, scale=None, largest_dim_errors=None,
                      lattice_type="", packing_radius=1.0):    
    
    # ===================== get lattice class
    lattice_type = lattice_type.lower() 
    if lattice_type in ('packing','covering'):
        # ------------------- 
        if ndim == 1:
            # gives both packing and covering
            lattice_type = 'z'
        # ------------------- 
        elif ndim == 2:
            # gives both packing and covering            
            lattice_type = 'a'
        # ------------------- 
        elif ndim == 3:
            # gives packing (a) and covering (a*)            
            lattice_type = 'a'
        # ------------------- 
        elif ndim == 4:
            if lattice_type == 'packing':
                lattice_type = 'd'
            elif lattice_type == 'covering':
                lattice_type = 'a' # (a*)
        # ------------------- 
        elif ndim == 5:
            if lattice_type == 'packing':
                lattice_type = 'd'
            elif lattice_type == 'covering':
                lattice_type = 'a' # (a*)
        # ------------------- 
        elif ndim == 6:
            if lattice_type == 'packing':
                LatticeImplementationError("e6 not implemented yet")
                lattice_type = 'e6'
            elif lattice_type == 'covering':
                lattice_type = 'a' # (a*)
        # ------------------- 
        elif ndim == 7:
            if lattice_type == 'packing':
                LatticeImplementationError("e7 not implemented yet")
                lattice_type = 'e7'
            elif lattice_type == 'covering':
                lattice_type = 'a' # (a*)
        # ------------------- 
        elif ndim == 8:
            if lattice_type == 'packing':
                LatticeImplementationError("e8 not implemented yet")
                lattice_type = 'e8'
            elif lattice_type == 'covering':
                lattice_type = 'a' # (a*)
        # ------------------- 
        elif ndim == 12:
            if lattice_type == 'packing':
                LatticeImplementationError("k12 not implemented yet")
                lattice_type = 'k12'
            elif lattice_type == 'covering':
                lattice_type = 'a' # (a*)
        # ------------------- 
        elif ndim in (16,24):
            if lattice_type == 'packing':
                LatticeImplementationError("not planning to implement lambda16 or 24 lattices")                
            elif lattice_type == 'covering':
                lattice_type = 'a' # (a*) 
        else:
            lattice_type = 'a'
            
    if lattice_type not in lattice_types:
        raise ValueError("lattice_type must be in ({}), see NOTE1 in doc string".format(", ".join(list(lattice_types.keys()))))
    latclass = lattice_types[lattice_type] 
    
    # ===================== get scale
    if scale == None:
        scale = 1.0
    scale /= packing_radius
    largest_dim_errors # ndarray, which gives the desired largest errors in each dimension
    
    # ===================== get origin
    
    
    # ===================== get rotation
    rotation = None
    
    # ===================== create lattice
    lat = latclass(ndim, origin, scale, rotation) 
    
    return lat

generate_lattice.__doc__ =     """ Function for getting a lattice object based on input parameters
    
    Parameters
    ----------
    ndim : integer
        Number of dimensions
    origin : array-like of floats, shape=(ndim,)
        1D array-like object which gives the origin of lattice in ndim
    scale : float or array-like of floats, shape=(ndim,)
        If a float then cast to an 1D array of length ndim. The 1D array is used to scale the data space
    lattice_type : 'covering', 'packing', 'z', 'd', 'a'
        Gives the family of lattices to generate. See NOTES1.
        * 'covering' : thinnest covering, take point packing expand spheres until they cover all the points. thickness=sum(sphere_volume)/total_volum 
        * 'packing' : tightest packing, get the points as close as possible
        * 'z' : ZLattice
        * 'd' : DLattice
        * 'a' : ALattice
    
    packing_radius : float (optional)
        This is used to modify the scale. scale \= packing_radius
        
    Returns
    -------
    Lattice : {0}
        Depending on family, this returns a lattice object
    
    
    Notes
    -----
    __1)__ Families of lattices are defined TODO: finish
        * ALattice : ndim=2 is a hexbin lattice
    
    """.format(", ".join([val.__name__ for val in lattice_types.values()]))

    
    
