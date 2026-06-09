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
        # Define os campos do modelo que serão expostos no formulário web
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
        """
        Garante a integridade do nome do local removendo espaços inúteis
        e exigindo uma extensão mínima de 3 caracteres textuais.
        """
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise forms.ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return nome


# =============================================================================
# FORMSET DE IMAGENS DA GALERIA
# =============================================================================

# inlineformset_factory cria uma estrutura para gerenciar múltiplos sub-formulários na mesma tela
# Cria uma relação direta N:1 controlada pelo modelo pai (LocalRural) com o modelo filho (ImagemLocal)
ImagemLocalFormSet = inlineformset_factory( 
    LocalRural,
    ImagemLocal,
    fields  = ['imagem', 'legenda', 'ordem'],
    # Deixa sempre 3 espaços vazios prontos para upload simultâneo de novas mídias.
    extra   = 3,
    # Renderiza um checkbox invisível/visível que permite marcar imagens salvas para exclusão
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
    """
    Formulário para o sistema de notas por estrelas.
    O campo utiliza HiddenInput pois a interação visual (clique nas estrelas)
    é capturada via JavaScript e injetada no value deste input oculto.
    """
    class Meta:
        model  = Avaliacao
        fields = ['nota']
        widgets = {
            'nota': forms.HiddenInput(attrs={'id': 'id_nota_estrela'}),
        }

    def clean_nota(self):
        """
        Validação matemática rigorosa da nota enviada:
        1. Impede submissão nula.
        2. Garante o intervalo de notas aceito pelo modelo (entre 0.5 e 5.0).
        3. Verifica se a nota é fracionada em passos de 0.5 (evita burlar via console do navegador).
        """
        nota = self.cleaned_data.get('nota')
        if nota is None:
            raise forms.ValidationError('Selecione uma nota.')
        if not (0.5 <= nota <= 5.0):
            raise forms.ValidationError('Nota deve ser entre 0.5 e 5.0.')
        
        # Multiplica por 2 e valida se o resultado é um número inteiro (ex: 4.5 * 2 = 9.0 -> válido)
        if (nota * 2) != int(nota * 2):
            raise forms.ValidationError('Nota deve ser múltiplo de 0.5.')
        return nota


# =============================================================================
# COMENTÁRIO / RESPOSTA
# =============================================================================

class ComentarioForm(forms.ModelForm):
    """
    Gerencia tanto comentários de nível superior (raízes) quanto respostas diretas 
    aninhadas a outros comentários, baseando-se no mesmo campo de conteúdo de texto.
    """
    class Meta:
        model  = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Escreva seu comentário...',
                'maxlength': 1000, # Proteção de tamanho direto na camada HTML do navegador
            }),
        }
        labels = {'conteudo': ''}

    def clean_conteudo(self):
        """
        Sanitiza o corpo do comentário contra envios nulos, strings compostas 
        apenas por espaços em branco ou de comprimento menor que 3 caracteres.
        """
        conteudo = self.cleaned_data.get('conteudo', '').strip()
        if not conteudo:
            raise forms.ValidationError('O comentário não pode estar em branco.')
        if len(conteudo) < 3:
            raise forms.ValidationError('Mínimo de 3 caracteres.')
        return conteudo