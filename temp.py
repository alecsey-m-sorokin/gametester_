import json

with open('c:/testing/response2.json') as json_file:
    data = json.load(json_file)
    data_str = json.dumps(data)

print(data)
print(data_str)

userSavedState = data['SpinResult']['UserSavedState']['StepPlayerContracts'][1]['WinStateInfo']
print(userSavedState)


if 'WinStateInfo' in data_str:
    print('OK')
else:
    print('missing ...')


# print(json.dumps(data, indent=2))
