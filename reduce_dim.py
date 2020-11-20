import numpy as np


def reduce_dim_keyed_vec(wv, reduce_dim, comps_to_keep=[0,1]):
    '''
    Applies the provided dimensionality-reduction function to the provided keyed vector, maintaining the labels.
    
    Input.  wv: a KeyedVector.
            reduce_dim: a function for dimensionality reduction, taking as input a (n_samples * n_features) array-like.
            comps_to_keep: the components to keep.
    Output. wv_red: a dictionary mapping the same words as wv to dimensionality-reduced vectors.
    '''
    
    # Build (n_samples * n_features) matrix
    X = emb_to_coordinates(wv) 
    
    # Reduce dimensionality
    X_red = reduce_dim(X) #wv.vectors is a 2d NumPy array
    
    # Reconstruct a dictionary out of X_red (the order is preserved)
    wv_red = dict()
    for i, word in enumerate(wv.vocab.keys()):
        wv_red[word] = X_red[i][comps_to_keep]
    
    return wv_red
    

def emb_to_coordinates(wv):
    '''
    Function that takes a model created by word2vec, and returns an array, 
    containing for each word its coordinates in the embedding space
    Input : model created by word2vec, size of the embedding space
    Output : Array of size (nb of vocab words in word2vec) x (size of the embedding space), containing the coordinates
    of each word in this embedding space
    '''
    vocab = list(wv.vocab.keys()) #chords
    size = wv[vocab[0]].shape[0]
    coordinates = np.ones((len(vocab), size)) #initialisation of the matrix containing coordinates in the embedding space
    for indx, chord in enumerate(vocab): #For each chord
        coordinates[indx,:] = wv[chord] #we add the coordinates
    return coordinates
