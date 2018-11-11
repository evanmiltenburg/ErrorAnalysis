import json
from collections import namedtuple
from tabulate import tabulate

def load_metrics(filename):
    "Function to load metrics generated using eval.sh"
    with open(filename) as f:
        # Skip the first two lines.
        for i in range(2):
            next(f)
        data = f.read()
    # We can run eval() because the generated metrics file is trusted.
    # We know that the string data is a dictionary. Eval() returns that dictionary.
    return eval(data)

def select_and_round_scores(data):
    "Select BLEU-4 and Meteor scores."
    bleu = round(data['Bleu_4'] * 100, ndigits=1)
    meteor = round(data['METEOR'] * 100, ndigits=1)
    return bleu, meteor

def get_metrics(filename):
    "Wrapper for the above functions"
    data = load_metrics(filename)
    bleu, meteor = select_and_round_scores(data)
    return (bleu, meteor)

def generate_rows():
    base_bleu, base_meteor = get_metrics('./metrics/baseline.metrics')
    rows = [['Baseline', base_bleu, '----', base_meteor, '----']]
    
    # Load the other metrics.
    comparisons = []
    metrics = get_metrics('./metrics/color-of-clothing.metrics')
    comparisons.append(('Color of clothing', metrics))
    
    metrics = get_metrics('./metrics/activity.metrics')
    comparisons.append(('Activity', metrics))
    
    metrics = get_metrics('./metrics/type-of-clothing.metrics')
    comparisons.append(('Type of clothing', metrics))
    
    metrics = get_metrics('./metrics/gender.metrics')
    comparisons.append(('Gender', metrics))
    
    metrics = get_metrics('./metrics/scene-event-location.metrics')
    comparisons.append(('Scene/event/location', metrics))
    
    for name, data in comparisons:
        bleu, meteor = data
        row = [name,
               bleu,
               round(bleu - base_bleu, ndigits=1),
               meteor,
               round(meteor - base_meteor, ndigits=1)]
        rows.append(row)
    return rows

rows = generate_rows()
table = tabulate(rows,
                 headers=['Category', 'Bleu', 'Delta', 'Meteor', 'Delta'],
                 tablefmt="latex_booktabs")
# Replace Delta by the Delta symbol.
table = table.replace('Delta', '$\\Delta$')
# The dashes result in right-alignment, because the function thinks it's a text cell.
# Let's fix that:
table = table.replace('lrlrl','lrrrr')
print(table)
