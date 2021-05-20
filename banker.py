
def LTE(vec1, vec2):
    for i in range(len(vec1)):
        if vec1[i] > vec2[i]:
            return False
    return True

n = int(input("Enter the number of threads in the system : ")) #number of threads
m = int(input("Enter the number of resources types in the system : ")) #number of resources types
#print(n, m)

print("Enter the available vector")
available = [int(i) for i in input().split()]
#print(available)

print("Enter MAX matrix")
MAX = [[int(j) for j in input().split()] for i in range(n)]
#print(MAX)

print("Enter Allocation matrix")
allocation = [[int(j) for j in input().split()] for i in range(n)]
#print(allocation)

need = list()
for i in range(n):
    lst = list()
    for j in range(m):
        entry = (MAX[i][j] - allocation[i][j])
        lst.append(entry)
    need.append(lst)   
print("Need Matrix")
for row in need:
    print(row)
#print(need)

def safe(allocation, available, need):
    global n, m
    thread_sequence = list()#----------
    work = list(available)
    finish = [0 for i in range(n)] #0 indicates false, 1=true so the sum indicate the num of true
    j=0
    while(j<n):
        for i in range(0, n):
            #print("finish", finish)
            #print("index", i, "need", need[i], "work", work)
            if(finish[i]==0 and LTE(need[i], work)):
                work = [work[j]+allocation[i][j] for j in range(m)]
                #print("new work", work)
                finish[i] = 1
                thread_sequence.append(i)#---------
                #print("Thread", i)
                break
            elif(i==n-1):
                j=n            
    if(sum(finish) == n):
        return thread_sequence
    else:
        return False

def RR(request, Ti):
    global available, allocation, need, n, m
    if(not LTE(request, need[Ti])):
        print("Thread exceeded Maximum claim")
        return False
    if(not LTE(request, available)):
        print("No, Thread must wait")
        return False
    av_temp = [available[i]-request[i] for i in range(m)]
    #print("av_temp", av_temp)
    allo_temp = [[allocation[i][j] for j in range(m)]for i in range(n)]
    allo_temp[Ti] = [allo_temp[Ti][i]+request[i] for i in range(m)]
    #print(allo_temp)
    need_temp = [[need[i][j] for j in range(m)]for i in range(n)]
    need_temp[Ti] =  [need_temp[Ti][i]-request[i] for i in range(m)]
    #print(need_temp)
    if(safe(allo_temp, av_temp, need_temp)):
        available = av_temp
        allocation = allo_temp
        need = need_temp
        return safe(allo_temp, av_temp, need_temp)
    else:
        print("No, Thread must wait")
        return False

#if(safe(allocation, available, need)):
    #print(safe(allocation, available, need))

#print(RR([1, 0, 2], 1))
#print(RR([3, 3, 0], 4))
#print(RR([0, 2, 0], 0))
    
while(1):
    print("choose operation by number: ")
    print("0 : is system in safe state?")
    print("1 : can request be granted?")
    print("2 : exit")
    choice = int(input())
    if(choice==0):
        threads = safe(allocation, available, need)
        if(threads):
            #print("Yes, safe state <", end='')
            out = "Yes, safe state<"
            for i in range(len(threads)-1):
                out += 'P' + str(threads[i]) + ','
            out += 'P' + str(threads[-1]) + '>'
            print(out)
        else:
            print("No, system is not in safe state")
    elif(choice==1):
        print("Enter the request vector")
        request = [int(i) for i in input().split()]
        print("Enter the thread index")
        Ti = int(input())
        threads = RR(request, Ti)
        if(threads):
            out = "Yes request can be granted with safe state , Safe state <P"
            out += str(Ti) + "req"
            for thread in threads:
                out += ',P' + str(thread)
            out += '>'
            print(out)
    elif(choice==2):
        print("Exiting")
        break
    else:
        print("Wrong input")
        print("Exiting")
        break

