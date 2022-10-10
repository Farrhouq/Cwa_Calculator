import numbers
from re import L
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .models import ResultSet
from django.contrib.auth.decorators import login_required

# Create your views here.

number = 0

class specialStr:

    def __init__(self, ss):
        self.ss = ss
        self.part1 = ss[0:9]
        self.part2 = ss[9:19]
        self.part3 = ss[19:44]

    def correct(self):
        if self.part3[0] != 'c':
            self.part3 = 'c' + self.part3


class New:

    def __init__(self, tup):
        self.tup = tup
        self.p0 = tup[0]
        self.p1 = tup[1]
        self.p2 = tup[2]


def home(request):
    return render(
        request,
        'home.html',
    )


def to_randomize(request):
    global number
    number = request.POST.get('number')
    try:
        i =int(number)
    except:
        return redirect('home')

    if request.method == 'POST' and request.POST.get('randomize') == 'on':
        number = request.POST.get('number')
        to_randomize = request.POST.get('randomize')

        context = {
            'number': number,
            'to_randomize': to_randomize,
        }
        return render(request, 'to_randomize.html', context)
    elif number != None:
        try:
            range_list = [i + 1 for i in range(int(number))]
            return render(request, 'to_not_randomize.html', {
                'number': number,
                'range_list': range_list,   
            })
        except:
            return redirect('home')
    else:
        return redirect('home')


def three(request):
    #if user chooses not to randomize
    if number == 0 or number == None:
           return redirect('home')
    context = {}
    return render(request, 'to_not_randomize.html', context)
    


def randomize(credits, upper_bound, lower_bound) -> list:
    import random
    score_and_credits = []
    for j in credits:
        i = round(random.uniform(lower_bound, upper_bound), 2)
        j = int(j)
        score_and_credits.append((i, j))
    return score_and_credits


def new(request):

    n = number
    if n == 0:
        return redirect('home')
    upper_bound = int(request.POST.get('upper-bound'))
    lower_bound = int(request.POST.get('lower-bound'))
    _credits = request.POST.get('_credits')
    points_obtained = 0
    total_credits = 0
    lee = len(str(_credits))
    tru = str(lee) == str(n)
    if tru:
        sc = randomize(str(_credits), upper_bound, lower_bound)
        som = []
        ss = []
        ss2 = []
        for i, element in enumerate(sc, start=1):
            credit = element[1]
            score = element[0]
            ss.append(score)
            ss2.append(credit)
            som.append(
                f'course[{i}]score = {int(score)}credit hour(s) = {credit}')
            points_obtained += (score * credit)
            total_credits += credit
        
        points_obtained = 0
        total_credits = 0
        for i in range(len(ss)):
            points_obtained += (int(ss[i]) * int(ss2[i]))
            total_credits += ss2[i]

        cwa = points_obtained/total_credits

        part = []
        for element in som:
            el = specialStr(element)
            el.correct()
            part.append(el)
        context = {
            'lower_bound': lower_bound,
            'som': som,
            'credits': _credits,
            'p1': part,
            'upper_bound': upper_bound,
            'ss':ss,
            'ss2':ss2,
            'cwa':round(cwa, 2)
        }
        return render(request, 'new.html', context)
    else:
        return redirect('tr2')


def inter(request):
    try:
        i = int(number)
    except:
        return redirect('home')

    if number == 0 or number == None:
        return redirect('home')
    else:
        number_s = [i + 1 for i in range(int(number))]

        return render(request, 'inter.html', {
            'numbers': number_s,
            'number': number
        })


def tr2(request):
    try:
        i = int(number)
    except:
        return redirect('home')
    if number == 0:
        return redirect('home')
    return render(request, 'tr2.html', {'n': number})


def final(request):
    
    if request.POST.get('sc1') == None:
        return redirect('home')

    gotten = []
    gotten2 = []
    ov = []
    for n in range(int(number)):
        n += 1
        ov.append(n)
        gotten.append(request.POST.get('sc' + str(n)))
        gotten2.append(request.POST.get('cr' + str(n)))

    

    a = gotten
    b = gotten2
    c = ov
    listq = []
    for i in range(len(a)):
        listq.append((a[i], b[i], c[i]))

    points_obtained = 0
    total_credits = 0
    try:
        for i in range(len(listq)):
            el = New(listq[i])
            score = int(el.p0)
            credit = int(el.p1)
            points_obtained += (score * credit)
            total_credits += credit
    except:
        return redirect('inter')


    if request.user.is_authenticated:
        user_results = request.user.resultset_set.all()
        for i in user_results:
            total_credits += i.total_credits
            points_obtained += i.weight

    if total_credits == 0:
        cwa = None
    else:
        cwa = points_obtained / total_credits

    if len(ov) == 0:
        return redirect('home')

    
    sup = []
    for i in listq:
        el = New(i)
        sup.append(el)
    if request.user.is_authenticated:
        ResultSet.objects.create(
            user = request.user,
            weight = points_obtained,
            total_credits = total_credits
        )
    context = {
        'g1': gotten,
        'g2': gotten2,
        'ov': ov,
        'sup': sup,
        'cwa': round(cwa,2),
        
    }
    
    return render(request, 'final.html', context)


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
    context = {'form': form,}
    return render(request, 'register.html', {'form':form})

def logoutUser(request):

    logout(request)
    return redirect('home')


def refresh(request):
    page = 'delete_all'
    return render(request, 'refresh.html', {'page':page})


def delete_all(request):
    results = request.user.resultset_set.all()
    for i in results:
        i.delete()
    return redirect('home')

