from django import forms
from .models import Aviso


class AvisoForm(forms.ModelForm):
    """
    Formulário para criação e edição de avisos.
    Usado exclusivamente por usuários ADMIN.

    O campo `autor` é excluído do formulário pois é atribuído automaticamente
    na view com o usuário autenticado (request.user).
    """

    class Meta:
        model = Aviso
        fields = ['titulo', 'conteudo', 'categoria', 'imagem', 'alt_texto']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do aviso',
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descreva o aviso em detalhes...',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'alt_texto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Foto da entrada do auditório principal',
            }),
        }
        labels = {
            'alt_texto': 'Descrição da imagem (acessibilidade)',
        }

    def clean(self):
        cleaned_data = super().clean()
        imagem = cleaned_data.get('imagem')
        alt_texto = cleaned_data.get('alt_texto', '').strip()

        # Se uma imagem foi fornecida, o alt_texto se torna obrigatório
        if imagem and not alt_texto:
            self.add_error(
                'alt_texto',
                'Descreva a imagem para garantir acessibilidade.'
            )

        return cleaned_data