import json

# Open and read the file
with open('file_index.json', 'r') as file:
    data = json.load(file)

index_list = data['index_to_char']
human_file_indexs = data['human_files']

for idx,x in enumerate(index_list):
    if(int(x)==-1):
        print("")
        pass
    else:
        print(human_file_indexs[int(x)]['mdl_index'])