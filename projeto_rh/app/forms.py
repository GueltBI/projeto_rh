# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

#class CandidatoForm(forms.Form):
#    nome = forms.CharField(max_length=100, required=False)
#    idade = forms.IntegerField(required=False)
#    formacao = forms.CharField(widget=forms.Textarea, required=False)
#    hist_prof = forms.CharField(widget=forms.Textarea, required=False)
#    foco = forms.CharField(max_length=100, required=False)
#    pret_sal = forms.CharField(max_length=100, required=False)
#    cinco_anos = forms.CharField(widget=forms.Textarea, required=False)
#    pq_guelt = forms.CharField(widget=forms.Textarea, required=False)
#    certificado = forms.CharField(widget=forms.Textarea, required=False)
#    observacao = forms.CharField(widget=forms.Textarea, required=False)
#    status = forms.CharField(max_length=50, required=False)
#    data = forms.DateTimeField(required=False)
#
#   def __init__(self, *args, **kwargs):
#       super(CandidatoForm, self).__init__(*args, **kwargs)
#       self.helper = FormHelper()
#       self.helper.form_method = 'POST'
#       self.helper.layout = Layout(
#           Row(
#                Column('nome', css_class='form-group col-md-6 mb-0'),
#                Column('idade', css_class='form-group col-md-6 mb-0'),
#                css_class='form-row'
#            ),
#            'formacao',
#            'hist_prof',
#            Row(
#                Column('foco', css_class='form-group col-md-6 mb-0'),
#                Column('pret_sal', css_class='form-group col-md-6 mb-0'),
#                css_class='form-row'
#            ),
#            'cinco_anos',
#            'pq_guelt',
#            'certificado',
#            'observacao',
#            'status',
#            Submit('submit', 'Salvar')
#        )


########################### formulario de editar funcionário ################ SALVAR AGENTES #########



class CandidatoForm(forms.Form):

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('suspenso', 'Suspenso'),
    ]

    SN_CHOICES = [
        ('sim', 'Sim'),
        ('nao', 'Não'),
    ]


    nome = forms.CharField(max_length=100,required=False)
    idade = forms.IntegerField(required=False)
    formacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    hist_prof = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    foco = forms.CharField(max_length=100,required=False)
    pret_sal = forms.CharField(max_length=100,required=False)
    cinco_anos = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    pq_guelt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    certificado = forms.CharField(max_length=100,required=False)
    observacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    status = forms.CharField(max_length=50, required=False)
    
    #NOVOS ADICIONADOS
    linkedin = forms.CharField(max_length=100,required=False)
    meio = forms.CharField(max_length=100,required=False)
    uff = forms.CharField(max_length=4,required=False)
    vaga_aplicada = forms.CharField(max_length=100,required=False)
    Banco_de_Talentos = forms.ChoiceField(choices=SN_CHOICES,required=False)
    Perfil_Comercial = forms.ChoiceField(choices=SN_CHOICES,required=False) #BOX
    DISC = forms.CharField(max_length=200,required=False)
    Indicação = forms.CharField(max_length=100,required=False)
    Ultima_Remuneração = forms.CharField(max_length=100,required=False)
    Comportamento_Entrevista = forms.CharField(max_length=100,required=False)
    OBS1 = forms.CharField(max_length=100,required=False)
    OBS2 = forms.CharField(max_length=100,required=False)
    Area_de_interesse = forms.CharField(max_length=100,required=False)
    pontos_forteis = forms.CharField(max_length=150,required=False)
    pontos_fracos = forms.CharField(max_length=150,required=False)
    testes = forms.CharField(max_length=100,required=False)



    def __init__(self, *args, **kwargs):
        super(CandidatoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-4 mb-0'),
                Column('idade', css_class='form-group col-md-2 mb-0'),
                Column('linkedin', css_class='form-group col-md-2 mb-0'),
                Column('meio', css_class='form-group col-md-2 mb-0'),
                Column('uff', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'formacao',
            'hist_prof',
            Row(
                Column('foco', css_class='form-group col-md-2 mb-0'),
                Column('pret_sal', css_class='form-group col-md-2 mb-0'),
                Column('certificado', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
            'cinco_anos',
            'observacao',        
            Row(
                Column('status', css_class='form-group col-md-2 mb-0'),
                Column('Perfil_Comercial', css_class='form-group col-md-2 mb-0'),
                Column('Comportamento_Entrevista', css_class='form-group col-md-4 mb-0'),
                Column('Banco_de_Talentos', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('pontos_forteis', css_class='form-group col-md-2 mb-0'),
                Column('pontos_fracos', css_class='form-group col-md-2 mb-0'),
                Column('DISC', css_class='form-group col-md-4 mb-0'),
            ),
            Submit('submit', 'Salvar')
                   
         )


########################### formulario de funcionario ################ INSERIR ANGENTES #########



class FuncionarioForm(forms.Form):

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('suspenso', 'Suspenso'),
    ]

    SN_CHOICES = [
        ('sim', 'Sim'),
        ('nao', 'Não'),
    ]


    nome = forms.CharField(max_length=100,required=False)
    idade = forms.IntegerField(required=False)
    formacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    hist_prof = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    foco = forms.CharField(max_length=100,required=False)
    pret_sal = forms.CharField(max_length=100,required=False)
    cinco_anos = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    pq_guelt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    certificado = forms.CharField(max_length=100,required=False)
    observacao = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}),required=False)
    status = forms.CharField(max_length=50, required=False)
    
    #NOVOS ADICIONADOS
    linkedin = forms.CharField(max_length=100,required=False)
    meio = forms.CharField(max_length=100,required=False)
    uff = forms.CharField(max_length=4,required=False)
    vaga_aplicada = forms.CharField(max_length=100,required=False)
    Banco_de_Talentos = forms.ChoiceField(choices=SN_CHOICES,required=False)
    Perfil_Comercial = forms.ChoiceField(choices=SN_CHOICES,required=False) #BOX
    DISC = forms.CharField(max_length=200,required=False)
    Indicação = forms.CharField(max_length=100,required=False)
    Ultima_Remuneração = forms.CharField(max_length=100,required=False)
    Comportamento_Entrevista = forms.CharField(max_length=100,required=False)
    OBS1 = forms.CharField(max_length=100,required=False)
    OBS2 = forms.CharField(max_length=100,required=False)
    Area_de_interesse = forms.CharField(max_length=100,required=False)
    pontos_forteis = forms.CharField(max_length=150,required=False)
    pontos_fracos = forms.CharField(max_length=150,required=False)
    testes = forms.CharField(max_length=100,required=False)




    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-4 mb-0'),
                Column('idade', css_class='form-group col-md-2 mb-0'),
                Column('linkedin', css_class='form-group col-md-2 mb-0'),
                Column('meio', css_class='form-group col-md-2 mb-0'),
                Column('uff', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'formacao',
            'hist_prof',
            Row(
                Column('foco', css_class='form-group col-md-2 mb-0'),
                Column('pret_sal', css_class='form-group col-md-2 mb-0'),
                Column('certificado', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
            'cinco_anos',
            'observacao',        
            Row(
                Column('status', css_class='form-group col-md-2 mb-0'),
                Column('Perfil_Comercial', css_class='form-group col-md-2 mb-0'),
                Column('Comportamento_Entrevista', css_class='form-group col-md-4 mb-0'),
                Column('Banco_de_Talentos', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('pontos_forteis', css_class='form-group col-md-2 mb-0'),
                Column('pontos_fracos', css_class='form-group col-md-2 mb-0'),
                Column('DISC', css_class='form-group col-md-4 mb-0'),
            ),
            Submit('submit', 'Salvar')
                   
         )
