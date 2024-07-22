import glob
import os
import numpy as np
from Bio import motifs
from app.utils.utils import *


def ensure_directory_exists(directory):
    """Ensure that a directory exists, and create it if it does not."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created.")
    else:
        print(f"Directory {directory} already exists.")


def pwm2pssm(FPM, psw):
    """Return TF name and his PositionSpecificScoringMatrix object from a .jaspar file and
    a given PositionWeigthMAtrix object.
    """
    motifs_dir = "./data/motifs"

    # Ensure the motifs directory exists
    ensure_directory_exists(motifs_dir)

    # Download the motif
    download_motif(FPM, motifs_dir)

    motif_file_path = os.path.join(motifs_dir, f"{FPM}.jaspar")

    with open(motif_file_path) as handle:
        m = motifs.read(handle, "jaspar")

    # Debug: Print motif information
    print(f"Motif {FPM}:")
    print(m.counts)

    # Get the PSSM from PSW.
    pssm = m.counts.normalize(pseudocounts=psw).log_odds()

    return pssm, m.name


def scan_sequence(pssm, seq, scorethreshold):
    """Return a list of tuples with position and score of hits in the promotor sequences with the psw that are
    greater or equal to the given scorethreshold.

    Note: both=False refers to only positions on the positive strand.
    """
    results = list(pssm.search(seq, threshold=scorethreshold, both=True))

    # Debug: Print scan results
    print(f"Scanning sequence {seq[:30]}... for threshold {scorethreshold}")
    for position, score in results:
        print(f"Position: {position}, Score: {score}")

    return results


def scan_all_sequences(pssm, list_seq, scorethreshold):
    """Create a dictionnary of couple position/score for multiple sequences.

    It uses scan_sequence(pssm, seq, scorethreshold) compute for each seq the position and score of the TBFS hits,
    store them into a dictionnay with the key being the sequence id and values the list of (position/score).
    """

    data_struct = dict()
    # Returns a list of SeqIO object from a list of.
    seq_obj_list = Seq_obj_from_files(list_seq)

    for seq_object, mrna in zip(seq_obj_list, mRNAs):
        data_struct[mrna] = scan_sequence(
            pssm, seq_object.seq, scorethreshold
        )  # -> {id1:[(pos,score,),...],id2:[(pos2,score2),..],....}
    return data_struct


# def score_window(sas, start, end):
#     """Scan a window between a start and end positions ( points ).

#     This function uses the sliding window algorithm to analyze a certain window between a starting and ending
#     points. The main algorithm ( approach ) used to calculate the score, is to check if hits (occurences) of a set
#     of genes are near to each other; For instance, we can say that to points are in a proximity if their distance is
#     close to zero. So we calculate the diffrence like this : diff = abs(pointA - pointB), then we campute a score on the difference:
#                      A -> 1 ( 100 %)
#                      B -> x ( ?% )
#                      diff = abs ( A - B )
#                      x = diff/B
#     Here x means the percentage of the distance between A and B, if x is less or equal then the third of the window size / 100 ( to get
#     the percentage ), then A is near to B, else A is not in proximty of B, those occurences are far from each other and the score of this window
#     is not the preferead score ( see best_window ).
#     It returns start, end , sum(scores), and widow info. The window info contains the hits of the sequences.
#     """

#     samples = list()  # A list to hold samples from each sequences.
#     # A list to hold scores of distances between elements of consecutive rows.
#     percentage = list()
#     # A list to hold all the scores that are less or equal than a percentage threshold.
#     occurences = list()
#     i = 0  # Index.
#     r = 0  # Rows.
#     window_info = dict()

#     # Iterate througth our dict of seq object.
#     for item in sas:
#         # For each sequence, create a row.
#         row = []
#         # Iterate througth pos,score in each sequence.
#         for position, score in sas[item]:
#             # If the position is neg, it means we are in the - srand.
#             window_info[item] = position, score
#             if position < 0:
#                 # Calculate the correcte position.
#                 # position = prom_len + position + 1
#                 # If the algorithm finds a occurence in the window, then
#                 # append it to the row.
#                 if (prom_len + position + 1) >= start and (
#                     prom_len + position + 1
#                 ) < end:
#                     row.append(prom_len + position + 1)
#             else:
#                 # Same as above but in the + srand.
#                 neg_srand = False
#                 if position >= start and position < end:
#                     row.append(position)
#         # If we have non-empty row,
#         # add it to the samples.
#         if row != []:
#             samples.append(row)
#             r += 1  # Increment the rows.
#         else:
#             pass

#     # If non-empty samples.
#     if samples != []:
#         # For each row, compare each element of it with
#         # the next row, and so on.
#         for i in range(r - 1):
#             curr_row = samples[i - 1]
#             next_row = samples[i]
#             for e in curr_row:
#                 for n in next_row:
#                     # Calculate the distence between two positions.
#                     diff = abs(e - n)
#                     # Give a percentage like score for the difference,
#                     # Then add it to the percentage list.
#                     percentage.append(diff / n)
#             # For each elements of percentage, take only those with
#             # a value less or equal then threshold, i.e that all this values
#             # are in proximity.
#             occurences = [x for x in percentage if x < seuil]
#     # Sum up the score for this window.

#     return start, end, sum(occurences), window_info


import numpy as np


def score_window(sas, start, end):
    """Scan a window between a start and end positions (points).

    This function uses a sliding window algorithm to analyze a window between starting and ending points.
    The main approach is to calculate the distance between occurrences (hits) of TFBS and compute a score based on proximity.

    Returns start, end, sum(scores), and window info.
    """

    samples = []  # List to hold samples from each sequence.
    window_info = (
        {}
    )  # Dictionary to hold positional information and scores for each sequence.

    # Iterate through the sequences and collect positions within the window.
    for item in sas:
        row = []
        for position, score in sas[item]:
            adjusted_position = prom_len + position + 1 if position < 0 else position
            if start <= adjusted_position < end:
                row.append(adjusted_position)
                window_info[item] = (position, score)
        if row:
            samples.append(row)

    if not samples:
        return start, end, 0, window_info

    # Convert samples to a NumPy array for vectorized operations.
    samples = [np.array(row) for row in samples]
    num_rows = len(samples)

    # Calculate scores based on proximity.
    scores = []
    for i in range(num_rows - 1):
        curr_row = samples[i]
        next_row = samples[i + 1]
        diff_matrix = np.abs(curr_row[:, None] - next_row)
        percentage_matrix = diff_matrix / next_row
        valid_scores = percentage_matrix[percentage_matrix < seuil]
        scores.extend(valid_scores)

    return start, end, np.sum(scores), window_info


def best_window(sas, window_size):
    """Calculate the best window score by scanning a set of sequences.

    Start from the head of sequences, and then slide througth the set, between each starting point in a sequence
    and the size of the window, calls scan_window to compute a score on this locations, then check if the score is
    lower or equal to the window threshold given as argument.

    Returns windows infos, a dictionnary with the score, start and end position and the window info on this specific location.
    """

    global seuil  # Define a global threshlod for the score_window condition.
    # Take the percentage of the third of the window size.
    seuil = (window_size / 3) / 100

    start_bw = 0  # Starting point for the best window.
    end_bw = 0  # End point for the best window.
    start = 0  # Start the scan at position 0 for all the sequences.
    bws = 0  # Define a bws for the scans.
    tmp = 0
    end = window_size  # Set the end for the window scan.
    window_index = 1

    slide_step = 7  # Arbitrary value to indicate the slide step of the window

    windows_info = dict()

    # Scann all the sequences entil reaching the end.
    while start < (prom_len - window_size):
        # Get the score of the current window between start and end positions.
        start_curr, end_curr, curr_bws, window_info = score_window(sas, start, end)
        # Check if the current score is valid.
        if curr_bws > 0 and w_threshold > curr_bws:
            # To get ride of same value.
            if tmp != curr_bws:
                # Set it start and end window as the best start window.
                start_bw = start_curr
                end_bw = end_curr
                windows_info[window_index] = (start_bw, end_bw, curr_bws, window_info)
                window_index += 1
            tmp = curr_bws
        # Take a step further.
        start += slide_step
        end += slide_step
    return windows_info


def search_luncher(
    list_mRNA,
    jaspar_matrix_name,
    psw,
    threshold,
    len_prom,
    window_size,
    window_threshlod,
):
    """Act as a luncher for the putative_TFBS.py script.

    This function is like a main, takes all the arguments from the input from users, process
    the search, and returns TF name and a dictionnary of the winodws informations.
    """
    print("Searching for TFBS...")
    global prom_len
    prom_len = len_prom

    global w_threshold
    w_threshold = window_threshlod

    global mRNAs
    mRNAs = list_mRNA

    pssm, tf_name = pwm2pssm(jaspar_matrix_name, psw)

    # directory to store downlaoded promotors.
    file_path_sequences = "./data/sequences"

    # Check if there's no .fa file, so the program starts downloading data, else just use the data in the dir.
    if os.path.exists(file_path_sequences) and os.path.isdir(file_path_sequences):
        if not any(fname.endswith(".fa") for fname in os.listdir(file_path_sequences)):
            print("No mRNA found in the database. Downloading the file, please wait...")
            # download promoters.
            download_promotors(mRNAs, prom_len, file_path_sequences)
            print("Downloading is finished ✅")
        else:
            print("Using files from directory.")
    else:
        print("Given directory doesn't exist")
        print("Creating the '" + file_path_sequences + "' directory")
        os.makedirs(file_path_sequences)
        # download promoters.
        download_promotors(mRNAs, prom_len, file_path_sequences)
        print("Downloading is finished ✅")

    # create a list with all the files in the download directory.
    file_list = glob.glob(os.path.join(os.getcwd(), file_path_sequences, "*.fa"))
    dict_seq = scan_all_sequences(pssm, file_list, threshold)

    return tf_name, best_window(dict_seq, window_size)
