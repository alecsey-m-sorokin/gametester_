import json


def findall(v, k):
    if type(v) == type({}):
        for k1 in v:
            if k1 == k:
                print(v[k1])
                return v[k1]
            result = findall(v[k1], k)
            if result is not None:
                return result

    if type(v) == type([]):
        for k1 in v:
            result = findall(k1, k)
            if result is not None:
                return result


with open('c:/testing/response2.json') as json_file:
    data = json.load(json_file)
    data_str = json.dumps(data)

    results = findall(data, "WinStateInfo")

    print(results["WinState"])
    print(results["FreeSpinCount"])
    print(results["Multiplier"])

# print(json.dumps(data, indent=2))
