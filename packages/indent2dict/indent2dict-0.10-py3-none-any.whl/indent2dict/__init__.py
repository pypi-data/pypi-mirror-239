from collections import defaultdict
from functools import cache
from itertools import takewhile
from nested2nested import nested_list_to_nested_dict
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from splitlistatindex import list_split


class subi(dict):
    def __missing__(self, k):
        self[k] = self.__class__()
        return self[k]


def indent2dict(data, removespaces):
    r"""
    Convert an indented text or list of strings into a nested dictionary structure based on the indentation levels.

    Args:
        data (str, bytes, or list): The input data to be converted into a nested dictionary. It can be a string, bytes,
            or a list of strings.
        removespaces (bool): If True, leading and trailing whitespaces in the strings will be removed when constructing
            the dictionary keys. If False, whitespaces will be preserved.

    Returns:
        dict: A nested dictionary structure where each level is determined by the indentation in the input data.
            The structure represents a hierarchy of items based on the indentation levels.

    Example:
        input_data = [
            "Category 1",
            "  Subcategory 1.1",
            "    Item 1.1.1",
            "  Subcategory 1.2",
            "Category 2",
            "  Item 2.1",
        ]

        result = indent2dict(input_data, removespaces=True)

        The 'result' will be:
        {
            'Category 1': {
                'Subcategory 1.1': {'Item 1.1.1': 0},
                'Subcategory 1.2': 1
            },
            'Category 2': {'Item 2.1':2}
        }
    """

    @cache
    def strstrip(x):
        return x.strip()

    def convert_to_normal_dict_simple(di):
        globcounter = 0

        def _convert_to_normal_dict_simple(di):
            nonlocal globcounter
            globcounter = globcounter + 1
            if not di:
                return globcounter
            if isinstance(di, subi):
                di = {k: _convert_to_normal_dict_simple(v) for k, v in di.items()}
            return di

        return _convert_to_normal_dict_simple(di)

    def splitfunc(alli, dh):
        def splifu(lix, ind):
            try:
                firstsplit = [n for n, y in enumerate(lix) if y[0] == ind]
            except Exception:
                return lix
            result1 = list_split(l=lix, indices_or_sections=firstsplit)
            newi = ind + 1
            splitted = []
            for l in result1:
                if newi < (lendh):
                    if isinstance(l, list):
                        if l:
                            la = splifu(l, newi)
                            splitted.append(la)
                    else:
                        splitted.append(l)
                else:
                    splitted.append(l)
            return splitted

        lendh = len(dh.keys())
        alli2 = [alli[0]] + alli
        return splifu(alli2, ind=0)

    if isinstance(data, (str, bytes)):
        da2 = data.splitlines()
    else:
        da2 = list(data)

    d = defaultdict(list)
    dox = da2.copy()
    dox = [x for x in dox if x.strip()]
    for dx in dox:
        eg = len(dx) - len(dx.lstrip())
        d[eg].append(dx)

    dh = {k: v[1] for k, v in enumerate(sorted(d.items()))}

    alli = []
    for xas in dox:
        for kx, kv in dh.items():
            if xas in kv:
                alli.append([kx, xas])
                break

    iu = splitfunc(alli, dh)

    allra = []
    d = nested_list_to_nested_dict(l=iu)
    lookupdi = {}
    for iasd, ius in enumerate((q for q in fla_tu(d) if not isinstance(q[0], int))):
        if iasd == 0:
            continue
        it = list(takewhile(lambda o: o == 0, reversed(ius[1][:-2])))
        it = ius[1][: -2 - len(it)]
        allra.append([it, ius[0]])
        lookupdi[it] = ius[0]

    allmils = []
    for im, ls in allra:
        mili = []
        for x in reversed(range(1, len(im) + 1)):
            mili.append(lookupdi[im[:x]])
        mili = tuple(reversed(mili))
        allmils.append(mili)
    allmilssorted = sorted(allmils, key=len, reverse=True)
    countdict = defaultdict(int)
    difi = subi()
    allmilssorted = [
        tuple(map(strstrip, x) if removespaces else x) for x in allmilssorted
    ]
    for ixas in allmilssorted:
        for rad in range(len(ixas) + 1):
            countdict[ixas[:rad]] += 1
    for key, item in countdict.items():
        if item != 1:
            continue
        vaxu = difi[key[0]]
        for inxa, kax in enumerate(key):
            if inxa == 0:
                continue
            vaxu = vaxu[kax]
    difi2 = convert_to_normal_dict_simple(difi)
    return difi2


