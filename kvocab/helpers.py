import csv

def write_out(outfile, word_dict):
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for pair in sorted(word_dict.items(),key = lambda x : x[1][0], reverse=True):
            pos_pair, data = pair
            word, pos = pos_pair
            count, example = data
            writer.writerow([word, pos, count, example])
            