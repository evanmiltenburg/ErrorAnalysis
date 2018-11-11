"""
Corrections.py - Emiel van Miltenburg, 2017.

This script loads the congruent and incongruent descriptions, and asks the user
to correct (a subset of) the incongruent descriptions. The output is a .txt file
with one description on each line, in the same order as the original descriptions.
"""
from __future__ import unicode_literals
from flask import Flask, url_for, request, render_template, redirect
import glob
import json

def load_annotations_json(filename):
    "Function to load annotation files, and turns the keys into integers."
    with open(filename) as f:
        data = json.load(f)
        annotations = {int(i): result for i,result in data.items()}
    return annotations

################################################################################
# Main variables.

IMAGE_PATH = '/static/images/'

# Get image names.
with open('val_images.txt') as f:
    validation_images = {i: IMAGE_PATH + line.strip() for i,line in enumerate(f)}

with open('./satyrid/19-sept-2016-error-analysis.dev.txt') as f:
    generated = {i:line.strip() for i,line in enumerate(f)}

total = len(generated)
incongruent = load_annotations_json('./annotations_emiel/incongruent_final.json')
modified_descriptions = generated.copy()

####################################################
# MODIFY THIS LINE TO ANNOTATE A DIFFERENT CATEGORY:
categories_to_annotate = {'scene/event/location'}
####################################################

# Prepare filename, and prevent bad characters to be in there.
target_file = '_'.join(categories_to_annotate) + '_fixed.txt'
target_file = target_file.replace(' ', '-')
target_file = target_file.replace('/', '-')

# Create to do list.
todo = [i for i,cats in incongruent.items() if set(cats) & categories_to_annotate]
print('category:', categories_to_annotate, len(todo), 'items to correct.')
################################################################################

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def main_page(i = 0):
    """
    Annotation page.
    """
    if request.method == 'POST':
        global modified_descriptions
        modified_index = int(request.form['number'])
        modified_description = request.form['description']
        print('Modifying description with index', modified_index)
        print('Old description:', modified_descriptions[modified_index])
        print('New description:', modified_description)
        modified_descriptions[modified_index] = modified_description
    
    global todo
    try:
        i = todo.pop()
        print('Preparing to display:', i)
    except IndexError:
        with open('./fixed/' + target_file, 'w') as f:
            for i, description in sorted(modified_descriptions.items()):
                f.write(description + '\n')
        return "Done."
    
    relevant_categories = set(incongruent[i]) & set(categories_to_annotate)
    return render_template("corrections.html",
                           image = validation_images[i],
                           index = i,
                           description = generated[i],
                           categories = ' '.join(relevant_categories),
                           all_categories = incongruent[i]
                           )

if __name__ == '__main__':
    app.debug = True
    app.run()
