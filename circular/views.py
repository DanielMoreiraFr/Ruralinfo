from django.shortcuts import render


def horarios(request):
    """ Renderiza a página estática informativa com os horários de ônibus da UFRPE. """
    return render(request, 'mural/horarios.html')