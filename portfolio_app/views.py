from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, PortfolioForm
from .models import Portfolio
from .forms import PortfolioForm
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# @login_required
# def choose_template(request):
#     if request.method == 'POST':
#         template = request.POST.get('template')
#         if template:
#             return redirect('create_portfolio', template=template)
#     return render(request, 'choose_template.html')
def choose_template(request):
    # Check if the user is authenticated and their portfolio exists
    if request.user.is_authenticated:
        try:
            # Try to get the user's portfolio
            portfolio = Portfolio.objects.get(user=request.user)
            # Redirect to the edit portfolio view if it exists
            return redirect('edit_portfolio')
        except Portfolio.DoesNotExist:
            # If the portfolio doesn't exist, redirect to create one
            if request.method == 'POST':
                return redirect('create_portfolio')
    
    # If the request method is not POST, render the choose template page
    return render(request, 'choose_template.html')
# def choose_template(request):
#     if request.method == 'POST':
#         # You can handle template selection here if needed, but not use it directly
#         return redirect('create_portfolio')  # No need to pass any parameters
#     return render(request, 'choose_template.html')


# @login_required
# def create_portfolio(request, template):
#     if request.method == 'POST':
#         form = PortfolioForm(request.POST)
#         if form.is_valid():
#             portfolio = form.save(commit=False)
#             portfolio.user = request.user
#             portfolio.template = template
#             portfolio.save()
#             return redirect('edit_portfolio', portfolio_id=portfolio.id)
#     else:
#         form = PortfolioForm(initial={'template': template})
#     return render(request, 'create_portfolio.html', {'form': form, 'template': template})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import Portfolio, Project
from .forms import PortfolioForm, ProjectForm

# @login_required
# def edit_portfolio(request):
#     portfolio, created = Portfolio.objects.get_or_create(user=request.user)
#     ProjectFormSet = inlineformset_factory(Portfolio, Project, form=ProjectForm, extra=1, can_delete=True)
    
#     if request.method == 'POST':
#         form = PortfolioForm(request.POST, instance=portfolio)
#         formset = ProjectFormSet(request.POST, request.FILES, instance=portfolio)
#         if form.is_valid() and formset.is_valid():
#             form.save()
#             formset.save()
#             return redirect('view_portfolio')
#     else:
#         form = PortfolioForm(instance=portfolio)
#         formset = ProjectFormSet(instance=portfolio)
    
#     context = {
#         'form': form,
#         'formset': formset,
#     }
#     return render(request, 'edit_portfolio.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import Portfolio, Project
from .forms import PortfolioForm, ProjectForm

@login_required
def edit_portfolio(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    ProjectFormSet = inlineformset_factory(
        Portfolio, 
        Project, 
        form=ProjectForm, 
        extra=1, 
        can_delete=True
    )

    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        formset = ProjectFormSet(request.POST, request.FILES, instance=portfolio)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Your portfolio has been updated successfully.')
            return redirect('view_portfolio')
        else:
            messages.error(request, 'There was an error updating your portfolio. Please check the form and try again.')
    else:
        form = PortfolioForm(instance=portfolio)
        formset = ProjectFormSet(instance=portfolio)

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'edit_portfolio.html', context)

# @login_required
# def view_portfolio(request):
#     portfolio = Portfolio.objects.filter(user=request.user).first()
    
#     if not portfolio:
#         return redirect('create_portfolio')  # Redirect to the portfolio creation page if it doesn't exist
    
#     context = {
#         'portfolio': portfolio,
#     }
#     return render(request, 'view_portfolio.html', context)

@login_required
def view_portfolio(request):
    portfolio = Portfolio.objects.filter(user=request.user).first()
    
    if not portfolio:
        return redirect('create_portfolio')  # Redirect to the portfolio creation page if it doesn't exist
    
    # Fetch all projects associated with this portfolio
    projects = Project.objects.filter(portfolio=portfolio)
    skills = [skill.strip() for skill in portfolio.skills.split(',')] if portfolio.skills else []
    share_url = request.build_absolute_uri(portfolio.get_absolute_url())

    context = {
        'portfolio': portfolio,
        'projects': projects,
        'skills': skills,
        'share_url':share_url,
    }
    return render(request, 'view_portfolio.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Portfolio, Project, Feedback
from .forms import FeedbackForm

# def view_portfolio(request, username):
#     portfolio = Portfolio.objects.filter(user__username=username).first()
    
#     if not portfolio:
#         return redirect('home')  # or wherever you want to redirect if the portfolio doesn't exist
    
#     projects = Project.objects.filter(portfolio=portfolio)
#     skills = [skill.strip() for skill in portfolio.skills.split(',')] if portfolio.skills else []
    
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.portfolio = portfolio
#             feedback.save()
#             messages.success(request, 'Your feedback has been submitted successfully!')
#             return redirect('view_portfolio', username=username)
#     else:
#         form = FeedbackForm()
    
#     feedbacks = Feedback.objects.filter(portfolio=portfolio).order_by('-created_at')
    
#     context = {
#         'portfolio': portfolio,
#         'projects': projects,
#         'skills': skills,
#         'form': form,
#         'feedbacks': feedbacks,
#     }
#     return render(request, 'view_portfolio.html', context)

@login_required
def view_feedbacks(request):
    portfolio = Portfolio.objects.filter(user=request.user).first()
    if not portfolio:
        return redirect('create_portfolio')
    
    feedbacks = Feedback.objects.filter(portfolio=portfolio).order_by('-created_at')
    
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'view_feedbacks.html', context)

# @login_required
# def create_portfolio(request, template):
#     if request.method == 'POST':
#         form = PortfolioForm(request.POST)
#         if form.is_valid():
#             portfolio = form.save(commit=False)
#             portfolio.user = request.user
#             portfolio.template = template
#             portfolio.save()
#             return redirect('edit_portfolio')
#     else:
#         form = PortfolioForm()
    
#     context = {
#         'form': form,
#         'template': template
#     }
#     return render(request, 'create_portfolio.html', context)


# @login_required
# def create_portfolio(request):
#     if request.method == 'POST':
#         form = PortfolioForm(request.POST)
#         if form.is_valid():
#             portfolio = form.save(commit=False)
#             portfolio.user = request.user
#             # Set a default template or leave it blank
#             portfolio.template = 'default_template'  # Set a default or remove this line
#             portfolio.save()
#             return redirect('edit_portfolio')
#     else:
#         form = PortfolioForm()
    
#     return render(request, 'create_portfolio.html', {'form': form})




@login_required
def create_portfolio(request):
    try:
        # Try to get the user's existing portfolio
        portfolio = Portfolio.objects.get(user=request.user)
        is_new_portfolio = False
    except Portfolio.DoesNotExist:
        # If it doesn't exist, we'll create a new one
        portfolio = None
        is_new_portfolio = True

    ProjectFormSet = inlineformset_factory(Portfolio, Project, form=ProjectForm, extra=1, can_delete=True)
    
    if request.method == 'POST':
        if is_new_portfolio:
            form = PortfolioForm(request.POST, request.FILES)
        else:
            form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            
            formset = ProjectFormSet(request.POST, request.FILES, instance=portfolio)
            if formset.is_valid():
                formset.save()
            
            share_url = request.build_absolute_uri(portfolio.get_absolute_url())
            action = "created" if is_new_portfolio else "updated"
            return render(request, 'portfolio_created.html', {
                'portfolio': portfolio, 
                'share_url': share_url,
                'action': action
            })
    else:
        form = PortfolioForm(instance=portfolio)
        formset = ProjectFormSet(instance=portfolio)
    
    return render(request, 'create_portfolio.html', {
        'form': form, 
        'formset': formset,
        'is_new_portfolio': is_new_portfolio
    })

def public_portfolio_view(request, user_id):
    # Fetch portfolio by user_id
    portfolio = get_object_or_404(Portfolio, user__id=user_id)
    projects = Project.objects.filter(portfolio=portfolio)
    
    # Pass the portfolio and projects to the template
    return render(request, 'view_portfolio.html', {
        'portfolio': portfolio,
        'projects': projects
    })