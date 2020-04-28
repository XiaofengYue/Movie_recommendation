import time
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity

## 程序运行时间
def calculate_function_run_time(func):
    def call_fun(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        end_time = time.time()
        print('%s() 运行时间为：%s s' % (func.__name__, int(end_time - start_time)))
        return f
    return call_fun


import pymysql
import pandas as pd
@calculate_function_run_time
def load_data(filename=None):
    # read_sql 方式   15s
    # con = pymysql.connect(host='127.0.0.1', user='root', password='wozhiai0',db='movies')
    # Ratings = pd.read_sql("select * from rate", con)
    # return Ratings

    # 查询数据库方式
    con = pymysql.connect(host='127.0.0.1', user='root', password='wozhiai0',db='movies')
    cursor = con.cursor()
    cursor.execute('select * from rate')
    D = cursor.fetchall()
    print(type(D))
    return D

## 建立倒查表
@calculate_function_run_time
def create_movie_dic(data):
    # 每一条评价纪录 生成movie_dic = {'12':['beijinglife','yxf']...}
    movie_dic = {}
    for rate in data:
        u_id = rate[1]
        m_id = rate[2]
        movie_dic.setdefault(m_id,[])
        movie_dic[m_id].append(u_id)
    return movie_dic

@calculate_function_run_time
def create_user_user_dic(movie_dic):
    # 根据movie_dic 得到用户-用户观看相同电影的count
    u_u_dic = {} 
    for m_id,u_list in movie_dic.items():
        for u in u_list:
            u_u_dic.setdefault(u,{})
            for v in u_list:
                if (u==v):
                    continue
                u_u_dic[u].setdefault(v,0)
                u_u_dic[u][v] += 1
    return u_u_dic

## 寻找最近的k个用户
@calculate_function_run_time
def get_n_nearest_nei(u_u_dic, k=5):
    u_nearest_k = {}
    for user,user_dic in u_u_dic.items():
        u_nearest_k[user] = [i[0] for i in sorted(u_u_dic[user].items(), key=itemgetter(1), reverse=True)[0:k]]
    return u_nearest_k

## 生成user-item矩阵
@calculate_function_run_time
def create_user_item_matrix(Ratings):
    mean = Ratings.groupby(by='user_id',as_index=False)['star'].mean()
    Ratings_mean = pd.merge(Ratings,mean,on='user_id')
    # 添加一列 偏好程度
    Ratings_mean['adg'] = Ratings_mean['star_x']-Ratings_mean['star_y']
    user_item_matrix = pd.pivot_table(Ratings_mean,index='user_id',columns='movie_id',values='adg')
    # Nan补充为电影平均分
    user_item_matrix = user_item_matrix.fillna(user_item_matrix.mean(axis=0))
    return user_item_matrix

# 计算某个user的相似用户相似度
def cal_user_similarity(user, user_item_matrix, u_nearest_k):
    u1_data = list(user_item_matrix.loc[user])
    for u2 in u_nearest_k[user]:
        u2_data = list(user_item_matrix.loc[u2])
        similarity = cosine_similarity([u1_data],[u2_data])
        user_similaruser_value[u2] = list(similarity)[0][0]
        #print("user_id:{} 的相似度:{}".format(u2,similarity))
    return user_similaruser_value



data = load_data()
movie_dic = create_movie_dic(data)
u_u_dic = create_user_user_dic(movie_dic)
u_nerest_k = get_n_nearest_nei(u_u_dic, k=5)
user_item_matrix = create_user_item_matrix(data)
cal_user_similarity('beijinglife', user_item_matrix, u_nearest_k)

