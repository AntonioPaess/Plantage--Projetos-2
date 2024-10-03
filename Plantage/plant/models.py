from django.db import models

class Espaco(models.Model):
    nome = models.CharField(max_length=20)
    tipo_de_solo = models.CharField(max_length=50)  # Ex: solo barroso
    
    def __str__(self):
        return self.nome


class Canteiro(models.Model):
    espaco = models.ForeignKey(Espaco, on_delete=models.CASCADE)
    nome = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nome


class Planta(models.Model):
    nome = models.CharField(max_length=20)
    necessidade_de_nutrientes = models.CharField(max_length=20) #ex: baixa, media, alta
    ciclo_de_podagem = models.IntegerField()  # Ciclo em dias, por exemplo
    ciclo_de_colheita = models.IntegerField()  # Ciclo em dias
    imagem = models.URLField(max_length = 20, default = None)

    
    def __str__(self):
        return self.nome


class InteracaoPlanta(models.Model):
    planta1 = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='interacoes_como_planta1')
    planta2 = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='interacoes_como_planta2')
    relacao = models.CharField(max_length=20)  # Ex: boa, ruim
    tipo_de_interacao = models.CharField(max_length=20)  # Ex: Controle de pragas, compatibilidade geral, etc.
    
    def __str__(self):
        return f'{self.planta1} - {self.planta2} ({self.relacao})'


class Praga(models.Model):
    nome_praga = models.CharField(max_length=30)
    planta_afetada = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='pragas_afetam')
    planta_afetada2 = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True, blank=True, related_name='pragas_afetam2')
    planta_repele = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name='pragas_repelidas_por')
    planta_repele2 = models.ForeignKey(Planta, on_delete=models.CASCADE, null=True, blank=True, related_name='pragas_repelidas_por2')
    
    def __str__(self):
        return self.nome_praga
