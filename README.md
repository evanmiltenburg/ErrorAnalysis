# ErrorAnalysis

This repository provides code and data for our unpublished error analysis of an attention-based image description model.
If you use this work, please cite:

```
@article{DBLP:journals/corr/MiltenburgE17,
  author    = {Emiel van Miltenburg and
               Desmond Elliott},
  title     = {Room for improvement in automatic image description: an error analysis},
  journal   = {CoRR},
  volume    = {abs/1704.04198},
  year      = {2017},
  url       = {http://arxiv.org/abs/1704.04198},
  archivePrefix = {arXiv},
  eprint    = {1704.04198},
  timestamp = {Mon, 13 Aug 2018 16:48:09 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/MiltenburgE17},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
}
```

## Requirements
* Python 3.6 or higher.
* Flask 1.0.2
* Tabulate 0.8.2 (only for visualizing the results in our paper)

## How to use this repository

### The annotation task

* Run `python congruency.py`
* Go to http://127.0.0.1:5000/ in your browser to start annotating.

You will see a screen with several menu items:

* **Home**: This is the start page.
* **Congruency**: This page shows the coarse-grained annotation task.
* **Load congruency data**: This page allows you to load annotations from another annotator. To load the annotations from our main annotator, enter "annotations_emiel/congruency_data_final.json".
* **Inspect congruent**: This page allows you to leaf through the congruent descriptions.
* **Inspect incongruent**: This page allows you to leaf through the in congruent descriptions.
* **Categorize incongruent**: This page shows the second annotation task, which is to categorize to errors from the incongruent descriptions.

### The correction task

* As the file suggests, modify line 38 to annotate corrections, and save the file.
```python
# MODIFY THIS LINE TO ANNOTATE A DIFFERENT CATEGORY:
categories_to_annotate = {'scene/event/location'}
```
* Run `python corrections.py`
* Go to http://127.0.0.1:5000/ in your browser to start correcting the errors.
* Once you're done, the results will be stored in `./fixed/CATEGORY_fixed.txt`.

### Evaluating the results

The file `eval.sh` contains all commands to evaluate the results using the MS COCO evaluation scripts (also included in this repository).
It assumes that there is a Python 2 environment, created using Anaconda, called 'python2'. This is because the MS COCO evaluation scripts do not work well with Python 3.
To use this script, run: `bash eval.sh`

### Printing the evaluation scores

Run `python generate_metrics_table.py` to print the table from our paper.
