from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from plant.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import calendar
from datetime import datetime



@login_required
def HomeView(request):
        user_profile = Profile.objects.get(user=request.user)  # Obtém o perfil do usuário logado
        espacos = Espaco.objects.filter(user=user_profile)
        canteiros = Canteiro.objects.filter(user=user_profile)
        plantas = Planta.objects.filter(user=user_profile)

        # Renderiza o template passando os canteiros com suas plantas associadas
        return render(request, 'home.html', {
            'espacos': espacos,
            'canteiros': canteiros,  # Os canteiros já terão suas plantas associadas devido ao prefetch_related
            'plantas': plantas
        })


# views.py
@method_decorator(login_required, name='dispatch')
class AddPlanta(View):
    def get(self, request):
        # Inclui todas as plantas para seleção de plantas inimigas
        plantas = Planta.objects.all()
        return render(request, 'forms/plantaForms.html', {'plantas': plantas})

    def post(self, request):
        name = request.POST.get("nome")
        nutri = request.POST.get("necessidade_de_nutrientes")
        poda = request.POST.get("ciclo_de_podagem")
        colhe = request.POST.get("ciclo_de_colheita")
        urlImagem = request.POST.get("imagem")
        plantas_inimigas_ids = request.POST.getlist("plantas_inimigas")

        # Converte os valores para inteiros com verificação de erro
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

        # Adiciona as plantas inimigas ao relacionamento
        if plantas_inimigas_ids:
            planta.plantas_inimigas.add(*plantas_inimigas_ids)

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
            quantCante = int(quantCante)  # Converte para float ou use int() se preferir
            
        
            if quantCante <= 0:
                raise ValueError("Os valores precisam ser números positivos.")

        except (ValueError, TypeError):
            messages.warning(request, 'A quantidade de canteiros no seu espaço necessita ser um valor maior que zero.')
            return redirect('add-espaco')

        user_profile = Profile.objects.get(user=request.user)  # Obtém o perfil do usuário logado

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
        espaco = get_object_or_404(Espaco, id=espaco_id)  # Carrega o espaço correspondente
        return render(request, 'forms/canteiroForms.html', {'espaco': espaco})

    def post(self, request, espaco_id):
        espaco = get_object_or_404(Espaco, id=espaco_id)  # Obtém o espaço

        nome = request.POST.get("nome")
        quantPlantMax = request.POST.get("quantMaxPlant")

        # Validação de `quantPlantMax`
        try:
            quantPlantMax = int(quantPlantMax)  # Converte para int
            if quantPlantMax <= 0:
                raise ValueError("O número de plantas precisa ser positivo.")
        except (ValueError, TypeError):
            messages.warning(request, 'A quantidade máxima de plantas deve ser um valor numérico positivo.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        # Validação de caracteres especiais no nome
        if any(char in nome for char in [".", "!", "@", "#", "$", "%", "&"]):
            messages.warning(request, 'Alguns caracteres especiais não são permitidos no nome do canteiro.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        # Verificação do limite de canteiros no espaço
        limiteCant = espaco.quantMaxCanteiro  # Limite de canteiros no espaço
        quantCanteiros = espaco.canteiro_set.count()  # Total de canteiros no espaço

        if quantCanteiros >= limiteCant:
            messages.warning(request, 'O número máximo de canteiros para este espaço já foi atingido.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        user_profile = Profile.objects.get(user=request.user)  # Obtém o perfil do usuário logado

        # Criação do canteiro com `quantPlantMax`
        try:
            canteiro = Canteiro(nome=nome, user=user_profile, espaco=espaco, quantMaxPlant=quantPlantMax)
            canteiro.save()
            messages.success(request, 'Canteiro adicionado com sucesso.')
            return redirect('home')  # Redireciona para uma URL de sucesso
        except Exception as e:
            messages.error(request, f'Erro ao adicionar canteiro: {str(e)}')
            return render(request, 'forms/canteiroForms.html', {'espaco': espaco})


class ListAllView(View):
    def get(self, request):
        user_profile = Profile.objects.get(user=request.user)  # Obtém o perfil do usuário logado
        plantas = Planta.objects.filter(user=user_profile)

        ctx = {
            'allPlantas': plantas, 
        }

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




def calendario(request):
    user_profile = Profile.objects.get(user=request.user)  # Obtém o perfil do usuário logado
    plantas = Planta.objects.filter(user=user_profile)

    now = datetime.now()
    yy = now.year
    mm = now.month
    calendario_mes = calendar.monthcalendar(yy, mm)
    nome_mes = calendar.month_name[mm]

    ctx = {
        'plantas': plantas,
        'meses': calendar.month_name,
        'calendario': calendario_mes,
        'yy': yy,
        'mm': mm,
        'nome_mes': nome_mes,
    }

    return render(request, 'calendario.html', ctx)
    

