from collections import namedtuple
from csv import DictReader
from typing import List, Dict, Union


def read_csv(file_path: str) -> List:
    """Reads a csv file and returns a list of Ordered Maps
    """
    with open(file_path, 'r') as csv_file:
        reader = DictReader(csv_file, delimiter=',')
        return list(reader)


# TODO: modify sorted, only if it is necessary.

def country_dict(csv_data: List[Dict]) -> List[Union[dict, List[dict]]]:
    """
    calculate the average length of regions
    :param csv_data: A csv with the regions
    :return: list csv with the average length on region
    """
    countries = dict()
    sample = namedtuple("sample", "id length")
    for i, test in enumerate(csv_data):
        id_sample, location, length = (i,
                                       test.get("Geo_Location", " "),
                                       test.get("Length", 0))
        countries.setdefault(location, [])
        countries[location].append(sample(id_sample, length))
    countries_ordered = {x: sorted(countries[x],
                                   key=lambda s: s.length)
                         for x in countries}
    average_samples = {c: countries_ordered[c][len(countries_ordered[c]) // 2]
                       for c in countries_ordered}
    target_samples = [csv_data[x.id] for x in average_samples.values()]
    return target_samples


def get_average_id(values):
    sorted_values = sorted(values, key=lambda x: x[1])
    average_value = sorted_values[len(values) // 2]
    sample_id = average_value[0]
    return sample_id


def filter_country_average_length(data: List[Dict]) -> List[Dict]:
    country_dict = dict()
    for sample in data:
        # Creem les llistes de tuples id-length
        rna_id, country, length = sample['Accession'], sample['Geo_Location'], sample['Length']
        country_dict.setdefault(country, []).append((rna_id, length))
    # Transformem el diccionari a una llista de average_ids
    average_ids = [get_average_id(country_dict[country]) for country in country_dict]    
    # Filtrem la llista de input
    return list(filter(lambda sample: sample['Accession'] in average_ids, data))
