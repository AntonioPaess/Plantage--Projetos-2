from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from plant.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

@login_required
def HomeView(request):
    return render(request, 'home.html')

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
    def get(self, request):
        espacos = Espaco.objects.all()  # Carrega os espaços para o formulário
        return render(request, 'forms/canteiroForms.html', {'espacos': espacos})

    def post(self, request):
        espacos = Espaco.objects.all()  # Carrega os espaços para o caso de erro no formulário
        if request.method == "POST":
            name = request.POST.get("nome")
            quantPlantMax = request.POST.get("quantMaxPlant")
            espaco_id = request.POST.get('espaco')

            try:
                # Verifica se o espaço selecionado existe
                espaco = Espaco.objects.get(id=espaco_id)

                # Verifica o limite de canteiros e o número atual
                limiteCant = espaco.quantMaxCanteiro  # Pega o limite de canteiros no espaço
                quantCanteiros = espaco.canteiro_set.count()  # Pega o total de canteiros no espaço

                # Verifica se ainda há espaço para um novo canteiro
                if quantCanteiros >= limiteCant:
                    messages.warning(request, 'O número máximo de canteiros para este espaço já foi atingido.')
                    return redirect('add-canteiro')

                # Verifica se a quantidade máxima de plantas no canteiro é válida
                try:
                    quantPlantMax = int(quantPlantMax)
                    if quantPlantMax <= 0:
                        raise ValueError("Os valores precisam ser números positivos.")
                except (ValueError, TypeError):
                    messages.warning(request, 'A quantidade de plantas no seu canteiro necessita ser um valor maior que zero.')
                    return redirect('add-canteiro')

                # Cria o novo canteiro
                Canteiro.objects.create(espaco=espaco, nome=name, quantMaxPlant=quantPlantMax)
                return redirect('home')

            except Espaco.DoesNotExist:
                # Caso o espaço não exista
                messages.warning(request, 'Espaço inválido!')
                return render(request, 'forms/canteiroForms.html', {'espacos': espacos})

        return render(request, 'forms/canteiroForms.html', {'espacos': espacos})

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