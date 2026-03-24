from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from carsapp.models import CarMake, CarModel
import json
import urllib.request
import urllib.error


def health_check(request):
    return JsonResponse({"status": "ok", "message": "Django server is running"})


def api_whoami(request):
    """Trả về trạng thái đăng nhập (session Django, ví dụ sau khi login /admin/)."""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'username': request.user.username,
        })
    return JsonResponse({'authenticated': False, 'username': None})


# ==================== AUTH API ====================
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'username': user.username
                })
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials'
            }, status=401)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout successful'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')

            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'}, status=400)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return JsonResponse({'success': True, 'message': 'User registered successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ==================== CAR MAKES & MODELS API ====================
def api_get_all_carmakes(request):
    makes = CarMake.objects.all().prefetch_related('carmodel_set')
    data = []
    for make in makes:
        models = list(make.carmodel_set.values('id', 'name', 'type', 'year'))
        data.append({
            'id': make.id,
            'name': make.name,
            'description': make.description,
            'models': models
        })
    return JsonResponse({'makes': data})


@csrf_exempt
def api_carmake_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            make = CarMake.objects.create(
                name=data['name'],
                description=data.get('description', '')
            )
            return JsonResponse({'success': True, 'id': make.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_carmodel_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model = CarModel.objects.create(
                car_make_id=data['car_make_id'],
                name=data['name'],
                type=data.get('type', 'Sedan'),
                year=data.get('year', 2024)
            )
            return JsonResponse({'success': True, 'id': model.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ==================== DEALER & REVIEW API (Proxy to Microservice) ====================


def proxy_dealers(request):
    try:
        url = f'{settings.MICROSERVICE_URL}/fetchDealers'
        with urllib.request.urlopen(url, timeout=5) as response:
            data = response.read()
            return JsonResponse(json.loads(data), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def proxy_dealers_by_state(request, state):
    try:
        # Map state abbreviations to full names used in microservice data
        state_map = {
            'TX': 'Texas',
            'MN': 'Minnesota',
            'KS': 'Kansas',
            'CA': 'California',
            'NY': 'New York',
            'FL': 'Florida',
            'GA': 'Georgia',
            'IL': 'Illinois',
            'OH': 'Ohio',
            'PA': 'Pennsylvania',
            'MI': 'Michigan',
            'VA': 'Virginia',
            'NC': 'North Carolina',
            'NJ': 'New Jersey',
            'WA': 'Washington',
            'AZ': 'Arizona',
            'MA': 'Massachusetts',
            'TN': 'Tennessee',
            'IN': 'Indiana',
            'MO': 'Missouri',
            'MD': 'Maryland',
            'WI': 'Wisconsin',
            'CO': 'Colorado',
            'AL': 'Alabama',
            'SC': 'South Carolina',
            'LA': 'Louisiana',
            'KY': 'Kentucky',
            'OR': 'Oregon',
            'OK': 'Oklahoma',
            'CT': 'Connecticut',
            'IA': 'Iowa',
            'UT': 'Utah',
            'NV': 'Nevada',
            'NM': 'New Mexico',
            'WV': 'West Virginia',
            'ID': 'Idaho',
            'HI': 'Hawaii',
            'NH': 'New Hampshire',
            'ME': 'Maine',
            'MT': 'Montana',
            'RI': 'Rhode Island',
            'DE': 'Delaware',
            'ND': 'North Dakota',
            'SD': 'South Dakota',
            'AK': 'Alaska',
            'DC': 'District of Columbia',
        }
        full_name = state_map.get(state, state)
        url = f'{settings.MICROSERVICE_URL}/fetchDealers/{full_name}'
        with urllib.request.urlopen(url, timeout=5) as response:
            data = response.read()
            return JsonResponse(json.loads(data), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def proxy_dealer_by_id(request, dealer_id):
    try:
        url = f'{settings.MICROSERVICE_URL}/fetchDealer/{dealer_id}'
        with urllib.request.urlopen(url, timeout=5) as response:
            data = response.read()
            return JsonResponse(json.loads(data), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== REVIEW API ====================
REVIEWS_DB = {}  # In-memory store: {dealer_id: [reviews]}


def get_reviews(dealer_id):
    if dealer_id not in REVIEWS_DB:
        REVIEWS_DB[dealer_id] = []
    return REVIEWS_DB[dealer_id]


def api_get_dealer_reviews(request, dealer_id):
    reviews = get_reviews(dealer_id)
    return JsonResponse({'dealer_id': int(dealer_id), 'reviews': reviews})


@csrf_exempt
def api_post_review(request, dealer_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            review = {
                'id': len(get_reviews(dealer_id)) + 1,
                'dealer_id': int(dealer_id),
                'reviewer': data.get('reviewer', 'Anonymous'),
                'rating': int(data.get('rating', 5)),
                'text': data.get('text', ''),
                'sentiment': data.get('sentiment', 'neutral')
            }
            get_reviews(dealer_id).append(review)
            return JsonResponse({'success': True, 'review': review})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ==================== DEALER DETAIL PAGE ====================
def dealer_detail(request, dealer_id):
    return render(request, 'dealer.html', {'dealer_id': dealer_id})


# ==================== SENTIMENT ANALYSIS API ====================
def api_analyze_sentiment(request):
    text = request.GET.get('text', '')
    text_lower = text.lower()

    if any(word in text_lower for word in ['fantastic', 'excellent', 'amazing', 'wonderful', 'great', 'love', 'best', 'perfect']):
        sentiment = 'Positive'
        score = 0.95
    elif any(word in text_lower for word in ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'poor', 'disappointed']):
        sentiment = 'Negative'
        score = -0.85
    else:
        sentiment = 'Neutral'
        score = 0.1

    return JsonResponse({
        'text': text,
        'sentiment': sentiment,
        'score': score
    })


# ==================== ADMIN DATA API (for seeding) ====================
@csrf_exempt
def api_seed_data(request):
    if request.method == 'POST':
        # Seed CarMake and CarModel data
        makes_data = [
            {'name': 'Toyota', 'description': 'Reliable and fuel-efficient vehicles', 'models': [
                {'name': 'Camry', 'type': 'Sedan', 'year': 2023},
                {'name': 'RAV4', 'type': 'SUV', 'year': 2023},
                {'name': 'Corolla', 'type': 'Sedan', 'year': 2024},
            ]},
            {'name': 'Honda', 'description': 'Performance and innovation', 'models': [
                {'name': 'Accord', 'type': 'Sedan', 'year': 2023},
                {'name': 'CR-V', 'type': 'SUV', 'year': 2023},
                {'name': 'Civic', 'type': 'Sedan', 'year': 2024},
            ]},
            {'name': 'Ford', 'description': 'Built Ford Tough', 'models': [
                {'name': 'F-150', 'type': 'WAGON', 'year': 2023},
                {'name': 'Explorer', 'type': 'SUV', 'year': 2023},
                {'name': 'Mustang', 'type': 'Sedan', 'year': 2024},
            ]},
            {'name': 'Chevrolet', 'description': 'American automotive excellence', 'models': [
                {'name': 'Silverado', 'type': 'WAGON', 'year': 2023},
                {'name': 'Equinox', 'type': 'SUV', 'year': 2023},
                {'name': 'Malibu', 'type': 'Sedan', 'year': 2024},
            ]},
            {'name': 'BMW', 'description': 'The ultimate driving machine', 'models': [
                {'name': '3 Series', 'type': 'Sedan', 'year': 2024},
                {'name': 'X3', 'type': 'SUV', 'year': 2024},
                {'name': '5 Series', 'type': 'Sedan', 'year': 2024},
            ]},
        ]

        created = 0
        for make_data in makes_data:
            models_data = make_data.pop('models')
            make, _ = CarMake.objects.get_or_create(
                name=make_data['name'],
                defaults={'description': make_data['description']}
            )
            for model_data in models_data:
                CarModel.objects.get_or_create(
                    car_make=make,
                    name=model_data['name'],
                    defaults={'type': model_data['type'], 'year': model_data['year']}
                )
                created += 1

        # Seed reviews
        seed_reviews = {
            1: [
                {'reviewer': 'John Doe', 'rating': 5, 'text': 'Fantastic services! Highly recommend this dealership.', 'sentiment': 'Positive'},
                {'reviewer': 'Jane Smith', 'rating': 4, 'text': 'Good experience overall, friendly staff.'},
            ],
            2: [
                {'reviewer': 'Mike Johnson', 'rating': 5, 'text': 'Amazing service and great car selection!', 'sentiment': 'Positive'},
            ],
            3: [
                {'reviewer': 'Sarah Williams', 'rating': 4, 'text': 'Professional team, smooth buying process.', 'sentiment': 'Positive'},
            ],
        }
        for dealer_id, reviews in seed_reviews.items():
            if dealer_id not in REVIEWS_DB:
                REVIEWS_DB[dealer_id] = []
            for i, r in enumerate(reviews):
                REVIEWS_DB[dealer_id].append({
                    'id': i + 1,
                    'dealer_id': dealer_id,
                    'reviewer': r['reviewer'],
                    'rating': r['rating'],
                    'text': r['text'],
                    'sentiment': r.get('sentiment', 'Neutral')
                })

        return JsonResponse({'success': True, 'message': f'Seeded data successfully. {created} models created.'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
