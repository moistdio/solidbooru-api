def pageresult(data, page = 2, steps = 5):
    count = data.count()

    if not count or page <= 0:
        return None

    if page*steps < count:
        count = page*steps
    
    data_slice = [data[i:i+steps] for i in range((page*steps)-steps, count, steps)]

    if len(data_slice) is 0:
        return None

    return data_slice[0]
