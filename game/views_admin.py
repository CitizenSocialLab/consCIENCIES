from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django import forms

from game.models import *
from django.shortcuts import redirect
import random
from django.utils import timezone

from game.vars import *

import datetime

random.seed(datetime.datetime.now())

def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

@csrf_exempt
def registre(request, **kwargs):
    partida_activa = Partida.objects.filter(status="REGISTRANT")
    if len(partida_activa)>0:

        ######################################################################
        ##############  CODI PER QUAN S'ESTA LLISTANT USUARIS ################
        ######################################################################

        partida_activa = partida_activa[0]
        users = User.objects.filter(current_game=partida_activa)

        # Si hi ha una partida registrant i es un POST, vol dir que hem de comensar la partida nova
        if request.method == 'POST':

                if 1 > len(users) or len(users) > 6:
                    print 'Error number of active users: %d' % (len(users))
                    return redirect('admin.registre')

                # Generate Public Goods
                generate_users_public_goods(users)

                # Generate Bots if n < 6
                if len(users) < 6:
                    generate_bots(users)

                partida_activa.status = "GENERANT_DADES"
                partida_activa.save()
                partida_activa.status = "PLAYING"
                partida_activa.date_started = timezone.now()
                partida_activa.save()

                return redirect('admin.partida')

        # List of registered users
        return render_to_response('admin_registre.html', {'registre_iniciat': True,
                                                         'usuaris': users,
                                                         'partida': partida_activa,
                                                         'pagina': 'registre',
                                                         'lang': request.session['lang'],
                                                         'text': request.session['text']},
                                  context_instance=RequestContext(request))


    ######################################################################
    ##############  CODI PER QUAN NO HI HA REGISTER OBERT
    # No
    if request.method == 'POST':
        results = Partida.objects.all().order_by('-num_partida')
        npartida = 1
        #Si hi ha mes d'un result, mirem quin es el seguent num de partida
        if len(results) > 0:
            npartida = results[0].num_partida+1

        partida = Partida.objects.create(num_partida=npartida,
                                         status="REGISTRANT",
                                         classe=EXPERIMENT)
        partida.save()
        return redirect('admin.registre')

    #Sino es un post, ensenyem el boto per crear registre nou
    return render_to_response('admin_registre.html', {
                                        'registre_iniciat': False,
                                         'lang': request.session['lang'],
                                         'pagina': 'registre',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

def generate_users_public_goods(users):

    for user in users:

        public_goods = PublicGoods()
        public_goods.user = user
        public_goods.game = user.current_game
        public_goods.is_robot = 0

        public_goods.save()

    return redirect('admin.registre')

def generate_bots(users):

    user = users[0]

    for i in range(0,6-len(users),1):

        user_bot = User()
        user_bot.nickname = random.choice(['#010', '#011', '#012', '#013', '#014', '#015', '#016', '#017', '#018', '#019', '#020'])
        user_bot.age = random.choice(['r1', 'r2', 'r3', 'r4', 'r5'])
        user_bot.gender = random.choice(['W', 'M', 'NB', 'NA'])
        user_bot.studies = random.choice(['r1', 'r2', 'r3', 'r4', 'r5'])
        user_bot.postal_code = random.choice(range(8000,8100,1))
        user_bot.is_robot = True
        user_bot.current_game = user.current_game
        user_bot.num_seleccions = 1
        user_bot.save()

        public_goods = PublicGoods()
        public_goods.user = user_bot
        public_goods.game = user.current_game
        public_goods.is_robot = True
        public_goods.selection = random.choice(['C', 'I', 'D'])
        public_goods.date_selection = timezone.now() + datetime.timedelta(seconds=random.choice(range(0,30,1)))
        public_goods.save()

        current_story = Story.objects.filter(game_id=user.current_game)[0]

        story = Story()
        story.game = user.current_game
        story.user = user_bot
        story.type = current_story.type
        story.question1 = random.choice(['r1', 'r2', 'r3', 'r4'])
        story.question2 = random.choice(['r1', 'r2', 'r3', 'r4'])
        story.question3 = random.choice(['r1', 'r2', 'r3', 'r4'])
        story.save()

    return True

@csrf_exempt
def partida(request, **kwargs):
    #Si no hi ha partida jugant-se mostrar avis
    return render_to_response('admin_partida.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'partida',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def stats(request, **kwargs):
    #Sino es un post, ensenyem el boto per crear registre nou
    return render_to_response('admin_stats.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'stats',
                                         'text': request.session['text']},
                          context_instance=RequestContext(request))

@csrf_exempt
def partida_detail(request, **kwargs):
    num_partida = kwargs.get('num_partida', None)

    #Si no hi ha partida jugant-se mostrar avis
    return render_to_response('admin_partida_detail.html', {
                                         'lang': request.session['lang'],
                                         'num_partida': num_partida,
                                         'pagina': 'partida_detail',
                                         'text': request.session['text']},
                                        context_instance=RequestContext(request))

@csrf_exempt
def users(request, **kwargs):

    users = []

    for u in User.objects.filter(is_robot=False).order_by('-date_updated'):

        user = {'id': u.id, 'nickname': u.nickname, 'current_game': u.current_game_id if u.current_game_id else '-', 'storyA': '-', 'storyB': '-',
                'storyC': '-', 'storyD': '-', 'total': 0, 'status': u.status if u.status else '-'}

        public_goods = PublicGoods.objects.filter(user=u)

        for pg in public_goods:
            s = Story.objects.filter(user=u).filter(game=pg.game)[0]
            if s.type == 'A':
                user['storyA'] = pg.selection
                user['total'] += 1
            if s.type == 'B':
                user['storyB'] = pg.selection
                user['total'] += 1
            if s.type == 'C':
                user['storyC'] = pg.selection
                user['total'] += 1
            if s.type == 'D':
                user['storyD'] = pg.selection
                user['total'] += 1

        users.append(user)

    print users
    users_1 = users[0:18]
    users_2 = users[18:36]


    return render_to_response('admin_users.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'users',
                                         'text': request.session['text'],
                                         'users_1': users_1,
                                         'users_2': users_2},
                          context_instance=RequestContext(request))

@csrf_exempt
def users_reset(request, **kwargs):
    user_id = kwargs.get('user_id', None)
    print "Reseting user", user_id
    if user_id is not None:
        user = User.objects.get(id=user_id)
        if user is not None:
            user.current_game=None
            user.save()
            request.session['user'] = user
    return redirect('admin.users')

@csrf_exempt
def partida_list(request, **kwargs):

    partides = [{'num_partida': p.num_partida,
                 'classe': p.classe,
                 'date_created': p.date_created,
                 'users': []}
                for p in Partida.objects.filter(status__in=("FINISHED", "FINISHED_MANUAL")).order_by('-date_ended')[0:20]]
    partides_1 = partides[0:10]
    partides_2 = partides[10:20]
    return render_to_response('admin_partida_list.html', {
                                         'lang': request.session['lang'],
                                         'pagina': 'partida_list',
                                         'text': request.session['text'],
                                         'partides_1': partides_1,
                                         'partides_2': partides_2},
                          context_instance=RequestContext(request))


