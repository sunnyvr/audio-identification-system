import os
import numpy as np
from fingerprint import fingerprintBuilder
from pick import loadpickle
from tqdm.auto import tqdm
from collections import Counter, defaultdict


def get_offsets(q, db):

    offsettime = defaultdict(list)  #Offset value for every hash

    for feature in q:
        if feature in db.data:
            datast = db.data[feature][0]
            qst = q[feature]
            identity = db.data[feature][1]
            title = db.title[identity]
            time_offset = datast - qst
            offsettime[title].append(time_offset)

    return offsettime


def match(queryfile, db):

    d = db.fingerprint(queryfile)
    time_offsets = get_offsets(d, db)
    scoring = Counter()  

    for title in time_offsets:
        trackoffsets = time_offsets[title]
        offsetcount = Counter()

        for offset in trackoffsets:
            offsetcount[offset] += 1

        counts = sorted(offsetcount.values())
        scoring[title] = counts[-1] #this has the most relavent audio that was matched
        
    return scoring.most_common()[:3]  #returns top three matched outputs


#Query matching
def audioIdentification(querysetPath, indexfile, outfile):
    db = load_pickle(indexfile)
    f = open(outfile, 'w')

    for queryfile in tqdm(os.listdir(querysetPath)):
        tmatch = match(querysetPath+'/'+queryfile, db)

        #Top 3 best matches are outputed in the .txt file
        output_line = queryfile + '\t'
        for matches in tmatch:
            output_line = output_line + matches[0] + '\t'
        f.write(output_line+'\n')
        
