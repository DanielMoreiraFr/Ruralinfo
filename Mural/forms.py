from django import forms
from .models import Aviso, Sugestao

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
    

class SugestaoForm(forms.ModelForm):
    """
    Formulário de envio de sugestão de pauta.
    Disponível para usuários COMUM e ADMIN — visitantes não têm acesso.
    """
 
    class Meta:
        model  = Sugestao
        fields = ['texto', 'categoria']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Descreva o acontecimento ou pauta que deseja sugerir...',
            }),
            'categoria': forms.Select(),
        }
        labels = {
            'texto':     'Descrição da Sugestão',
            'categoria': 'Categoria Sugerida',
        }
 
    def clean_texto(self):
        texto = self.cleaned_data.get('texto', '').strip()
        if len(texto) < 10:
            raise forms.ValidationError(
                'A sugestão deve ter pelo menos 10 caracteres.'
            )
        return texto
 