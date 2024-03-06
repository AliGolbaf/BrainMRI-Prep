import os
import subprocess

root_dir = os.path.dirname(os.path.abspath(__file__))
script   = root_dir + '/script.py' 

def main():
    subprocess.run(["python", script])


if __name__ == "__main__":
    main()
