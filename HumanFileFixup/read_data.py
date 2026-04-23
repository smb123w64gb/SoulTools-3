import json

# Open and read the file
with open('file_index.json', 'r') as file:
    data = json.load(file)

index_list = data['index_to_char']
human_file_indexs = data['human_files']


char_mdl_indx = []
for idx,x in enumerate(index_list):
    if(int(x)>-1):
        if(int(human_file_indexs[int(x)]['mdl_index'])>-1):
            char_mdl_indx.append(int(human_file_indexs[int(x)]['mdl_index']))
char_mdl_indx.sort()
char_mdl_indx= list(dict.fromkeys(char_mdl_indx))
dist_mdl = []
for x in range(len(char_mdl_indx)-1):
    dist_mdl.append(char_mdl_indx[x+1]-char_mdl_indx[x])
print(dist_mdl)