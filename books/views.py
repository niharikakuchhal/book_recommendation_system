from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import search_books
from .forms import RegisterForm, RecommendationForm, CommentForm
from django.http import JsonResponse
from .models import Recommendation, Comment, Like
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages

def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'books/home.html', {'username': username})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'books/register.html')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        auth_login(request, user)
        return redirect('home')

    return render(request, 'books/register.html')
    #     user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
    #     user.save()
    #     return redirect('login')
    # return render(request, 'books/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_recommendation')
        else:
            return render(request, 'books/login.html', {'error': 'Invalid credentials'})
    return render(request, 'books/login.html')

def user_logout(request):
    logout(request)
    # return render(request, 'books/login.html')
    return redirect('login')

def book_recommendation(request):
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'books/home.html', {'username': username})

@login_required
def add_comment(request, recommendation_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        recommendation = get_object_or_404(Recommendation, pk=recommendation_id)
        Comment.objects.create(recommendation=recommendation, user=request.user, text=text)
        return redirect('recommended_books')
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required   
def like_recommendation(request):
    if request.method == 'POST':
        recommendation_id = request.POST.get('recommendation_id')
        recommendation = get_object_or_404(Recommendation, id=recommendation_id)
        user = request.user
        
        # Check if the user has already liked this recommendation
        existing_like = Like.objects.filter(user=user, recommendation=recommendation).first()
        
        if existing_like:
            messages.info(request, 'You have already liked this recommendation.')
        else:
            # Add a new like
            Like.objects.create(user=user, recommendation=recommendation)
            messages.success(request, 'You liked this recommendation.')
        
        return redirect('recommended_books')
    
    return redirect('home')
    #  if request.method == "POST":
    #     recommendation_id = request.POST.get('recommendation_id')
    #     recommendation = Recommendation.objects.get(id=recommendation_id)
        
    #     # Check if the user has already liked this recommendation
    #     if Like.objects.filter(user=request.user, recommendation=recommendation).exists():
    #         return JsonResponse({"message": "You have already liked this recommendation"})
        
    #     # Proceed to add the like
    #     like = Like(user=request.user, recommendation=recommendation)
    #     like.save()
        
    #     # After liking, redirect or return a response
    #     return JsonResponse({"message": "You liked this recommendation"})
    # if request.method == 'POST':
    #     recommendation_id = request.POST.get('recommendation_id')
    #     recommendation = get_object_or_404(Recommendation, pk=recommendation_id)
    #     if request.user not in recommendation.likes.all():
    #         recommendation.likes.add(request.user)
    #         recommendation.save()
    #     return redirect('recommended_books')
    # return JsonResponse({'error': 'Invalid request'}, status=400)

    # if request.method == 'POST':
    #     recommendation_id = request.POST.get('recommendation_id')
    #     if not recommendation_id:
    #         return JsonResponse({'error': 'Recommendation ID is required'}, status=400)

    #     try:
    #         recommendation = get_object_or_404(Recommendation, pk=recommendation_id)
    #         recommendation.likes += 1
    #         recommendation.save()
    #         return JsonResponse({'likes': recommendation.likes})
    #     except Exception as e:
    #         return JsonResponse({'error': str(e)}, status=400)
    # return JsonResponse({'error': 'Invalid request'}, status=400)
    #     recommendation.likes += 1
    #     recommendation.save()
    #     return JsonResponse({'likes': recommendation.likes})
    # return JsonResponse({'error': 'Invalid request'}, status=400)
    

@api_view(['GET'])
def search_book(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'title')
    page = int(request.GET.get('page', 1))
    limit = 25
    start_index = (page - 1) * limit
    response = search_books(query, search_type, start_index, limit)

    if 'error' in response:
        return render(request, 'books/search_result.html', {'error': response['error']})

    books = response.get('items', [])
    total_items = response.get('totalItems', 0)
    total_pages = (total_items // limit) + (1 if total_items % limit > 0 else 0)

    context = {
        'books': books,
        'page': page,
        'total_pages': total_pages,
        'query': query,
        'search_type': search_type,
        'limit': limit,
    }

    return render(request, 'books/search_results.html', context)

@api_view(['POST'])
@login_required
def add_to_recommendations(request):
    if request.method == 'POST':
        book_data = {
            'book_title': request.POST.get('book_title'),
            'book_description': request.POST.get('book_description'),
            'author': request.POST.get('author'),
            'link': request.POST.get('link'),
            'cover_image': request.POST.get('cover_image'),
            'rating': request.POST.get('rating'),
            'category': request.POST.get('category'),
            'publication_date': request.POST.get('publication_date'),
            
        }
        user = request.user
        recommendation = Recommendation(user=user, **book_data)
        recommendation.save()

        # Create a Like object to link the user with this recommendation
        Like.objects.create(user=user, recommendation=recommendation)
        # recommendation.save()
        return render(request, 'books/success.html', {"message": "Book added to recommendations successfully"})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
    

@login_required
def view_recommendations(request):
    recommendations = Recommendation.objects.filter(user=request.user)
    context = {
        'recommendations': recommendations,
    }
    return render(request, 'books/my_recommendations.html', context)
    # recommendations = Recommendation.objects.filter(user=request.user)
    # return render(request, 'books/my_recommendations.html', {'recommendations': recommendations})
    

def recommended_books(request):
    recommendations = Recommendation.objects.all()
    genres = Recommendation.objects.values_list('category', flat=True).distinct()
    category = request.GET.get('category')
    if category:
        recommendations = recommendations.filter(category=category)
    sort_by = request.GET.get('sort_by')
    if sort_by == 'rating':
        recommendations = recommendations.order_by('-rating')
    elif sort_by == 'publication_date':
        recommendations = recommendations.order_by('-publication_date')
    recommendation_count = recommendations.count()
    context = {
        'recommendations': recommendations,
        'genres': genres,
        'recommendation_count': recommendation_count
    }
    return render(request, 'books/recommended_books.html', context)

@login_required
def recommend_book_form(request):
    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        link = request.POST.get('link')
        book_description = request.POST.get('book_description')
        publication_date = request.POST.get('publication_date')
        recommendation = Recommendation.objects.create(
            user=request.user,
            book_title=book_title,
            author=author,
            category=category,
            link=link,
            book_description=book_description,
            publication_date=publication_date,
        )
        # return JsonResponse({'success': True, 'message': 'Book recommended successfully', 'redirect_url': 'recommended_books'})
        return redirect('recommended_books')

    return render(request, 'books/recommend_book_form.html')
