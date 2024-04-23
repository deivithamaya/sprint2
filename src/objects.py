from sklearn.pipeline import Pipeline
import os
from pathlib import Path

def main() -> None:
    #print(dir(os))
    #print(os.getcwd())
    path = str(Path(__file__).parent.parent) 
    if not 'objects' in os.listdir(path):
        print("the folder is not exists")
        os.mkdir(path + '/objects')
    else:
        path += '/objects'
        if len(os.listdir(path)):
            listOfNameObjects = os.listdir(path)
        else:
            print("there is nothing")

if __name__=='__main__':
    main()
