import os
import signal
from os.path import join
from sys import argv

from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap

signal.signal(signal.SIGTSTP, signal.SIG_IGN)


def main():
    data_dir = argv[1]
    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    print("\nReading and processing files...")
    csv_table = CsvTable(csv_path).group_countries_by_median_length()
    ids = csv_table.values('Accession')
    fasta_map = FastaMap(fasta_path).filter(lambda item: item[0] in ids)
    csv_table = csv_table.dict_by_id()
    print("Files processing finished!")

    print("\nBuilding hierarchy...")
    fasta_map.build_hierarchy(csv_table)
    print("Done!")


if __name__ == '__main__':
    if len(argv) == 2:
        pid_h = os.fork()
        if pid_h == 0:
            main()
        else:
            try:
                os.wait()
            except KeyboardInterrupt:
                os.kill(pid_h, signal.SIGKILL)
                print("\nshutdown")
    else:
        print("python sarscovhierarchy.py <data_path>")
