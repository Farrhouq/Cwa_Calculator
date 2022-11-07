import numbers
from re import L
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .models import ResultSet
from django.contrib.auth.decorators import login_required
from logic.functions import randomize
from logic.classes import SpecialStr, New

# Create your views here.

def home(request):
    return render(
        request,
        'home.html',
    )


def to_randomize(request):
    number = request.POST.get('number')
    if number == None:
        return redirect('home')
    if request.method == 'POST':
        if request.POST.get('randomize') == 'on':
            number = request.POST.get('number')
            context = {
                'number': number,
            }
            return render(request, 'tr2.html', context)

        else:
            range_list = [i + 1 for i in range(int(number))]
            return render(request, 'enter_scores.html', {
                'number': number,
                'range_list': range_list,
            })


def new(request):
    try:
        number = request.POST.get('number')
        upper_bound = int(request.POST.get('upper-bound'))
        lower_bound = int(request.POST.get('lower-bound'))
        _credits = request.POST.get('_credits')
    except:
        return redirect('to_randomize')

    points_obtained = 0
    total_credits = 0
    lee = len(str(_credits))
    tru = str(lee) == str(number)
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
            som.append([i, score, credit])
            points_obtained += (score * credit)
            total_credits += credit

        points_obtained = 0
        total_credits = 0
        for i in range(len(ss)):
            points_obtained += (int(ss[i]) * int(ss2[i]))
            total_credits += ss2[i]

        cwa = points_obtained / total_credits

        part = []
        for element in som:
            el = SpecialStr(element)
            part.append(el)
        context = {
            'lower_bound': lower_bound,
            'som': som,
            'credits': _credits,
            'p1': part,
            'upper_bound': upper_bound,
            'ss': ss,
            'ss2': ss2,
            'cwa': round(cwa, 2)
        }
        return render(request, 'new.html', context)
    else:
        return redirect('to_randomize')


def final(request):
    number = request.POST.get('number')
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
        return redirect('home')

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

    if number == 0 or number == None:
        return redirect('home')

    sup = []
    for i in listq:
        el = New(i)
        sup.append(el)
    if request.user.is_authenticated:
        ResultSet.objects.create(user=request.user,
                                 weight=points_obtained,
                                 total_credits=total_credits)
    context = {
        'g1': gotten,
        'g2': gotten2,
        'ov': ov,
        'sup': sup,
        'cwa': round(cwa, 2),
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
    context = {
        'form': form,
    }
    return render(request, 'register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


def refresh(request):
    page = 'delete_all'
    return render(request, 'refresh.html', {'page': page})


def delete_all(request):
    results = request.user.resultset_set.all()
    for i in results:
        i.delete()
    return redirect('home')
