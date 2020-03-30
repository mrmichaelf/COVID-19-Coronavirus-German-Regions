def extract_x_and_y_data(data: list) -> list:
    """
    data of (x,y) -> data_x, data_y
    """
    data_x = []
    data_y = []
    for pair in data:
        data_x.append(pair[0])
        data_y.append(pair[1])
    return data_x, data_y


def extract_data_according_to_fit_ranges(data: list, fit_range_x: list, fit_range_y: list):
    # reduce the data on which we fit
    data_x_for_fit = []
    data_y_for_fit = []
    for i in range(len(data)):
        if data[i][0] >= fit_range_x[0] and data[i][0] <= fit_range_x[1] and data[i][1] >= fit_range_y[0] and data[i][1] <= fit_range_y[1]:
            data_x_for_fit.append(data[i][0])
            data_y_for_fit.append(data[i][1])
    return (data_x_for_fit, data_y_for_fit)
