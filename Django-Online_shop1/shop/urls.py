from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
   
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.home, name='category_filter'),
    path('search/', views.search, name='search_products'),
    path('search/', views.search, name='search'),  # Add this line
    path('<slug:slug>/', views.product_detail, name='product_detail'),  # Keep this last to avoid conflicts
]
    


