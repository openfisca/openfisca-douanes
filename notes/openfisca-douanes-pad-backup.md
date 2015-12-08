#OpenFisca Douanes

Questions / réponses entre les équipes

##Accès aux données

Les données sont importées dans OpenFisca.

Elles sont soit transformées dans un format interne à OpenFisca, soit simplement téléchargées et lues au démarrage d'OpenFisca.

Dans tous les cas les données utilisées par le simulateur doivent être publiques sous licence GPLv3 ou Licence publique.

##Simulations plus précises

Est-il envisagé / envisageable d'aller vers des résultats de simulation plus précis que ceux présentés dans les organigrammes ?
Quelles données seraient utilisées pour cela ?

##Hébergement

##Suivi de projet

Tabacs 
Tous produits
Récupération des données
Hébergement sur l'infrastructure OpenFisca

##Nomenclature XML

Mes questions :

   * Avez-vous travaillé en produisant directement les organigrammes ou bien êtes-vous partis de fichiers de données contenant cette logique de décision, que vous auriez transposés en représentation graphique ?
Réponse : Les franchises et les prohibitions applicables aux particuliers ne sont pas disponibles sous forme de fichier de données (xml ou autres). A ce stade, nous avons uniquement converti les informations réglementaires sous une forme graphique d'organigramme.


   * Existe-t-il en dehors des fichiers XML de la nomenclature, des fichiers ou une API permettant d'obtenir les informations de droits de douane et de consommation, et la TVA en fonction des quantités mais aussi du pays de provenance et de l'âge ?
Réponse :  A CONFIRMER le 1er décembre avec les équipes techniques. Nous disposons de fichiers xml sur les droits de douane, de consommation et sur la TVA applicable en fonction de la nomenclature et du pays de provenance. Le critère de l'âge de l'acheteur qui n'est utile que pour déterminer les seuils de franchise d'un particulier n'est pas repris (cf. réponse 1).

Voici l'explication détaillée montrant le besoin.

La nomenclature contient des "lignes", par exemple :

*    <ligne>
*      <Type>0</Type>
*      <Code>2401207000</Code>
*      <Lig\_Prod>80</Lig\_Prod>
*      <Alinea>2</Alinea>
*      <Description>Tabacs dark air cured</Description>
*    </ligne>

Cette entrée ne contient pas les droits de douane ni de TVA.

Dans un autre exemple :

*    <ligne>
*      <code>0101300000</code>
*      <alinea>1</alinea>
*      <statut>1</statut>
*      <datDeb>01/01/2012</datDeb>
*      <us>
*        <codMesa>NAR</codMesa>
*        <codQualif/>
*      </us>
*      <description>Anes</description>
*      <mesuresTec>
*        <mesureTec>
*          <codGeo>1011</codGeo>
*          <datDeb>01/01/2012</datDeb>
*          <droitDouane>
*            <unite>%</unite>
*            <taux>7.7</taux>
*          </droitDouane>
*          <taxeTva>
*            <unite>%</unite>
*            <taux>10</taux>
*          </taxeTva>
*        </mesureTec>
*      </mesuresTec>
*    </ligne>

On trouve un "droitDouane" et une "taxeTva".

Mais on n'a pas la même information que dans les organigrammes, où on trouve notamment le critère de quantité qui dit si le produit est taxé ou pas.

J'en déduis que (corrigez-moi si je me trompe) :

   * la nomenclature ne suffit pas,
   * qu'il faut transformer les organigrammes en fichiers de données,
   * et établir une correspondance entre les cases de l'organigramme (ie "Cigarillos") et la nomenclature avec soit un numéro de produit (ou plusieurs) soit un numéro de catégorie.
Réponse : OUI

Par exemple un fichier qui dirait :

   * Pour les cigarillos (numéro de produit 2402000000), si <= 50 unités alors droits = 0, sinon 0-26% droits douane + consommation
   * Si l'importateur a moins de 17 ans, pour le produit XXX, ce sera interdit
   * etc.
Sinon si cela n'existe pas nous devrons les reconstituer ensemble sur la base d'un format de fichiers que je commencerai à créer et vous ou moi-même pourrons les remplir graduellement.

Merci !

##Droits de douane et de consommation mélangés

L'équation a mal été comprise, est-ce :
    (20% TVA) + (0-26% droits douane et de consommation confondus)
    ou
    (20% TVA) + (0-26% droits douane) + (droits de consommation inconnus)    

soutDans l'organigramme du tabac par exemple, on trouve pour les produits hors UE des droits de douane et de consommation chiffrés entre 0 et X%. sout
soutPour certains autres produit soumis uniquement au droits de douane et pas de consommation, par exemple les produits alimentaires et végétaux, on voit que les droits de douane sont chiffrés de 0 à X%.sout

soutPar conséquent il faut également connaître pour chaque produit son éligibilité aux droits de douane et aux droits de consommation.sout


##Modélisation OpenFisca

Ces questions concernent l'équipe OpenFisca.

Faut-il introduire une nouvelle entité ProduitImporte ou utiliser l'entité Individu ?
Si non, pour simuler plusieurs produits il faut lancer plusieurs simulations ou lancer une simulation avec plusieurs individus, chacun ayant un produit.

Comment gérer les périodes dans les fichiers YAML ?
