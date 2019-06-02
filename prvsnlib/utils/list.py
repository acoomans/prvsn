
def unique(l):
    s = set()
    r = []
    for x in l:
        if x not in s:
            s.add(x)
            r.append(x)
    return r
