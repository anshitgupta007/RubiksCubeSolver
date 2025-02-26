from src import solver 
from vision import cam


def main():

    mycube = cam.getcube()
    if mycube is None:
        return
   
    solver.solve(mycube)
if __name__ == "__main__":
    main()

