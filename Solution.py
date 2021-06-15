#TAKING INPUT
import csv
with open('mempool.csv', 'r') as file:
    dic={}
    check={}
    ar=[]
    sum=0
    reader = csv.reader(file, delimiter="\t")
    for i, line in enumerate(reader):
        a,b,c,d=line[0].split(',')
        lst=[b,c,d]
        if(a!="tx_id"):
            dic[a]=lst
            check[a]=0
            ar.append(a)
        
# MAKING ADJACENCY LIST FOR GRAPH AND ASSOCIATING tx_id with a number..
    graph=dict()
    ass={} #This will have a unique number assigned to each transaction and since all transactions are unique we do not need any string hash function
    assrev={} # This will be the inverse of the hashed map
    a=1
    ass['']=0
    graph.setdefault(0,[])
    for i in ar:
        ass[i]=int(a)
        assrev[a]=i
        graph.setdefault(ass[i],[])
        a+=1
    for i in ar:
        lis=dic[i][2].split(';')
        for j in range(len(lis)):
            graph[ass[lis[j]]].append(ass[i]) 
    
# SINCE DATA IS VERY LARGE AND DIRECTLY APPLYING CONSTRAINED DP ON TREE WILL HAVE VERY HIGH RUNNING TIME.
# SO, APPLYTING GREEDY TO TAKE MAX PROFIT/WEIGHT RATIO..
    memo={} #memoisation dictionary of weight of transactions till the parent is the root node
    memop={} #memoisation dict. of profit
    vis={} #Visited dict. so that same transaction is not counted twice
    visp={}
    ans=[] # Will have all the included transactions
    # Initialisation
    for i in ar:
        memo[i]=-1
        memop[i]=-1
        vis[i]=0
        visp[i]=0
    #Now we write some functions to do the task
    def sum(i):
        if(vis[i]==1):
            return 0
        if(memo[i]!=-1):
            vis[i]=1
            return memo[i]
        if(len(dic[i][2])==0):
            memo[i]=int(dic[i][1])
            vis[i]=1
            return int(dic[i][1])
        else:
            sm=int(dic[i][1])
            lis=dic[i][2].split(';')
            for j in range(len(lis)):
                sm+=sum(lis[j])
            memo[i]=sm
            vis[i]=1
            return sm
    
    def sum_x_vis(i):
        if(memo[i]!=-1):
            return memo[i]
        if(len(dic[i][2])==0):
            memo[i]=int(dic[i][1])
            return int(dic[i][1])
        else:
            sm=int(dic[i][1])
            lis=dic[i][2].split(';')
            for j in range(len(lis)):
                sm+=sum_x_vis(lis[j])
            memo[i]=sm
            return sm

    def a(i):
        if(visp[i]==1):
            return 0
        if(memop[i]!=-1):
            visp[i]=1
            return memop[i]
        if(len(dic[i][2])==0):
            memop[i]=int(dic[i][0])
            visp[i]=1
            ans.append(i)
            return int(dic[i][0])
        else:
            sm=int(dic[i][0])
            lis=dic[i][2].split(';')
            for j in range(len(lis)):
                sm+=a(lis[j])
            memop[i]=sm
            ans.append(i)
            visp[i]=1
            return sm

    def a_x_vis(i):
        if(memop[i]!=-1):
            return memop[i]
        if(len(dic[i][2])==0):
            memop[i]=int(dic[i][0])
            return int(dic[i][0])
        else:
            sm=int(dic[i][0])
            lis=dic[i][2].split(';')
            for j in range(len(lis)):
                sm+=a_x_vis(lis[j])
            memop[i]=sm
            return sm

    for i in ar:
        memo[i]=-1
        memop[i]=-1
        vis[i]=0
        visp[i]=0

    w=4000000
    x=0
    p=0
    t=[]
    tot=0
    totw=0
    for i in ar:
        t.append([a_x_vis(i)/sum_x_vis(i), ass[i]])
        tot+=int(dic[i][0])
        totw+=int(dic[i][1])
    t.sort(reverse=True)
    for i in ar:
        memo[i]=-1
        memop[i]=-1
        vis[i]=0
        visp[i]=0
    while w>1000 and x<5214:
        sj=sum(assrev[t[x][1]])
        if(w-sj<1000):
            break
        w=w-sj
        p=p+a(assrev[t[x][1]])
        x+=1

    # f = open("block.txt", "a")
    # for i in ans:
    #     f.write(i)
    #     f.write("\n")

#APPLYING DP THE REMAINING DATA
# ANALYZING THE DATA IT IS CLEAR THAT THERE ARE 927 TRANSACTIONS WITHOUT ANY PARENT AND CHILDREN, AND THERE ARE <100 TRANSACTIONS WITH CHILDRENS
# SO WE CAN USE KNAPSACK ON THE REMAINING DATA
    node_val=[]
    node_wei=[]
    node_num=[]
    inc=[]
    for i in ar:
        if(vis[i]==0 and dic[i][2]=='' and len(graph[ass[i]])==0):
            node_val.append(dic[i][0])
            node_wei.append(dic[i][1])
            node_num.append(ass[i])
    n=len(node_val)
    t = [[-1 for i in range(w + 1)] for j in range(n + 1)]
    def knapsack(w,node_val,node_wei,n):
        K = [[0 for w in range(w + 1)]
                for i in range(n + 1)]   
        # Built a table K[][] in bottom up manner
        for i in range(n + 1):
            for j in range(w + 1):
                if i == 0 or j == 0:
                    K[i][j] = 0
                elif int(node_wei[i - 1]) <= j:
                    K[i][j] = max(int(node_val[i - 1])
                    + K[i - 1][j - int(node_wei[i - 1])],
                                K[i - 1][j])
                else:
                    K[i][j] = K[i - 1][j]
        res = K[n][w] # This gives the resulting profit
        # Now we will find the chosen transaction IDs
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == K[i - 1][w]:
                continue
            else:
    
                # This item is included.
                inc.append(assrev[node_num[i - 1]])
                res = res - int(node_val[i - 1])
                w = w - int(node_wei[i - 1])
    knapsack(w,node_val,node_wei,n)
    # for i in inc:
    #     f.write(i)
    #     f.write("\n")
    # f.close()
#CNFRMATION IF THE WEIGHT IS EQUAL TO THE 4*10**6
    # cnf=0
    # for i in ans:
    #     cnf+=int(dic[i][1])
    # for i in inc:
    #     cnf+=int(dic[i][1])
    # print(cnf)
