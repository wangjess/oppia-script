"""Module that will extract the class names from valid *.css files."""

import os
import shutil
from pathlib import Path
import tinycss2
import subprocess
import sys

log_file = 'log.txt'


def install_bs4():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])

def get_classes(contents, filename):
    """Gets classes and writes to filename.

    Args:
        contents: the contents of the *.css file.
        filename: the file to output class names.
    Returns:
        Number of classes found.

    """
    exclusions = ['a', 'li', 'ul', 'p', 'focus', 'h5']
    classes = []

    # A list of QualifiedRules
    rules = tinycss2.parse_stylesheet(
        contents, skip_comments=True, skip_whitespace=True)
    for rule in rules:
        if rule.type == 'qualified-rule':  # handles typical classname selectors
            for val in rule.prelude:
                if val.type == 'ident':
                    if val.value not in exclusions:
                        classes.append(val.value)
        elif rule.type == 'at-rule':  # handles @ rules, gets classnames defined within
            for val in rule.content:
                if val.type == 'ident':
                    if val.value not in exclusions:
                        classes.append(val.value)
    # Get unique set
    new_classes = set(list(set(classes)))
    with open(filename, 'a') as log:
        for val in new_classes:
            print(val, file=log)

    return len(new_classes)


def main():
    print('Start!')

    try:
        from bs4 import BeautifulSoup
    except:
        install_bs4()
        from bs4 import BeautifulSoup

    # Obtain all valid *.css files:
    # Ignore files in third_party/, node_modules/, dist/, scripts/ and .direnv/
    # Only those in /core/ and /extensions/ are fair game.
    css_files = []
    with os.popen("find '/Users/kaka/OpenSource/oppia' -name '*.css' ! -path '*/webpack_bundles/*' ! -path '*/node_modules/*' \
                  ! -path '*/third_party/*' ! -path '*/dist/*' ! -path '*/scripts/*' \
                  ! -path '*/.direnv/*'") as pipe:
        for line in pipe:
            css_files.append(line.strip('\n'))

    # Delete & re-create output/ folder
    if os.path.isdir("output"):
        shutil.rmtree("output", ignore_errors=True)
        os.mkdir("output")
    else:
        os.mkdir("output")

    # Print data to log.txt
    with open(log_file, 'a', encoding='UTF-8') as f:
        print('# total valid css_files:', len(css_files), file=f)

    # Obtain classes from each *.css file
    for f in css_files:
        # Create corresponding output files
        filename = Path(f).name
        out_f = filename[0:filename.find('.')] + '_classes.txt'
        if out_f == "about-page_classes.txt":
            print("OK")
        final_out = "output/" + out_f

        with open(f, 'r', encoding='UTF-8') as file:
            file_contents = file.read()
            num_classes = get_classes(file_contents, final_out)
            with open(log_file, 'a') as log:
                print('==================================', file=log)
                print(f, file=log)
                print(num_classes, file=log)

    # Parse output/ and report findings in to_delete/ (contains unused classes)
    # Delete & re-create to_delete/ folder
    if os.path.isdir("to_delete"):
        shutil.rmtree("to_delete", ignore_errors=True)
        os.mkdir("to_delete")
    else:
        os.mkdir("to_delete")

    # Get all HTML files inside oppia/ project root folder
    all_classes = []
    with os.popen("find '/Users/kaka/OpenSource/oppia' -name '*.html'") as pipe:
        for line in pipe:
            html_file = line.strip('\n')
            try:
                with open(html_file, 'r') as file:
                    html_as_string = file.read()
                    soup = BeautifulSoup(html_as_string, 'html.parser')
                    for element in soup.find_all(class_=True):
                        all_classes.extend(element["class"])
            except AttributeError as err:
                print(err, html_file)

    # Only get unique list of classes
    all_classes = sorted(list(set(all_classes)))
    if "conversation-skin-future-tutor-card" not in all_classes:
        print("NOT FOUND")

    # Search for class usage in HTML files
    directory_to_loop = "output/"
    with os.scandir(directory_to_loop) as it:
        for entry in it:
            if entry.is_file():
                with open(entry.path, 'r') as file:
                    for line in file:
                        # if file.name == 'output/tutor-card_classes.txt':
                        #     print("STOP HERE")
                        if line.strip('\n') not in all_classes:
                            # if line.strip('\n') == 'conversation-skin-future-tutor-card':
                            #     print("FOUND GUY")
                            findings = 'to_delete/' + entry.name
                            fp = open(findings, 'w')
                            fp.write(line)
                            fp.close()

    # Call helper script to manually grep



if __name__ == '__main__':
    main()
