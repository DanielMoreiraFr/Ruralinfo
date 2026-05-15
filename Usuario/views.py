from django.shortcuts import render


def usuario_cadastrar(request):
    return render(request, 'usuario/usuario_cadastrar.html')    