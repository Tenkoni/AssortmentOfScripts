import csv
import copy
import hashlib
import unidecode

route = 'routes/'

with open(route+'adapted.csv', mode='r', encoding='iso-8859-1') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    header = next(csv_reader)
    data = list(csv_reader)

full_dataset = []
repeated_dataset = []
hash_table = []

for row in data:
    m = hashlib.sha256()
    introw = row

    m.update(str(unidecode.unidecode(row[0])).encode('utf-8'))
    #m.update(str.encode(",".join(introw)))
    digest = m.digest()
    if digest not in hash_table:
        hash_table.append(digest)
        full_dataset.append(introw)
    else:
        repeated_dataset.append(introw)
        print(digest)



with open(route+"locations.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(full_dataset)

with open(route+"repeated_locations.csv", "w", newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(repeated_dataset)


