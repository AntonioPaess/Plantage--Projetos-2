from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from plant.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import calendar
from datetime import datetime, date, timedelta
from operator import itemgetter

@login_required
def HomeView(request):
    user_profile = Profile.objects.get(user=request.user)
    espacos = Espaco.objects.filter(user=user_profile)
    canteiros = Canteiro.objects.filter(user=user_profile)
    plantas = Planta.objects.filter(user=user_profile)

    # Chama a função AtividadeDiaria para obter as atividades
    atividades = AtividadeDiaria(user_profile)

    return render(request, 'home.html', {
        'espacos': espacos,
        'canteiros': canteiros,
        'plantas': plantas,
        'atividades': atividades,  # Passa as atividades para o template
    })

@method_decorator(login_required, name='dispatch')
class AddPlanta(View):
    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        plantas = Planta.objects.filter(user=user_profile)
        return render(request, 'forms/plantaForms.html', {'plantas': plantas})

    def post(self, request):
        name = request.POST.get("nome")
        nutri = request.POST.get("necessidade_de_nutrientes")
        poda = request.POST.get("ciclo_de_podagem")
        colhe = request.POST.get("ciclo_de_colheita")
        urlImagem = request.POST.get("imagem")
        plantas_inimigas_ids = request.POST.getlist("plantas_inimigas")

        try:
            poda = int(poda)
            colhe = int(colhe)
            if poda <= 0 or colhe <= 0:
                raise ValueError("Os valores precisam ser números positivos.")
        except (ValueError, TypeError):
            messages.warning(request, 'O manejo e dias de colheita precisam ser números positivos.')
            return redirect('add')

        user_profile = Profile.objects.get(user=request.user)

        planta = Planta(
            nome=name,
            necessidade_de_nutrientes=nutri,
            ciclo_de_podagem=poda,
            ciclo_de_colheita=colhe,
            imagem=urlImagem,
            user=user_profile
        )
        planta.save()

        if plantas_inimigas_ids:
            plantas_inimigas = Planta.objects.filter(id__in=plantas_inimigas_ids, user=user_profile)
            planta.plantas_inimigas.add(*plantas_inimigas)

        return redirect('home')

@method_decorator(login_required, name='dispatch')
class AddEspaco(View):
    def get(self, request):
        return render(request, 'forms/areaForms.html')

    def post(self, request):
        name = request.POST.get("nome")
        tipoSolo = request.POST.get("tipo_de_solo")
        quantCante = request.POST.get("quantMaxCanteiro")
        try:
            quantCante = int(quantCante)
            if quantCante <= 0:
                raise ValueError("Os valores precisam ser números positivos.")
        except (ValueError, TypeError):
            messages.warning(request, 'A quantidade de canteiros no seu espaço necessita ser um valor maior que zero.')
            return redirect('add-espaco')

        user_profile = Profile.objects.get(user=request.user)
        area = Espaco(
            nome=name,
            tipo_de_solo=tipoSolo,
            quantMaxCanteiro=quantCante,
            user=user_profile
        )
        area.save()
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class AddCanteiro(View):
    def get(self, request, espaco_id):
        espaco = get_object_or_404(Espaco, id=espaco_id)
        return render(request, 'forms/canteiroForms.html', {'espaco': espaco})

    def post(self, request, espaco_id):
        espaco = get_object_or_404(Espaco, id=espaco_id)
        nome = request.POST.get("nome")
        quantPlantMax = request.POST.get("quantMaxPlant")

        try:
            quantPlantMax = int(quantPlantMax)
            if quantPlantMax <= 0:
                raise ValueError("O número de plantas precisa ser positivo.")
        except (ValueError, TypeError):
            messages.warning(request, 'A quantidade máxima de plantas deve ser um valor numérico positivo.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        if any(char in nome for char in [".", "!", "@", "#", "$", "%", "&"]):
            messages.warning(request, 'Alguns caracteres especiais não são permitidos no nome do canteiro.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        limiteCant = espaco.quantMaxCanteiro
        quantCanteiros = espaco.canteiro_set.count()

        if quantCanteiros >= limiteCant:
            messages.warning(request, 'O número máximo de canteiros para este espaço já foi atingido.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        user_profile = Profile.objects.get(user=request.user)

        try:
            canteiro = Canteiro(nome=nome, user=user_profile, espaco=espaco, quantMaxPlant=quantPlantMax)
            canteiro.save()
            messages.success(request, 'Canteiro adicionado com sucesso.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Erro ao adicionar canteiro: {str(e)}')
            return render(request, 'forms/canteiroForms.html', {'espaco': espaco})

class ListAllView(View):
    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)
        plantas = Planta.objects.filter(user=user_profile)
        ctx = {'allPlantas': plantas}
        return render(request, 'visualizarTodas.html', ctx)

class PlantaDetail(View):
    def get(self, request, id):
        ctx = {'planta': Planta.objects.filter(id=id).first()}
        return render(request, 'visualizarPlanta.html', ctx)

def testeview(request):
    return render(request, 'teste.html')

@login_required
def adicionar_planta_canteiro(request):
    if request.method == 'POST':
        canteiro_id = request.POST.get('canteiro_id')
        planta_id = request.POST.get('planta_id')
        quantidade = int(request.POST.get('quantidade', 1))

        canteiro = get_object_or_404(Canteiro, id=canteiro_id)
        planta = get_object_or_404(Planta, id=planta_id)

        # Verifica o número total de plantas já no canteiro
        total_plantas_no_canteiro = sum(
            item.quantidade for item in CanteiroPlanta.objects.filter(canteiro=canteiro)
        )

        # Verifica se o novo total excede o limite
        if total_plantas_no_canteiro + quantidade > canteiro.quantMaxPlant:
            return JsonResponse({
                'success': False,
                'error': 'Número máximo de plantas para este canteiro atingido.'
            }, status=400)

        # Verificação de plantas inimigas já presentes no canteiro
        plantas_existentes = CanteiroPlanta.objects.filter(canteiro=canteiro).values_list('planta', flat=True)
        plantas_inimigas = planta.plantas_inimigas.values_list('id', flat=True)
        
        # Interseção para verificar se alguma planta inimiga já está no canteiro
        if set(plantas_existentes) & set(plantas_inimigas):
            return JsonResponse({
                'success': False,
                'error': 'Esta planta possui plantas inimigas no mesmo canteiro.'
            }, status=400)

        # Adiciona ou atualiza a quantidade de plantas no canteiro
        canteiro_planta, created = CanteiroPlanta.objects.get_or_create(canteiro=canteiro, planta=planta)
        if not created:
            canteiro_planta.quantidade += quantidade
        else:
            canteiro_planta.quantidade = quantidade

        canteiro_planta.save()

        return JsonResponse({
            'success': True,
            'planta_nome': planta.nome,
            'planta_imagem': planta.imagem,
            'quantidade': canteiro_planta.quantidade
        })

    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


@login_required
def calendario(request):
    user_profile = Profile.objects.get(user=request.user)
    plantas = Planta.objects.filter(user=user_profile)

    # Pegar o mês e ano da URL ou usar o atual
    yy = int(request.GET.get('ano', datetime.now().year))
    mm = int(request.GET.get('mes', datetime.now().month))

    # Calcular mês anterior e próximo
    if mm == 1:
        mes_anterior = 12
        ano_anterior = yy - 1
    else:
        mes_anterior = mm - 1
        ano_anterior = yy

    if mm == 12:
        proximo_mes = 1
        proximo_ano = yy + 1
    else:
        proximo_mes = mm + 1
        proximo_ano = yy

    calendar.setfirstweekday(calendar.SUNDAY)
    calendario_mes = calendar.monthcalendar(yy, mm)
    nome_mes = calendar.month_name[mm]

    # Obter as atividades
    atividades = AtividadeDiaria(user_profile)

    # Criar um dicionário para mapear dias às atividades
    atividades_por_dia = {}
    for atividade in atividades:
        data_atividade = atividade['data']
        if data_atividade.month == mm and data_atividade.year == yy:
            dia = data_atividade.day
            if dia not in atividades_por_dia:
                atividades_por_dia[dia] = []
            atividades_por_dia[dia].append(atividade)

    ctx = {
        'plantas': plantas,
        'calendario': calendario_mes,
        'yy': yy,
        'mm': mm,
        'nome_mes': nome_mes,
        'atividades_por_dia': atividades_por_dia,
        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'proximo_mes': proximo_mes,
        'proximo_ano': proximo_ano
    }

    return render(request, 'calendario.html', ctx)


def AtividadeDiaria(user_profile):
    canteiros_plantas = CanteiroPlanta.objects.filter(canteiro__user=user_profile)
    atividades = []
    hoje = date.today()

    for cp in canteiros_plantas:
        if not cp.data_plantio:
            continue
            
        data_plantio = cp.data_plantio
        ciclo_podagem = cp.planta.ciclo_de_podagem
        ciclo_colheita = cp.planta.ciclo_de_colheita
        planta_imagem = cp.planta.imagem or ''

        # Calcula próxima podagem
        if ciclo_podagem and ciclo_podagem > 0:
            dias_desde_plantio = max(0, (hoje - data_plantio).days)
            proxima_podagem_em_dias = ciclo_podagem - (dias_desde_plantio % ciclo_podagem)
            proxima_data_podagem = hoje + timedelta(days=proxima_podagem_em_dias)
            
            atividades.append({
                'planta': cp.planta.nome,
                'planta_imagem': planta_imagem,
                'atividade': 'Podar',
                'data': proxima_data_podagem,  # Mantém o objeto date para ordenação
                'data_formatada': proxima_data_podagem.strftime('%d/%m/%Y')  # Data formatada para exibição
            })

        # Calcula próxima colheita
        if ciclo_colheita and ciclo_colheita > 0:
            dias_desde_plantio = max(0, (hoje - data_plantio).days)
            proxima_colheita_em_dias = ciclo_colheita - (dias_desde_plantio % ciclo_colheita)
            proxima_data_colheita = hoje + timedelta(days=proxima_colheita_em_dias)
            
            atividades.append({
                'planta': cp.planta.nome,
                'planta_imagem': planta_imagem,
                'atividade': 'Colher',
                'data': proxima_data_colheita,  # Mantém o objeto date para ordenação
                'data_formatada': proxima_data_colheita.strftime('%d/%m/%Y')  # Data formatada para exibição
            })

    # Ordena as atividades por data
    return sorted(atividades, key=lambda x: x['data'])