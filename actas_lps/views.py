from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import csv_files as CsvFilesModel
from .models import clean_actas as CleanActasModel
from .models import actas_bd as ActasModel
from .models import Print as PrintedActasModel
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pandas as pd





# ACTAS.HTML VIEW
def actas_view(request):

    bd_records = ActasModel.objects.all()

    if request.user.is_authenticated:
        # Send the record to the template
        return render( request, 'actas_lps/actas.html', {'bd_records': bd_records} )
    
    else:
        messages.error(request, "Please login to view this page.")
        return redirect('home')



# GENERAR_ACTAS.HTML VIEW
def generar_actas(request):
    if request.user.is_authenticated:
        if 'file_uploaded' in request.session:
            del request.session['file_uploaded']

        context = {}            
        # Send the record to the template
        return render( request, 'actas_lps/generar_actas.html', context )
    
    else:
        messages.error(request, "Please login to view this page.")
        return redirect('home')

# UPLOAD CSV FILE
@csrf_exempt
def csv_files(request):
    if request.method == 'POST':
        file = request.FILES['file']
        # Handle the file upload here. For example, you could save it to your model:
        my_model = CsvFilesModel(file=file)
        my_model.save()

        # Set the session variable to True
        request.session['file_uploaded'] = True


        return JsonResponse({'message': 'File uploaded successfully!'})

    else:
        return redirect('generar_actas')
    
# SHOW CSV FILES IN TABLE
def process_csv(request):
    # Check if the file was uploaded
    if 'file_uploaded' in request.session:
        # Get the most recently uploaded CSV file
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        processed_data = df.to_dict('records')
        
        return render(request, 'actas_lps/generar_actas.html', {'records_csv': processed_data})
    
    else:
        messages.error(request, "Sube un archivo para poder procesarlo.")
        return redirect('generar_actas')

#update data
@csrf_exempt
def update_data(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        column = request.POST.get('column')
        new_value = request.POST.get('new_value')

        # Update the data in your model
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        df.objects.filter(id=id).update(**{column: new_value})

        return JsonResponse({'status': 'success'})


# CLEAN CSV FILE
def cleaned_csv(request):
    # Check if the file was uploaded
    if 'file_uploaded' in request.session:
        # Get the most recently uploaded CSV file
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()
        df_cleaned = CleanActasModel(df)

        print(df.dtypes)
        #capitalice the columns
        df_cleaned.upper_case_column('EECC')
        df_cleaned.upper_case_column('Proyecto')

        #Erase the white spaces from the columns
        df_cleaned.no_spaces('EECC')
        df_cleaned.no_spaces('Proyecto')

        #Erase the commas from the columns
        df_cleaned.no_commas('total_OC')
        df_cleaned.no_commas('total_certificar')

        #convert to int
        df_cleaned.convert_to_int('OC')

        #clean the NaN values in column posicions    
        df_cleaned.clean_nan('posiciones')

        #round the values to 2 decimals
        df_cleaned.value_rounded_2(['total_OC','total_certificar'])

        df = df_cleaned.return_df()

        processed_data = df.to_dict('records')
        print(df.dtypes)

        # Save the cleaned data to the csv file
        df.to_csv(my_model.file.path, sep=';', encoding='latin-1', index=False)

        return render(request, 'actas_lps/generar_actas.html', {'records_csv': processed_data})
    
    else:
        messages.error(request, "Error al procesar el archivo.")
        return redirect('generar_actas')
    
    
#Save the data from the last csv to my bd_model
@csrf_exempt
def save_data(request):
    if 'file_uploaded' in request.session:
        # Get the most recently uploaded CSV file And save it to the bd_model
        my_model = CsvFilesModel.objects.latest('id')
        df = my_model.m_read_csv()

        df['termino_obra'] = pd.to_datetime(df['termino_obra'], format='%d/%m/%Y')
        df['servicio_obra'] = pd.to_datetime(df['servicio_obra'], format='%d/%m/%Y')

        # Iterate over the rows of the DataFrame
        for index, row in df.iterrows():
            ActasModel.objects.create(
                eecc=row['EECC'],
                project=row['Proyecto'],
                oc=row['OC'],
                ip_hijo=row['IP_Hijo'],
                total_OC=row['total_OC'],
                total_certificar=row['total_certificar'],
                termino_obra=row['termino_obra'],
                servicio_obra=row['servicio_obra'],
                posiciones=row['posiciones'],
            )

        #Initiate the printed actas
        df_to_xlsx = PrintedActasModel(df)

        df_to_xlsx.print_actas()

        df_to_xlsx.created_excel_files_zip()

        #Delete the csv file
        my_model.delete()

        # Create a FileResponse object.
        response = FileResponse(open('actas_lps/printed_xls/zip_files/excel_files.zip', 'rb'))

        # Set the Content-Disposition header to make the browser download the file
        response['Content-Disposition'] = 'attachment; filename="excel_files.zip"'

        return response

    else:
        messages.error(request, "Necesitas subir un archivo primero.")
        return redirect('generar_actas')
