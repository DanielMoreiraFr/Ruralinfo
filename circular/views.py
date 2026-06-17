from django.shortcuts import render
from datetime import datetime
import pytz
from django.http import JsonResponse

HORARIOS_CIRCULAR = [
    {"ponto": "Zootecnia", "horarios": ["07:00", "08:05", "09:10", "10:15", "11:00", "11:45", "12:30", "13:15", "14:00", "15:05", "16:10", "17:15", "18:20", "19:25", "—", "—"]},
    {"ponto": "Cegoe", "horarios": ["07:03", "08:08", "09:13", "10:18", "11:03", "11:48", "12:33", "13:18", "14:03", "15:08", "16:13", "17:18", "18:23", "19:28", "—", "—"]},
    {"ponto": "Guarita Piscina", "horarios": ["07:05", "08:10", "09:15", "10:20", "11:05", "11:50", "12:35", "13:20", "14:05", "15:10", "16:15", "17:20", "18:25", "19:30", "20:25", "21:20"]},
    {"ponto": "Reitoria", "horarios": ["07:06", "08:11", "09:16", "10:21", "11:06", "11:51", "12:36", "13:21", "14:06", "15:11", "16:16", "17:21", "18:26", "19:31", "20:27", "21:22"]},
    {"ponto": "Biblioteca", "horarios": ["07:08", "08:13", "09:18", "10:23", "11:08", "11:53", "12:38", "13:23", "14:08", "15:13", "16:18", "17:23", "18:28", "19:33", "20:28", "21:23"]},
    {"ponto": "Veterinária", "horarios": ["07:10", "08:15", "09:20", "10:25", "11:10", "11:55", "12:40", "13:25", "14:10", "15:15", "16:20", "17:25", "18:30", "19:35", "20:32", "21:27"]},
    {"ponto": "Setorial", "horarios": ["07:11", "08:16", "09:21", "10:26", "11:11", "11:56", "12:41", "13:26", "14:11", "15:16", "16:21", "17:26", "18:31", "19:36", "20:33", "21:28"]},
    {"ponto": "Estufa", "horarios": ["07:12", "08:17", "09:22", "10:27", "11:12", "11:57", "12:42", "13:27", "14:12", "15:17", "16:22", "17:27", "18:32", "19:37", "20:34", "21:29"]},
    {"ponto": "Pesca", "horarios": ["07:14", "08:19", "09:24", "10:29", "11:14", "11:59", "12:44", "13:29", "14:14", "15:19", "16:24", "17:29", "18:34", "19:39", "20:36", "21:32"]},
    {"ponto": "Ceagri", "horarios": ["07:15", "08:20", "09:25", "10:30", "11:15", "12:00", "12:45", "13:30", "14:15", "15:20", "16:25", "17:30", "18:35", "19:40", "20:36", "21:33"]},
    {"ponto": "Ceagri Portão", "horarios": ["07:17", "08:22", "09:27", "10:32", "11:17", "12:02", "12:47", "13:32", "14:17", "15:22", "16:27", "17:32", "18:37", "19:42", "20:39", "21:35"]},
    {"ponto": "Estufa", "horarios": ["07:19", "08:24", "09:29", "10:34", "11:19", "12:04", "12:49", "13:34", "14:19", "15:24", "16:29", "17:34", "18:39", "19:44", "20:41", "21:37"]},
    {"ponto": "Zootecnia", "horarios": ["07:21", "08:26", "09:31", "10:36", "11:21", "12:06", "12:51", "13:36", "14:21", "15:26", "16:31", "17:36", "18:41", "—", "—", "—"]},
    {"ponto": "Cegoe", "horarios": ["07:24", "08:29", "09:34", "10:39", "11:24", "12:09", "12:54", "13:39", "14:24", "15:29", "16:34", "17:39", "18:44", "—", "—", "—"]},
    {"ponto": "Guarita Piscina", "horarios": ["07:26", "08:31", "09:36", "10:41", "11:26", "12:11", "12:56", "13:41", "14:26", "15:31", "16:36", "17:41", "18:46", "19:48", "20:45", "21:41"]},
    {"ponto": "Reitoria", "horarios": ["07:27", "08:32", "09:37", "10:42", "11:27", "12:12", "12:57", "13:42", "14:27", "15:32", "16:37", "17:42", "18:47", "19:49", "20:46", "21:42"]},
    {"ponto": "Biblioteca", "horarios": ["07:29", "08:34", "09:39", "10:44", "11:29", "12:14", "12:59", "13:44", "14:29", "15:34", "16:39", "17:44", "18:49", "19:51", "20:48", "21:44"]},
    {"ponto": "Veterinária", "horarios": ["07:31", "08:36", "09:41", "10:46", "11:31", "12:16", "13:01", "13:46", "14:31", "15:36", "16:41", "17:46", "18:51", "19:53", "20:50", "21:46"]},
    {"ponto": "Setorial", "horarios": ["07:32", "08:37", "09:42", "10:47", "11:32", "12:17", "13:02", "13:47", "14:32", "15:37", "16:42", "17:47", "18:52", "19:54", "20:51", "21:47"]},
    {"ponto": "Estufa", "horarios": ["07:33", "08:38", "09:43", "10:48", "11:33", "12:18", "13:03", "13:48", "14:33", "15:38", "16:43", "17:48", "18:53", "19:55", "20:52", "21:48"]},
    {"ponto": "Zootecnia", "horarios": ["07:35", "08:40", "09:45", "10:50", "11:35", "12:20", "13:05", "13:50", "14:35", "15:40", "16:45", "17:50", "18:55", "—", "—", "—"]}
]


def horarios(request):
    """ Renderiza a página estática informativa com os horários de ônibus da UFRPE. """
    return render(request, 'mural/horarios.html')


# transforma os horarios de string para minutos em int para facilitar a localização e comparação
def str_para_minutos(hora_str):
    if not hora_str or hora_str == "—":
        return None
    h, m = map(int, hora_str.split(':'))
    return h * 60 + m


def api_circular_ao_vivo(request):
    menor_min_futuro = float('inf') # inicializa variável flot com valor infinito
    proximo_ponto = None
    horario_ponto = None
    # coordenadas do ponto e horário escolhido
    linha_index_escolha = None
    coluna_index_escolha = None

    time_zone = pytz.timezone('America/Recife')
    agora = datetime.now(time_zone)
    min_agora = agora.hour * 60 + agora.minute # monta o horário atual em minutos ( do mesmo jeito que o str_para_minutos faz )

    for l_index, linha in enumerate(HORARIOS_CIRCULAR):
        nome_ponto = linha['ponto']
        for c_index, hora_str in enumerate(linha['horarios']):
            min_horario = str_para_minutos(hora_str)

            if min_horario is None:
                continue
            if min_agora <= min_horario < menor_min_futuro:
                menor_min_futuro = min_horario
                proximo_ponto = nome_ponto
                horario_ponto = hora_str
                linha_index_escolha = l_index
                coluna_index_escolha = c_index

    if proximo_ponto is not None:
        min_restantes = menor_min_futuro - min_agora
        context = {
            'operando': True,
            'ponto': proximo_ponto,
            'horario': horario_ponto,
            'minutos_restantes': min_restantes,
            'linha_index': linha_index_escolha,
            'coluna_index': coluna_index_escolha,
            'relogio_atual': agora.strftime("%H:%M"),
        }
    else:
        context = {
            'operando': False,
            'ponto': proximo_ponto,
            'horario': horario_ponto,
            'minutos_restantes': min_restantes,
            'linha_index': linha_index_escolha,
            'coluna_index': coluna_index_escolha,
            'relogio_atual': agora.strftime("%H:%M"),
        }

    return JsonResponse(context)