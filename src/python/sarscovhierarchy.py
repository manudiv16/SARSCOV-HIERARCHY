from sys import argv, exit
from os.path import join
from utils.csv_table import CsvTable
from utils.fasta_map import FastaMap

if __name__ == '__main__':
    if len(argv) != 2:
        print("python sarscovhierarchy.py <directory>")
        exit()
    data_dir = argv[1]
    csv_path = join(data_dir, "sequences.csv")
    fasta_path = join(data_dir, "sequences.fasta")

    csv_table = CsvTable(csv_path).group_by_country()
    print(csv_table)

    # ids = csv_table.values('Accession')

    # fasta_map = FastaMap(fasta_path) \
    #            .filter(lambda item: item[0] in ids)

    # fasta.group_samples(csv_table)
