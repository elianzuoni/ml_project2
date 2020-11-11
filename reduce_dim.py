import numpy as np


def reduce_dim_keyed_vec(wv, reduce_dim):
    '''
    Applies the provided dimensionality-reduction function to the provided keyed vector, maintaining the labels.
    
    Input.  wv: a KeyedVector.
            reduce_dim: a function for dimensionality reduction, taking as input a (n_samples * n_features) array-like.
    Output. wv_red: a dictionary mapping the same words as wv to dimensionality-reduced vectors.
    '''
      
    # Reduce dimensionality
    X_red = reduce_dim(wv.vectors) #wv.vectors is a 2d NumPy array
    
    # Reconstruct a dictionary out of X_red (the order is preserved)
    wv_red = dict()
    for i, word in enumerate(wv.vocab.keys()):
        wv_red[word] = X_red[i, :]
    
    return wv_red
    