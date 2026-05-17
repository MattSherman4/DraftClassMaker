#- Ploting Utils -#
#_  _#
#  Gets size of scatter points with a minimall size 
def scatter_size(x):
    max_len = 800
    if len(x) > max_len:
        return (x * 200/max_len) ** 2
    else:
        return (x * 200/len(x)) ** 2