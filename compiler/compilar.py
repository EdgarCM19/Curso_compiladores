import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compilador para el lenguaje Arduino')
    parser.add_argument('file_name', metavar='FILE_NAME', type=str, help='Name of file to compile')

    args = parser.parse_args()  

    

