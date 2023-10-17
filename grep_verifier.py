import os
import subprocess
import sys
def main():
    directory_to_loop = "to_delete/"
    with os.scandir(directory_to_loop) as it:
        for entry in it:
            if entry.is_file():
                with open(entry.path, 'r') as file:
                    for line in file:
                        classname = line.strip('\n')
                        command = fr"""grep -r '/Users/kaka/OpenSource/oppia' --include '\*.html' -e '{classname}"""
                        result = subprocess.run(command)
                        if result != '':
                            print(classname, "is found")


if __name__ == '__main__':
    main()