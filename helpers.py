import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models import Word2Vec
from sklearn.decomposition import PCA

#folders 
data_folder = 'C:/Users/HP/ML_project_chord/data/'
chord_folder = 'C:/Users/HP/ML_project_chord/data/chord/'
key_folder = 'C:/Users/HP/ML_project_chord/data/key/'


#functions
def load_key_data(file):
    '''
    Function that returns the csv file as a dataframe for one composer
    
    - Input : file name (example : 'Bach.csv')'''
    #We use sep='\n' to be able to first separate each line, but we'll have just one column
    data = pd.read_csv(key_folder + file, sep='\n' ,header= None, error_bad_lines = False)
    
    #same as before : we add columns for the case when there is more than one symbol
    data = data[0].str.split(',', expand=True)
    
    #If we want to remove lines with only one symbol : uncomment the following line
    data = data.drop(data[data[1].apply(lambda x: x is None)].index) #drop all lines for which the value of the second column is 'None'
    return data


def models_word2vec(file_names, min_count, size, window, sg):
    '''
    Function that loads the data of a list of file names (names of composers), and returns 3 word2vec models : one containing both MAJOR and MINOR modes (it doesn't distinguish the two modes), one for the MAJOR mode and one for the MINOR mode
    Input : file names list and word2vec parameters
    Output : models for MAJOR and MINOR sentences
    '''
    data = pd.DataFrame() #initialization of what will contain all the sentences (for each composers)
    for file in file_names:
        #Load the data as a dataframe (the second column contain all chords separetd by ':')
        data_file = pd.read_csv(chord_folder + file, sep=';' ,header= None, error_bad_lines = False)
        data = pd.concat([data, data_file], ignore_index=True)
    
    #We create the list of list necessary for word2vec, for each MAJOR/MINOR mode
    sentences = [row.split(',') for row in data[1]]
    sentences_maj = [row.split(',') for row in data[data[0] == 'MAJOR'][1]]
    sentences_min = [row.split(',') for row in data[data[0] == 'MINOR'][1]]
    
    #Word2Vec models :
    model = Word2Vec(sentences, min_count=min_count, size=size, window=window, sg=sg)
    model_maj = Word2Vec(sentences_maj, min_count=min_count, size=size, window=window, sg=sg)
    model_min = Word2Vec(sentences_min, min_count=min_count, size=size, window=window, sg=sg)
    
    return model, model_maj, model_min



def emb_to_coordinates(model, size):
    '''
    Function that takes a model created by word2vec, and returns an array, 
    containing for each word its coordinates in the embedding space
    Input : model created by word2vec, size of the embedding space
    Output : Array of size (nb of vocab words in word2vec) x (size of the embedding space), containing the coordinates
    of each word in this embedding space
    '''
    vocab = model.wv.vocab.keys() #chords
    coordinates = np.ones((len(vocab), size)) #initialisation of the matrix containing coordinates in the embedding space
    for indx, chord in enumerate(vocab): #For each chord
        coordinates[indx,:] = model.wv[chord] #we add the coordinates
    return coordinates



def pca_2d(model, model_maj, model_min, size):
    '''
    Function that takes as input the 3 models, performs PCA, plot the coordinates of each chord.
    Input : word2vec model for the general case, and for the MAJOR and the MINOR key, size of the embedding space
    Output : None (Plot)
    '''
    #Arrays containing the coordinates of each word in the embedding space, for the 3 models
    coordinates = emb_to_coordinates(model, size)
    coordinates_maj = emb_to_coordinates(model_maj, size) 
    coordinates_min = emb_to_coordinates(model_min, size) 
    
    #Remove the mean before applying pca
    coordinates = coordinates - np.mean(coordinates, axis=0)
    coordinates_maj = coordinates_maj - np.mean(coordinates_maj, axis=0)
    coordinates_min = coordinates_min - np.mean(coordinates_min, axis=0) 

    #Perform PCA
    pca = PCA(n_components=2)
    
    ppal_components = pca.fit_transform(coordinates)
    ppal_components_maj = pca.fit_transform(coordinates_maj)
    ppal_components_min = pca.fit_transform(coordinates_min)
    
    return ppal_components, ppal_components_maj, ppal_components_min


def visualization(file_names, min_count, size, window, sg):
    '''
    Function that plot the chord in a 2d space for each the major and the minor mode
    Input : file name, parameters for the word2vec model
    Output : None (Plot)
    '''
    #Word2vec models
    model, model_maj, model_min = models_word2vec(file_names, min_count, size, window, sg)
    
    #PCA
    ppal_components, ppal_components_maj, ppal_components_min = pca_2d(model, model_maj, model_min, size)
    
    #Labels (to use for the vizualisation)
    labels = [chord for chord in model.wv.vocab.keys()]
    labels_maj = [chord for chord in model_maj.wv.vocab.keys()]
    labels_min = [chord for chord in model_min.wv.vocab.keys()]
    
    #Creation of the figure and plots
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10,7), dpi = 150)
    (ax1 , ax2, ax3) = axs
    ax1.scatter(ppal_components[:,0], ppal_components[:,1], color = 'red')
    ax1.set_title('Major and Minor mode trained together')
    
    ax2.scatter(ppal_components_maj[:,0], ppal_components_maj[:,1], color = 'green')
    ax2.set_title('Major')
    
    ax3.scatter(ppal_components_min[:,0], ppal_components_min[:,1], color = 'blue')
    ax3.set_title('Minor')
    
    #Set x and y labels
    for ax in axs.flat:
        ax.set(xlabel='component 1 of PCA', ylabel='component 2 of PCA')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
        
    #Title : if there is less than 3 composers in file_names, it highlight which one it is, but if there is more than 3, it says 'all composers'
    if len(file_names) <= 3:
        fig.suptitle('Chords in the embedding space for ', [i for i in file_names])
    else:
        fig.suptitle('Chords in the embedding space for all composers')

    #Annotate the points to know which chord it is
    for i, chord in enumerate(labels_maj):
        ax1.annotate(chord, (ppal_components[:,0][i], ppal_components[:,1][i]), color='red')
    for i, chord in enumerate(labels_maj):
        ax2.annotate(chord, (ppal_components_maj[:,0][i], ppal_components_maj[:,1][i]), color='green')
    for i, chord in enumerate(labels_min):
        ax3.annotate(chord, (ppal_components_min[:,0][i], ppal_components_min[:,1][i]), color='blue')