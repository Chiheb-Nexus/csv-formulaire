import csv
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import StreamingHttpResponse
from form_app import signup_form, csv_models

class Registration(View):
    form_class = signup_form.RegistrationForm
    template = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template, {'form': form}) 

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # On peut modifier les attributs de account_form
            # avant le sauvegarde
            account_form, user = form.save()
            account_form.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect(reverse('home'))
        else:
            return render(request, self.template, {'form': form})

class Home(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = ''
    template = 'home.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'message': 'Login avec succès!'})

class UpdateDB(View):
    '''
        Mettre à jour la base de donnée selon les valeurs trouvées dans le document PDF
        convertis en tableaux des tuples.
        Écraser les données s'ils existent
    '''

    template = 'home.html'
    persons = [(1, 'THIERRY', 5), (2, 'DAVID', 7), (3, 'STAN', 8), (4, 'JAMAL', 6), 
                (5, 'SHEME', 4), (6, 'NOLWENN', 7), (7, 'JULIEN', 6), (8, 'EDOUARD', 6), 
                (9, 'PAUL', 1), (10, 'FLORIAN', 4)]
    roles = [(1, None, 'CTO'), (2, None, 'DEVELOPPEUR'), (3, 2, 'BACK'), (4, 3, 'PHP'), 
                (5, 4, 'LEAD'), (6, 3, 'PYTHON'), (7, 2, 'FRONT'), (8, None, 'STAGIAIRE')]

    def get(self, request, *args, **kwargs):
        
        for role_id, parent, role in self.roles:
            parent_db = csv_models.Role.objects.filter(roleID=parent).first()
            if parent_db:
                # Create
                role_db = csv_models.Role(roleID=role_id, parentRoleID=parent_db, roleName=role)
            else:
                # Update
                role_db = csv_models.Role(roleID=role_id, roleName=role)
            role_db.save()

        for person_id, person_name, role_id in self.persons:
            role_db = csv_models.Role.objects.filter(roleID=role_id).first()
            if role_db:
                person_db = csv_models.Person(personID=person_id, personName=person_name, roleID=role_db)
                person_db.save()


        return render(request, self.template, {'message': 'Mise à jour de la base de donnée avec succès'})

class DisplayPersons(View):
    template_name = 'display_persons.html'

    def get(self, request, *args, **kwargs):
        '''
        Utiliser l'ORM de django pour faire un group by et un join
        La requête en SQLite est comme suit:
            SELECT "form_app_role"."roleName", COUNT("form_app_person"."roleID_roleID") 
                AS "num" FROM "form_app_person" INNER JOIN "form_app_role" ON 
                    ("form_app_person"."roleID_roleID" = "form_app_role"."roleID") 
                        GROUP BY "form_app_role"."roleName"

        '''
        roles_counts = csv_models.Person.objects.all(
                        ).values('roleID__roleName').annotate(num=Count('roleID_id'))
        persons = csv_models.Person.objects.all()
        return render(request, self.template_name, {'roles': roles_counts, 'persons': persons})

class Echo:
    def write(self, value):
        return value

class StreamCSV(View):
    """Streaming d'un large fichier CSV"""
    
    def get_row(self, obj):
        '''yield les éléments de l'objet'''
        for key, value in enumerate(obj):
            if key == 1:
                yield from value
            else:
                yield value        
    

    def get(self, request, *args, **kwargs):
        roles_counts = csv_models.Person.objects.all(
                        ).values('roleID__roleName').annotate(num=Count('roleID_id'))
        persons = csv_models.Person.objects.all()

        headers = [''] + [role.get('roleID__roleName') for role in roles_counts]
        body = ([person.personName] + list(map(
            lambda x: 'X' if x['roleID__roleName'] == person.roleID.roleName else '' , roles_counts)
            ) for person in persons)
        footer = ['total'] + list(map(lambda x: str(x['num']), roles_counts))

        buffer_ = Echo()
        writer = csv.writer(buffer_)
        # Ou bien on peut créer une liste
        # Mais inefficace pour les grands CSV
        #rows = []
        #rows.append(headers)
        #for elm in body:
        #    rows.append(elm)
        #rows.append(footer)
        rows = [headers, body, footer]
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in self.get_row(rows)), 
            content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="test.csv"'
        return response
            
            
        
        



