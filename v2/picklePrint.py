import pickle

print('=========================================')
print('Current Operation Mode\n')
print(pickle.load(open('pickles/current.p', 'rb')))

print('=========================================')
print('Hour Modes\n')
print(pickle.load(open('pickles/hourModes.p', 'rb')))

print('=========================================')
print('LMP\n')
print(pickle.load(open('pickles/LMP.p', 'rb')))

'''
print('=========================================')
print('Meter Data (Not recommended)\n')
print(pickle.load(open('pickles/meter.p', 'rb')))
'''
