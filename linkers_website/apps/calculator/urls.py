from django.urls import path
from .views import  calc
app_name = "calculator"

urlpatterns = [
    path('', calc, name='calculator'),  # Function-based view
    #path('search/', search_view, name='search_results'),  # Function-based view
    #path('search/results/', CalcResultsView.as_view(), name='search_results_list'),
    #path('search/results/',flex_calc,name='flex_calc')
    
]