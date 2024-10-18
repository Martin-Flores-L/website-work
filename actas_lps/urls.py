from django.urls import path
from . import views

urlpatterns = [
    path('actas_lps/' , views.actas_view, name='actas'),
    path('actas_lps/actas/' , views.actas_view, name='actas'),
    path('actas_lps/actas/<int:pk>' , views.actas_record, name='actas_record'),
    path('actas_lps/update_actas/<int:pk>' , views.actas_update, name='actas_update'),
    path('actas_lps/delete_actas/<int:pk>' , views.actas_delete, name='actas_delete'),
    path('actas_lps/actas_create' , views.actas_create, name='actas_create'),
    path('actas_lps/multiple_select/' , views.multiple_select, name='multiple_select'),
    path('actas_lps/generar_actas/' , views.generar_actas, name='generar_actas'),
    path('actas_lps/csv_files/' , views.csv_files, name='csv_files'),
    path('actas_lps/generar_actas/process' , views.process_csv, name='process_csv'),
    path('actas_lps/generar_actas/cleaned' , views.cleaned_csv, name='cleaned_csv'),
    path('actas_lps/generar_actas/update_data' , views.update_data, name='update_data'),
    path('actas_lps/generar_actas/save_data' , views.save_data, name='save_data'),
    path('actas_lps/search_actas' , views.search_actas, name='search_actas'),
    path('actas_lps/search_actas/process' , views.process_csv_search, name='process_csv_search'),
    path('actas_lps/search_actas/download_csv' , views.download_csv_search, name='download_csv_search'),
    path('actas_lps/search_actas/print_actas_s' , views.print_actas_s, name='print_actas_s'),
]