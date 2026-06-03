# Révision 31/03/2026


### Exercice 1
___
Proposer un document xml qui est valide selon le DTD suivant :

```dtd
<!ELEMENT Personne ( (M | Mme | Mlle), Prenom+, Nom ) >
<!ELEMENT M EMPTY>
<!ELEMENT Mme EMPTY>
<!ELEMENT Mlle EMPTY>
<!ELEMENT Prenom (#PCDATA) >
<!ELEMENT Nom (#PCDATA) > 
```


### Exercice 2
___
Proposer un document xml qui est valide selon le DTD suivant :

```dtd
<!ELEMENT Personne ( (M | Mme | Mlle), Prenom+, Nom ,DateNaissance) >
<!ELEMENT M EMPTY>
<!ELEMENT Mme EMPTY>
<!ELEMENT Mlle EMPTY>
<!ELEMENT prenom (#PCDATA) >
<!ELEMENT nom (#PCDATA) >
<!ELEMENT DateNaissance(jour,mois,annee)>
<!ELEMENT jour (#PCDATA) >
<!ELEMENT mois (#PCDATA) >
<!ELEMENT annee (#PCDATA) >
```

### Exercice 3
___

Proposer un DTD pour que le document xml suivant soit valide : 

```xml
<?xml  version="1.0" encoding="UTF-8" ?>
<Modules>
    <cours>
        <titre>Prog des applications Web coté client</titre>
        <mh>  180h </mh>
        <coefficient>3</coefficient>
    </cours>
    <cours>
        <titre>PS</titre>
        <mh>120h</mh>
    </cours>
</Modules>
```


### Exercice 4
___

*Des projets et des gens...*  

Le LRI, dont le directeur est Michel Beaudouin-Lafon, dispose de plusieurs équipes de recherche. Parmis elles,
on trouve l’équipe Programmation (directrice Marie-Claude Gaudel), l’équipe Démonstration (directrice Chris
tine Paulin), l’équipe Intelligence Artificielle et Systemes d’Inference (directrice Chantal Reynaud), l’équipe In
ference et Apprentissage (directrice Michèle Sebag) et l’équipe Bases de données (directeur Nicolas Spyratos).
Ces équipes participent à différents projets avec l’INRIA. Le projet GEMO (directeur Serge Abiteboul) implique
l’équipe Intelligence Artificielle et Systemes d’Inference et l’équipe Bases de données, le projet TAO (directeur
Marc Shoenauer) implique l’équipe Inference et Apprentissage, le projet InSitu (directrice Wendy Mackay) im
plique l’équipe Programmation et les projets Proval et Logical (directeur Gilles Dowek) impliquent l’équipe Démonstration.

1. Représentez les informations données dans l’énoncé ci-dessus, et ce sans redondance, dans le formalisme
XML. Vérifiez que votre document est bien formé.
2. Ajouter une DTD au fichier XML.
3. Validez avec `validator.py`.


### Exercice 5
___

*Traitement d’une commande...*

**Contexte**  
Vous développez une API pour une application de livraison de repas.
Une application mobile envoie une requête HTTP contenant un JSON pour créer une commande.

Votre backend doit :
- Valider les données reçues
- Refuser les données incorrectes
- Extraire certaines informations

**Donnée reçue**
```json
{
    "customer": {
        "id": 123,
        "name": "Alice Dupont",
        "email": "alice@example.com"
    },
    "restaurantId": 45,
    "items": [
        {
            "productId": 1,
            "name": "Pizza",
            "quantity": 2,
            "price": 12.5
        },
        {
            "productId": 2,
            "name": "Tiramisu",
            "quantity": 0,
            "price": 6
        }
    ],
    "status": "delivered"
}
```

1. **Analyse.** Observer le JSON: Quelles sont les erreurs ou incohérences dans ces données ?

2. **JSON Schema** Créer un JSON Schema qui valide :
```
customer.id : entier
customer.email : email valide
items : tableau
quantity ≥ 1
price ≥ 0
status appartient à { "pending", "preparing", "delivered", "cancelled" }
```
3. Modifier votre Schema pour :
- rendre items obligatoire
- imposer au moins 1 item
- interdire les champs inconnus dans customer

On suppose maintenant que les données sont valides.

4. Écrire les expressions JSONPath pour :
- Récupérer tous les noms des produits
- Récupérer toutes les quantités
- Récupérer l’email du client

5. Écrire les expressions JSONPath pour :
- Les items avec quantité ≥ 2
- Les items avec prix > 10a

6. Votre backend doit calculer le total. Extraire avec JSONPath :
- les prix
- les quantités

(Le calcul peut être fait en pseudo-code)

7. Cas d’erreur API.
On reçoit maintenant ce JSON :

```json 
{
    "customer": {
        "id": "abc",
        "email": "not-an-email"
    },
    "items": [],
    "status": "unknown"
}
```
- Lister toutes les erreurs
- Expliquer pourquoi le JSON doit être refusé
- Indiquer quelles règles du Schema sont violées

8. Proposer une version corrigée du JSON initial