# -*- coding: utf-8 -*-
#
# CLASSIX: Fast and explainable clustering based on sorting
#
# MIT License
#
# Copyright (c) 2023 Stefan Güttel, Xinye Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import warnings

import os
import copy

import numpy as np
import pandas as pd
from numpy.linalg import norm


def cython_is_available(verbose=0):
    "Check if CLASSIX is using cython."
    
    __cython_type__ = "memoryview"
    
    from . import __enable_cython__
    if __enable_cython__:
        try:
            # %load_ext Cython
            # !python3 setup.py build_ext --inplace
            import numpy
            
            try:
                from .aggregation_cm import aggregate
                from .merging_cm import density_merging, distance_merging
                # cython with memoryviews
                # Typed memoryviews allow efficient access to memory buffers, such as those underlying NumPy arrays, without incurring any Python overhead. 
            
            except ModuleNotFoundError:
                from .aggregation_c import aggregate, precompute_aggregate, precompute_aggregate_pca
                
                __cython_type__ =  "trivial"

            if verbose:
                if __cython_type__ == "memoryview":
                    print("This CLASSIX is using Cython typed memoryviews.")
                else:
                    print("This CLASSIX is not using Cython typed memoryviews.")
            
            return True

        except (ModuleNotFoundError, ValueError):
            if verbose:
                print("This CLASSIX is not using Cython.")
            return False
    else:
        if verbose:
            print("Currently, the Cython implementation is disabled. Please try to set ``__enable_cython__`` to True to enable Cython if needed.")
        return False
    
    
    
def loadData(name='vdu_signals'):
    """Obtain the built-in data.
    
    Parameters
    ----------
    name: str, {'vdu_signals', 'Iris', 'Dermatology', 'Ecoli', 'Glass', 'Banknote', 'Seeds', 'Phoneme', 'Wine'}, default='vdu_signals'
        The support build-in datasets for CLASSIX.

    Returns
    -------
    X, y: numpy.ndarray
        Data and ground-truth labels.    
    """
    
    current_dir, current_filename = os.path.split(__file__)
    
    if not os.path.isdir(os.path.join(current_dir, 'data')):
        os.mkdir(os.path.join(current_dir, 'data/'))
        
    if name == 'vdu_signals':
        DATA_PATH = os.path.join(current_dir, 'data/vdu_signals.npy')
        if not os.path.isfile(DATA_PATH):
            get_data(current_dir)
        return np.load(DATA_PATH)
    
    if name == 'Iris':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Irirs.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Irirs.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Iris')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name == 'Dermatology':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Dermatology.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Dermatology.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Dermatology')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name == 'Ecoli':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Ecoli.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Ecoli.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Ecoli')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name == 'Glass':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Glass.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Glass.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Glass')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name == 'Banknote':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Banknote.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Banknote.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Banknote')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name == 'Seeds':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Seeds.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Seeds.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Seeds')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name == 'Phoneme':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Phoneme.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Phoneme.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Phoneme')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name == 'Wine':
        DATA_PATH_X = os.path.join(current_dir, 'data/X_Wine.npy')
        DATA_PATH_Y = os.path.join(current_dir, 'data/y_Wine.npy')
        if not os.path.isfile(DATA_PATH_X) or not os.path.isfile(DATA_PATH_Y):
            get_data(current_dir, 'Wine')
        return np.load(DATA_PATH_X), np.load(DATA_PATH_Y)
    
    if name not in ['vdu_signals', 'Iris', 'Dermatology', 'Ecoli', 'Glass', 'Banknote', 'Seeds', 'Phoneme', 'Wine']:
        warnings.warn("Currently not support this data.")


        

def get_data(current_dir='', name='vdu_signals'):
    """Download the built-in data."""
    import requests
    
    if name == 'vdu_signals':
        url_parent = "https://github.com/nla-group/classix/raw/master/classix/source/vdu_signals.npy"
        vdu_signals = requests.get(url_parent).content
        with open(os.path.join(current_dir, 'data/vdu_signals.npy'), 'wb') as handler:
            handler.write(vdu_signals)
         
    elif name == 'Iris':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Irirs.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Irirs.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Irirs.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Irirs.npy'), 'wb') as handler:
            handler.write(y)
            
    elif name == 'Dermatology':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Dermatology.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Dermatology.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Dermatology.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Dermatology.npy'), 'wb') as handler:
            handler.write(y)
    
    elif name == 'Ecoli':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Ecoli.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Ecoli.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Ecoli.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Ecoli.npy'), 'wb') as handler:
            handler.write(y)
    
    elif name == 'Glass':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Glass.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Glass.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Glass.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Glass.npy'), 'wb') as handler:
            handler.write(y)
    
    elif name == 'Banknote':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Banknote.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Banknote.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Banknote.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Banknote.npy'), 'wb') as handler:
            handler.write(y)
    
    elif name == 'Seeds':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Seeds.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Seeds.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Seeds.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Seeds.npy'), 'wb') as handler:
            handler.write(y)
            
    elif name == 'Phoneme':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Phoneme.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Phoneme.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Phoneme.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Phoneme.npy'), 'wb') as handler:
            handler.write(y)
    
    elif name == 'Wine':
        url_parent_x = "https://github.com/nla-group/classix/raw/master/classix/source/X_Wine.npy"
        url_parent_y = "https://github.com/nla-group/classix/raw/master/classix/source/y_Wine.npy"
        x = requests.get(url_parent_x).content
        y = requests.get(url_parent_y).content
        with open(os.path.join(current_dir, 'data/X_Wine.npy'), 'wb') as handler:
            handler.write(x)
        with open(os.path.join(current_dir, 'data/y_Wine.npy'), 'wb') as handler:
            handler.write(y)
                    

                    




# ******************************************** the main wrapper ********************************************
class CLASSIX:
    """CLASSIX: Fast and explainable clustering based on sorting.
    
    The user only need to concern the hyperparameters of ``sorting``, ``radius``, and ``minPts`` in the most cases.
    If want a flexible clustering, might consider other hyperparameters such as ``group_merging``, ``scale``, and ``post_alloc``.
    
    Parameters
    ----------
    sorting : str, {'pca', 'norm-mean', 'norm-orthant', None}，default='pca'
        Sorting method used for the aggregation phase.
        
        - 'pca': sort data points by their first principal component
        
        - 'norm-mean': shift data to have zero mean and then sort by 2-norm values
        
        - 'norm-orthant': shift data to positive orthant and then sort by 2-norm values
        
        - None: aggregate the raw data without any sorting

        
    radius : float, default=0.5
        Tolerance to control the aggregation. If the distance between a starting point 
        and an object is less than or equal to the tolerance, the object will be allocated 
        to the group which the starting point belongs to. For details, we refer users to [1].

    
    group_merging : str, {'density', 'distance', None}, default='distance'
        The method for merging the groups. 
        
        - 'density': two groups are merged if the density of data points in their intersection 
           is at least as high the smaller density of both groups. This option uses the disjoint 
           set structure to speedup merging.
        
        - 'distance': two groups are merged if the distance of their starting points is at 
           most scale*radius (the parameter above). This option uses the disjoint 
           set structure to speedup merging.
        
        For more details, we refer to [1].
        If the users set group_merging to None, the clustering will only return the labels formed by aggregation as cluster labels.

    
    minPts : int, default=0
        Clusters with less than minPts points are classified as abnormal clusters.  
        The data points in an abnormal cluster will be redistributed to the nearest normal cluster. 
        When set to 0, no redistribution is performed. 

    
    norm : boolean, default=True
        If normalize the data associated with the sorting, default as True. 
        
    scale : float
        Design for distance-clustering, when distance between the two starting points 
        associated with two distinct groups smaller than scale*radius, then the two groups merge.

    post_alloc : boolean, default=True
        If allocate the outliers to the closest groups, hence the corresponding clusters. 
        If False, all outliers will be labeled as -1.

    mergeTinyGroups : boolean, default=True
        If it is False, then group merging will ignore all groups with <minPts points, otherwise not.
    
    algorithm : str, default='bf'
        Algorithm to merge connected groups.

        - 'bf': Use brute force routines to speed up the merging of connected groups.
        
        - 'set': Use disjoint set structure to merge connected groups.

    memory: bool, default=True
        If cython memoryviews is disable, a fast algorithm with less efficient momory comsuming is triggered
          since precomputation for aggregation is used. 
        Setting it True will use a memory efficient computing.  
        If cython memoryviews is effective, thie parameter can be ignored. 

    verbose : boolean or int, default=1
        Whether print the logs or not.
             
             
    Attributes
    ----------
    groups_ : list
        Groups labels of aggregation.
    
    splist_ : numpy.ndarray
        List of starting points formed in the aggregation.
        
    labels_ : numpy.ndarray
        Clustering class labels for data objects 

    group_outliers_ : numpy.ndarray
        Indices of outliers (aggregation groups level), 
        i.e., indices of abnormal groups within the clusters with fewer 
        data points than minPts points.
        
    clean_index_ : numpy.ndarray
        The data without outliers. Given data X,  the data without outliers 
        can be exported by X_clean = X[classix.clean_index_,:] while the outliers can be exported by 
        Outliers = X[~classix.clean_index_,:] 
        
    connected_pairs_ : list
        List for connected group labels.


    Methods
    ----------
    fit(data):
        Cluster data while the parameters of the model will be saved. The labels can be extracted by calling ``self.labels_``.
        
    fit_transform(data):
        Cluster data and return labels. The labels can also be extracted by calling ``self.labels_``.
        
    predict(data):
        After clustering the in-sample data, predict the out-sample data.
        Data will be allocated to the clusters with the nearest starting point in the stage of aggregation. Default values.

    gc2ind(spid):
        Return the group center (i.e., starting point) location in the data.
        
    explain(index1, index2, ...): 
        Explain the computed clustering. 
        The indices index1 and index2 are optional parameters (int) corresponding to the 
        indices of the data points. 
        
    References
    ----------
    [1] X. Chen and S. Güttel. Fast and explainable sorted based clustering, 2022
    """
        
    def __init__(self, sorting="pca", radius=0.5, minPts=0, group_merging="distance", norm=True, scale=1.5, post_alloc=True, mergeTinyGroups=True,
                 memory=False, verbose=1): 


        self.verbose = verbose
        self.minPts = minPts

        self.sorting = sorting
        self.radius = radius
        self.group_merging = group_merging
        self.sp_to_c_info = False # combine with visualization and data analysis, ensure call PCA and form groups information table only once

        self.centers = None
        self.norm = norm # usually, we do not use this parameter
        self.scale = scale # For distance measure, usually, we do not use this parameter
        self.post_alloc = post_alloc
        self.mergeTinyGroups = mergeTinyGroups

        self.sp_info = None
        self.groups_ = None
        self.clean_index_ = None
        self.labels_ = None
        self.connected_pairs_ = None
        self.connected_paths = None
        self.half_nrm2 = None
        self.inverse_ind = None
        self.label_change = None

        if self.verbose:
            print(self)
        
        self.splist_indices = [None]
        self.index_data = []
        self.memory = memory

        from . import __enable_cython__
        self.__enable_cython__ = __enable_cython__
        self.__enable_aggregation_cython__ = False
        
        if self.__enable_cython__:
            try:
                try:
                    from .aggregation_cm import aggregate
                    from .aggregation_cm import aggregate as precompute_aggregate, precompute_aggregate_pca
                    
                except ModuleNotFoundError:
                    from .aggregation_c import aggregate, precompute_aggregate, precompute_aggregate_pca 
                
                self.__enable_aggregation_cython__ = True

                import platform
                
                if platform.system() == 'Windows':
                    from .merging_cm_win import density_merging, distance_merging, distance_merging_mtg
                else:
                    from .merging_cm import density_merging, distance_merging, distance_merging_mtg

            except (ModuleNotFoundError, ValueError):
                if not self.__enable_aggregation_cython__:
                    from .aggregation import aggregate, precompute_aggregate, precompute_aggregate_pca
                
                from .merging import density_merging, distance_merging, distance_merging_mtg
                warnings.warn("This CLASSIX installation is not using Cython.")

        else:
            from .aggregation import aggregate, precompute_aggregate, precompute_aggregate_pca
            from .merging import density_merging, distance_merging, distance_merging_mtg
            warnings.warn("This run of CLASSIX is not using Cython.")

        if not self.memory:
            if sorting == 'pca':
                self._aggregate = precompute_aggregate_pca
            else:
                self._aggregate = precompute_aggregate
            
        else:
            self._aggregate = aggregate

        self._density_merging = density_merging
        
        if self.mergeTinyGroups:
            self._distance_merging = distance_merging
        else:
            self._distance_merging = distance_merging_mtg

            
    def fit(self, data):
        """ 
        Cluster the data and return the associated cluster labels. 
        
        Parameters
        ----------
        data : numpy.ndarray
            The ndarray-like input of shape (n_samples,)
        
            
        """
        if isinstance(data, pd.core.frame.DataFrame):
            self.index_data = data.index
            
        if not isinstance(data, np.ndarray):
            data = np.array(data)
            if len(data.shape) == 1:
                data = data.reshape(-1,1)
                
        if data.dtype !=  'float64':
            data = data.astype('float64')
            
        if self.sorting == "norm-mean":
            self._mu = data.mean(axis=0)
            self.data = data - self._mu
            self._scl = self.data.std()
            if self._scl == 0: # prevent zero-division
                self._scl = 1
            self.data = self.data / self._scl
        
        elif self.sorting == "pca":
            self._mu = data.mean(axis=0)
            self.data = data - self._mu # mean center
            rds = norm(self.data, axis=1) # distance of each data point from 0
            self._scl = np.median(rds) # 50% of data points are within that radius
            if self._scl == 0: # prevent zero-division
                self._scl = 1
            self.data = self.data / self._scl # now 50% of data are in unit ball 
            
        elif self.sorting == "norm-orthant":
            self._mu = data.min(axis=0)
            self.data = data - self._mu
            self._scl = self.data.std()
            if self._scl == 0: # prevent zero-division
                self._scl = 1
            self.data = self.data / self._scl
            
        else:
            self._mu, self._scl = 0, 1 # no normalization
            self.data = (data - self._mu) / self._scl
        
        # aggregation
        if not self.memory:
            self.groups_, self.splist_, self.dist_nr, self.ind, sort_vals, self.data, self.half_nrm2 = self._aggregate(data=self.data,
                                                                                                    sorting=self.sorting, 
                                                                                                    tol=self.radius
                                                                                                ) 
        else:
            self.groups_, self.splist_, self.dist_nr, self.ind, sort_vals, self.data = self._aggregate(data=self.data,
                                                                                                sorting=self.sorting, 
                                                                                                tol=self.radius
                                                                                            ) 
        self.splist_ = np.array(self.splist_)
        
        if self.group_merging is None:
            self.labels_ = copy.deepcopy(self.groups_) 
        
        elif self.group_merging.lower()=='none':
            self.labels_ = copy.deepcopy(self.groups_) 
        
        else:
            self.labels_ = self.merging(
                data=self.data,
                agg_labels=self.groups_, 
                splist=self.splist_,  
                ind=self.ind, sort_vals=sort_vals, 
                radius=self.radius, 
                method=self.group_merging, 
                minPts=self.minPts
            ) 

        return self


        
    def fit_transform(self, data):
        """ 
        Cluster the data and return the associated cluster labels. 
        
        Parameters
        ----------
        data : numpy.ndarray
            The ndarray-like input of shape (n_samples,)
        
        Returns
        -------
        labels : numpy.ndarray
            Index of the cluster each sample belongs to.
            
        """
        
        return self.fit(data).labels_
        
        
        
    def predict(self, data, memory=False):
        """
        Allocate the data to their nearest clusters.
        
        - data : numpy.ndarray
            The ndarray-like input of shape (n_samples,)

        - memory : bool, default=False
        
            - True: default, use precomputation is triggered to speedup the query

            - False: a memory efficient way to perform query 

        Returns
        -------
        labels : numpy.ndarray
            The predicted clustering labels.
        """
        labels = list()

        data = (np.asarray(data) - self._mu) / self._scl
        indices = self.splist_[:,0].astype(int)
        splist = data[indices]
        num_of_points = data.shape[0]

        if self.label_change is None:
            if self.inverse_ind is None:
                self.inverse_ind = np.argsort(self.ind)
                groups = np.array(self.groups_)
            self.label_change = dict(zip(groups[self.inverse_ind].ravel(), self.labels_)) # how object change group to cluster.

        if not memory:
            xxt = np.einsum('ij,ij->i', splist, splist)
            for i in range(num_of_points):
                splabel = np.argmin(euclid(xxt, splist, data[i]))
                labels.append(self.label_change[splabel])

        else:
            for i in range(num_of_points):
                splabel = np.argmin(np.linalg.norm(splist - data[i], axis=1, ord=2))
                labels.append(self.label_change[splabel])

        return labels
    
    
    
    def merging(self, data, agg_labels, splist, ind, sort_vals, radius=0.5, method="distance", minPts=0):
        """
        Merge groups after aggregation. 

        Parameters
        ----------
        data : numpy.ndarray
            The input that is array-like of shape (n_samples,).
        
        agg_labels: list
            Groups labels of aggregation.
        
        splist: numpy.ndarray
            List formed in the aggregation storing starting points.
        
        ind : numpy.ndarray
            Sort values.

        radius : float, default=0.5
            Tolerance to control the aggregation hence the whole clustering process. For aggregation, 
            if the distance between a starting point and an object is less than or equal to the tolerance, 
            the object will be allocated to the group which the starting point belongs to. 
        
        method : str
            The method for groups merging, 
            default='distance', other options: 'density', 'mst-distance', and 'scc-distance'.

        minPts : int, default=0
            The threshold, in the range of [0, infity] to determine the noise degree.
            When assgin it 0, algorithm won't check noises.

        algorithm : str, default='bf'
            Algorithm to merge connected groups.
 
            - 'bf': Use bruteforce routines to speed up the merging of connected groups.

            - 'set': Use disjoint set structure to merge connected groups.


        Returns
        -------
        centers : numpy.ndarray
            The return centers of clusters
        
        clabels : numpy.ndarray 
            The clusters labels of the data
        """
        
        import collections
        if self.memory: self.half_nrm2 = norm(data, axis=1, ord=2)**2 * 0.5 # precomputation

        if method == 'density':
            agg_labels = np.asarray(agg_labels)
            labels = copy.deepcopy(agg_labels) 
            self.merge_groups, self.connected_pairs_ = self._density_merging(data, splist, 
                                                                             radius, sort_vals=sort_vals, 
                                                                             half_nrm2=self.half_nrm2)
            maxid = max(labels) + 1
            
            # after this step, the connected pairs (groups) will be transformed into merged clusters, 
            for sublabels in self.merge_groups: # some of aggregated groups might be independent which are not included in self.merge_groups
                # not labels[sublabels] = maxid !!!
                for j in sublabels:
                    labels[labels == j] = maxid
                maxid = maxid + 1
            
            # but the existent clusters may have some very independent clusters which are possibly be "noise" clusters.
            # so the next step is extracting the clusters with very rare number of objects as potential "noises".
            # we calculate the percentiles of the number of clusters objects. For example, given the dataset size of 100,
            # there are 4 clusters, the associated number of objects inside clusters are repectively of 5, 20, 25, 50. 
            # The 10th percentlie (we set percent=10, noise_scale=0.1) of (5, 20, 25, 50) is 14, 
            # and we calculate threshold = 100 * noise_scale =  10. Obviously, the first cluster with number of objects 5
            # satisfies both condition 5 < 14 and 5 < 10, so we classify the objects inside first cluster as outlier.
            # And then we allocate the objects inside the outlier cluster into other closest cluster.
            # This method is quite effective at solving the noise arise from small tolerance (radius).
            
            self.old_cluster_count = collections.Counter(labels)
            
            if minPts >= 1:
                potential_noise_labels = self.outlier_filter(min_samples=minPts) # calculate the min_samples directly
                SIZE_NOISE_LABELS = len(potential_noise_labels) 
                if SIZE_NOISE_LABELS == len(np.unique(labels)):
                    warnings.warn(
                        "Setting of noise related parameters is not correct, degenerate to the method without noises dectection.", 
                    DeprecationWarning)
                else:
                    for i in np.unique(potential_noise_labels):
                        labels[labels == i] = maxid # marked as noises, 
                                                    # the label number is not included in any of existing labels (maxid).
            else:
                potential_noise_labels = list()
                SIZE_NOISE_LABELS = 0

            # remove noise cluster, avoid connecting two separate to a single cluster
            # the label with the maxid is label marked noises
            
            if SIZE_NOISE_LABELS > 0:
                
                self.clean_index_ = labels != maxid
                agln = agg_labels[self.clean_index_]
                self.label_change = dict(zip(agln, labels[self.clean_index_])) # how object change group to cluster.
                # allocate the outliers to the corresponding closest cluster.
                
                self.group_outliers_ = np.unique(agg_labels[~self.clean_index_]) # abnormal groups
                unique_agln = np.unique(agln)
                splist_clean = splist[unique_agln]

                if self.post_alloc:
                    for nsp in self.group_outliers_:
                        alloc_class = np.argmin(
                            np.linalg.norm(data[splist_clean[:, 0].astype(int)] - data[int(splist[nsp, 0])], axis=1, ord=2)
                            )
                        
                        labels[agg_labels == nsp] = self.label_change[unique_agln[alloc_class]]
                else:
                    labels[np.isin(agg_labels, self.group_outliers_)] = -1
                
            labels = self.reassign_labels(labels) 

        else:
            
            labels, self.old_cluster_count, SIZE_NOISE_LABELS = self._distance_merging(data=data, 
                                                                    labels=agg_labels,
                                                                    splist=splist,
                                                                    radius=radius,
                                                                    minPts=minPts,
                                                                    scale=self.scale, 
                                                                    sort_vals=sort_vals,
                                                                    half_nrm2=self.half_nrm2
                                                                )
            



        labels = labels[np.argsort(ind)]

        if self.verbose == 1:
            print("""CLASSIX aggregated the {datalen} data points into {num_group} groups. """.format(datalen=len(data), num_group=splist.shape[0]))
            print("""In total, {dist:.0f} distances were computed ({avg:.1f} per data point). """.format(dist=self.dist_nr, avg=self.dist_nr/len(data)))
            print("""The {num_group} groups were merged into {c_size} clusters with sizes: """.format(
                num_group=splist.shape[0], c_size=len(self.old_cluster_count)))

            
            self.pprint_format(self.old_cluster_count)

            if self.minPts > 1 and SIZE_NOISE_LABELS > 0:
                print("As minPts is {minPts}, the number of clusters has been reduced to {r}.".format(
                    minPts=self.minPts, r=len(np.unique(labels))
                ))
                
            print("Try the .explain() method to explain the clustering.")

        return labels 
    
    
    def explain(self, index1=None, index2=None, showalldata=False, showallgroups=False, showsplist=False, max_colwidth=None, replace_name=None, 
                plot=False, figsize=(10, 7), figstyle="default", savefig=False, bcolor="#f5f9f9", obj_color="k", width=1.5,  obj_msize=160, sp_fcolor="tomato",
                sp_marker="+", sp_size=72, sp_mcolor="k", sp_alpha=0.05, sp_pad=0.5, sp_fontsize=10, sp_bbox=None, sp_cmarker="+", sp_csize=110, 
                sp_ccolor="crimson", sp_clinewidths=2.7,  dp_fcolor="bisque", dp_alpha=0.3, dp_pad=2, dp_fontsize=10, dp_bbox=None,  show_all_grp_circle=False,
                show_connected_grp_circle=False, show_obj_grp_circle=True,  color="red", connect_color="green", alpha=0.5, cline_width=2,  add_arrow=True, 
                arrow_linestyle="--", arrow_fc="darkslategrey", arrow_ec="k", arrow_linewidth=1,
                arrow_shrinkA=2, arrow_shrinkB=2, directed_arrow=0, axis='off', figname=None, fmt="pdf"):
        
        """
        'self.explain(object/index) # prints an explanation for why a point object1 is in its cluster (or an outlier)
        'self.explain(object1/index1, object2/index2) # prints an explanation why object1 and object2 are either in the same or distinct clusters

        
        Here we unify the terminology:
            [-] data points
            [-] groups (made up of data points, formed by aggregation)
            [-] clusters (made up of groups)
        
        
        Parameters
        ----------
        index1 : int or numpy.ndarray, optional
            Input object1 [with index 'index1'] for explanation.
        
        index2 : int or numpy.ndarray, optional
            Input object2 [with index 'index2'] for explanation, and compare objects [with indices 'index1' and 'index2'].
        
        showalldata : boolean, default=False
            Whether or not to show all data points in global view when too many data points for plot.

        showallgroups : boolean, default=False
            Whether or not to show the start points marker.

        showsplist : boolean, default=False
            Whether or not to show the starting points information, which include the number of data points (NumPts), 
            corresponding clusters, and associated coordinates. This only applies to both index1 and index2 are "NULL".
            Default as True. 
        
        max_colwidth : int, optional
            Max width to truncate each column in characters. By default, no limit.
            
        replace_name : str or list, optional
            Replace the index with name. 
            * For example: as for indices 1 and 1300 we have 
            
            ``classix.explain(1, 1300, plot=False, figstyle="seaborn") # or classix.explain(obj1, obj4)``
            
            The data point 1 is in group 9 and the data point 1300 is in group 8, both of which were merged into cluster #0. 
            These two groups are connected via groups 9 -> 2 -> 8.
            * if we specify the replace name, then the output will be
            
            ``classix.explain(1, 1300, replace_name=["Peter Meyer", "Anna Fields"], figstyle="seaborn")``
            
            The data point Peter Meyer is in group 9 and the data point Anna Fields is in group 8, both of which were merged into cluster #0. 
            These two groups are connected via groups 9 -> 2 -> 8.

        plot : boolean, default=False
            Determine if visulize the explaination. 
        
        figsize : tuple, default=(9, 6)
            Determine the size of explain figure. 

        figstyle : str, default="default"
            Determine the style of visualization.
            see reference: https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
        
        savefig : boolean, default=False
            Determine if save figure, the figure will be saved in the folder named "img".
        
        bcolor : str, default="#f5f9f9"
            Color for figure background.
        
        obj_color : str, default as "k"
            Color for the text of data of index1 and index2.
        
        obj_msize : float, optional:
            Size for markers for data of index1 and index2.
    
        sp_fcolor : str, default='tomato'
            The color marked for starting points text box. 
        
        sp_marker : str, default="+"
            The marker for the start points.
        
        sp_size : int, default=66
            The marker size for the start points.
        
        sp_mcolor : str, default='k'
            The color marked for startpoint points scatter marker.

        sp_alpha : float, default=0.3
            The value setting for transprency of text box for starting points. 
            
        sp_pad : int, default=2
            The size of text box for starting points. 
        
        sp_bbox : dict, optional
            Dict with properties for patches.FancyBboxPatch for starting points.
    
        sp_fontsize : int, optional
            The fontsize for text marked for starting points. 

        sp_cmarker : str, default="+"
            The marker for the connected starting points.
        
        sp_csize : int, default=100
            The marker size for the connected starting points.
        
        sp_ccolor : str, default="crimson"
            The marker color for the connected starting points.
        
        sp_clinewidths : str, default=2.5
            The marker width for the connected starting points. 

        dp_fcolor : str, default='bisque'
            The color marked for specified data objects text box. 
            
        dp_alpha : float, default=0.3
            The value setting for transprency of text box for specified data objects. 
            
        dp_pad : int, default=2
            The size of text box for specified data objects. 
            
        dp_fontsize : int, optional
            The fontsize for text marked for specified data objects.    
                      
        dp_bbox : dict, optional
            Dict with properties for patches.FancyBboxPatch for specified data objects.
        
        show_all_grp_circle : bool, default=False
            Whether or not to show all groups' periphery within the objects' clusters 
            (only applies to when data dimension is less than or equal to 2).
        
        show_connected_grp_circle : bool, default=False
            Whether or not to show all connected groups' periphery within the objects' clusters 
            (only applies to when data dimension is less than or equal to 2).
        
        show_obj_grp_circle : bool, default=True
            Whether or not to show the groups' periphery of the objects
            (only applies to when data dimension is less than or equal to 2).

        color : str, default='red'
            Color for text of starting points labels in visualization. 
        
        alpha : float, default=0.5
            Scalar or None. 
    
        cline_width : float, default=2
            Set the patch linewidth of circle for starting points.

        add_arrow : bool, default=False 
            Whether or not add arrows for connected paths.

        arrow_linestyle : str, default='--' 
            Linestyle for arrow.
        
        arrow_fc : str, default='darkslategrey' 
            Face color for arrow.

        arrow_ec : str, default='k'
            Edge color for arrow.

        arrow_linewidth : float, default=1
            Set the linewidth of the arrow edges.

        directed_arrow : int, default=0
            Whether or not the edges for arrows is directed.
            Values at {-1, 0, 1}, 0 refers to undirected, -1 refers to the edge direction opposite to 1.
        
        shrinkA, shrinkB : float, default=2
            Shrinking factor of the tail and head of the arrow respectively.

        axis : boolean, default=True
            Whether or not add x,y axes to plot.

        figname : str, optional
            Set the figure name for the image to be saved.
            
        fmt : str
            Specify the format of the image to be saved, default as 'pdf', other choice: png.
        
        """
        from scipy.sparse.linalg import svds
        from matplotlib import pyplot as plt
        import matplotlib.colors as colors
        
        # -----------------------------second method--------------------------------
        if sp_bbox is None:
            sp_bbox = dict()
            sp_bbox['facecolor'] = sp_fcolor
            sp_bbox['alpha'] = sp_alpha
            sp_bbox['pad'] = sp_pad
       
        if dp_bbox is None:
            dp_bbox = dict()
            dp_bbox['facecolor'] = dp_fcolor
            dp_bbox['alpha'] = dp_alpha
            dp_bbox['pad'] = dp_pad


        if self.inverse_ind is None:
            self.inverse_ind = np.argsort(self.ind)

            groups_ = np.array(self.groups_)
            self.label_change = dict(zip(groups_[self.inverse_ind].ravel(), self.labels_)) # how object change group to cluster.

        data = self.data[self.inverse_ind]
        groups_ = np.array(self.groups_)
        groups_ = groups_[self.inverse_ind]
        
        if not self.sp_to_c_info: #  ensure call PCA and form groups information table only once
            
            if data.shape[1] > 2:
                warnings.warn("If the group periphery is displayed, the group radius in the visualization might not be accurate.")
                _U, self._s, self._V = svds(data, k=2, return_singular_vectors=True)
                self.x_pca = np.matmul(data, self._V[np.argsort(self._s)].T)
                self.s_pca = self.x_pca[self.ind[self.splist_[:, 0]]]
                
            elif data.shape[1] == 2:
                self.x_pca = data.copy()
                self.s_pca = data[self.ind[self.splist_[:, 0]]] 

            else: # when data is one-dimensional, no PCA transform
                self.x_pca = np.ones((len(data.copy()), 2))
                self.x_pca[:, 0] = data[:, 0]
                self.s_pca = np.ones((len(self.splist_), 2))
                self.s_pca[:, 0] = data[self.ind[self.splist_[:, 0]]].reshape(-1) 
                
            self.form_starting_point_clusters_table()
            
        if index1 is None and index2 is not None:
            raise ValueError("Please enter a valid value for index1.")
        
        
        # pd.options.display.max_colwidth = colwidth
        dash_line = "--------"*5 
            
        
        if index1 is None: # analyze in the general way with a global view
            if plot == True:
                self.explain_viz(showalldata=showalldata, figsize=figsize, showallgroups=showallgroups, figstyle=figstyle, bcolor=bcolor, savefig=savefig, 
                                 fontsize=sp_fontsize, bbox=sp_bbox, sp_marker=sp_marker, sp_mcolor=sp_mcolor, width=width, axis=axis, fmt=fmt)
                
            data_size = data.shape[0]
            feat_dim = data.shape[1]
            
            print("CLASSIX clustered {length:.0f} data points with {dim:.0f} features. ".format(length=data_size, dim=feat_dim))
            print("The radius parameter was set to {tol:.2f} and minPts was set to {minPts:.0f}. ".format(tol=self.radius, minPts=self.minPts))
            print("As the provided data was auto-scaled by a factor of 1/{scl:.2f},\npoints within a radius R={tol:.2f}*{scl:.2f}={tolscl:.2f} were grouped together. ".format(
                scl=self._scl, tol=self.radius, tolscl=self._scl*self.radius
            ))
            print("In total, {dist:.0f} distances were computed ({avg:.1f} per data point). ".format(dist=self.dist_nr, avg=self.dist_nr/data_size))
            print("This resulted in {groups:.0f} groups, each with a unique group center. ".format(groups=self.splist_.shape[0]))
            print("These {groups:.0f} groups were subsequently merged into {num_clusters:.0f} clusters. ".format(groups=self.splist_.shape[0], num_clusters=len(np.unique(self.labels_))))
            
            if showsplist:
                print("A list of all group centers is shown below.")
                print(dash_line)
                print(self.sp_info.to_string(justify='center', index=False, max_colwidth=max_colwidth))
                print(dash_line)       
            else:
                print("For a visualisation of the clusters, use .explain(plot=True). ")
                
            print("""In order to explain the clustering of individual data points, \n"""
                  """use .explain(ind1) or .explain(ind1, ind2) with data indices.""")
            
        else: # index is not None, explain(index1)
            if isinstance(index1, int):
                object1 = self.x_pca[index1] # data has been normalized
                agg_label1 = groups_[index1] # get the group index for object1
            
            elif isinstance(index1, str):
                if index1 in self.index_data:
                    if len(set(self.index_data)) != len(self.index_data):
                        warnings.warn("The index of data is duplicate.")
                        object1 = self.x_pca[np.where(self.index_data == index1)[0]][0]
                        agg_label1 = groups_[np.where(self.index_data == index1)[0][0]]
                    else:
                        object1 = self.x_pca[self.index_data == index1][0]
                        agg_label1 = groups_[self.index_data == index1][0]
                        
                else:
                    raise ValueError("Please enter a legal value for index1.")
                    
            elif isinstance(index1, list) or isinstance(index1, np.ndarray):
                index1 = np.array(index1)
                object1 = (index1 - self._mu) / self._scl # allow for out-sample data
                
                if data.shape[1] > 2:
                    object1 = np.matmul(object1, self._V[np.argsort(self._s)].T)
                    
                agg_label1 = np.argmin(np.linalg.norm(self.s_pca - object1, axis=1, ord=2)) # get the group index for object1

                    
            else:
                raise ValueError("Please enter a legal value for index1.")
                
            
            # explain one object
            if index2 is None:
                if replace_name is not None:
                    if isinstance(replace_name, list):
                        index1 = replace_name[0]
                    else:
                        index1 = replace_name
                else:
                    index1 = index1

                cluster_label1 = self.label_change[agg_label1]
                
                if plot == True:

                    if self.x_pca.shape[0] > 1e5 and not showalldata:
                        warnings.warn("Too many data points for plot. Randomly subsampled 1e5 points.")
                        selectInd = np.random.choice(self.x_pca.shape[0], 100000, replace=False)      
                    else:
                        selectInd = np.arange(self.x_pca.shape[0])

                    plt.style.use(style=figstyle)
                    fig, ax = plt.subplots(figsize=figsize)
                    
                    ax.set_facecolor(bcolor)

                    s_pca = self.s_pca[self.sp_info.Cluster == cluster_label1]
                    
                    ax.scatter(self.x_pca[selectInd, 0], self.x_pca[selectInd, 1], marker=".", linewidth=0.5*width, 
                               c=self.labels_[selectInd])
                    
                    ax.scatter(s_pca[:, 0], s_pca[:, 1], marker=sp_marker, label='group centers in cluster #{0}'.format(cluster_label1), 
                               s=sp_size, linewidth=0.9*width, c=sp_mcolor, alpha=0.4)
                    
                    if show_obj_grp_circle:
                        ax.add_patch(plt.Circle((self.s_pca[agg_label1, 0], self.s_pca[agg_label1, 1]), self.radius, fill=False, 
                                                color='lime', alpha=alpha, lw=cline_width*1.5, clip_on=False))
                        
                    
                    
                    if dp_fontsize is None:
                        ax.text(object1[0], object1[1], s=' ' + str(index1), bbox=dp_bbox, color=obj_color, zorder=1, ha='left', va='bottom')
                    else:
                        ax.text(object1[0], object1[1], s=' ' + str(index1), fontsize=dp_fontsize, bbox=dp_bbox, color=obj_color, zorder=1, ha='left', va='bottom')


                    ax.scatter(object1[0], object1[1], marker="*", s=obj_msize, label='data point {} '.format(index1))

                    for i in range(s_pca.shape[0]):
                        if data.shape[1] <= 2 and show_all_grp_circle:
                            ax.add_patch(plt.Circle((s_pca[i, 0], s_pca[i, 1]), self.radius, fill=False, color=color,
                                                     alpha=alpha, lw=cline_width*1.5, clip_on=False))
                        
                        if showallgroups:
                            if sp_fontsize is None:
                                ax.text(s_pca[i, 0], s_pca[i, 1],
                                        s=str(self.sp_info.Group[self.sp_info.Cluster == cluster_label1].astype(int).values[i]),
                                        bbox=sp_bbox, zorder=1, ha='left'
                                )
                            else:
                                ax.text(s_pca[i, 0], s_pca[i, 1],
                                        s=str(self.sp_info.Group[self.sp_info.Cluster == cluster_label1].astype(int).values[i]),
                                        fontsize=sp_fontsize, bbox=sp_bbox, zorder=1, ha='left'
                                )


                    
                    ax.scatter(self.s_pca[agg_label1, 0], self.s_pca[agg_label1, 1], 
                               marker='.', s=sp_csize*0.3, c='lime', linewidths=sp_clinewidths, 
                               label='group center {0}'.format(agg_label1)
                               )

                    ax.set_aspect('equal', adjustable='datalim')
                    ax.plot()

                    ax.legend(ncols=3, loc='best') # bbox_to_anchor=(0.5, -0.2)
                    
                    if axis:
                        ax.axis('on')
                        if data.shape[1] > 1:
                            ax.set_xlabel("1st principal component")
                            ax.set_ylabel("2nd principal component")
                        else:
                            ax.set_xlabel("1st principal component")
                    else:
                        ax.axis('off') # the axis here may not be consistent, so hide.
                    
                    ax.set_title("""{num_clusters:.0f} clusters (radius={tol:.2f}, minPts={minPts:.0f})""".format(
                        num_clusters=len(np.unique(self.labels_)),tol=self.radius, minPts=self.minPts))
                    
                    ax.spines['right'].set_color('none')
                    ax.spines['top'].set_color('none')

                    if savefig:
                        if not os.path.exists("img"):
                            os.mkdir("img")
                        if fmt == 'pdf':
                            fm = 'img/' + str(figname) + str(index1) +'.pdf'
                            plt.savefig(fm, bbox_inches='tight')
                        elif fmt == 'png':
                            fm = 'img/' + str(figname) + str(index1) +'.png'
                            plt.savefig(fm, bbox_inches='tight')
                        else:
                            fm = 'img/' + str(figname) + str(index1) +'.'+fmt
                            plt.savefig(fm, bbox_inches='tight')
                        
                        print("image successfully save as", fm)
                    
                    plt.show()
                    
                
                if showsplist:
                    select_sp_info = self.sp_info.iloc[[agg_label1]].copy(deep=True)
                    select_sp_info.loc[:, 'Label'] = str(np.round(index1,3))
                    print(dash_line)
                    print(select_sp_info.to_string(justify='center', index=False, max_colwidth=max_colwidth))
                    print(dash_line)       

                print(
                    """The data point %(index1)s is in group %(agg_id)i, which has been merged into cluster #%(m_c)i."""% {
                        "index1":index1, "agg_id":agg_label1, "m_c":cluster_label1
                    }
                )

            # explain two objects relationship
            else: 
                if isinstance(index2, int):
                    object2 = self.x_pca[index2] # data has been normalized
                    agg_label2 = groups_[index2] # get the group index for object2
                    
                elif isinstance(index2, str):
                    if index2 in self.index_data:
                        if len(set(self.index_data)) != len(self.index_data):
                            warnings.warn("The index of data is duplicate.")
                            object2 = self.x_pca[np.where(self.index_data == index2)[0][0]][0]
                            agg_label2 = groups_[np.where(self.index_data == index2)[0][0]]
                        else:
                            object2 = self.x_pca[self.index_data == index2][0]
                            agg_label2 = groups_[self.index_data == index2][0]
                    else:
                        raise ValueError("Please enter a legal value for index2.")
                        
                elif isinstance(index2, list) or isinstance(index2, np.ndarray):
                    index2 = np.array(index2)
                    object2 = (index2 - self._mu) / self._scl # allow for out-sample data
                    
                    if data.shape[1] > 2:
                        object2 = np.matmul(object2, self._V[np.argsort(self._s)].T)
                    
                    agg_label2 = np.argmin(np.linalg.norm(self.s_pca - object2, axis=1, ord=2)) # get the group index for object2
                
                else:
                    raise ValueError("Please enter a legal value for index2.")

                if showsplist:
                    
                    select_sp_info = self.sp_info.iloc[[agg_label1, agg_label2]].copy(deep=True)
                    if isinstance(index1, int) or isinstance(index1, str):
                        select_sp_info.loc[:, 'Label'] = [index1, index2]
                    else:
                        select_sp_info.loc[:, 'Label'] = [str(np.round(index1, 3)), str(np.round(index2, 3))]
                        
                    print(dash_line)
                    print(select_sp_info.to_string(justify='center', index=False, max_colwidth=max_colwidth))
                    print(dash_line)       

                if replace_name is not None:
                    if isinstance(replace_name, list) or isinstance(replace_name, np.ndarray):
                        try:
                            index1 = replace_name[0]
                            index2 = replace_name[1]
                        except:
                            index1 = replace_name[0]
                            
                else:
                    index1 = index1
                    index2 = index2

                cluster_label1, cluster_label2 = self.label_change[agg_label1], self.label_change[agg_label2]

                
                if agg_label1 == agg_label2: # when ind1 & ind2 are in the same group
                    connected_paths = [agg_label1]
                else:
                    from scipy.sparse import csr_matrix
                    
                    if self.connected_pairs_ is None:
                        distm = pairwise_distances(self.s_pca)
                        distm = (distm <= self.radius*self.scale).astype(int)
                        self.connected_pairs_ = return_csr_matrix_indices(csr_matrix(distm)).tolist() # list
                        
                    if cluster_label1 == cluster_label2:
                        connected_paths = find_shortest_path(agg_label1,
                                                             self.connected_pairs_,
                                                             self.splist_.shape[0],
                                                             agg_label2
                        )
                        
                        connected_paths_vis = " <-> ".join([str(group) for group in connected_paths]) 
                        
                    else: 
                        connected_paths = []
                        
                if plot == True:

                    if self.x_pca.shape[0] > 1e5 and not showalldata:
                        warnings.warn("Too many data points for plot. Randomly subsampled 1e5 points.")
                        selectInd = np.random.choice(self.x_pca.shape[0], 100000, replace=False)      
                    else:
                        selectInd = np.arange(self.x_pca.shape[0])

                    plt.style.use(style=figstyle)
                    fig, ax = plt.subplots(figsize=figsize)
                    ax.set_facecolor(bcolor)
                    
                    # select indices
                    union_ind = np.where((self.sp_info.Cluster == cluster_label1) | (self.sp_info.Cluster == cluster_label2))[0]
                    s_pca = self.s_pca[union_ind]
                    
                    ax.scatter(self.x_pca[selectInd, 0], self.x_pca[selectInd, 1], marker=".", c=self.labels_[selectInd], linewidth=width)
                    ax.scatter(s_pca[:,0], s_pca[:,1], label='group centers', marker=sp_marker, s=sp_size, c=sp_mcolor, linewidth=0.9*width, alpha=0.4)

                    
                    if show_obj_grp_circle:
                        ax.add_patch(plt.Circle((self.s_pca[agg_label1, 0], self.s_pca[agg_label1, 1]), self.radius, fill=False,
                                        color='lime', alpha=alpha, lw=cline_width*1.5, clip_on=False))
                        
                        ax.add_patch(plt.Circle((self.s_pca[agg_label2, 0], self.s_pca[agg_label2, 1]), self.radius, fill=False,
                                        color='cyan', alpha=alpha, lw=cline_width*1.5, clip_on=False))
                                        
                    if isinstance(index1, int) or isinstance(index1, str):
                        if dp_fontsize is None:
                            ax.text(object1[0], object1[1], s=' '+str(index1), ha='left', va='bottom', zorder=1, bbox=dp_bbox, color=obj_color)
                            ax.text(object2[0], object2[1], s=' '+str(index2), ha='left', va='bottom', zorder=1, bbox=dp_bbox, color=obj_color)
                        else:
                            ax.text(object1[0], object1[1], s=' '+str(index1), ha='left', va='bottom', zorder=1, fontsize=dp_fontsize, bbox=dp_bbox, color=obj_color)
                            ax.text(object2[0], object2[1], s=' '+str(index2), ha='left', va='bottom', zorder=1, fontsize=dp_fontsize, bbox=dp_bbox, color=obj_color)
                    else:
                        if dp_fontsize is None:
                            ax.text(object1[0], object1[1], s=' '+'index 1', ha='left', va='bottom', zorder=1, bbox=dp_bbox, color=obj_color)
                            ax.text(object2[0], object2[1], s=' '+'index 2', ha='left', va='bottom', zorder=1, bbox=dp_bbox, color=obj_color)
                        else:
                            ax.text(object1[0], object1[1], s=' '+'index 1', ha='left', va='bottom', zorder=1, fontsize=dp_fontsize, bbox=dp_bbox, color=obj_color)
                            ax.text(object2[0], object2[1], s=' '+'index 2', ha='left', va='bottom', zorder=1, fontsize=dp_fontsize, bbox=dp_bbox, color=obj_color)

                    ax.scatter(object1[0], object1[1], marker="*", s=obj_msize, 
                               label='data point {} '.format(index1)+'(cluster #{0})'.format(
                                   cluster_label1)
                            )
                    
                    ax.scatter(object2[0], object2[1], marker="*", s=obj_msize,
                                label='data point {} '.format(index2)+'(cluster #{0})'.format(
                                    cluster_label2)
                            )

                    for i in range(s_pca.shape[0]):
                        if data.shape[1] <= 2 and show_all_grp_circle:
                                ax.add_patch(plt.Circle((s_pca[i, 0], s_pca[i, 1]), self.radius, fill=False,
                                                    color=color, alpha=alpha, lw=cline_width*1.5, clip_on=False)
                                                    )
                                
                        if union_ind[i] in connected_paths:
                            # draw circle for connected starting points or not, 
                            # and also determine the marker of the connected starting points.
                            if union_ind[i] == connected_paths[0]: 
                                ax.scatter(s_pca[i,0], s_pca[i,1], marker=sp_cmarker, s=sp_csize, 
                                       label='connected groups', c=sp_ccolor, linewidths=sp_clinewidths)
                            else:
                                ax.scatter(s_pca[i,0], s_pca[i,1], marker=sp_cmarker, s=sp_csize, c=sp_ccolor, 
                                           linewidths=sp_clinewidths)
                                
                            if data.shape[1] <= 2:
                                if show_connected_grp_circle:
                                    ax.add_patch(plt.Circle((s_pca[i, 0], s_pca[i, 1]), self.radius, fill=False,
                                                    color=connect_color, alpha=alpha, lw=cline_width*1.5, clip_on=False))
                                    
                        ax.set_aspect('equal', adjustable='datalim')
                        
                        if showallgroups:
                            if sp_fontsize is None:
                                ax.text(s_pca[i, 0], s_pca[i, 1], 
                                        s=self.sp_info.Group[
                                            (self.sp_info.Cluster == cluster_label1) | (self.sp_info.Cluster == cluster_label2)
                                            ].values[i].astype(int).astype(str),
                                        zorder=1, ha='left', bbox=sp_bbox
                                )

                            else:
                                ax.text(s_pca[i, 0], s_pca[i, 1], 
                                        s=self.sp_info.Group[union_ind].values[i].astype(int).astype(str),
                                        fontsize=sp_fontsize, ha='left', bbox=sp_bbox
                                )

                    ax.scatter(self.s_pca[agg_label1, 0], self.s_pca[agg_label1, 1], 
                            marker='.', s=sp_csize*0.3, c='lime', linewidths=sp_clinewidths, 
                            label='group center {0}'.format(agg_label1)
                            )

                    ax.scatter(self.s_pca[agg_label2, 0], self.s_pca[agg_label2, 1], 
                            marker='.', s=sp_csize*0.3, c='cyan', linewidths=sp_clinewidths, 
                            label='group center {0}'.format(agg_label2)
                            )
                    
                    nr_cps = len(connected_paths)
                    
                    if add_arrow:
                        for i in range(nr_cps - 1):
                            arrowStart=(self.s_pca[connected_paths[i], 0], self.s_pca[connected_paths[i], 1])
                            arrowStop=(self.s_pca[connected_paths[i+1], 0], self.s_pca[connected_paths[i+1], 1])

                            if directed_arrow == 0:
                                ax.annotate("", arrowStop, 
                                            xytext=arrowStart, 
                                            arrowprops=dict(arrowstyle="-|>",
                                                            shrinkA=arrow_shrinkA, 
                                                            shrinkB=arrow_shrinkB, 
                                                            edgecolor=arrow_fc,
                                                            facecolor=arrow_ec,
                                                            linestyle=arrow_linestyle,
                                                            linewidth=arrow_linewidth
                                                            )
                                            )
                                
                                ax.annotate("", arrowStart,
                                            xytext=arrowStop, 
                                            arrowprops=dict(arrowstyle="-|>",
                                                            shrinkA=arrow_shrinkA, 
                                                            shrinkB=arrow_shrinkB, 
                                                            edgecolor=arrow_fc,
                                                            facecolor=arrow_ec,
                                                            linestyle=arrow_linestyle,
                                                            linewidth=arrow_linewidth
                                                            )
                                            )
                                    
                            elif directed_arrow == 1:
                                ax.annotate("", arrowStop,
                                            xytext=arrowStart,
                                            arrowprops=dict(arrowstyle="-|>",
                                                            shrinkA=arrow_shrinkA, 
                                                            shrinkB=arrow_shrinkB, 
                                                            edgecolor=arrow_fc,
                                                            facecolor=arrow_ec,
                                                            linestyle=arrow_linestyle,
                                                            linewidth=arrow_linewidth
                                                            )
                                            )

                            else:
                                ax.annotate("", arrowStart,
                                            xytext=arrowStop, 
                                            arrowprops=dict(arrowstyle="-|>",
                                                            shrinkA=arrow_shrinkA, 
                                                            shrinkB=arrow_shrinkB, 
                                                            edgecolor=arrow_fc,
                                                            facecolor=arrow_ec,
                                                            linestyle=arrow_linestyle,
                                                            linewidth=arrow_linewidth
                                                            )
                                            )
                                

                    if cluster_label1 == cluster_label2: # change the order of legend
                        handles, lg_labels = ax.get_legend_handles_labels()
                        lg_labels = [lg_labels[i] for i in [0,3,1,2,4,5]]
                        handles = [handles[i] for i in [0,3,1,2,4,5]]
                        ax.legend(handles, lg_labels, ncols=3, loc='best')
                    else:
                        ax.legend(ncols=3, loc='best')

                    ax.set_title("""{num_clusters:.0f} clusters (radius={tol:.2f}, minPts={minPts:.0f})""".format(
                        num_clusters=len(np.unique(self.labels_)),tol=self.radius, minPts=self.minPts))
                    
                    ax.spines['right'].set_color('none')
                    ax.spines['top'].set_color('none')

                    if axis:
                        ax.axis('on')
                        if data.shape[1] > 1:
                            ax.set_xlabel("1st principal component")
                            ax.set_ylabel("2nd principal component")
                        else:
                            ax.set_xlabel("1st principal component")
                    else:
                        ax.axis('off') # the axis here may not be consistent, so hide.

                    ax.plot()
                    if savefig:
                        if not os.path.exists("img"):
                            os.mkdir("img")
                        if fmt == 'pdf':
                            fm = 'img/' + str(figname) + str(index1) + '_' + str(index2) +'.pdf'
                            plt.savefig(fm, bbox_inches='tight')
                        elif fmt == 'png':
                            fm = 'img/' + str(figname) + str(index1) + '_' + str(index2) +'.png'
                            plt.savefig(fm, bbox_inches='tight')
                        else:
                            fm = 'img/' + str(figname) + str(index1) + '_' + str(index2) +'.'+fmt
                            plt.savefig(fm, bbox_inches='tight')
                            
                        print("image successfully save as", fm)
                        
                    plt.show()

                    if agg_label1 == agg_label2: # when ind1 & ind2 are in the same group
                        print("The data points %(index1)s and %(index2)s are in the same group %(agg_id)i, hence were merged into the same cluster #%(m_c)i"%{
                            "index1":index1, "index2":index2, "agg_id":agg_label1, "m_c":cluster_label1}
                        )
                    else:
                        if cluster_label1 == cluster_label2:
                            print(
                            """The data point %(index1)s is in group %(agg_id1)s and the data point %(index2)s is in group %(agg_id2)s, """
                                """\nboth of which were merged into cluster #%(cluster)i. """% {
                                "index1":index1, "index2":index2, "cluster":cluster_label1, "agg_id1":agg_label1, "agg_id2":agg_label2}
                            )
                            
                            print("""These two groups are connected via groups %(connected)s.""" % {
                                "connected":connected_paths_vis}
                            )
                        else: 
                            connected_paths = []
                            print("""The data point %(index1)s is in group %(agg_id1)i, which has been merged into cluster %(c_id1)s.""" % {
                                "index1":index1, "agg_id1":agg_label1, "c_id1":cluster_label1})

                            print("""The data point %(index2)s is in group %(agg_id2)i, which has been merged into cluster %(c_id2)s.""" % {
                                "index2":index2, "agg_id2":agg_label2, "c_id2":cluster_label2})   
                            
                            print("""There is no path of overlapping groups between these clusters.""")

                    self.connected_paths = connected_paths
        return 
    


    def explain_viz(self, showalldata=False, figsize=(10, 7), showallgroups=False, figstyle="default", bcolor="white", width=0.5, sp_marker="+", sp_mcolor="k", 
                    savefig=False, fontsize=None, bbox=None, axis="off", fmt="pdf"):
        """Visualize the starting point and data points"""
        
        from matplotlib import pyplot as plt

        if self.x_pca.shape[0] > 1e5 and not showalldata:
            warnings.warn("Too many data points for plot. Randomly subsampled 1e5 points.")
            selectInd = np.random.choice(self.x_pca.shape[0], 100000, replace=False)      
        else:
            selectInd = np.arange(self.x_pca.shape[0])

        plt.style.use(style=figstyle)
        plt.figure(figsize=figsize)
        plt.rcParams['axes.facecolor'] = bcolor

        plt.scatter(self.x_pca[selectInd,0], self.x_pca[selectInd,1], marker=".", linewidth=width, c=self.labels_[selectInd])

        if showallgroups:
            for j in range(self.s_pca.shape[0]):
                if fontsize is None:
                    plt.text(self.s_pca[j, 0], self.s_pca[j, 1], str(j), zorder=1, ha='left', bbox=bbox)
                else:
                    plt.text(self.s_pca[j, 0], self.s_pca[j, 1], str(j), zorder=1, ha='left', fontsize=fontsize, bbox=bbox)

        if showallgroups:
            plt.scatter(self.s_pca[:,0], self.s_pca[:,1], label='group centers', 
                        marker=sp_marker, linewidth=0.9*width, c=sp_mcolor)

        plt.axis('equal')
        plt.title("""{num_clusters:.0f} clusters (radius={tol:.2f}, minPts={minPts:.0f})""".format(num_clusters=len(np.unique(self.labels_)),tol=self.radius, minPts=self.minPts))

        if axis:
            plt.axis('on')
            if self.s_pca.shape[1] > 1:
                plt.xlabel("1st principal component")
                plt.ylabel("2nd principal component")
            else:
                plt.xlabel("1st principal component")
        else:
            plt.axis('off') # the axis here may not be consistent, so hide.

        plt.gca().spines['right'].set_color('none')
        plt.gca().spines['top'].set_color('none')

        if savefig:
            if not os.path.exists("img"):
                os.mkdir("img")
            if fmt == 'pdf':
                fm = 'img/explain_viz.pdf'
                plt.savefig(fm, bbox_inches='tight')
            elif fmt == 'png':
                fm = 'img/explain_viz.png'
                plt.savefig(fm, bbox_inches='tight')
            else:
                fm = 'img/explain_viz.'+fmt
                plt.savefig(fm, bbox_inches='tight')
                
            print("image successfully save as", fm)
            
        plt.show()
            
        return
    
        

    def form_starting_point_clusters_table(self, aggregate=False):
        """form the columns details for starting points and clusters information"""
        
        # won't change the original order of self.splist_
        cols = ["Group", "NrPts"]
        coord = list()
        
        if aggregate:
            for i in np.around(self.s_pca, 2).tolist():
                fill = ""
                if len(i) <= 5:
                    for j in i:
                        fill = fill + str(j) + " "
                else:
                    for j in i[:5]:
                        fill = fill + str(j) + " "
                    fill = fill + "..."
                fill += ""
                coord.append(fill)


        else:
            for i in self.splist_[:, 0]:
                fill = ""
                sp_item = np.around(self.data[int(i), :], 2).tolist()
                if len(sp_item) <= 5:
                    for j in sp_item:
                        fill = fill + str(j) + " "
                else:
                    for j in sp_item[:5]:
                        fill = fill + str(j) + " "
                    fill = fill + "..."
                fill += ""
                coord.append(fill)
                
        self.sp_info = pd.DataFrame(columns=cols)
        self.sp_info["Group"] = np.arange(0, self.splist_.shape[0])
        self.sp_info["NrPts"] = self.splist_[:, 1].astype(int)
        self.sp_info["Cluster"] = [self.label_change[i] for i in range(self.splist_.shape[0])]
        self.sp_info["Coordinates"] = coord 
        self.sp_to_c_info = True
        return
        
        
    
    def visualize_linkage(self, scale=1.5, figsize=(10,7), labelsize=24, markersize=320, plot_boundary=False, bound_color='red', path='.', fmt='pdf'):
        
        """Visualize the linkage in the distance clustering.
        
        
        Parameters
        ----------
        scale : float
            Design for distance-clustering, when distance between the two starting points 
            associated with two distinct groups smaller than scale*radius, then the two groups merge.
        
        labelsize : int 
            The fontsize of ticks. 
            
        markersize : int 
            The size of the markers for starting points.
            
        plot_boundary : boolean
            If it is true, will plot the boundary of groups for the starting points.
            
        bound_color : str
            The color for the boundary for groups with the specified radius.
            
        path : str
            Relative file location for figure storage.
            
        fmt : str
            Specify the format of the image to be saved, default as 'pdf', other choice: png.
        
        """
        from scipy.sparse import csr_matrix
        from matplotlib import pyplot as plt
                              
        distm, n_components, labels = visualize_connections(self.data, self.splist_, radius=self.radius, scale=round(scale,2))
        plt.rcParams['axes.facecolor'] = 'white'

        P = self.data[self.splist_[:, 0].astype(int)]
        link_list = return_csr_matrix_indices(csr_matrix(distm))
        
        fig, ax = plt.subplots(figsize=figsize)
        for i in range(self.splist_.shape[0]):
            ax.scatter(P[i,0], P[i,1], s=markersize, c='k', marker='.')
            if plot_boundary and self.data.shape[1] <= 2:
                ax.add_patch(plt.Circle((P[i, 0], P[i, 1]), self.radius, 
                                        color=bound_color, fill=False, clip_on=False)
                            )
            ax.set_aspect('equal', adjustable='datalim')

        for edge in link_list:
            i, j = edge
            ax.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], linewidth=3, c='k') 
        
        ax.tick_params(axis='both', labelsize=labelsize, colors='k')
        if not os.path.isdir(path):
            os.makedirs(path)
        if fmt == 'pdf':
            fig.savefig(path + '/linkage_scale_'+str(round(scale,2))+'_tol_'+str(round(self.radius,2))+'.pdf', bbox_inches='tight')
        else:
            fig.savefig(path + '/linkage_scale_'+str(round(scale,2))+'_tol_'+str(round(self.radius,2))+'.png', bbox_inches='tight')
        


    def gc2ind(self, spid):
        return self.ind[self.splist_[spid, 0]]



    def load_cluster_centers(self):
        """Load cluster centers."""
        
        if self.centers is None:
            self.centers = calculate_cluster_centers(self.data*self._scl + self._mu, self.labels_)
            return self.centers
        else:
            return self.centers
        
        
    def calculate_group_centers(self, data, labels):
        """Compute data center for each label according to label sequence."""
        
        centers = list() 
        for c in set(labels):
            indc = [i for i in range(data.shape[0]) if labels[i] == c]
            indc = (labels==c)
            center = [-1, c] + np.mean(data[indc,:], axis=0).tolist()
            centers.append( center )
            
        return centers

    
    def load_splist_indices(self):
        """Get the starting point indices."""
        
        if self.splist_indices is not None:
            self.splist_indices = np.full(self.data.shape[0], 0, dtype=int)
            self.splist_indices[self.splist_[:,0].astype(int)] = 1
            
        return self.splist_indices


    
    def outlier_filter(self, min_samples=None, min_samples_rate=0.1): # percent
        """Filter outliers in terms of ``min_samples`` or ``min_samples_rate``. """
        
        if min_samples == None:
            min_samples = min_samples_rate*sum(self.old_cluster_count.values())
            
        return [i[0] for i in self.old_cluster_count.items() if i[1] < min_samples]
    



    def reassign_labels(self, labels):
        """Renumber the labels to 0, 1, 2, 3, ..."""
        
        sorted_dict = sorted(self.old_cluster_count.items(), key=lambda x: x[1], reverse=True)

        clabels = copy.deepcopy(labels)
        for i in range(len(sorted_dict)):
            clabels[labels == sorted_dict[i][0]]  = i
        return clabels

    

    def pprint_format(self, items):
        """Format item value for clusters. """
        
        cluster = 0
        if isinstance(items, dict):
            for key, value in sorted(items.items(), key=lambda x: x[1], reverse=True): 
                if cluster > 19:
                    print("      ... truncated ...")
                    break
                    
                print("      * cluster {:2} : {}".format(cluster, value))
                cluster = cluster + 1
                
                
        elif isinstance(items, list) or isinstance(items, tuple):
            for item in items:
                print("      * ", item)
            
        return 
            

            
    def __repr__(self):
        _name = "CLASSIX(radius={0.radius!r}, minPts={0.minPts!r}, group_merging={0.group_merging!r})".format(self)
        return _name 

    
    
    def __str__(self):
        _name = 'CLASSIX(radius={0.radius!r}, minPts={0.minPts!r}, group_merging={0.group_merging!r})'.format(self)
        return _name
    
    
    
    @property
    def radius(self):
        return self._radius
    
    
    
    @radius.setter
    def radius(self, value):
        if not isinstance(value, float) and not isinstance(value,int):
            raise TypeError('Expected a float or int type')
        if value <= 0:
            raise ValueError(
                "Please feed an correct value (>0) for tolerance.")
 
        self._radius = value
    
    
        
    @property
    def sorting(self):
        return self._sorting
    
    
    
    @sorting.setter
    def sorting(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string type')
        if value not in ['pca', 'norm-mean', 'norm-orthant'] and value != None:
            raise ValueError(
                "Please refer to an correct sorting way, namely 'pca', 'norm-mean' and 'norm-orthant'.")
        self._sorting = value

        
    
    @property
    def group_merging(self):
        return self._group_merging
    
    
    
    @group_merging.setter
    def group_merging(self, value):
        if not isinstance(value, str) and not isinstance(None, type(None)):
            raise TypeError('Expected a string type or None.')
        if value not in ['density', 
                         'distance'
                        ] and value is not None: # 'mst-distance', 'scc-distance', 'trivial-distance', 'trivial-density'
            if value.lower()!='none':
                raise ValueError(
                "Please refer to an correct sorting way, namely 'density' and 'distance' or None."
                ) # 'scc-distance' and 'mst-distance'
        self._group_merging = value
        

    
    
    
    @property
    def minPts(self):
        return self._minPts
    
    
    
    @minPts.setter
    def minPts(self, value):
        if isinstance(value, str):
            raise TypeError('Expected a float or int type.')
        
        if isinstance(value, bool):
            raise TypeError('Expected a float or int type.')
        
        if isinstance(value, dict):
            raise TypeError('Expected a float or int type.')
        
        if hasattr(value, "__len__"):
            raise TypeError('Expected a scalar.')
        
        if value < 0 or (0 < value & value < 1):
            raise ValueError('Noise_scale must be 0 or greater than 1.')
        
        self._minPts = int(round(value))
    
    




def pairwise_distances(X):
    """Calculate the Euclidean distance matrix."""
    distm = np.zeros((X.shape[0], X.shape[0]))
    for i in range(X.shape[0]):
        for j in range(i, X.shape[0]):
            distm[i, j] = distm[j, i] = norm(X[i,:]-X[j,:], ord=2)
    return distm



def visualize_connections(data, splist, radius=0.5, scale=1.5):
    """Calculate the connected components for graph constructed by starting points given radius and scale."""

    from scipy.sparse.csgraph import connected_components
    
    distm = pairwise_distances(data[splist[:,0].astype(int)])
    tol = radius*scale
    distm = (distm <= tol).astype(int)
    n_components, labels = connected_components(csgraph=distm, directed=False, return_labels=True)
    return distm, n_components, labels
    
    
    
def novel_normalization(data, base):
    """Initial data preparation of CLASSIX."""
    if base == "norm-mean":
        _mu = data.mean(axis=0)
        ndata = data - _mu
        _scl = ndata.std()
        ndata = ndata / _scl

    elif base == "pca":
        _mu = data.mean(axis=0)
        ndata = data - _mu # mean center
        rds = norm(ndata, axis=1) # distance of each data point from 0
        _scl = np.median(rds) # 50% of data points are within that radius
        ndata = ndata / _scl # now 50% of data are in unit ball 

    elif base == "norm-orthant":
        _mu = data.min(axis=0)
        ndata = data - _mu
        _scl = ndata.std()
        ndata = ndata / _scl

    else:
        _mu, _scl = 0, 1 # no normalization
        ndata = (data - _mu) / _scl
    return ndata, (_mu, _scl)



def calculate_cluster_centers(data, labels):
    """Calculate the mean centers of clusters from given data."""
    classes = np.unique(labels)
    centers = np.zeros((len(classes), data.shape[1]))
    for c in classes:
        centers[c] = np.mean(data[labels==c,:], axis=0)
    return centers




# ##########################################################################################################
# **************<!-- the independent functions of finding shortest path between two objects ***************
# ##########################################################################################################




def find_shortest_path(source_node=None, connected_pairs=None, num_nodes=None, target_node=None):
    """Get single-sourse shortest paths as well as distance from source node,
    design especially for unweighted undirected graph. The time complexity is O(|V| + |E|)
    where |V| is the number of vertices and |E| is the number of edges.
    
    Parameters
    ----------
    source_node: int
        A given source vertex.
    
    connected_pairs: list
        The list stores connected nodes pairs.
    
    num_nodes: int
        The number of nodes existed in the graph.
        
    target_node: int, default=None
        Find the shortest paths from source node to target node.
        If not None, function returns the shortest path between source node and target node,
        otherwise returns table storing shortest path information.
        
    Returns
    -------
    dist_info: numpy.ndarray
        The table storing shortest path information.
    
    shortest_path_to_target: list
        The shortest path between source node and target node
    
    """
    visited_nodes = [False]*num_nodes
    queque = list()
    graph = pairs_to_graph(connected_pairs, num_nodes) # return sparse matrix
    dist_info = np.empty((num_nodes, 3), dtype=int) # node, dist, last node
    
    dist_info[:,0] = np.arange(num_nodes)
    dist_info[:,1] = num_nodes # np.iinfo(np.int64).max
    dist_info[:,2] = -1
    
    source_node = int(source_node)
    queque.append(source_node+1)
    dist_info[source_node,1] = 0

    while(np.any(queque)):
        node = queque.pop(0)
        if not visited_nodes[node-1]:
            neighbor = list()
            visited_nodes[node-1] = True
            for i in range(int(num_nodes)):
                if graph[node-1, i] == 1 and not visited_nodes[i] and not i+1 in queque:
                    neighbor.append(i+1)
                    dist_info[i, 1], dist_info[i, 2] = dist_info[node-1, 1]+1, node-1
            queque = queque + neighbor
            
    if target_node != None:
        shortest_path_to_target = list()
        if dist_info[target_node,1] == np.iinfo(np.int64).min:
            print("no path between {} and {}".format(source_node, target_node))
            return None
        
        predecessor = target_node
        while(dist_info[predecessor, 2] != -1):
            shortest_path_to_target.append(predecessor)
            predecessor = dist_info[predecessor, 2]
            
        shortest_path_to_target.append(source_node)
        shortest_path_to_target.reverse()
        return shortest_path_to_target
    else:
        return dist_info

    

def pairs_to_graph(pairs, num_nodes, sparse=True):
    """Transform the pairs represented by list into graph."""
    from scipy.sparse import csr_matrix
    
    graph = np.full((num_nodes, num_nodes), -99, dtype=int)
    for i in range(num_nodes):
        graph[i, i] = 0
    
    for pair in pairs:
        graph[pair[0], pair[1]] = graph[pair[1], pair[0]] = 1
    if sparse:
        graph = csr_matrix(graph)
    return graph



def return_csr_matrix_indices(csr_mat): 
    """Return sparce matrix indices."""

    from scipy.sparse import _sparsetools
    
    shape_dim1, shape_dim2 = csr_mat.shape
    length_range = csr_mat.indices

    indices = np.empty(len(length_range), dtype=csr_mat.indices.dtype)
    _sparsetools.expandptr(shape_dim1, csr_mat.indptr, indices)
    return np.array(list(zip(indices, length_range)))




def euclid(xxt, X, v):
    return (xxt + np.inner(v,v).ravel() -2*X.dot(v)).astype(float)






