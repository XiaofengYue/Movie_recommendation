import random
import math
from operator import itemgetter


# 读文件得到“用户-电影”数据
def get_dataset(filename, pivot=0.75):
    trainSet_len = 0
    testSet_len = 0
    
    trainSet = {}
    testSet = {}
    
    for line in load_file(filename):
        timestamp, movie, rating, user = line.split(',')
        if random.random() < pivot:
            trainSet.setdefault(user, {})
            trainSet[user][movie] = rating
            trainSet_len += 1
        else:
            testSet.setdefault(user, {})
            testSet[user][movie] = rating
            testSet_len += 1
    print('Split trainingSet and testSet success!')
    print('TrainSet = %s' % trainSet_len)
    print('TestSet = %s' % testSet_len)
    
    return trainSet, testSet


# 读文件，返回文件的每一行
def load_file(filename):
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i == 0:  # 去掉文件第一行的title
                continue
            yield line.strip('\r\n')
    print('Load %s success!' % filename)


# 计算用户之间的相似度
def calc_user_sim(trainSet):
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

    # 计算相似性
    print('Calculating user similarity matrix ...')
    for u, related_users in user_sim_matrix.items():
        for v, count in related_users.items():
            user_sim_matrix[u][v] = count / math.sqrt(len(trainSet[u]) * len(trainSet[v]))
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
        for movie in trainSet[v]:
            if movie in watched_movies:
                continue
            rank.setdefault(movie, 0)
            rank[movie] += wuv
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
