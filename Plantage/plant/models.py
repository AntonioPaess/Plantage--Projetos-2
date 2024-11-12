from django.db import models
from a_users.models import Profile

class Espaco(models.Model):
    nome = models.CharField(max_length=20)
    tipo_de_solo = models.CharField(max_length=50)
    quantMaxCanteiro = models.IntegerField(default=5)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Planta(models.Model):
    nome = models.CharField(max_length=100)
    necessidade_de_nutrientes = models.TextField()
    ciclo_de_podagem = models.IntegerField()
    ciclo_de_colheita = models.IntegerField()
    imagem = models.URLField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    # Novo campo para plantas inimigas
    plantas_inimigas = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.nome

class Canteiro(models.Model):
    espaco = models.ForeignKey(Espaco, on_delete=models.CASCADE)
    nome = models.CharField(max_length=20)
    quantMaxPlant = models.IntegerField()
    plantas = models.ManyToManyField(Planta, through='CanteiroPlanta', blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# Novo modelo intermediário que gerencia plantas dentro do canteiro
class CanteiroPlanta(models.Model):
    canteiro = models.ForeignKey(Canteiro, on_delete=models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)  # Quantidade de plantas no canteiro

    class Meta:
        unique_together = ('canteiro', 'planta')  # Garante que a combinação de canteiro e planta seja única

    def __str__(self):
        return f'{self.quantidade}x {self.planta.nome} em {self.canteiro.nome}'



class InteracaoPlanta(models.Model):
    planta1 = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='interacoes_como_planta1')
    planta2 = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='interacoes_como_planta2')
    relacao = models.CharField(max_length=20)  # Ex: boa, ruim
    tipo_de_interacao = models.CharField(max_length=20)  # Ex: Controle de pragas, compatibilidade geral, etc.
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.planta1} - {self.planta2} ({self.relacao})'


class Praga(models.Model):
    nome_praga = models.CharField(max_length=30)
    planta_afetada = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='pragas_afetam')
    planta_afetada2 = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True, blank=True, related_name='pragas_afetam2')
    planta_repele = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='pragas_repelidas_por')
    planta_repele2 = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True, blank=True, related_name='pragas_repelidas_por2')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome_praga


