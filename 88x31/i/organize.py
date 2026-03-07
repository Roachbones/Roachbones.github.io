import json
from os import listdir


with open('meta.json') as f:
    metadata = json.load(f)

for filename in listdir('.'):
    if filename.endswith('.py') or filename.endswith('.json'): continue
    if filename not in [m['src'] for m in metadata]:
        print('Unsorted file:',filename)
        metadatum = {'src':filename}
        while 1:
            i = input(' attr value:')
            if not i: break
            if ' ' not in i: continue
            attr, attr_val = i.split(' ',maxsplit=1)
            metadatum[attr] = attr_val
        if len(list(metadata))>1:
            metadata.append(metadatum)

with open('meta.json','w') as f:
    json.dump(metadata,f,indent=1)
