"""
whatIwant.tools
Lucas A. Gerber
"""


import os, math


def verbosePrint(verbose, statement):
    if verbose:
        print(statement)


def numGen():
    i = 0
    while True:
        yield i
        i += 1


def createDestination(result_path, output_name, output_type):
    destination = result_path + '/' + output_name + '.' + output_type
    log_destination = result_path + '/' + output_name + '.csv'
    
    i = (i+1 for i in numGen())
    while os.path.exists(destination):
        destination = result_path + '/' + output_name + str(next(i)) + '.' + output_type
        log_destination = result_path + '/' + output_name + str(next(i)) + '.csv'
        
    return destination, log_destination


def collectFiles(path_s, file_extension_s, weighted=False):
    
    if type(file_extension_s) is str:
        file_extension_s = [file_extension_s]

    if type(path_s) is str:
        path_s = [path_s]
        
    file_name_list = [path + '/' + file for path in path_s for file in os.listdir(path) if file.split('.')[-1] in file_extension_s]

    if weighted:
        total_weight = sum([os.stat(file_name).st_size for file_name in file_name_list])
        file_name_list_weighted = list()
        for file_name in file_name_list:
            weight = min(math.ceil(os.stat(file_name).st_size * 100 / total_weight), 20)
            file_name_list_weighted.extend([file_name] * weight)
        return file_name_list_weighted
    
    return file_name_list


def yesInput(message):
    text = input(message)
    if 'y' in text.lower().strip():
        yes_param = True
    elif 'n' in text.lower().strip() or not text:
        yes_param = False
    else:
        print('>>Please enter yes or no.')
        yes_param = yes_input(message)

    return yes_param


def main():
    pass


if __name__ == '__main__':
    main()
