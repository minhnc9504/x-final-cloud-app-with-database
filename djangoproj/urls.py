from django.contrib import admin
from django.urls import path
from django.urls.converters import register_converter
from django.views.generic import TemplateView
from . import views


# Custom URL converter: only accepts valid US state abbreviations
class StateConverter:
    regex = r'(TX|MN|KS|CA|NY|FL|GA|IL|OH|PA|MI|VA|NC|NJ|WA|AZ|MA|TN|IN|MO|MD|WI|MN|CO|AL|SC|LA|KY|OR|OK|CT|IA|UT|NV|NM|WV|ID|HI|NH|ME|MT|RI|DE|ND|SD|AK|DC)'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(StateConverter, 'state_code')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Static HTML pages
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact/', TemplateView.as_view(template_name="Contact.html"), name='contact'),

    # Health check
    path('api/health/', views.health_check, name='health_check'),
    path('api/whoami/', views.api_whoami, name='api_whoami'),

    # Auth APIs
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/register/', views.api_register, name='api_register'),

    # Car Makes & Models APIs
    path('api/carmakes/', views.api_get_all_carmakes, name='api_get_all_carmakes'),
    path('api/carmakes/create/', views.api_carmake_create, name='api_carmake_create'),
    path('api/carmodels/create/', views.api_carmodel_create, name='api_carmodel_create'),

    # Dealer detail page (must come before generic patterns)
    path('dealer/<int:dealer_id>/', views.dealer_detail, name='dealer_detail'),

    # Review APIs
    path('api/dealers/<int:dealer_id>/reviews/', views.api_get_dealer_reviews, name='api_get_dealer_reviews'),
    path('api/dealers/<int:dealer_id>/reviews/post/', views.api_post_review, name='api_post_review'),

    # Dealer APIs (proxy to microservice)
    path('api/dealers/', views.proxy_dealers, name='proxy_dealers'),
    path('api/dealers/dealer/<int:dealer_id>/', views.proxy_dealer_by_id, name='proxy_dealer_by_id'),
    # State filter - uses custom converter that only matches valid US state abbreviations
    path('api/dealers/<state_code:state>/', views.proxy_dealers_by_state, name='proxy_dealers_by_state'),

    # Sentiment Analysis API
    path('api/analyze/sentiment/', views.api_analyze_sentiment, name='api_analyze_sentiment'),

    # Seed Data API
    path('api/seed/', views.api_seed_data, name='api_seed_data'),
]
