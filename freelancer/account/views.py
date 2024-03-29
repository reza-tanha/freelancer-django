from itertools import chain

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from freelancer.project.models import Project, ApplyProject
from freelancer.account.models import Profile

from .forms import UserLoginForm, UserRegisterForm, EditProfileForm, ConversationForm


def Home(request):
    projects = Project.objects.all()[:4]
    return render(request=request, template_name='account/home/index.html', context={"projects": projects})


def login_user(request, next_url='account:dashboard',
               form_class=UserLoginForm, template_name="account/login.html"):
    """
    Login user to the account

    Args:
        next_url (str):
            This is a success_url to redirect logged-in users.

        form_class (Form, optional): 
            User Login Form.
            
        template_name (str, optional):
            Name of the template to be rendered in this view.
    """
    success_url = redirect(next_url)
    if request.user.is_authenticated:
        return success_url
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data  
            user = authenticate(
                request=request, 
                email=cd['email'],
                password=cd['password'])
            
            if user is not None:
                login(request=request, user=user)
                messages.success(request=request, message='شما با موفقیت لاگین شدید', extra_tags="success")
                return success_url
            else:
                messages.error(request=request, message="یوزرنیم یا پسورد وارد شده اشتباه است!", extra_tags="danger")
                return render(request=request,
                    template_name=template_name,
                    context={"form_login": form})

    else:
        form = form_class()
    context = {'form_login': form}
    
    return render(request=request,
        template_name=template_name,
        context=context)


def register_user(request, next_url='account:dashboard',
                form_class=UserRegisterForm, template_name='account/register.html'):
    """
    Register new user(sign up).

    Args:
        next_url (str):
            This is a success_url to redirect logged-in users.

        form_class (Form, optional): 
            User Register Form.
            
        template_name (str, optional):
            Name of the template to be rendered in this view.
    """
    success_url = redirect(next_url)
    if request.user.is_authenticated:
        return success_url
    
    if request.method == 'POST':
        form = form_class(data=request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user =  get_user_model().objects.create_user(
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                username=cd['username'].lower(),
                email=cd['email'],
                password=cd['password'],
            )
            user.is_active = True
            user.save()
            login(request=request, user=user)
            messages.success(request=request, message="ثبت نام با موفقیت انجام شد.", extra_tags="success")
            return success_url
        else:
            messages.error(request=request, message="موارد گفته شده را به درستی وارد نمایید", extra_tags="danger")
            return render(request=request,
                    template_name=template_name,
                    context={"form_register": form})
    else:
        form = form_class()

    context = {'form_register': form}
    
    return render(request=request,
        template_name=template_name,
        context=context)


@login_required
def logout_user(request):
    """
    Logged out the user and redirect to the home page
    """
    logout(request)
    messages.success(
        request=request,
        message='خروج از حساب کاربری با موفقیت انجام شد.', 
        extra_tags="success")
    return redirect("account:home")


def pagination(object_list, per_page: int, page_number: int):
    """
    Determine how many projects will be displayed per page.

    Args:
        object_list (project): project QuerySet.
        per_page (int): Number of projects per page.
        page_number (int): page number(page=1, page=2, etc...)

    Returns:
        list of projects.
    """
    paginator = Paginator(object_list=object_list, per_page=per_page)
    projects = paginator.get_page(number=page_number)

    context = {'obj_list': projects}
    return context


@login_required
def dashboard(request, template_name='account/dashboard/dashboard.html'):
    """ Not completed """
    return render(request=request, template_name=template_name)


@login_required
def manage_received_apply(request, model_form=ConversationForm, template_name='account/dashboard/manage-received-apply.html'):
    """ Not completed """
    page_number = request.GET.get('page')
    applay_project = ApplyProject.objects.filter(project__user=request.user)
    applays = pagination(applay_project, 10, page_number)

    context = {
        "applys": applys,
        "reply_form": model_form()
    }
    return render(request, template_name=template_name, context=context)


@login_required
def manage_send_apply(request, model_form=ConversationForm, template_name='account/dashboard/manage-send-apply.html'):
    """ Not completed """
    page_number = request.GET.get('page')
    applay_project = ApplyProject.objects.filter(user=request.user).prefetch_related("conversation")
    applys = pagination(applay_project, 10, page_number)

    context = {
        "applys": applys,
        "reply_form": model_form()
    }
    return render(request=request, template_name=template_name, context=context)


@login_required
def candidate_profile(request, username, template_name='account/dashboard/candidate-profile.html'):
    """ Not completed """
    user = get_object_or_404(get_user_model(), username=username)
    context = {'user_prof':user}
    return render(request, template_name=template_name, context=context)


@login_required
def user_messages(request, template_name='account/dashboard/user-messages.html'):
    """ Not completed """
    return render(request, template_name=template_name)


@login_required
def edit_profile(request, success_url="account:dashboard", form_class=EditProfileForm,
    template_name='account/dashboard/edit-profile.html'):
    """
    Update user profile.
    """
    profile = get_object_or_404(klass=Profile, user=request.user)

    #=> Add existing values
    initial_form_data = {
        "first_name": profile.user.first_name,
        "last_name": profile.user.last_name,
        "bio": profile.bio,
        "skills": request.user.user_cv.skills,
        "avatar": profile.avatar}

    if request.method == "POST":
        form = form_class(data=request.POST, files=request.FILES, initial=initial_form_data)
        if form.is_valid():
            form.save(user_id=request.user.id, profile_model=Profile)
            messages.success(request=request, message="پروفایل شما با موفقیت اپدیت شد.")
            return redirect(success_url)
    else:
        form = form_class(initial=initial_form_data)
        return render(request=request, template_name=template_name, context={'forms': form})


@login_required
def manage_project(request, template_name='account/dashboard/manage-project.html'):
    """
    Show a list of available user projects.
    """
    page_number = request.GET.get('page')
    projects = Project.objects.filter(
        user=request.user).order_by("-created")
    context = pagination(object_list=projects, per_page=5, page_number=page_number)
    return render(request=request, template_name=template_name, context=context)
