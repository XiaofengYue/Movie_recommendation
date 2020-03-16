x2 = []
with open('users.txt','r') as f:
    x = f.read().split('\n')
    print(len(x))
    x2 = list(set(x))
    print(len(x2))

with open('users3.txt','a') as f:
    x = '\n'.join(x2)
    f.write(x)