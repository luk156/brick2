# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
# Create your models here.
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class CategoriaAttivita(MPTTModel):
    nome = models.CharField('Nome', max_length=30)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return u'%s' % (self.nome)

    class Meta:
        verbose_name = "Categoria dell'attività"
        verbose_name_plural = "Categorie delle attività"

    class MPTTMeta:
        order_insertion_by = ['nome']


class Attivita(models.Model):
    nome = models.CharField('Nome', max_length=30)
    categoria = models.ForeignKey(CategoriaAttivita, related_name='categoria_attivita')

    def __str__(self):
        return u'%s ( %s )' % (self.nome, self.categoria)

    class Meta:
        verbose_name = "Attività"
        verbose_name_plural = "Attività"


class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=30)
    cognome = models.CharField('Cognome', max_length=30, null=True, blank=True)
    mail = models.EmailField('E-Mail', null=True, blank=True)
    telefono = models.IntegerField('Telefono principale', null=True, blank=True)
    indirizzo = models.TextField('Indirizzo', max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.nome, self.cognome)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"


class Cantiere(models.Model):
    descrizione = models.CharField('Descrizione', max_length=100)
    indirizzo = models.TextField('Indirizzo', max_length=100, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, related_name='cliente_cantiere')

    def ore_preventivo(self):
        return self.cantiere_scheda.filter(attivita_svolte__schedaattivita__ext_preventivo=False).aggregate(Sum('attivita_svolte__schedaattivita__ore'))['attivita_svolte__schedaattivita__ore__sum']

    def ore_extra_preventivo(self):
        return self.cantiere_scheda.filter(attivita_svolte__schedaattivita__ext_preventivo=True).aggregate(Sum('attivita_svolte__schedaattivita__ore'))['attivita_svolte__schedaattivita__ore__sum']

    def __str__(self):
        return '%s' % (self.descrizione)

    class Meta:
        verbose_name = "Cantiere"
        verbose_name_plural = "Cantieri"


class Dipendente(models.Model):
    nome = models.CharField('Nome', max_length=30)
    cognome = models.CharField('Cognome', max_length=30)

    def __str__(self):
        return '%s %s' % (self.nome, self.cognome)

    class Meta:
        verbose_name = "Dipendente"
        verbose_name_plural = "Dipendenti"


class SchedaLavoro(models.Model):
    dipendente = models.ForeignKey(Dipendente, related_name='dipendente_scheda')
    cantiere = models.ForeignKey(Cantiere, related_name='cantiere_scheda')
    attivita_svolte = models.ManyToManyField(Attivita, related_name='attivita_scheda', through='SchedaAttivita')
    data = models.DateField()

    def __str__(self):
        return '%s (%s) - %s' % (self.id, self.dipendente, self.data)

    class Meta:
        verbose_name = "Scheda lavoro"
        verbose_name_plural = "Schede lavoro"


class SchedaAttivita(models.Model):
    scheda = models.ForeignKey(SchedaLavoro)
    attivita = models.ForeignKey(Attivita)
    ore = models.IntegerField('Ore Lavorative')
    ext_preventivo = models.BooleanField('Extra preventivo', default=False)
