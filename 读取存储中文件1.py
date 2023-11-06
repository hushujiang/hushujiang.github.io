import os

'''
This hacks the python built-in function "open" which add some pre-processing for file operations
to allows the program runs locally and in the Agit environment without modifications.
'''
if 'CLOUD_PROVIDER' in os.environ and os.environ['CLOUD_PROVIDER'] == 'Agit':
    from agit import open # override the open function
    dataset_path = 'agit://' # data path in the Agit cloud environment
else:
    dataset_path = './dataset/' # data path for local running

'''
Agit Datasets only allow read-only mode, the default mode "r" (open for reading text, synonym of "rt")
and "rb " (open for reading binary) are available.
'''
with open(dataset_path + 'datafile.txt', mode='rb', encoding=None) as file:
    print(file.read())