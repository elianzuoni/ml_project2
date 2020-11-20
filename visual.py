import matplotlib.pyplot as plt


def visual_reduced_chord_vectors(wv_red, dimred_method, plot_title, figsize=(6,6), dpi=250, remove_key_mode=False, 
                                 chord_types_to_label=[], chord_types_not_to_label=[], label_size=3, 
                                 marker_map={'MAJOR':'o', 'MINOR':'s', 'UNSPEC':'D'}, marker_size=5, 
                                 colour_map={'I':'blue', 'II':'yellow', 'III':'green', 'IV':'purple', 'V':'red', 
                                             'VI':'orange', 'VII':'pink'}, fig_name='figures/sarno.png'):
    '''
    Plots the 2d-reduced vectors corresponding to each chord. Colours each point according to the 
    key it's in, and to its base note.
    
    Input.  wv_red: a dictionary mapping a chord (string) to a list of 2 coordinates.
            dimred_method: the method was used for dimensionality reduction.
            plot_title: the label to display at the top of the plot.
            figsize: the size of the graph.
            dpi: the dot-per-inch of the graph.
            remove_key_mode: flag signalling whether to remove the key mode indication from the chord.
            chord_types_to_label: list containing substrings. Chords containing any of those substring will have a label with the
                                 chord name near the point in the graph.
            chord_types_not_to_label: list containing substrings. Chords containing any of those substring will not have the label.
                                      Overrides chord_types_to_label.
            label_size: the font size of the labels.
            marker_map: dictionary mapping key mode ('MAJOR'/'MINOR'/'UNSPEC') to marker.
            marker_size: the size of each marker.
            colour_map: dictionary mapping each root ('I' through 'VII') to a colour string.
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
        
    # Add labels, where required
    for chord in all_chords:
        # Skip if current chord contains a forbidden substring, or if it contains none of the allowed substrings
        forbidden = any(chord_type in chord for chord_type in chord_types_not_to_label)
        required = any(chord_type in chord for chord_type in chord_types_to_label)
        if forbidden or not required:
            continue
        x, y = wv_red[chord]
        # Remove the key mode indication, if required
        if remove_key_mode:
            chord = get_without_key_mode(chord)
        ax.annotate(chord, xy = (x, y), fontsize=label_size)

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