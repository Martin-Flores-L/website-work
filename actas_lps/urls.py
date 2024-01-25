from django.urls import path
from . import views

urlpatterns = [
    path('actas_lps/' , views.actas_view, name='actas'),
    path('actas_lps/actas/' , views.actas_view, name='actas'),
    path('actas_lps/generar_actas/' , views.generar_actas, name='generar_actas'),
    path('actas_lps/csv_files/' , views.csv_files, name='csv_files'),
    path('actas_lps/generar_actas/process' , views.process_csv, name='process_csv'),
    path('actas_lps/generar_actas/cleaned' , views.cleaned_csv, name='cleaned_csv'),
    path('actas_lps/generar_actas/update_data' , views.update_data, name='update_data'),
    path('actas_lps/generar_actas/save_data' , views.save_data, name='save_data'),
]