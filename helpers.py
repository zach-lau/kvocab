import csv

def write_out(outfile, word_dict):
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for pair in sorted(word_dict.items(),key = lambda x : x[1], reverse=True):
            pos_pair, count = pair
            word, pos = pos_pair
            writer.writerow([word, pos, count])