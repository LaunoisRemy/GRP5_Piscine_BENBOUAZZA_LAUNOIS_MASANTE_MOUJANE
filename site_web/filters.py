from .models import ScoreParPartie
import django_filters

class SearchFilter(django_filters.FilterSet):

### Filtre sur la base de donnée des ScoreParPartie (bonne réponse par sous partie)
    class Meta:
        model = ScoreParPartie
        fields = ['id_TOEICEnCours__id_TOEIC', 'id_Eleve__nom', 'id_Eleve__groupe__lib_Groupe','id_Eleve__classe__lib_Classe','id_Eleve__classe__annee_Promo','id_SousPartie__lib_Partie','id_SousPartie__type_Partie'
         ]

class FiltreNoteParPartie(django_filters.FilterSet):

    class Meta:
        model = ScoreParPartie
        id_Eleve = django_filters.ModelChoiceFilter(field_name='Oui')
        fields = ['id_TOEICEnCours__id_TOEIC', 'id_Eleve','id_Eleve__groupe','id_Eleve__classe'
         ]

         # On filtre par toeic, classe, groupe de td, année de promo