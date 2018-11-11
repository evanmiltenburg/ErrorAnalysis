"""
congruency.py - Emiel van Miltenburg, 2017.

This is a Flask app designed to annotate image descriptions for the Flickr30K data.
All the annotation data is represented through dictionaries. This tool outputs them
as JSON files.

The JSON files map image indices to annotations. Those indices correspond to (0-indexed)
line numbers in val_images.txt. Each line contains the filename of an image.
"""


from __future__ import unicode_literals
from flask import Flask, url_for, request, render_template, redirect
import glob
import json
from collections import defaultdict

app = Flask(__name__)

# Set variables.
IMAGE_PATH = '/static/images/'

# Get image names.
with open('val_images.txt') as f:
    validation_images = {i:line.strip() for i,line in enumerate(f)}

# Get generated sentences.
with open('./satyrid/19-sept-2016-error-analysis.dev.txt') as f:
    generated_sentences = {i:line.strip() for i,line in enumerate(f)}

# Load all the reference sentences.
def load_references(path):
    "Load all reference sentences."
    references = defaultdict(list)
    for filename in glob.glob(path):
        with open(filename) as f:
            for i,line in enumerate(f):
                references[i].append(line.strip())
    return references

references = load_references('./flickr30k_dev/reference*')

# Modify this number if you want to annotate only a subset:
total = len(references) # Change len(reference) to e.g. 100
congruency = dict()

assert len(references) == len(validation_images)
assert len(references) == len(generated_sentences)
print("Successfully loaded the data.")

def congruency_indices(d,judgment):
    "Return indices from d for all items that have a particular judgment."
    return sorted(i for i,j in d.items() if j == judgment)

@app.route('/',methods=['GET'])
def main_page(i = 0):
    """
    Main page. Might be extended to quickly go to a particular image.
    Right now it's just useful to see how the template works.
    """
    # Start at the beginning.
    return render_template('index.html',
                            number=i,
                            total=total,
                            refs=references[i],
                            generated=generated_sentences[i],
                            image=IMAGE_PATH + validation_images[i])

@app.route('/congruency/',methods=['GET','POST'])
def check_congruency():
    "Annotate descriptions for congruency."
    # We'll make use of this global variable.
    global congruency
    
    # Start at the beginning.
    if request.method == 'GET':
        # Reset the congruency dict.
        print("Resetting congruency dict.")
        congruency = dict()
        # This variable corresponds to the first image.
        i=0
    
    # If we got a POST-request.
    else:
        number = request.form['number']
        congruency[number] = request.form['congruency']
        i = int(number) + 1
        with open('congruency_data.json','w') as f:
            json.dump(congruency,f)
        # If we are done, we don't need to go to the annotation page anymore.
        if i == total:
            return render_template('done.html',
                                    message="Done! Go to 'Load Congruency' to load the JSON file!")
    
    return render_template('congruency.html',
                            number=i,
                            total=total,
                            refs=references[i],
                            generated=generated_sentences[i],
                            image=IMAGE_PATH + validation_images[i])

@app.route('/load_congruency/',methods=['GET','POST'])
def load_congruency():
    "Load a specific congruency file"
    # This method modifies the global variable 'congruency' by loading JSON data.
    global congruency
    # Dictionaries with all images judged to be congruent/incongruent.
    global congruent
    global incongruent
    # Length of those dictionaries.
    global total_congruent
    global total_incongruent
    
    if request.method == 'POST':
        filename = request.form['filename']
        with open(filename) as f:
            congruency = json.load(f)
            congruency = {int(i):judgment for i,judgment in congruency.items()}
            congruent = dict(enumerate(congruency_indices(congruency, 'congruent')))
            incongruent = dict(enumerate(congruency_indices(congruency, 'incongruent')))
            total_congruent = len(congruent)
            total_incongruent = len(incongruent)
        return render_template('load_congruency.html', loaded=True)
    return render_template('load_congruency.html')


@app.route('/inspect_congruent/',methods=['GET','POST'])
def inspect_congruent():
    "Inspect the data with a previous/next-button."
    if request.method == 'GET':
        idx = 0
    else:
        idx = int(request.form['number'])
        if request.form['target'] == 'next' and not idx == total_congruent:
            idx += 1
        elif request.form['target'] == 'previous' and not idx == 0:
            idx -= 1
    
    try:
        i = congruent[idx]
    except NameError:
        return render_template('done.html',
                                message="Please load the congruency data from disk.")
    return render_template('inspect_congruency.html',
                            task_url='/inspect_congruent/',
                            number=i,
                            congruency_index=idx,
                            total=total,
                            category_total=total_congruent,
                            refs=references[i],
                            generated=generated_sentences[i],
                            image=IMAGE_PATH + validation_images[i])

@app.route('/inspect_incongruent/',methods=['GET','POST'])
def inspect_incongruent():
    "Inspect the data with a previous/next-button."
    if request.method == 'GET':
        idx = 0
    else:
        idx = int(request.form['number'])
        if request.form['target'] == 'next' and not idx == total_incongruent:
            idx += 1
        elif request.form['target'] == 'previous' and not idx == 0:
            idx -= 1
    
    try:
        i = incongruent[idx]
    except NameError:
        return render_template('done.html',
                                message="Please load the congruency data from disk.")
    return render_template('inspect_congruency.html',
                            task_url='/inspect_incongruent/',
                            number=i,
                            congruency_index=idx,
                            total=total,
                            category_total=total_incongruent,
                            refs=references[i],
                            generated=generated_sentences[i],
                            image=IMAGE_PATH + validation_images[i])


@app.route('/categorize_incongruent/',methods=['GET','POST'])
def categorize_incongruent():
    "Categorize the incongruent descriptions according to different error categories."
    global incongruent_categories
    if request.method == 'GET':
        next_index = 0
        incongruent_categories = dict()
    else:
        # Get information about the categorized description.
        idx = int(request.form['number'])
        categorized = incongruent[idx]
        features = request.form.getlist('feature')
        print(features)
        incongruent_categories[categorized] = features
        # Write out the data.
        with open('incongruent_categorized.json','w') as f:
            json.dump(incongruent_categories, f)
        # Get the index for the next incongruent image.
        next_index = idx + 1
        if next_index == total_incongruent:
            # Show the user that we are finished.
            return render_template('done.html',
                                    message="Saved judgment data to file: incongruent_categorized.json")
    try:
        i = incongruent[next_index]
    except NameError:
        return render_template('done.html',
                                message="Please load the congruency data from disk.")
    return render_template('categorize_incongruent.html',
                            task_url='/categorize_incongruent/',
                            number=i,
                            congruency_index=next_index,
                            total=total,
                            category_total=total_incongruent,
                            refs=references[i],
                            generated=generated_sentences[i],
                            image=IMAGE_PATH + validation_images[i])


if __name__ == '__main__':
    app.debug = True
    app.run()
