import random
from math import *
from operator import itemgetter
import numpy as np

# 读文件得到“用户-电影”数据
def get_dataset(filename, pivot=0.75):
    trainSet_len = 0
    testSet_len = 0
    
    trainSet = {}
    testSet = {}
    m_dic = {}
    
    for line in load_file(filename):
        user, movie, rating,timestamp  = line.split(',')
        if random.random() < pivot:
            trainSet.setdefault(user, {})
            trainSet[user][movie] = rating
            trainSet_len += 1
            m_dic.setdefault(movie,[])
            m_dic[movie].append(float(rating))
        else:
            testSet.setdefault(user, {})
            testSet[user][movie] = rating
            testSet_len += 1
    print('Split trainingSet and testSet success!')
    print('TrainSet = %s' % trainSet_len)
    print('TestSet = %s' % testSet_len)
    
    return trainSet, testSet, m_dic


# 读文件，返回文件的每一行
def load_file(filename):
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:  # 去掉文件第一行的title
                continue
            yield line.strip('\r\n')
    print('Load %s success!' % filename)


def getab(dic_u, dic_v):
    sim_movie = list(dic_u.keys()&dic_v.keys())
    a = []
    b = []
    for m in sim_movie:
        a.append(float(dic_u[m]))
        b.append(float(dic_v[m]))
    
    for k,v in dic_u.items():
        if k not in sim_movie:
            a.append(float(v))
            b.append(0)
    
    for k,v in dic_v.items():
        if k not in sim_movie:
            a.append(0)
            b.append(float(v))

    return a,b

def get_adj_ab(dic_u, dic_v, m_dic):
    sim_movie = list(dic_u.keys()&dic_v.keys())
    a = []
    b = []
    for m in sim_movie:
        num = sum(m_dic[m])/len(m_dic[m])
        a.append(float(dic_u[m])-num)
        b.append(float(dic_v[m])-num)
    
    for k,v in dic_u.items():
        if k not in sim_movie:
            num = sum(m_dic[k])/len(m_dic[k])
            a.append(float(v)-num)
            b.append(-num)
    
    for k,v in dic_v.items():
        if k not in sim_movie:
            num = sum(m_dic[k])/len(m_dic[k])
            a.append(-num)
            b.append(float(v)-num)
    return a,b

def eculidSim(x,y):
    return sqrt(sum(pow(a-b,2) for a,b in zip(x,y)))

def manhattan_dis(x,y):
    return sum(abs(a-b) for a,b in zip(x,y))

def cos_sim(x, y):

    x = np.mat(x)
    y = np.mat(y)
    num = float(x * y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    sim = num / denom
    return sim

def jaccard_sim(x,y):
    intersection_cardonality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardonality/float(union_cardinality)

def pearson(vb,vc):
    return np.mean(np.multiply((vc-np.mean(vc)),(vb-np.mean(vb))))/(np.std(vb)*np.std(vc))


# 计算用户之间的相似度
def calc_user_sim(trainSet, method, m_dic):
    # 构建“电影-用户”倒排索引
    # key = movieID, value = list of userIDs who have seen this movie
    print('Building movie-user table ...')
    movie_user = {}
    
    user_sim_matrix = {}
    movie_count = 0
    
    for user, movies in trainSet.items():
        for movie in movies:
            if movie not in movie_user:
                movie_user[movie] = set()
            movie_user[movie].add(user)
    print('Build movie-user table success!')

    movie_count = len(movie_user)
    print('Total movie number = %d' % movie_count)

    print('Build user co-rated movies matrix ...')
    for movie, users in movie_user.items():
        for u in users:
            for v in users:
                if u == v:
                    continue
                user_sim_matrix.setdefault(u, {})
                user_sim_matrix[u].setdefault(v, 0)
                user_sim_matrix[u][v] += 1
    print('Build user co-rated movies matrix success!')


    if method == 'sim':
        ######      最基本的那种
        # 计算相似性
        print('Calculating user similarity matrix ...   原始方法')
        for u, related_users in user_sim_matrix.items():
            for v, count in related_users.items():
                user_sim_matrix[u][v] = count / sqrt(len(trainSet[u]) * len(trainSet[v]))
        print('Calculate user similarity matrix success!')
        ######

    if method == 'eculidSim':
        ######  欧几里得距离
        print('Calculating user similarity matrix ...   欧几里得')
        for u, related_users in user_sim_matrix.items():
            for v, count in related_users.items():
                if count!= 0:
                    a,b = getab(trainSet[u],trainSet[v])
                    user_sim_matrix[u][v] = eculidSim(a,b)
                else:
                    user_sim_matrix[u][v] = 0
        print('Calculate user similarity matrix success!')
        ######
    
    if method == 'manhattan':
        print('Calculating user similarity matrix ...   曼哈顿')
        for u, related_users in user_sim_matrix.items():
            for v, count in related_users.items():
                if count!= 0:
                    a,b = getab(trainSet[u],trainSet[v])
                    user_sim_matrix[u][v] = manhattan_dis(a,b)
                else:
                    user_sim_matrix[u][v] = 0
        print('Calculate user similarity matrix success!')

    if method == 'jaccard':
        print('Calculating user similarity matrix ...   jaccard')
        for u, related_users in user_sim_matrix.items():
            for v, count in related_users.items():
                if count!= 0:
                    a,b = getab(trainSet[u],trainSet[v])
                    user_sim_matrix[u][v] = jaccard_sim(a,b)
                else:
                    user_sim_matrix[u][v] = 0
        print('Calculate user similarity matrix success!')

    if method == 'cosine':
        print('Calculating user similarity matrix ...   余弦')
        for u, related_users in user_sim_matrix.items():
            for v, count in related_users.items():
                if count!= 0:
                    a,b = getab(trainSet[u],trainSet[v])
                    user_sim_matrix[u][v] = cos_sim(a,b)
                else:
                    user_sim_matrix[u][v] = 0
        print('Calculate user similarity matrix success!')


    if method == 'pearson':
        print('Calculating user similarity matrix ...   皮尔逊')
        for u, related_users in user_sim_matrix.items():
            for v, count in related_users.items():
                if count!= 0:
                    a,b = getab(trainSet[u],trainSet[v])
                    user_sim_matrix[u][v] = pearson(a,b)
                else:
                    user_sim_matrix[u][v] = 0
        print('Calculate user similarity matrix success!')
    
    if method == 'adj_cosine':
        print('Calculating user similarity matrix ...   改进余弦')
        for u, related_users in user_sim_matrix.items():
            for v, count in related_users.items():
                if count!= 0:
                    a,b = get_adj_ab(trainSet[u],trainSet[v], m_dic)
                    user_sim_matrix[u][v] = cos_sim(a,b)
                else:
                    user_sim_matrix[u][v] = 0
        print('Calculate user similarity matrix success!')
    
    return user_sim_matrix, movie_count


# 针对目标用户U，找到其最相似的K个用户，产生N个推荐
def recommend(user, n_sim_user, n_rec_movie, trainSet, user_sim_matrix):
    K = n_sim_user
    N = n_rec_movie
    rank = {}
    watched_movies = trainSet[user]

    # v=similar user, wuv=similar factor
    # print(user)
    xxx = sorted(user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]
    for v, wuv in xxx:
        for movie,value in trainSet[v].items():
            if movie in watched_movies:
                continue
            rank.setdefault(movie, 0)
            rank[movie] += wuv*float(value)
    return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]


# 产生推荐并通过准确率、召回率和覆盖率进行评估
def evaluate(n_rec_movie, trainSet, user_sim_matrix, testSet, n_sim_user, movie_count):
    print("Evaluation start ...")
    N = n_rec_movie
    # 准确率和召回率
    hit = 0
    rec_count = 0
    test_count = 0
    # 覆盖率
    all_rec_movies = set()

    for i, user, in enumerate(trainSet):
        if user in user_sim_matrix:
            test_movies = testSet.get(user, {})
            rec_movies = recommend(user, n_sim_user, n_rec_movie, trainSet, user_sim_matrix)
            for movie, w in rec_movies:
                if movie in test_movies:
                    hit += 1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_movies)

    precision = hit / (1.0 * rec_count)
    recall = hit / (1.0 * test_count)
    coverage = len(all_rec_movies) / (1.0 * movie_count)
    print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))


# trainSet, testSet = get_dataset(filename = 'ml/rating.csv', pivot=1)
# user_sim_matrix, movie_count = calc_user_sim(trainSet)
# n_sim_user = 10
# n_rec_movie = 20

trainSet, testSet, m_dic = get_dataset(filename = 'ml/ratings.csv')
methods = ['adj_cosine','sim', 'eculidSim', 'manhattan', 'jaccard', 'cosine', 'pearson']
for method in methods:
    user_sim_matrix, movie_count = calc_user_sim(trainSet, method, m_dic)
    for num in [1,5,8,10,20]: 
        n_sim_user = num
        n_rec_movie = 30
        print('最相似用户为{}个'.format(num))
        evaluate(n_rec_movie, trainSet, user_sim_matrix, testSet, n_sim_user, movie_count)