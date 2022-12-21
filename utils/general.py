def pageresult(data, page = 2, steps = 5):
    if not data.count():
        return None
    
    data_slice = [data[i:i+steps] for i in range((page*steps)-steps, data.count(), steps)]
    if len(data_slice) < page:
        return None
    return data_slice[page-1]
