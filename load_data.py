import pandas as pd


# Data folders
data_folder = 'data/'
chord_folder = 'data/chord/'
key_folder = 'data/key/'

# File names
all_composers = ['Bach.csv', 'Beethoven.csv','Chopin.csv', 'Corelli.csv', 'Couperin.csv', 'Debussy.csv', 'Dvorak.csv', 
              'Gesualdo.csv', 'Grieg.csv', 'Kozeluh.csv', 'Liszt.csv', 'Medtner.csv', 'Mendelssohn.csv', 'Monteverdi.csv',
              'Mozart.csv','Pleyel.csv', 'Ravel.csv', 'Schubert.csv', 'Schumann.csv', 'Schütz.csv', 'Sweelinck.csv',
              'Tchaikovsky.csv', 'Wagner.csv','WFBach.csv']


def load_key_data(composers, drop_one_worders=True):
    '''
    Read the key datasets for a list of composers, and return them in a list containing all the sentences.
    Each sentence is a list of words. Each word is a string.
    If specified by the argument, we drop the sentences with just one word.
    
    - Input.  composers: iterable of file names (example: ['Bach.csv']).
              drop_one_worders: flag to control whether to include sentences with one word.
    - Output. sentences: list of words (strings).
    '''
    
    # Dataframe that will contain all sentences
    frame = pd.DataFrame()
    
    for composer in composers:
        # We use sep='\n' to be able to first separate each line, but we'll have just one column
        data = pd.read_csv(key_folder + composer, sep='\n', names=['sentence'], header=None, error_bad_lines=False)
        # We replace the sentence column with a list of split words
        data['sentence'] = data['sentence'].str.split(',', expand=False)
        
        # If we want to remove sentences with only one word: drop all lines for which the length of the list is 1
        if drop_one_worders:
            data = data[data['sentence'].apply(lambda sent : len(sent)>1)]
            
        # Concatenate to global frame
        frame = pd.concat([frame, data], ignore_index=True)
        
    # Final list of sentences
    sentences = frame['sentence'].tolist()
    
    return sentences


def load_chord_data(composers, key_mode='both'):
    '''
    Read the chord datasets for a list of composers, and return them in a list containing all the sentences.
    Each sentence is a list of words. Each word is a string.
    The 'key_mode' argument specifies whether we want just the sections in a major or minor key, or if we want them all.
    
    - Input.  composers: iterable of file names (example: ['Bach.csv']).
              key_mode: string to control whether to include sentences in major/minor mode, or both.
    - Output. sentences: list of words (strings).
    '''
    
    # Dataframe that will contain all sentences
    frame = pd.DataFrame()
    
    for composer in composers:
        # We use sep=';' to split into a 'mode' column and a 'sentence' column
        data = pd.read_csv(chord_folder + composer, sep=';', names=['key_mode', 'sentence'], header=None, error_bad_lines=False)
        # We replace the sentence column with a list of split words
        data['sentence'] = data['sentence'].str.split(',', expand=False)
            
        # Concatenate to global frame
        frame = pd.concat([frame, data], ignore_index=True)
        
    # If both modes are required, we have to modify words so as to include the mode. Else, we have to drop irrelevant sentences
    if key_mode == 'both':
        frame['sentence'] = frame.apply(lambda row : get_augmented_sentence(row['key_mode'], row['sentence']), axis=1)
    else:
        frame = frame[frame['key_mode'] == key_mode.upper()]
    
    # List of sentences to return
    sentences = frame['sentence'].tolist()
    
    return sentences


def get_augmented_sentence(key_mode, sentence):
    '''
    Modifies each word in the sentence, by pre-pending the mode to it.
    
    - Input.  sentence: list of words (strings).
              key_mode: a word.
    - Output. aug: list of augmented words (strings).
    '''
    
    aug = []
    for word in sentence:
        aug.append(key_mode + ';' + word)
        
    return aug







