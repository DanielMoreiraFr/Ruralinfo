from django import forms
from .models import Aviso


class AvisoForm(forms.ModelForm):
    """
    Formulário de criação e edição de avisos.
    O campo `autor` é excluído — atribuído automaticamente na view
    com request.user (equivale ao id da sessão do legado).
    """

    # campo oculto pra ser preenchudo na view
    class Meta:
        model  = Aviso
        fields = ['conteudo', 'categoria', 'imagem', 'alt_texto', 'publicado']
        widgets = {
            'conteudo':  forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escreva o aviso...'}),
            'categoria': forms.Select(),
            'imagem':    forms.ClearableFileInput(),
            'alt_texto': forms.TextInput(attrs={'placeholder': 'Descrição da imagem para acessibilidade'}),
        }

    # validações
    def clean(self):
        cleaned   = super().clean()
        imagem    = cleaned.get('imagem')
        alt_texto = cleaned.get('alt_texto')

        # Se alt_texto não for None, aplica o strip e limpa o texto
        if alt_texto:
            alt_texto = alt_texto.strip()
            cleaned['alt_texto'] = alt_texto
        else:
            alt_texto = ''  # Garante que vire string vazia caso seja None

        # Se há imagem, o alt_texto se torna obrigatório (acessibilidade)
        if imagem and not alt_texto:
            self.add_error(
                'alt_texto',
                'Descreva a imagem para garantir acessibilidade.'
            )
            
        return cleaned