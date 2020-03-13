
l = []
for i in range(1,30):
    with open(str(i)+".txt",'r') as f:
        l+=f.read().split("\n")
        
with open('id.txt','a') as f:
    s = "\n".join(l)
    f.write(s)