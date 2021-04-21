from fingerprint import fingerprintBuilder
from audioidentification import audioIdentification


def exec():
    fingerprintBuilder('data/database_recordings', 'data/fingerprints/output.pickle')
    audioIdentification('data/query_recordings', 'data/fingerprints/output.pickle', 'data/output.txt')

if __name__ == '__main__':
    exec()