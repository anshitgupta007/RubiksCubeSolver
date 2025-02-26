from src import solver 
from vision import cam
from src import cube


def main():
    mycube = cam.getcube()
   
    solver.solve(mycube)
if __name__ == "__main__":
    main()

