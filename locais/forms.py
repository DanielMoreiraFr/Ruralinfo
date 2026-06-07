from django import forms
from django.forms import inlineformset_factory

from .models import Avaliacao, Comentario, LocalRural, ImagemLocal


# =============================================================================
# FORMULÁRIO DO LOCAL
# =============================================================================

class LocalRuralForm(forms.ModelForm):
    """Formulário de criação e edição de um local da Rural."""

    class Meta:
        model  = LocalRural
        fields = ['nome', 'descricao', 'imagem_principal']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex: Biblioteca Central, Restaurante Universitário...',
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva o local, sua função e características...',
            }),
            'imagem_principal': forms.ClearableFileInput(),
        }
        labels = {
            'imagem_principal': 'Imagem de Capa',
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise forms.ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return nome


# =============================================================================
# FORMSET DE IMAGENS DA GALERIA
# =============================================================================

# inlineformset_factory cria um conjunto de formulários vinculados ao LocalRural
# extra=3 → exibe 3 linhas vazias prontas para upload
# can_delete=True → permite marcar imagens para remoção
ImagemLocalFormSet = inlineformset_factory(
    LocalRural,
    ImagemLocal,
    fields  = ['imagem', 'legenda', 'ordem'],
    extra   = 3,
    can_delete = True,
    widgets = {
        'imagem':  forms.ClearableFileInput(),
        'legenda': forms.TextInput(attrs={'placeholder': 'Legenda opcional'}),
        'ordem':   forms.NumberInput(attrs={'min': 0, 'style': 'width:70px'}),
    },
)


# =============================================================================
# AVALIAÇÃO
# =============================================================================

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model  = Avaliacao
        fields = ['nota']
        widgets = {
            'nota': forms.HiddenInput(attrs={'id': 'id_nota_estrela'}),
        }

    def clean_nota(self):
        nota = self.cleaned_data.get('nota')
        if nota is None:
            raise forms.ValidationError('Selecione uma nota.')
        if not (0.5 <= nota <= 5.0):
            raise forms.ValidationError('Nota deve ser entre 0.5 e 5.0.')
        if (nota * 2) != int(nota * 2):
            raise forms.ValidationError('Nota deve ser múltiplo de 0.5.')
        return nota


# =============================================================================
# COMENTÁRIO / RESPOSTA
# =============================================================================

class ComentarioForm(forms.ModelForm):
    class Meta:
        model  = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Escreva seu comentário...',
                'maxlength': 1000,
            }),
        }
        labels = {'conteudo': ''}

    def clean_conteudo(self):
        conteudo = self.cleaned_data.get('conteudo', '').strip()
        if not conteudo:
            raise forms.ValidationError('O comentário não pode estar em branco.')
        if len(conteudo) < 3:
            raise forms.ValidationError('Mínimo de 3 caracteres.')
        return conteudo