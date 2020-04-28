import pandas as pd
import numpy as np
import pymysql
# 计算余弦相似度
from sklearn.metrics.pairwise import cosine_similarity
# 计算欧式距离
from sklearn.metrics import pairwise_distances

settings = {
    'engine_name':'movielens',
    'movie_data':'movies.csv',
    'rating_data':'ratings.csv',

    'host':'127.0.0.1',
    'user':'root',
    'password':'wozhiai0',
    'db':'movies',
}

import time

def calculate_function_run_time(func):
    def call_fun(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        end_time = time.time()
        print('%s() run time：%s s' % (func.__name__, int(end_time - start_time)))
        return f
    return call_fun


class UserCF(object):
    # 加载数据
    
    def load_data(self):
        self.movies=None
        self.Ratings = None
        self.rating_column_user = ""
        self.rating_column_movie = ""
        self.rating_column_rate = ""
        self.movie_column_movie = ""

    @calculate_function_run_time
    def create_table(self):
        print('正在生成用户-电影矩阵透视表......')
        # 新的df (每个用户的平均评分标准)
        self.Mean = self.Ratings.groupby(by=self.rating_column_user,as_index=False)[self.rating_column_rate].mean()

        # 新的df (用户行为Ratings添加新的两列1.用户平均评分，2.用户偏好差距评分)
        self.Rating_avg = pd.merge(self.Ratings,self.Mean,on=self.rating_column_user)
        # 添加电影与平均评分的差距
        x = self.rating_column_rate+'_x'
        y = self.rating_column_rate+'_y'
        self.Rating_avg['adg_rating']=self.Rating_avg[x]-self.Rating_avg[y]

        # 生成透视表 用户-电影 矩阵 （index纵坐标用户ID columns横坐标电影ID 内容，rating_x评分）
        self.check = pd.pivot_table(self.Rating_avg,values=x,index=self.rating_column_user,columns=self.rating_column_movie)
        # 生成透视表 用户-电影 矩阵 （index纵坐标用户ID columns横坐标电影ID 内容，adg评分）
        self.final = pd.pivot_table(self.Rating_avg,values='adg_rating',index=self.rating_column_user,columns=self.rating_column_movie)
        # 替换透视表中的Nan值
        # 替换为用户平均分
        self.final_user = self.final.apply(lambda row: row.fillna(row.mean()), axis=1)
        # 替换为电影平均分
        self.final_movie = self.final.fillna(self.final.mean(axis=0))
        print('透视表生成完成!')

    @calculate_function_run_time
    def calculate_similarity(self, n_user):
        print('正在计算{}个最相似用户列表'.format(n_user))
        # 计算final_user的用户相似度
        b = cosine_similarity(self.final_user)
        np.fill_diagonal(b, 0 )
        self.similarity_with_user = pd.DataFrame(b,index=self.final_user.index)
        self.similarity_with_user.columns=self.final_user.index
        print('最相似用户列表生成完成!')

        # 计算final_movie的用户相似度
        cosine = cosine_similarity(self.final_movie)
        np.fill_diagonal(cosine, 0 )
        self.similarity_with_movie = pd.DataFrame(cosine,index=self.final_movie.index)
        self.similarity_with_movie.columns=self.final_user.index

        # 对于final_user的最近三十个
        self.sim_user_30_u = self.find_n_neighbours(self.similarity_with_user,n_user)
        # 对于final_movie的最近三十个
        self.sim_user_30_m = self.find_n_neighbours(self.similarity_with_movie,n_user)

    # 寻找最近的n个邻居
    def find_n_neighbours(self,df,n):
        # order = np.argsort(df.values, axis=1)[:, :n]
        df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
            .iloc[:n].index, 
            index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
        return df
    
    # 获得两个用户共同评价电影矩阵
    def get_user_similar_movies(self,user1, user2 ):
        common_movies = self.Rating_avg[self.Rating_avg.userId == user1].merge(
        self.Rating_avg[self.Rating_avg.userId == user2],
        on = self.rating_column_movie,
        how = "inner" )
        return common_movies.merge( self.movies, on = self.movie_column_movie )
    
    
    # 得到用户基于相似用户对item的评分
    def User_item_score(self,user,item):
        # 获得user相似的三十个用户
        a = self.sim_user_30_m[self.sim_user_30_m.index==user].values
        # a 转变成列表
        b = a.squeeze().tolist()
        # 获得user-item 电影平均分矩阵某项电影的全部用户评分
        c = self.final_movie.loc[:,item]
        # 获得c中在相似用户里面的值
        d = c[c.index.isin(b)]
        # 此用户相似用户的对此电影的偏差喜好评分
        f = d[d.notnull()]
        # 获得此用户的电影平均分
        avg_user = self.Mean.loc[self.Mean[self.rating_column_user] == user,self.rating_column_rate].values[0]
        # 相似用户ID列表
        index = f.index.values.squeeze().tolist()
        # 此用户对于相似用户的相似程度列表
        corr = self.similarity_with_movie.loc[user,index]
        # 生成用户对此电影的偏差评分和对用户的相似度
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score','correlation']
        # fin添加一列预测偏差喜欢评分score
        fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
        
        # 计算公式 所有score和／所有相关系数和 + 平均打分
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume/deno)
        return final_score
    
    @calculate_function_run_time
    def User_item_score1(self, user, n_movies):
        print('正在生成用户ID:{}推荐{}部电影列表'.format(user,n_movies))

        # 将Rating_avg中的movieID修改类型为str
        self.Rating_avg = self.Rating_avg.astype({self.rating_column_movie: str})
        # 获得Rating列表中 用户ID观看的所有movieID
        Movie_user = self.Rating_avg.groupby(by = self.rating_column_user)[self.rating_column_movie].apply(lambda x:','.join(x))

        # 用户user看过的movie
        Movie_seen_by_user = self.check.columns[self.check[self.check.index==user].notna().any()].tolist()
        # a为与user相似的三十个用户列表
        a = self.sim_user_30_m[self.sim_user_30_m.index==user].values
        b = a.squeeze().tolist()
        # 最相似三十个用户看过的电影df
        d = Movie_user[Movie_user.index.isin(b)]
        # 所有看过的电影大杂烩
        l = ','.join(d.values)
        # 看过电影的全部列表切分元素
        Movie_seen_by_similar_users = l.split(',')
        # 相似用户看过而自己没有看过的电影列表 第二行将movieid转换成int
        Movies_under_consideration = list(set(Movie_seen_by_similar_users)-set(list(map(str, Movie_seen_by_user))))
        Movies_under_consideration = list(map(int, Movies_under_consideration))
        
        # 没有看过的电影列表评分表
        score = []
        for item in Movies_under_consideration:
            # 获得电影预测评分
            c = self.final_movie.loc[:,item]
            d = c[c.index.isin(b)]
            f = d[d.notnull()]
            avg_user = self.Mean.loc[self.Mean[self.rating_column_user] == user,self.rating_column_rate].values[0]
            index = f.index.values.squeeze().tolist()
            corr = self.similarity_with_movie.loc[user,index]
            fin = pd.concat([f, corr], axis=1)
            fin.columns = ['adg_score','correlation']
            fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
            nume = fin['score'].sum()
            deno = fin['correlation'].sum()
            final_score = avg_user + (nume/deno)
            score.append(final_score)
        # 电影ID 和预测评分 df
        data = pd.DataFrame({self.rating_column_movie:Movies_under_consideration,'score':score})
        # 获得最高评分五部电影
        top_5_recommendation = data.sort_values(by='score',ascending=False).head(n_movies)
        # print(top_5_recommendation)
        # 获得最高评分五步电影名称
        # Movie_Name = top_5_recommendation.merge(self.movies, how='inner', on=self.movie_column_movie)
        # Movie_Names = Movie_Name.title.values.tolist()

        print('推荐列表生成完成!')
        return top_5_recommendation

class UserCF_Movielens(UserCF):

    def load_data(self):
        self.movies = pd.read_csv(settings['movie_data'])
        self.Ratings = pd.read_csv(settings['rating_data'])
        self.rating_column_user = "userId"
        self.rating_column_movie = "movieId"
        self.rating_column_rate = "rating"
        self.movie_column_movie = "movieId"

    def run(self,user, n_user, n_movies):
        self.load_data()
        self.create_table()
        self.calculate_similarity(n_user)
        predict_movies =  self.User_item_score1(user,n_movies)
        return predict_movies

class UserCF_DB(UserCF):
    @calculate_function_run_time
    def load_data(self):
        print('正在加载数据中......')
        print('正在链接数据库......')
        con = pymysql.connect(host=settings['host'],
                            user=settings['user'],
                            password=settings['password'],
                            db=settings['db'])
        print('数据库连接完成!')
        # self.movies = pd.read_sql("select * from info",con)
        self.Ratings = pd.read_sql("select * from rate", con)
        self.rating_column_user = "user_id"
        self.rating_column_movie = "movie_id"
        self.rating_column_rate = "star"
        self.movie_column_movie = "id"
        print('数据加载完成!')
    
    def run(self,user, n_user, n_movies):
        self.load_data()
        self.create_table()
        self.calculate_similarity(n_user)
        predict_movies =  self.User_item_score1(user,n_movies)
        return predict_movies


if __name__ == "__main__":
    if settings['engine_name'] == 'movielens':
        e = UserCF_Movielens()
        user = int(input("Enter the user id to whom you want to recommend : "))
        predicted_movies = e.run(user,30,10)
        print(" ")
        print("The Recommendations for User Id you give")
        print("   ")
        print(predicted_movies)
        # for i in predicted_movies:
        #     print(i)
    
    if settings['engine_name'] == 'db':
        e = UserCF_DB()
        # user = input("Enter the user id to whom you want to recommend : ")
        predicted_movies = e.run('123456',5,10)
        print(" ")
        print("The Recommendations for User Id you give")
        print("   ")
        print(predicted_movies)