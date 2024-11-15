from itertools import chain
from django.db.models import CharField, Value, Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Review, UserFollows
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import TicketForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.models import User
from review_app.models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def tickets(request):
    tickets = Ticket.objects.filter(user=request.user)

    tickets_with_reviews = []
    for ticket in tickets:
        reviews = ticket.review_set.filter(user=request.user)
        tickets_with_reviews.append({'ticket': ticket, 'reviews': reviews})

    return render(request, 'tickets.html', context={'tickets_with_reviews': tickets_with_reviews})



def get_users_viewable_tickets(user):
    tickets_from_user_and_followed = Ticket.objects.filter(
        Q(user=user) | Q(user__in=user.following.all())
    )
    posts = sorted(posts, key=lambda post: post.time_created, reverse=True)
    return tickets_from_user_and_followed

def get_users_viewable_reviews(user):
    reviews_from_user_and_followed = Review.objects.filter(
        Q(user=user) | Q(user__in=user.following.all()) | Q(ticket__user=user)
    )
    return reviews_from_user_and_followed

@login_required
def feed(request):
    user = request.user
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    followed_tickets = Ticket.objects.filter(user__in=followed_users).annotate(content_type=Value('TICKET', CharField()))
    followed_reviews = Review.objects.filter(user__in=followed_users).exclude(ticket=None).annotate(content_type=Value('REVIEW', CharField()))
    
    user_reviews = Review.objects.filter(user=user).exclude(ticket=None).annotate(content_type=Value('REVIEW', CharField()))
    user_tickets = Ticket.objects.filter(user=user).annotate(content_type=Value('TICKET', CharField()))
    responses_to_user_tickets = Review.objects.filter(ticket__user=user).exclude(user=user).annotate(content_type=Value('REVIEW', CharField()))
    user_tickets_with_reviews = Ticket.objects.filter(review__user=user)
    non_followed_tickets_with_reviews = Ticket.objects.filter(review__user__in=followed_users).exclude(user__in=followed_users).annotate(content_type=Value('TICKET', CharField()))
    
    posts = list(chain(followed_reviews, followed_tickets, user_reviews, user_tickets, responses_to_user_tickets, user_tickets_with_reviews,  non_followed_tickets_with_reviews))
    posts = sorted(posts, key=lambda post: post.time_created, reverse=True)
    
    return render(request, 'feed.html', context={'posts': posts})

@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('feed')
    else:
        form = TicketForm()

    return render(request, 'create_ticket.html', {'form': form})

@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed') 
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {
        'ticket': ticket,
        'form': form
    })
    
    
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "La critique a été modifiée avec succès.")
            return redirect('feed') 
    else:
        form = ReviewForm(instance=review)

    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "La critique a été supprimée avec succès.")
        return redirect('tickets')

    return render(request, 'delete_review.html', {'review': review})


@login_required
def create_ticket_and_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    
    return render(request, 'create_ticket_and_review.html', {'ticket_form': ticket_form, 'review_form': review_form})

@login_required
def request_review(request):
    """
    Permet de créer un billet pour demander une critique.
    """
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, "Votre demande de critique a été créée.")
            return redirect('feed')
    else:
        form = TicketForm()

    return render(request, 'request_review.html', {'form': form})


@login_required
def manage_follows(request):
    if request.method == 'POST':
        username_to_follow = request.POST.get('username')
        try:
            user_to_follow = CustomUser.objects.get(username=username_to_follow)
            UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow)
            messages.success(request, f"Vous suivez maintenant {username_to_follow}.")
        except CustomUser.DoesNotExist:
            messages.error(request, f"Utilisateur {username_to_follow} introuvable.")

    followed_users = UserFollows.objects.filter(user=request.user).select_related('followed_user')

    return render(request, 'manage_follows.html', {
        'followed_users': followed_users
    })
    
@login_required
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = CustomUser.objects.get(id=user_id)
        UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")

    return redirect('manage_follows')

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user) 
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save() 
            messages.success(request, "Le ticket a été modifié avec succès.")
            return redirect('tickets') 
    else:
        form = TicketForm(instance=ticket) 

    return render(request, 'edit_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user) 
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès.")
        return redirect('tickets')
    return render(request, 'delete_ticket.html', {'ticket': ticket})

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})

