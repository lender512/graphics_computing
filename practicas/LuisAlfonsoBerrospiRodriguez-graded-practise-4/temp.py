N = 6

import os

for i in range(N):
    folder = f"exercise{str(i+1).zfill(2)}"
    os.mkdir(folder)
    #create solution.py inside folder
    with open(f"{folder}/solution.py", "w") as f:
        f.write("# Solution goes here")
    