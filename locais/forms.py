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
    
    Utiliza um CharField com widget oculto para receber o valor do JavaScript
    sem restrições rígidas de ChoiceField ou interferências automáticas de 
    localização (como a conversão de ponto para vírgula no pt-br) do FloatField.
    """
    nota = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'id_nota_estrela'}))

    class Meta:
        model = Avaliacao
        fields = ['nota']

    def clean_nota(self):
        """
        Validação e normalização rigorosa da nota enviada pelo frontend.
        
        1. Converte o valor recebido para string e padroniza o separador decimal.
        2. Garante que o valor seja um número flutuante válido.
        3. Restringe a nota ao intervalo permitido (entre 0.5 e 5.0).
        4. Verifica se o valor respeita o incremento de meia estrela (múltiplo de 0.5).
        """
        try:
            # Recupera o valor e normaliza substituindo vírgulas por pontos antes de converter para float
            nota_raw = self.cleaned_data.get('nota')
            nota = float(str(nota_raw).replace(',', '.'))
            
            # Valida as regras de negócio: intervalo permitido e se o passo é múltiplo de 0.5
            if 0.5 <= nota <= 5.0 and (nota * 2) == int(nota * 2):
                return nota
                
        except (ValueError, TypeError, AttributeError):
            # Captura falhas de conversão de tipo ou manipulação de string nula
            pass
            
        # retorna um erro de validação
        raise forms.ValidationError('Nota inválida.')
    

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