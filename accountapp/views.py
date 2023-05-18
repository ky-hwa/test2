from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountUpdateForm
from accountapp.models import HelloWORLD

has_ownership = [account_ownership_required, login_required]

@login_required()
def hello_world(request):

    if request.method == "POST":

        temp = request.POST.get('hello_world_input')

        new_hello_world = HelloWORLD()
        new_hello_world.text = temp
        new_hello_world.save()

        hello_world_list = HelloWORLD.objects.all()

        return HttpResponseRedirect(reverse('accountapp:hello_world'))
    else:
        hello_world_list = HelloWORLD.objects.all()
        return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})
class AccountCreateView(CreateView):
    model = User    #user 라는 model 가져와서 쓰는 거임
    form_class = UserCreationForm   #UserCreationFrom을 가져와서 쓰는거임, 원래는 forms.py 파일을 쓴다.
    success_url = reverse_lazy('accountapp:hello_world')    #로그인 성공하고 어디로 갈지 지정해주기
    template_name = 'accountapp/create.html'

class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'     #별명 짓기, 객체 이름을 지정해주고 html(t)에게 알려주는 기능, 여기서는 user model을 뜻한다.
    template_name = 'accountapp/detail.html'

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'