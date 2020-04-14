import os
from tqdm import tqdm

"""
Loads all fixtures in fixtures dir
"""
def loaddata(file):
    if os.path.splitext(file)[1] == '.json' and file != 'initial_data.json':
        manage_py = os.path.join( os.path.dirname( __file__ ), '../manage.py' )
        os.system(f"python {manage_py} loaddata %s" % file)

def main():
    main_dir = os.path.dirname(__file__)
    fix_dir = os.listdir(main_dir + '../app/fixtures/')
    for each in tqdm(fix_dir):
        loaddata(each)

if __name__ == "__main__": 
    main()