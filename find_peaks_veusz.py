import numpy as np
maximas = np.array([])
indice_maximas = np.array([], dtype=np.uint32)

j = 1
y_data = GetData('Position (mm) Run #' + str(j))[0]
# x_data = GetData('"Time (s) Run #' + str(j) + '"')[0]
# x_data = GetData('"Time(s) Run  #1"')[0]
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

SetData('peaks' + str(j), maximas)
SetData('peak_times' + str(j), x_data[indice_maximas])
