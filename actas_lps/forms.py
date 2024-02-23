from django import forms
from .models import actas_bd

class BdActasForm(forms.ModelForm):
    EECC = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"EECC", "class":"form-control"}), label="")
    Proyecto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Proyecto", "class":"form-control"}), label="")
    OC = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Orden de Compra", "class":"form-control"}), label="")
    IP_Hijo = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"IP_Hijo", "class":"form-control"}), label="")
    total_OC = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Total_OC", "class":"form-control"}), label="")
    total_certificar = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Total_Certificar", "class":"form-control"}), label="")
    termino_obra = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Termino Obra", "class":"form-control"}), label="")
    servicio_obra = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Servicio Obra", "class":"form-control"}), label="")
    posiciones = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Posiciones", "class":"form-control"}), label="")

    class Meta:
        model = actas_bd
        exclude = ("user",)