from pathlib import Path

results_dict = {}

filename = input()

raw_file = Path(__file__).parent.resolve() / filename

with open(raw_file, 'r') as document:
    file_reader = document.readlines()
    
    for index, seasons in enumerate(file_reader):
        if index % 2 == 0 or index == 0:
            if seasons in results_dict:
                results_dict[seasons].append(file_reader[index + 1])
            else:
                results_dict[seasons] = [file_reader[index + 1]]
    
output_keys = Path(__file__).parent.resolve() / 'output_keys.txt'

with open(output_keys, 'w') as output_doc:
    sorted_dict = dict(sorted(results_dict.items()))
    
    for keys in sorted_dict:
        if len(sorted_dict[keys]) > 1:
            for values in sorted_dict[keys]:
                if values == sorted_dict[keys[-1]]:
                    output_doc.write(sorted_dict[keys])
                else:
                    output_doc.write(f'{sorted_dict[keys]}; ')
        else:
            output_doc.write(sorted_dict[keys])
            
output_titles = Path(__file__).parent.resolve() / 'output_titles.txt'

with open(output_titles, 'w') as output_doc:
    sorted_dict = dict(sorted(results_dict.values()))
    for values in sorted_dict:
        output_doc.write(f'{values}\n')