from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement
from .models import Character

def nauti_list(request):
        equipement=Equipement.objects.all()
        character=Character.objects.all()
        return render(request, 'nauti/nauti_list.html', {"Lieux_emblematiques" : equipement, "Nauti_membres" : character})

def lieu_detail(request, id_equip):
        equipement = get_object_or_404(Equipement, id_equip=id_equip)
        if equipement.id_equip=='Hangar':
                return render(request, 'nauti/lieu_detail.html', {'equipement': equipement, 'message': "Tout le monde peut se retrouver au hangar ! La place est illimitée\n et passer au hangar permet de se RESTAURER. En revanche si vous\nn'avez pas faim, c'est que vous avez sûrement autre chose à faire !"})
        if equipement.id_equip=='Banque SG':
                return render(request, 'nauti/lieu_detail.html', {'equipement': equipement, 'message': "La banque permet de venir emprunter de l'argent, et ainsi de passer\n de PAUVRE à RICHE, servez-vous en pour vous remplir les poches avant \nd'aller tout dépenser en préparant la soirée au R2 !"})
        if equipement.id_equip=="Appart d'Alexis":
                return render(request, 'nauti/lieu_detail.html', {'equipement': equipement, 'message': "L'appart d'Alexis est un petit coin de paradis où vous pourrez \nvous REPOSER en faisant du graphisme afin d'améliorer l'image de la Nauti \nsur les réseaux sociaux. Allez faire ça dès que vous vous sentez FATIGUÉ.\n Vrai moussailon ne dort pas !" })
        if equipement.id_equip=='R2 Terrasses du port':
                return render(request, 'nauti/lieu_detail.html', {'equipement': equipement, 'message': "Ah le R2, salle iconique de Marseille que la Nauti a réservé pour \n faire une super soirée ! Allez y pour préparer la soirée à venir, mais \nallez y avec de l'argent à dépenser ! Sinon il ne s'y passera rien."})

def membre_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    equipements = Equipement.objects.all()
    banque=get_object_or_404(Equipement, id_equip='Banque SG')
    terrasses=get_object_or_404(Equipement, id_equip='R2 Terrasses du port')
    appart=get_object_or_404(Equipement, id_equip="Appart d'Alexis")
    hangar=get_object_or_404(Equipement, id_equip='Hangar')
    lieu=character.lieu
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
        if form.is_valid():
                if form.data['lieu']=='Banque SG':
                        if banque.disponibilite=='Occupé':
                            return render(request ,"nauti/membre_detail.html", {'character': character, 'message': "C'est pas la peine d'être 50 à la banque ! (le changement ne sera pas enregistré)" , 'equipements': equipements})
                        elif character.etat=='Pauvre' and banque.disponibilite=='Libre':
                                ancien_lieu.disponibilite = "Libre"
                                ancien_lieu.save()
                                character.etat = 'Riche'
                                form.save()
                                nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
                                if nouveau_lieu.id_equip != "Hangar":
                                        nouveau_lieu.disponibilite = "Occupé"
                                else : 
                                        nouveau_lieu.disponibilite = "Libre"
                                nouveau_lieu.save()
                                return redirect('membre_detail', id_character=id_character)
                        else :
                                return render(request ,"nauti/membre_detail.html", {'character': character, 'message': character.id_character +" n'est pas en état d'y aller (le changement ne sera pas enregistré, veuillez consulter la description des lieux)" , 'equipements': equipements})



                if form.data['lieu']=="Appart d'Alexis":
                        if appart.disponibilite=='Occupé':
                            return render(request ,"nauti/membre_detail.html", {'character': character, 'message': "L'appart d'Alexis n'est pas assez grand pour autant de monde ! (le changement ne sera pas enregistré)" , 'equipements': equipements})
                        elif character.etat=='Fatigué' and appart.disponibilite=='Libre':
                                ancien_lieu.disponibilite = "Libre"
                                ancien_lieu.save()
                                character.etat = 'Pauvre'
                                form.save()
                                nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
                                if nouveau_lieu.id_equip != "Hangar":
                                        nouveau_lieu.disponibilite = "Occupé"
                                else : 
                                        nouveau_lieu.disponibilite = "Libre"
                                nouveau_lieu.save()
                                return redirect('membre_detail', id_character=id_character)
                        else :
                                return render(request ,"nauti/membre_detail.html", {'character': character, 'message': character.id_character +" n'est pas en état d'y aller (le changement ne sera pas enregistré, veuillez consulter la description des lieux)" , 'equipements': equipements})
                
                if form.data['lieu']=='R2 Terrasses du port':
                        if terrasses.disponibilite=='Occupé':
                            return render(request ,"nauti/membre_detail.html", {'character': character, 'message': "Il y a déjà quelqu'un au R2, va faire autre chose moussaillon ! (le changement ne sera pas enregistré)" , 'equipements': equipements})
                        elif character.etat=='Riche' and terrasses.disponibilite=='Libre':
                                ancien_lieu.disponibilite = "Libre"
                                ancien_lieu.save()
                                character.etat = 'Affamé'
                                form.save()
                                nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
                                if nouveau_lieu.id_equip != "Hangar":
                                        nouveau_lieu.disponibilite = "Occupé"
                                else : 
                                        nouveau_lieu.disponibilite = "Libre"
                                nouveau_lieu.save()
                                return redirect('membre_detail', id_character=id_character)
                        else :
                                return render(request ,"nauti/membre_detail.html", {'character': character, 'message': character.id_character +" n'est pas en état d'y aller (le changement ne sera pas enregistré, veuillez consulter la description des lieux)" , 'equipements': equipements})
                
                if form.data['lieu']=='Hangar':
                        if character.etat=='Affamé':
                                ancien_lieu.disponibilite = "Libre"
                                ancien_lieu.save()
                                character.etat = 'Fatigué'
                                form.save()
                                nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
                                if nouveau_lieu.id_equip != "Hangar":
                                        nouveau_lieu.disponibilite = "Occupé"
                                else : 
                                        nouveau_lieu.disponibilite = "Libre"
                                nouveau_lieu.save()
                                return redirect('membre_detail', id_character=id_character)
                        else:
                               return render(request ,"nauti/membre_detail.html", {'character': character, 'message': character.id_character +" n'est pas en état d'y aller (le changement ne sera pas enregistré, veuillez consulter la description des lieux)" , 'equipements': equipements})
                
    else:
        form = MoveForm()

        return render(request,
                  'nauti/membre_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form})
