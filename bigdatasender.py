import csv
import json
import uuid

with open('cryptonews.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    poz=0
    neg=0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            data = json.loads(row[1].replace("\'", "\""))
            if data["class"] == 'positive':
                with open('poza/' + str(uuid.uuid4()) + ".txt", 'w', encoding="utf-8") as f:
                    f.write(row[5])
                poz = poz + 1
            elif data["class"] == 'negative':
                with open('nega/' + str(uuid.uuid4()) + ".txt", 'w', encoding="utf-8") as f:
                    f.write(row[5])
                neg = neg + 1
            # print(f'\t json : {data["class"]} baslik: {row[5]}.')
            line_count += 1
    print(f'poz: {poz} neg: {neg}')