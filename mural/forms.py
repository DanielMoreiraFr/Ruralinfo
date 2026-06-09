from django import forms
from .models import Aviso, Sugestao

class AvisoForm(forms.ModelForm):
    """
    Formulário de criação e edição de avisos atualizado com o campo título.
    """
    class Meta:
        model  = Aviso
        # Define os tipos de postagens disponíveis
        fields = ['titulo', 'categoria', 'imagem', 'alt_texto', 'conteudo', 'publicado']
        
        # Injeta atributos HTML (como placeholders e classes CSS) diretamente nos campos
        widgets = {
            'titulo':    forms.TextInput(attrs={'placeholder': 'Ex: Inscrições abertas para monitoria'}),
            'categoria': forms.Select(),
            'imagem':    forms.ClearableFileInput(),
            'alt_texto': forms.TextInput(attrs={'placeholder': 'Descrição da imagem para acessibilidade'}),
            'conteudo':  forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escreva o corpo do aviso com detalhes...'}),
            'publicado': forms.CheckboxInput(),
        }

    def clean(self):
        """
        Validação cruzada (de mais de um campo): Garante que, se houver uma imagem, 
        o texto alternativo de acessibilidade se torne obrigatório.
        """
        cleaned   = super().clean()
        imagem    = cleaned.get('imagem')
        alt_texto = cleaned.get('alt_texto')

        # Remove espaços em branco extras do início e fim do texto alternativo
        if alt_texto:
            alt_texto = alt_texto.strip()
            cleaned['alt_texto'] = alt_texto
        else:
            alt_texto = ''

        # Regra de acessibilidade: impede o salvamento se houver imagem sem texto alternativo
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
        # Sobrescreve as propriedades 'verbose_name' do Model para exibição nos labels das tags HTML
        labels = {
            'texto':     'Descrição da Sugestão',
            'categoria': 'Categoria Sugerida',
        }
 
    def clean_texto(self):
        """
        Validação isolada do campo 'texto': Limpa os espaços e impede 
        sugestões vazias ou curtas demais (menos de 10 caracteres).
        """
        texto = self.cleaned_data.get('texto', '').strip()
        if len(texto) < 10:
            raise forms.ValidationError(
                'A sugestão deve ter pelo menos 10 caracteres.'
            )
        return texto