from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
import math, json
# 导入数据
from .models import Info,User,Rate
from .form import UserForm,RegisterForm
# from ml.engine import UserCF_DB

##########################################################################################
from ml.test import load_data,create_movie_dic,create_user_user_dic,get_n_nearest_nei,create_user_item_matrix
from ml.test import cal_user_similarity, recommend
data = None
movie_dic = None
u_u_dic = None
u_nerest_k = None
user_item_matrix = None

def start(k_nei):
    global data, movie_dic, u_u_dic, u_nearest_k, user_item_matrix
    data = load_data()
    movie_dic = create_movie_dic(data)
    u_u_dic = create_user_user_dic(movie_dic)
    u_nearest_k = get_n_nearest_nei(u_u_dic, k=k_nei)
    user_item_matrix = create_user_item_matrix(data)

start(1)
##########################################################################################


# Create your views here.

# 主界面
def index(request):
    context = {'infos': Info.objects.all().order_by('-star_five')[:12],
                'topten': Info.objects.all()[:10]}
    #已经登录
    if request.session.get('is_login',None):
        print('主界面推荐内容')
        data = []
        print(request.session['recommend_list'] )
        for i in request.session['recommend_list']:
            data.append(Info.objects.get(id=i))
        context['infos'] = data
        # context['infos'] = Info.objects.all().order_by('-star_four')[:12]
    return render(request, 'movies/base.html',context)    

# 电影信息详情
def detail(request,movie_id):
    info = get_object_or_404(Info, pk=movie_id)
    genres = info.genres.split(',')
    rating_sum = info.star_five + info.star_four + info.star_three + info.star_two + info.star_one
    if rating_sum != 0:
        aver = round((info.star_five*10 + info.star_four*8 + info.star_three*6 + info.star_two*4 + info.star_one*2)/rating_sum,1)
    else:
        aver = 0
    bigstar = math.ceil(aver)*5
    five=0
    four=0
    three=0
    two=0
    one = 0
    if rating_sum != 0:
        five = info.star_five*100//rating_sum
        four = info.star_four*100//rating_sum
        three = info.star_three*100//rating_sum
        two = info.star_two*100//rating_sum
        one = info.star_one*100//rating_sum
    # 查询是否已经评价过
    if request.session.get('is_login', None):
        rate = Rate.objects.filter(movie_id=movie_id, user_id=request.session['user_id'])
        if rate:
            return render(request, 'movies/detail2.html', {'info': info,'genres':genres,'aver':aver,'bigstar':bigstar,'rating_sum':rating_sum,
                    'five':five,'four':four,'three':three,'two':two,'one':one,'star':rate[0].star})
    return render(request, 'movies/detail2.html', {'info': info,'genres':genres,'aver':aver,'bigstar':bigstar,'rating_sum':rating_sum,
                    'five':five,'four':four,'three':three,'two':two,'one':one})

def search(request):
    keyword = request.POST.get('keyword')
    if(request.method == 'POST'):
        infos = Info.objects.filter(Q(title__icontains=keyword)\
		|Q(genres__icontains=keyword)|Q(countries__icontains=keyword))
        context = {'infos':infos}
        print('搜索内容:')
        print(context)
        return render(request, 'movies/search.html',context)

def user(request, user_id):
    rates = Rate.objects.filter(user_id=user_id).order_by('-id')
    data = []
    for rate in rates:
        dic = {}
        dic['star'] = rate.star
        dic['info'] = Info.objects.get(id=rate.movie_id)
        print('评价列表')
        print(dic)
        data.append(dic)
    return render(request, 'movies/user.html', {'data':data})


def rate(request,movie_id):
    if(request.method == 'POST'):
        print("the POST method")
        postBody = request.body
        star = json.loads(postBody)['star']
        user_id = request.session['user_id']
        print('user_id:{}为电影movie_id:{}评价了{}星级'.format(user_id, movie_id, star))
        # 回调给前端的data
        data = {}
        try:
            rate = Rate.objects.get(user_id=user_id,movie_id=movie_id)
            data['code'] = 0
            data['msg'] = '已经评价过了'
        except :
            try:
                new_rate = Rate.objects.create()
                new_rate.user_id = user_id
                new_rate.movie_id = movie_id
                new_rate.star = star
                new_rate.save()
                data['code'] = 1
                data['msg'] = '评价成功'
            except:
                data['code'] = 0
                data['msg'] = '评价失败'
        
        return HttpResponse(json.dumps(data))

def login(request):

    if request.session.get('is_login',None):
        return redirect('/movies/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(id=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name

                    # 生成个性化推荐列表

                    global data, movie_dic, u_u_dic, u_nearest_k, user_item_matrix
                    user_similaruser_value = cal_user_similarity(username, user_item_matrix, u_nearest_k)
                    recommend_list = [i[0] for i in recommend(data, username,user_similaruser_value,12)]
                    print('测试测试测试')
                    print(user_similaruser_value)
                    print(recommend_list)
                    request.session['recommend_list'] = list(recommend_list.movie_id)

                    # usercf = UserCF_DB()
                    # recommend_list = usercf.run(request.session['user_id'],5,12)
                    # print(recommend_list)
                    # request.session['recommend_list'] = list(recommend_list.movie_id)
                    return redirect('/movies/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'movies/login.html', locals())

    login_form = UserForm()
    return render(request, 'movies/login.html', locals())




def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/movies/")
    request.session.flush()
    recommend_list=[]
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/movies/")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/movies/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(id=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'movies/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'movies/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                print('ok')
                new_user = User.objects.create(id=username)
                new_user.password = password1
                new_user.email = email
                new_user.gender = sex
                new_user.save()
                return redirect('/movies/login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'movies/register.html', locals())





