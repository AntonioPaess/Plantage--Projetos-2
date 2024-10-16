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


@login_required
def HomeView(request):
        espacos = Espaco.objects.all()
        canteiros = Canteiro.objects.all() 
        plantas = Planta.objects.all()

        # Renderiza o template passando os canteiros com suas plantas associadas
        return render(request, 'home.html', {
            'espacos': espacos,
            'canteiros': canteiros,  # Os canteiros já terão suas plantas associadas devido ao prefetch_related
            'plantas': plantas
        })


@method_decorator(login_required, name='dispatch')
class AddPlanta(View):

    def get(self, request):
        return render(request, 'forms/plantaForms.html')

    def post(self, request):
        name = request.POST.get("nome")
        nutri = request.POST.get("necessidade_de_nutrientes")
        poda=request.POST.get("ciclo_de_podagem")
        colhe= request.POST.get("ciclo_de_colheita")
        urlImagem = request.POST.get("imagem")

        try:
            poda = int(poda)  # Converte para float ou use int() se preferir
            colhe = int(colhe)
        
            if poda <= 0 and colhe <= 0:
                raise ValueError("Os valores precisam ser números positivos.")

        except (ValueError, TypeError):
            messages.warning(request, 'O manejo e dias de colheita precisam ser números positivos.')
            return redirect('add')
        
        try:
            colhe = int(colhe)
        
            if colhe <= 0:
                raise ValueError("Os valores precisam ser números positivos.")

        except (ValueError, TypeError):
            messages.warning(request, 'Os dias de colheita precisam ser números positivos.')
            return redirect('add')
        
        try:
            poda = int(poda)  
            
        
            if poda <= 0:
                raise ValueError("Os valores precisam ser números positivos.")

        except (ValueError, TypeError):
            messages.warning(request, 'O tempo em dias para podar precisa ser  um número positivo.')
            return redirect('add')

        
    


        planta = Planta(
            nome=name,
            necessidade_de_nutrientes=nutri,
            ciclo_de_podagem=poda,
            ciclo_de_colheita=colhe,
            imagem = urlImagem
        )
        planta.save()
        return redirect('home')

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


        area = Espaco(
            nome=name,
            tipo_de_solo=tipoSolo,
            quantMaxCanteiro = quantCante,
            
        )
        area.save()
        return redirect('home')

class AddCanteiro(View):
    def get(self, request, espaco_id):
        espaco = Espaco.objects.get(id=espaco_id)  # Carrega o espaço correspondente
        return render(request, 'forms/canteiroForms.html', {'espaco': espaco})

    def post(self, request, espaco_id):
        espaco = Espaco.objects.get(id=espaco_id)  # Obtém o espaço

        name = request.POST.get("nome")
        quantPlantMax = request.POST.get("quantMaxPlant")

        # Verifica o limite de canteiros e o número atual
        limiteCant = espaco.quantMaxCanteiro  # Limite de canteiros no espaço
        quantCanteiros = espaco.canteiro_set.count()  # Total de canteiros no espaço

        if quantCanteiros >= limiteCant:
            messages.warning(request, 'O número máximo de canteiros para este espaço já foi atingido.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        try:
            quantPlantMax = int(quantPlantMax)
            if quantPlantMax <= 0:
                raise ValueError("Os valores precisam ser números positivos.")
        except (ValueError, TypeError):
            messages.warning(request, 'A quantidade de plantas no canteiro deve ser um valor maior que zero.')
            return redirect('add-canteiro', espaco_id=espaco_id)

        # Cria o novo canteiro
        Canteiro.objects.create(espaco=espaco, nome=name, quantMaxPlant=quantPlantMax)
        return redirect('home')


class ListAllView(View):
    def get(self, request):
        plantas = Planta.objects.all()

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

        # Verifica se a planta já está no canteiro
        canteiro_planta, created = CanteiroPlanta.objects.get_or_create(canteiro=canteiro, planta=planta)
        if not created:
            # Atualiza a quantidade da planta existente
            canteiro_planta.quantidade += quantidade
        else:
            # Define a quantidade da nova planta
            canteiro_planta.quantidade = quantidade
        canteiro_planta.save()

        return JsonResponse({
            'success': True,
            'planta_nome': planta.nome,
            'planta_imagem': planta.imagem,
            'quantidade': canteiro_planta.quantidade
        })

    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)