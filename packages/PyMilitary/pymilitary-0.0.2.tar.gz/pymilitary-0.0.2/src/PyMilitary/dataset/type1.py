def _read1(singled):
    data = singled.split("<br>")
    # 除去列表中的换行符
    if "\n" in data:
        n = data.index("\n")
        del data[n]
    di = dict()
    for i in data:
        mini = i.split(":",1)
        mini_dict = {mini[0]:mini[1]}
        di.update(mini_dict)
    return di