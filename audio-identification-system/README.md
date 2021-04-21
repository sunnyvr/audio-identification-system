# audio-identification-system
Audio Identification system with fingerprinting of provided audio files, implementing the algorithm presented by [Wang 2003](https://www.researchgate.net/publication/220723446_An_Industrial_Strength_Audio_Search_Algorithm). 
This is the approach that Shazam took when it initially started, but as we know today - its the best music detecting application yet.

## Code

* audioidentification.py - Indexes query and matches with fingerprints in database.
* fingerprint.py - Indexes database audio files as audio fingerprints.
* main.py - Runs the two main functions (fingerprintBuilder and audioIdentification)
* pick.py - Stores the fingerprints in database .pickle format.


## Setup
Run
```
main.py
```
A database of fingerprints can be constructed from a folder of audio documents as follows:

```python
from fingerprint import fingerprintBuilder

fingerprintBuilder('data/database_recordings', 'data/fingerprints/output.pickle')
```

A folder of queries can then be identified, and the top three results for each stored in a text file as follows:

```python
from audioidentification import audioIdentification

audioIdentification('data/query_recordings', 'data/fingerprints/output.pickle', 'data/output.txt')
```


### Input

* database_recordings - This has audio files of the GTZAN dataset.
* query_recordings - This has audio files from the same subset with background noise.


### Output


* data/fingerprints/output.pickle - Stores arrays of audio fingerprints in '.pickle' format.
* data/output.txt - Stores the top 3 matches for the query recording.
