from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import csv_files as CsvFilesModel
from .models import clean_actas as CleanActasModel
from .models import actas_bd as ActasModel
from .models import Print as PrintedActasModel
from .forms import BdActasForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pandas as pd

def actas_view(request):
    """
    Renders the 'actas.html' template and sends the 'bd_records' to the template.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template with the 'bd_records' context variable.
    """
    bd_records = ActasModel.objects.all()

    bd_records = bd_records.order_by('date_created')

    for record in bd_records:
         if record.posiciones == 'nan':
             record.posiciones = ''
             record.save()

    if request.user.is_authenticated:
        return render(request, 'actas_lps/actas.html', {'bd_records': bd_records})
    else:
        messages.error(request, "Please login to view this page.")
        return redirect('home')

def generar_actas(request):
    """
    Renders the 'generar_actas.html' template.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template.
    """
    if request.user.is_authenticated:
        if 'file_uploaded' in request.session:
            del request.session['file_uploaded']

        context = {}            
        return render(request, 'actas_lps/generar_actas.html', context)
    else:
        messages.error(request, "Please login to view this page.")
        return redirect('home')

@csrf_exempt
def csv_files(request):
    """
    Handles the POST request for uploading a CSV file.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A JSON response with a success message if the file is uploaded successfully.
    - Redirects to 'generar_actas' if the request method is not POST.
    """
    if request.method == 'POST':
        file = request.FILES['file']
        my_model = CsvFilesModel(file=file)
        my_model.save()
        request.session['file_uploaded'] = True
        return JsonResponse({'message': 'File uploaded successfully!'})  
    else:
        return redirect('generar_actas')

def process_csv(request):
    """
    Processes the uploaded CSV file and renders the 'generar_actas.html' template with the processed data.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template with the processed data.
    """
    if 'file_uploaded' in request.session:
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        processed_data = df.to_dict('records')
        return render(request, 'actas_lps/generar_actas.html', {'records_csv': processed_data})
    else:
        messages.error(request, "Sube un archivo para poder procesarlo.")
        return redirect('generar_actas')

@csrf_exempt
def update_data(request):
    """
    Updates the data in the CSV file based on the provided ID, column, and new value.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A JSON response with a success status.
    """
    if request.method == 'POST':
        id = request.POST.get('id')
        column = request.POST.get('column')
        new_value = request.POST.get('new_value')
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        df.objects.filter(id=id).update(**{column: new_value})
        return JsonResponse({'status': 'success'})

def cleaned_csv(request):
    """
    Cleans the uploaded CSV file and renders the 'generar_actas.html' template with the cleaned data.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template with the cleaned data.
    """
    if 'file_uploaded' in request.session:
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        df_cleaned = CleanActasModel(df)
        df_cleaned.upper_case_column('EECC')
        df_cleaned.upper_case_column('Proyecto')
        df_cleaned.no_spaces('EECC')
        df_cleaned.no_spaces('Proyecto')
        df_cleaned.no_commas('total_OC')
        df_cleaned.no_commas('total_certificar')
        df_cleaned.convert_to_int('OC')
        df_cleaned.clean_nan('posiciones')
        df_cleaned.value_rounded_2(['total_OC','total_certificar'])
        df = df_cleaned.return_df()
        processed_data = df.to_dict('records')
        df.to_csv(my_model.file.path, sep=';', encoding='latin-1', index=False)
        return render(request, 'actas_lps/generar_actas.html', {'records_csv': processed_data})
    else:
        messages.error(request, "Error al procesar el archivo.")
        return redirect('generar_actas')

@csrf_exempt
def save_data(request):
    """
    Saves the data from the last uploaded CSV file to the ActasModel and generates an Excel file.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A FileResponse object with the generated Excel file.
    """
    if 'file_uploaded' in request.session:
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        df['termino_obra'] = pd.to_datetime(df['termino_obra'], format='%d/%m/%Y')
        df['servicio_obra'] = pd.to_datetime(df['servicio_obra'], format='%d/%m/%Y')
        for index, row in df.iterrows():
            ActasModel.objects.create(
                EECC=row['EECC'],
                Proyecto=row['Proyecto'],
                OC=row['OC'],
                IP_Hijo=row['IP_Hijo'],
                total_OC=row['total_OC'],
                total_certificar=row['total_certificar'],
                termino_obra=row['termino_obra'],
                servicio_obra=row['servicio_obra'],
                posiciones=row['posiciones'],
            )
        df_to_xlsx = PrintedActasModel(df)
        df_to_xlsx.print_actas()
        df_to_xlsx.created_excel_files_zip()
        my_model.delete()
        response = FileResponse(open('actas_lps/printed_xls/zip_files/excel_files.zip', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="excel_files.zip"'
        return response
    else:
        messages.error(request, "Necesitas subir un archivo primero.")
        return redirect('generar_actas')
    
#Actas views


def actas_record(request, pk):

    if request.user.is_authenticated:
        # Get the record
        record_actas = ActasModel.objects.get(id=pk)

        # Send the record to the template
        return render( request, 'actas_lps/actas_record.html', {'record_actas': record_actas} )
    
    else:
        messages.error(request, "Please login to view this record.")
        return redirect('home')   


def actas_update(request, pk):
	if request.user.is_authenticated:
		current_record = ActasModel.objects.get(id=pk)
		form = BdActasForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('actas')
		return render(request, 'actas_lps/actas_updated.html', {'form':form})
	else:
		messages.error(request, "You Must Be Logged In...")
		return redirect('home')


def actas_delete(request, pk):
	if request.user.is_authenticated:
		delete_it = ActasModel.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('actas')
	else:
		messages.error(request, "You Must Be Logged In To Do That...")
		return redirect('home')
     
     
def actas_create(request):
    if request.user.is_authenticated:
        form = BdActasForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Created!")
            return redirect('actas')
        return render(request, 'actas_lps/actas_create.html', {'form':form})
    else:
        messages.error(request, "You Must Be Logged In To Do That...")
        return redirect('home')


@csrf_exempt
def multiple_select(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            selected_pks = request.POST.getlist('pks')
            selected_pks = [int(pk) for pk in selected_pks]

            if len(selected_pks) > 0:
                if request.POST.get('delete'):
                    deletes_multiple = ActasModel.objects.filter(pk__in=selected_pks)
                    deletes_multiple.delete()
                    messages.success(request, "Acta eliminada con exito...")
                    return redirect('actas')
            
                elif request.POST.get('print'):
                    df = pd.DataFrame(list(ActasModel.objects.filter(pk__in=selected_pks).values()), columns=['id','EECC', 'Proyecto', 'OC', 'IP_Hijo', 'total_OC', 'total_certificar', 'termino_obra', 'servicio_obra', 'posiciones', 'date_created'])
                    print(df)
                    df_to_xlsx = PrintedActasModel(df)
                    df_to_xlsx.print_actas()
                    df_to_xlsx.created_excel_files_zip()
                    response = FileResponse(open('actas_lps/printed_xls/zip_files/excel_files.zip', 'rb'))
                    response['Content-Disposition'] = 'attachment; filename="excel_files.zip"'
                    messages.success(request, "Imprimiendo Actas seleccionadas")
                    return response
                
            else:
                messages.success(request, "Selecciona alguna acta para poder continuar")
                return redirect('actas')
            
    else:
        messages.error(request, "You Must Be Logged In To Do That...")
        return redirect('home')
    

    # SEARCH ACTAS VIEWS

def search_actas(request):
    """
    Renders the 'generar_actas.html' template.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template.
    """
    if request.user.is_authenticated:
        if 'file_uploaded' in request.session:
            del request.session['file_uploaded']

        context = {}            
        return render(request, 'actas_lps/search_actas.html', context)
    else:
        messages.error(request, "Please login to view this page.")
        return redirect('home')
          

def process_csv_search(request):
    """
    Processes the uploaded CSV file and renders the 'generar_actas.html' template with the processed data.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template with the processed data.
    """
    if 'file_uploaded' in request.session:
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        #Search the df data in the database by OC then create a new df with a new column, if the OC is found in the database, the new column will be True, if not, False
        df['found'] = df['OC'].isin(ActasModel.objects.values_list('OC', flat=True))
        #get all the data from the database that matches the OC in the df
        df_db = ActasModel.objects.filter(OC__in=df['OC'])

        #convert the data from the database to a df
        df_db = pd.DataFrame(list(df_db.values()), columns=['id','EECC', 'Proyecto', 'OC', 'IP_Hijo', 'total_OC', 'total_certificar', 'termino_obra', 'servicio_obra', 'posiciones', 'date_created'])        
        #Merge the df and the df_db
        df = df.merge(df_db, on='OC', how='left')
        #Convert the id column to a int and fill the NaN values with 0
        df['id'] = df['id'].fillna(0).astype(int)

        processed_data = df.to_dict('records')
        return render(request, 'actas_lps/search_actas.html', {'records_csv': processed_data})
    else:
        messages.error(request, "Sube un archivo para poder procesarlo.")
        return redirect('search_actas')
    

def download_csv_search(request):
     # Use the records_csv context variable to create a new CSV file and download it
    if 'file_uploaded' in request.session:
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        df['found'] = df['OC'].isin(ActasModel.objects.values_list('OC', flat=True))
        df_db = ActasModel.objects.filter(OC__in=df['OC'])
        df_db = pd.DataFrame(list(df_db.values()), columns=['id','EECC', 'Proyecto', 'OC', 'IP_Hijo', 'total_OC', 'total_certificar', 'termino_obra', 'servicio_obra', 'posiciones', 'date_created'])        
        df = df.merge(df_db, on='OC', how='left')
        df['id'] = df['id'].fillna(0).astype(int)
        df = df.drop_duplicates(subset=["OC","total_OC","total_certificar"])
        df.to_csv(my_model.file.path, sep=';', encoding='latin-1', index=False)
        response = FileResponse(open(my_model.file.path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="searched_actas.csv"'
        return response
    else:
        messages.error(request, "Sube un archivo para poder procesarlo.")
        return redirect('search_actas')
    

def print_actas_s(request):
    """
    Saves the data from the last uploaded CSV file to the ActasModel and generates an Excel file.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A FileResponse object with the generated Excel file.
    """
    if 'file_uploaded' in request.session:
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        df['found'] = df['OC'].isin(ActasModel.objects.values_list('OC', flat=True))
        df_db = ActasModel.objects.filter(OC__in=df['OC'])
        df_db = pd.DataFrame(list(df_db.values()), columns=['id','EECC', 'Proyecto', 'OC', 'IP_Hijo', 'total_OC', 'total_certificar', 'termino_obra', 'servicio_obra', 'posiciones', 'date_created']) 
        #Erase duplicated in csv
        df_db.drop_duplicates(subset=["OC","total_OC","total_certificar"])
        print(df_db)
        df_to_xlsx = PrintedActasModel(df_db)
        df_to_xlsx.print_actas()
        df_to_xlsx.created_excel_files_zip()
        my_model.delete()
        response = FileResponse(open('actas_lps/printed_xls/zip_files/excel_files.zip', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="excel_files.zip"'
        return response
    else:
        messages.error(request, "Necesitas subir un archivo primero.")
        return redirect('search_actas') 
     
     