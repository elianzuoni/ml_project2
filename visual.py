import matplotlib.pyplot as plt


def visual_reduced_chord_vectors(wv_red, dimred_method, plot_title, figsize=(20,10), dpi=250, remove_key_mode=True,
                                 show_chords=False, marker_map={'MAJOR':'o', 'MINOR':'s', 'UNSPEC':'D'}, marker_size=50,
                                 colour_map={'I':'blue', 'II':'yellow', 'III':'green', 'IV':'purple', 'V':'red', 'VI':'black',
                                             'VII':'pink'}, fig_name='sarno.png'):
    '''
    Plots the 2d-reduced vectors corresponding to each chord. Colours each point according to the 
    key it's in, and to its base note.
    
    Input.  wv_red: a dictionary mapping a chord (string) to a list of 2 coordinates.
            dimred_method: the method was used for dimensionality reduction.
            plot_title: the label to display at the top of the plot.
            figsize: the size of the graph.
            dpi: the dot-per-inch of the graph.
            remove_key_mode: flag signalling whether to remove the key mode indication from the chord.
            show_chords: flag signalling whether to show a label with the chord name near each point.
            marker_map: dictionary mapping key mode ('MAJOR'/'MINOR'/'UNSPEC') to marker.
            marker_size: the size of each marker.
            colour_map: dictionary mapping each base degree ('I' through 'VII') to a colour string.
            fig_name: name of the file to save the plot to.
    Output. None: just plots the points.
    '''
    
    # Separate chords by key mode
    all_chords = list(wv_red.keys())
    key_modes = ['MAJOR', 'MINOR', 'UNSPEC']
    chords_by_key = {}
    chords_by_key['MAJOR'] = [chord for chord in all_chords if 'MAJOR' in chord]
    chords_by_key['MINOR'] = [chord for chord in all_chords if 'MINOR' in chord]
    chords_by_key['UNSPEC'] = [chord for chord in all_chords if 'MAJOR' not in chord and 'MINOR' not in chord]
    
    # Get, for each class of chords, the x's and the y's
    xs_by_key = {}
    ys_by_key = {}
    for key in key_modes:
        xs_by_key[key] = [wv_red[chord][0] for chord in chords_by_key[key]]
        ys_by_key[key] = [wv_red[chord][1] for chord in chords_by_key[key]]
    
    # Initialise figure
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_xlabel('First ' + dimred_method + ' component')
    ax.set_ylabel('Second ' + dimred_method + ' component')
    fig.suptitle(plot_title)
    
    # Scatter points, for each class of chords
    for key in key_modes:
        marker = marker_map[key]
        colours = [get_point_colour(chord, colour_map) for chord in chords_by_key[key]]
        ax.scatter(xs_by_key[key], ys_by_key[key], c=colours, marker=marker, s=marker_size)
        
    # Add labels, if required
    if show_chords:
        # Remove the key mode indication, if required
        if remove_key_mode:
            chords = [get_without_key_mode(chord) for chord in chords]
        for i, chord in enumerate(chords):
            ax.annotate(chord, xy = (xs[i], ys[i]))

    plt.savefig(fig_name)
    
    return


def get_point_colour(chord, colour_map):
    '''
    Returns the colour of the point corresponding to the chord, depending on its base degree.
    
    Input.  chord: a string.
    Output. colour: a colour string.
    '''
    
    # First, remove key mode
    no_key = chord.replace('MAJOR;', '').replace('MINOR;', '')
    # Then, remove alterations
    no_alter = no_key.replace('b', '').replace('#', '')
    # Finally, remove type (MAJ/MIN/AUG/DIM)
    no_type = no_alter.replace(':MAJ', '').replace(':MIN', '').replace(':AUG', '').replace(':DIM', '')
    
    colour = colour_map[no_type]
    return colour


def get_without_key_mode(chord):
    '''
    Removes the key mode indication from the chord. Also works if the indication is not present.
    
    Input.  chord: the chord. Possibly pre-pended with MAJOR/MINOR key mode indication.
    Output. chord_nokey: the chord without the indication.
    '''
    
    chord_nokey = chord.replace('MAJOR;', '').replace('MINOR;', '')
    return chord_nokey