import numpy as np
maximas = np.array([])
indice_maximas = np.array([], dtype=np.uint32)

for i, Y in enumerate(y_data):
    if i <= search_range:
        if Y >= max(y_data[0:i+search_range]):
            maximas = np.append(maximas, Y)
            indice_maximas = np.append(indice_maximas, i)
    elif len(y_data) - i <= search_range:
        if Y >= max(y_data[i-search_range:]):
            maximas = np.append(maximas, Y)
            indice_maximas = np.append(indice_maximas, i)
    else:
        if Y >= max(y_data[i-search_range:i+search_range]):
            maximas = np.append(maximas, Y)
            indice_maximas = np.append(indice_maximas, i)

SetData('peaks', maximas)
SetData('peak_times', x_data[indice_maximas])
