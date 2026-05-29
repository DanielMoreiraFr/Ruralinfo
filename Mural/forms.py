from django import forms
from .models import Aviso

class AvisoForm(forms.ModelForm):
    """
    Formulário de criação e edição de avisos atualizado com o campo título.
    """
    class Meta:
        model  = Aviso
        # Incluído o 'titulo' como primeiro campo do formulário
        fields = ['titulo', 'categoria', 'imagem', 'alt_texto', 'conteudo', 'publicado']
        widgets = {
            'titulo':    forms.TextInput(attrs={'placeholder': 'Ex: Inscrições abertas para monitoria'}),
            'categoria': forms.Select(),
            'imagem':    forms.ClearableFileInput(),
            'alt_texto': forms.TextInput(attrs={'placeholder': 'Descrição da imagem para acessibilidade'}),
            'conteudo':  forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escreva o corpo do aviso com detalhes...'}),
            'publicado': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned   = super().clean()
        imagem    = cleaned.get('imagem')
        alt_texto = cleaned.get('alt_texto')

        if alt_texto:
            alt_texto = alt_texto.strip()
            cleaned['alt_texto'] = alt_texto
        else:
            alt_texto = ''

        if imagem and not alt_texto:
            self.add_error(
                'alt_texto',
                'Descreva a imagem para garantir acessibilidade.'
            )
            
        return cleaned