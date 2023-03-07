import csv
import requests

add_list=[]
cur_list=[]

# \t is the delimiter used so that it can be used directly in google sheets.

with open("vocab.csv", "r") as vocab_file:
    csv_reader = csv.reader(vocab_file, delimiter='\t')
    for row in csv_reader:
        cur_list.append(row[0])

with open("vocab.csv", "a") as vocab_file:
    csv_writer = csv.writer(vocab_file, delimiter='\t',quoting=csv.QUOTE_NONE, quotechar='')
    for word in add_list:
        if word not in cur_list:

            req = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if req.status_code == 404:
                continue
            defs=req.json()[0]["meanings"]
            ret_lis=[word]

            for i in range(len(defs)):
                ret_str_i=""
                ret_str_i+=f"{defs[i]['partOfSpeech']}: "
                for j in range(len(defs[i]['definitions'])):
                    ret_str_i+=f" {j+1}. {defs[i]['definitions'][j]['definition']}"
                ret_lis.append(ret_str_i)
            csv_writer.writerow(ret_lis)
            cur_list.append(word)
