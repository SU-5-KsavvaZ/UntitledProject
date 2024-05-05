import pickle
import os
full_dir = os.path.abspath('start.dat')
def start():
    with open(full_dir, 'wb') as filehandle:
        pickle.dump(True, filehandle)
def stop():
    with open(full_dir, 'wb') as filehandle:
        pickle.dump(False, filehandle)
