from django.views.decorators.csrf import csrf_exempt

from game.models import *
from game.vars import *

import math

import datetime
from django.utils import timezone

import json
from django.http import HttpResponse

import random
random.seed(datetime.datetime.now())

@csrf_exempt
def demanar_dades(request, **kwargs):
    user_id = kwargs.get('user_id', None)

    response_data={}
    jugant = "false"

    user = None
    try:
        # partida que juga aquest usuari
        user = User.objects.get(id=user_id)
    except:
        print "Usuari "+str(user_id)+" no existeix"

    # Nomes si no es juga el clima
    if user.current_game.status == "PLAYING":
        jugant = "PLAYING"

    response_data["jugant"] = jugant
    return HttpResponse(json.dumps(response_data),content_type="application/json")

###############################################################################################
################################## PUBLIC GOODS ###############################################
###############################################################################################

@csrf_exempt
def send_action_public_goods(request, user_id=None, result=None, **kwargs):

    user_id = user_id
    result = result

    user = User.objects.get(id=user_id)

    user_public_goods = PublicGoods.objects.filter(user=user.id).filter(game=user.current_game)[0]

    if result=='D' or result=='I' or result=='C' or result=='T': # D: Defection, I:Intervention, C:cooperation, T: Timeout
        if user_public_goods.selection == "":
            user_public_goods.selection = result
            user_public_goods.is_robot = False
            user_public_goods.date_selection = timezone.now()
            user_public_goods.save()

            user.num_seleccions += 1
            user.save()

        response_data = {"saved": "ok"}
    else:
        response_data = {"saved": "error"}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def get_results_public_goods(request, **kwargs):

    response_data = {'user': 0,
                     'game': 0,
                     'users':0,
                     'total_selections':0,
                     'selections': [],
                     'threshold' : 0,
                     'result' : 0,
                     'finished': False,
                     'correcte': True }

    game_id = kwargs.get('game_id', None)
    user_id = kwargs.get('user_id', None)

    public_goods = PublicGoods.objects.filter(game_id = game_id).order_by('-date_selection')

    for pg in public_goods:
        if pg.selection != '':
            selections = {
                    'user_id': pg.user.id,
                    'user_nickname': pg.user.nickname,
                    'selection': pg.selection
                }
            response_data['selections'].append(selections)

    response_data['user'] = user_id
    response_data['game'] = game_id
    response_data['users'] = len(public_goods)
    response_data['threshold'], response_data['result'] = calculate_result(response_data['selections'])
    response_data['total_selections'] = len(response_data['selections'])

    if len(public_goods) == len(response_data['selections']):
        response_data['finished'] = True
        game = Partida.objects.get(id=game_id)
        game.date_ended = timezone.now()

        if response_data['result'] > 100:
            game.goal_achieved = True
        else:
            game.goal_achieved = False

        game.threshold = response_data['threshold']

        game.status = 'FINISHED'
        game.save()

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def calculate_result(selections):


    outcome = 0
    threshold_achieved = 0.66

    for s in selections:
        if s['selection'] == 'D':
            outcome += 0
        if s['selection'] == 'I':
            outcome += 1
        if s['selection'] == 'C':
            outcome += 3

    print 'Outcome: '+str(outcome)
    threshold = outcome / float(18)
    print 'Threshold: '+str(threshold)
    achieved = (threshold / float(threshold_achieved))*100
    print 'Achieved: '+str(achieved)

    return threshold, achieved

###############################################################################################
###############################################################################################
################         WEBSERVICES ADMINISTRACIO      #######################################
###############################################################################################
###############################################################################################
@csrf_exempt
def usuaris_registrats(request, **kwargs):
    response_data = {}

    partida_activa = Partida.objects.filter(status="REGISTRANT")
    if len(partida_activa) > 0:
        response_data['registrant'] = True

        partida_activa = partida_activa[0]

        all_users = []
        for usuari in User.objects.filter(current_game=partida_activa):
            data_users = { "num_registre": usuari.id,
                           "nom": usuari.nickname,
                           "story": Story.objects.filter(game_id=partida_activa).filter(user_id=usuari.id)[0].type,
                           "date_register": usuari.date_register.strftime("%a,  %d/%m/%Y - %H:%M:%S")}
            all_users.append(data_users)
        response_data['usuaris'] = all_users

    else:
        response_data['registrant'] = False

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def estat_partida(request, **kwargs):
    response_data = {'partides': []}

    for partida in Partida.objects.filter(status="PLAYING"):

        #Info de la partida
        users = User.objects.filter(current_game__num_partida = partida.num_partida)
        story = Story.objects.filter(game=partida.id)

        data = {'num_partida': partida.num_partida,
                'date_created': partida.date_created.strftime("%H:%M:%S (%d/%m )"),
                'date_started': partida.date_started.strftime("%H:%M:%S (%d/%m )"),
                'story': story[0].type,
                'time': float(TIME_DECISION - (timezone.now() - partida.date_started).total_seconds())
                }

        response_data['partides'].append(data)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def tancar_partida(request, **kwargs):
    print kwargs.get('num_partida', None)

    response_data = {}
    num_partida = kwargs.get('num_partida', None)
    partida = Partida.objects.get(num_partida=num_partida)

    response_data["correcte"] = False

    if partida.status == "PLAYING":
        partida.status = "FINISHED_MANUAL"
        partida.date_ended = timezone.now()
        partida.save()
        response_data["correcte"] = True


    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def llistat_partides(request, **kwargs):

    response_data = {}

    all_partides = []
    for partida in Partida.objects.filter().order_by('-id')[:15]:

        users = User.objects.filter(current_game__num_partida = partida.num_partida)
        #print(partida.date_ended)
        data_partida = {"num_partida": partida.num_partida,
                        "achieved": partida.goal_achieved,
                        "date_created": partida.date_created.strftime("%a, %H:%M:%S"),
                        "date_ended": partida.date_ended.strftime("%a, %H:%M:%S") if partida.date_ended else '-',
                        "status": partida.status,
                        "threshold": round(partida.threshold,2),

        }

        all_partides.append(data_partida)

    response_data["partida"] = all_partides

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def stats_partida(request, **kwargs):

    response_data = {}

    all_partides = []

    for partida in Partida.objects.filter(status="FINISHED").order_by('-id')[:100]:

        users = User.objects.filter(current_game__num_partida = partida.num_partida)
        data_partida = {"num_partida": partida.num_partida,
                        "goal_achieved": partida.goal_achieved,
                        "status": partida.status}


        all_partides.append(data_partida)

    response_data["partida"] = all_partides

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# Control during the game
@csrf_exempt
def stats_partida_detail(request, **kwargs):

    num_partida = kwargs.get('num_partida', None)

    game = Partida.objects.filter(num_partida=num_partida)[0]
    public_goods = PublicGoods.objects.filter(game_id=game.id).order_by('user_id')
    story = Story.objects.filter(game_id=game.id).order_by('user_id')

    response_data = {
        "num_partida": num_partida,
        "id": [pg.user.id for pg in public_goods],
        "status": [pg.user.status for pg in public_goods],
        "nickname": [pg.user.nickname for pg in public_goods],
        "story": [s.type for s in story],
        "selection": [pg.selection for pg in public_goods],
        "time_selection": [round((pg.date_selection - pg.game.date_started).total_seconds(),2) if pg.date_selection is not None else '-' for pg in public_goods],
        "date_created": game.date_created.strftime("%a, %H:%M:%S"),
        "date_ended": game.date_ended.strftime("%a, %H:%M:%S") if game.date_ended else '-',
        "time": round(TIME_DECISION - (timezone.now() - game.date_started).total_seconds(),0) if game.date_ended is None else '0',
        "threshold": round(game.threshold,2),
        "selections": N - len([pg for pg in public_goods if pg.selection == ""]),
        "achieved": game.goal_achieved,

    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")

