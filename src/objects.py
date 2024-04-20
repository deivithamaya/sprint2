from sklearn.pipeline import Pipeline
import os
from pathlib import Path

def main():
    #print(dir(os))
    #print(os.getcwd())
    path = str(Path(__file__).parent.parent) 
    if not 'objects' in os.listdir(path):
        print("the folder is not exists")
        os.mkdir(path + '/objects')
    #pass

if __name__=='__main__':
    main()
