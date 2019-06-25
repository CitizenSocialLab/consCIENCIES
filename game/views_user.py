from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import *

from django import forms
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from game.models import *
from game.vars import *

import datetime
from django.utils import timezone

import math

def user_exists_in_db(user):
    try:
        User.objects.get(pk=user.id)
        return True
    except:
        return False

#### 1. Index
def index(request, **kwargs):
    #Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = request.session['user']
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        print user.email
        return redirect('user.registre')

    return redirect('user.nickname')

#### 2. Nickname
class NicknameForm(forms.Form):
    nickname = forms.CharField(max_length=300)

@csrf_exempt
def nickname(request, **kwargs):

    # User validated
    if 'user' in request.session and request.session['user'] is not None:
        user = User.objects.get(id=request.session['user'].id)
        user.status = 'Nickname'
        user.save()
        request.session['user'] = user
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')

    # Delete nickname in the session
    if 'nickname' in request.session:
        del request.session['nickname']

    if request.method != 'POST':
        return render_to_response('nickname.html', {'lang': request.session['lang'], 'text': request.session['text']},
                                  context_instance=RequestContext(request))
    else:

        form = NicknameForm(request.POST)
        nick = form['nickname'].value()

        if not form.is_valid():
            return render_to_response('nickname.html',
                                      {'lang': request.session['lang'],
                                       'nickname_error': True,
                                       'nickname_error2': False,
                                       'text': request.session['text']},
                                      context_instance=RequestContext(request))

        if not nick or len(nick) == 0:
            return render_to_response('nickname.html',
                                      {'lang': request.session['lang'],
                                       'text': request.session['text']},
                                      context_instance=RequestContext(request))

        if len(nick) > 3:
            return render_to_response('nickname.html',
                                      {'nickname_error': True,
                                       'nickname_error2': False,
                                       'nickname': nick,
                                       'lang': request.session['lang'],
                                       'text': request.session['text']},
                                      context_instance=RequestContext(request))

        try:
            # User Exist
            user = User.objects.get(nickname=nick)
            request.session['user'] = user
            request.session['nickname'] = nick

            if user.consent:
                return redirect('user.story')
            else:
                return redirect('user.avis')

        except ObjectDoesNotExist:
            # User No Exist
            request.session['nickname'] = nick
            user = User()
            user.nickname = request.session['nickname']
            user.save()
            request.session['user'] = user
            return redirect('user.avis')

### Avis legal

class AvisForm(forms.Form):
    check_1 = forms.CharField(max_length=20)

@csrf_exempt
def avis(request, **kwargs):
    # Check valid user in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = User.objects.get(id=request.session['user'].id)
        user.status = 'Avis'
        user.save()
        request.session['user'] = user

        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
    else:
        return redirect('user.nickname')


    if request.method != 'POST':
        return render_to_response('avis.html',  {'lang': request.session['lang'], 'text': request.session['text']},
                              context_instance=RequestContext(request))
    else:
        form = AvisForm(request.POST)
        user = User.objects.get(id=request.session['user'].id)
        request.session['consent'] = True
        user.consent = True
        user.save()
        return redirect('user.story')

#### 3. Story
class storyForm(forms.Form):
    story = forms.CharField(max_length=100)

@csrf_exempt
def story(request, **kwargs):

    # User validated
    if 'user' in request.session and request.session['user'] is not None:
        user = User.objects.get(id=request.session['user'].id)
        user.status = 'Story'
        user.save()
        request.session['user'] = user

        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')

    # Nickname validation
    if 'nickname' not in request.session or request.session['nickname'] is None:
        return redirect('user.nickname')

    # Stories performed
    story_A = 0
    story_B = 0
    story_C = 0
    story_D = 0

    try:
        for s in Story.objects.filter(user_id=request.session['user'].id):
            # Stories ended
            if s.type == 'A' and s.date_ended is not None:
                story_A = 1
            elif s.type == 'B' and s.date_ended is not None:
                story_B = 1
            elif s.type == 'C' and s.date_ended is not None:
                story_C = 1
            elif s.type == 'D' and s.date_ended is not None:
                story_D = 1

    except Story.DoesNotExist:
        print 'Non Stories Performed'

    # All stories performed
    if story_A and story_B and story_C and story_D:
        return redirect('user.final_joc')

    # No Post, stories buttons
    if request.method != 'POST':
        return render_to_response('story.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'user': user,
                                   'story_A': story_A,
                                   'story_B': story_B,
                                   'story_C': story_C,
                                   'story_D': story_D},
                                  context_instance=RequestContext(request))

    form = storyForm(request.POST)
    story_type = form['story'].value()

    if not form.is_valid():
        return render_to_response('story.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'user': user,
                                   'story_A': story_A,
                                   'story_B': story_B,
                                   'story_C': story_C,
                                   'story_D': story_D},
                                  context_instance=RequestContext(request))

    else:

        user = User.objects.get(id=request.session['user'].id)
        request.session['story'] = story_type
        story = Story.objects.filter(user_id=request.session['user'].id).filter(type=request.session['story'])

        if len(story) > 0:
            # Game not assigned
            print 'Stories: '+str(len(story))

            if story[0].game is None:
                return redirect('user.narrative')
            # Game not ended
            elif story[0].game.date_ended is None:
                return redirect('user.registre')
            # Story not ended
            elif story[0].date_ended is None:
                return redirect('user.enquesta1')

        else:
            story = Story()
            story.type = story_type
            story.user = user
            story.save()

        return redirect('user.narrative')

#### 4. Narrative
@csrf_exempt
def narrative(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = User.objects.get(id=request.session['user'].id)
        user.status = 'Narrative'
        user.save()
        request.session['user'] = user

        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')


    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "Error: No nickname"
        return redirect('user.nickname')

    if 'story' not in request.session or request.session['story'] is None:
        print "Error: No story"
        #return redirect('user.story')

    return render_to_response('narrative.html',
                              {'lang': request.session['lang'],
                               'text': request.session['text'],
                               'user': user,
                               'story': request.session['story']},
                              context_instance=RequestContext(request))

#### 5. Registre
@csrf_exempt
def registre(request, **kwargs):

    if 'user' not in request.session or request.session['user'] is None:
        return redirect('user.nickname')

    # Update the user information of the session
    try:
        user = User.objects.get(pk=request.session['user'].id)
        user.status = 'Register'
        user.save()
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    #Mirem que aquest user no hagi acabat ja!!!
    #if user.data_finalitzacio:
    #    return redirect('user.final_joc')

    # User with no game
    if not user.current_game:
        print 'User without game'
        if request.method != 'POST':
            return render_to_response('registre.html',
                                      {'user': user,
                                       'lang': request.session['lang'],
                                       'text': request.session['text'],
                                       'error_partida':False,
                                       'waiting':0},
                                      context_instance=RequestContext(request))

        # Are there some active game?
        partida_activa = Partida.objects.filter(status="REGISTRANT")
        print 'Number of games:'+str(len(partida_activa))
        if len(partida_activa) > 0:

            # Current active game
            partida_activa = partida_activa[0]

            try:
                # Control max. N participants
                print 'Active game with %d users' %(partida_activa.registered)
                if partida_activa.registered < N:
                    partida_activa.registered += 1
                    partida_activa.save()
                    user.current_game = partida_activa
                    user.date_register = timezone.now()
                    user.save()

                    story = Story.objects.filter(user_id = request.session['user']).filter(type = request.session['story'])[0]
                    story.game = partida_activa
                    story.save()

                else:
                   return redirect('user.registre')

                #Si tot ha sortit be, redirigim l'usuari a la pantalla de joc
                return redirect('user.registre')
            except:
                #Si hi ha hagut error tornem a la pagina
                return redirect('user.registre')


        return render_to_response('registre.html',
                                  {'user': user,
                                   'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'error_partida':True,
                                   'waiting':0},
                                  context_instance=RequestContext(request))

    # User with game assigned
    else:
        print 'User with game as'
        if user.current_game and (user.current_game.status == "FINISHED" or user.current_game.status == "FINISHED_MANUAL"):
            return redirect('user.enquesta1')

        if user.current_game and (user.current_game.status == "PLAYING"):
            return redirect('user.public_goods1')

        return render_to_response('registre.html', {'user': user,
                                                    'lang': request.session['lang'],
                                                    'text': request.session['text'],
                                                    'error_partida':False,
                                                    'waiting':1},
                                  context_instance=RequestContext(request))

#### 6. Public Goods
@csrf_exempt
def public_goods1(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        user.status = 'Game'
        user.save()
        request.session['user'] = user

    except Exception as e:
        return redirect('user.nickname')

    #Check if he has played this game
    #ToDo: No comments and go to the next screen
    #if user.partida.status == 'FINISHED' or user.partida.status == 'FINISHED_MANUAL' or user.partida.status == 'PLAYING':
    #    if user_public_goods.selection != "":
    #        return redirect('')

    date_start = user.current_game.date_started+datetime.timedelta(0, TIME_DECISION)
    time = (date_start - timezone.now()).total_seconds()

    return render_to_response('public_goods1.html', {'lang': request.session['lang'],
                                                     'text': request.session['text'],
                                                     'user': request.session['user'],
                                                     'countdown_time': time*1000},
                              context_instance=RequestContext(request))

#### 8. Final Survey I
class SigninForm1(forms.Form):
    gender = forms.CharField(max_length=2)
    age = forms.CharField(max_length=2)
    studies = forms.CharField(max_length=2)
    postal_code = forms.CharField(max_length=10)

@csrf_exempt
def enquesta1(request, **kwargs):

    # User validated in the session
    if 'user' in request.session and request.session['user'] is not None:
        user = User.objects.get(id=request.session['user'].id)
        user.status = 'Survey1'
        user.save()
        request.session['user'] = user
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')

    # Nickname in the session
    if 'nickname' not in request.session or request.session['nickname'] is None:
        return redirect('user.nickname')

    # Survey answered
    if user.date_ended:
        return redirect('user.enquesta2')

    # Post
    if request.method != 'POST':
        return render_to_response('enquesta1.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'user': user},
                                  context_instance=RequestContext(request))

    form = SigninForm1(request.POST)
    gender = form['gender'].value()
    age = form['age'].value()
    postal_code = form['postal_code'].value()
    studies = form['studies'].value()

    if not form.is_valid():
        return render_to_response('enquesta1.html', {
            'gender': gender,
            'gender_danger': gender is None or len(gender) == 0,
            'gender_1_checked': 'bx-option-selected' if gender == 'M' else '',
            'gender_2_checked': 'bx-option-selected' if gender == 'W' else '',
            'gender_3_checked': 'bx-option-selected' if gender == 'NB' else '',
            'gender_4_checked': 'bx-option-selected' if gender == 'NA' else '',

            'age': age,
            'age_danger': age is None or len(age) == 0,
            'age_1_checked': 'bx-option-selected' if age == 'r1' else '',
            'age_2_checked': 'bx-option-selected' if age == 'r2' else '',
            'age_3_checked': 'bx-option-selected' if age == 'r3' else '',
            'age_4_checked': 'bx-option-selected' if age == 'r4' else '',
            'age_5_checked': 'bx-option-selected' if age == 'r5' else '',
            'age_6_checked': 'bx-option-selected' if age == 'r6' else '',
            'age_7_checked': 'bx-option-selected' if age == 'r7' else '',
            'age_8_checked': 'bx-option-selected' if age == 'r8' else '',

            'postal_code': postal_code,
            'postal_code_danger': postal_code is None or len(postal_code) == 0,

            'studies': studies,
            'studies_danger': studies is None or len(studies) == 0,
            'studies_1_checked': 'bx-option-selected' if studies == 'r1' else '',
            'studies_2_checked': 'bx-option-selected' if studies == 'r2' else '',
            'studies_3_checked': 'bx-option-selected' if studies == 'r3' else '',
            'studies_4_checked': 'bx-option-selected' if studies == 'r4' else '',
            'studies_5_checked': 'bx-option-selected' if studies == 'r5' else '',
            'studies_6_checked': 'bx-option-selected' if studies == 'r6' else '',

            'lang': request.session['lang'],
            'text': request.session['text'],
            'user': user,
        }, context_instance=RequestContext(request))

    else:
        request.session['gender'] = gender
        request.session['age'] = age
        request.session['postal_code'] = postal_code
        request.session['studies'] = studies

        user = User.objects.get(id=request.session['user'].id)

        user.gender = request.session['gender']
        user.age = request.session['age']
        user.studies = request.session['studies']
        user.postal_code = request.session['postal_code']

        user.date_ended = timezone.now()
        user.save()

        return redirect('user.enquesta2')

#### 9. Final Survey II
class SigninForm2(forms.Form):
    question1 = forms.CharField(max_length=2)
    question2 = forms.CharField(max_length=2)
    question3 = forms.CharField(max_length=2)

@csrf_exempt
def enquesta2(request, **kwargs):
    # Mirem si l'user ja esta validat a dins la sessio
    if 'user' in request.session and request.session['user'] is not None:
        user = User.objects.get(id=request.session['user'].id)
        user.status = 'Survey2'
        user.save()
        request.session['user'] = user
        if not user_exists_in_db(user):
            del request.session['user']
            return redirect('user.nickname')
        # print user.useremail_set.all()
        # return redirect('user.registre')

    # Ens assegurem que tenim l'email almenys
    if 'nickname' not in request.session or request.session['nickname'] is None:
        print "ERROR!!"
        return redirect('user.nickname')

    # Mirem si ens estan ja retornant dades per validar o hem de mostrar l'enquesta
    if request.method != 'POST':
        return render_to_response('enquesta2.html',
                                  {'lang': request.session['lang'],
                                   'text': request.session['text'],
                                   'user': user},
                                  context_instance=RequestContext(request))

    form = SigninForm2(request.POST)
    question1 = form['question1'].value()
    question2 = form['question2'].value()
    question3 = form['question3'].value()

    print form

    if not form.is_valid():
        return render_to_response('enquesta2.html', {

            'question1': question1,
            'question1_danger': question1 is None or len(question1) == 0,
            'question1_1_checked': 'bx-option-selected' if question1 == 'r1' else '',
            'question1_2_checked': 'bx-option-selected' if question1 == 'r2' else '',
            'question1_3_checked': 'bx-option-selected' if question1 == 'r3' else '',
            'question1_4_checked': 'bx-option-selected' if question1 == 'r4' else '',

            'question2': question2,
            'question2_danger': question2 is None or len(question2) == 0,
            'question2_1_checked': 'bx-option-selected' if question2 == 'r1' else '',
            'question2_2_checked': 'bx-option-selected' if question2 == 'r2' else '',
            'question2_3_checked': 'bx-option-selected' if question2 == 'r3' else '',

            'question3': question3,
            'question3_danger': question3 is None or len(question3) == 0,
            'question3_1_checked': 'bx-option-selected' if question3 == 'r1' else '',
            'question3_2_checked': 'bx-option-selected' if question3 == 'r2' else '',
            'question3_3_checked': 'bx-option-selected' if question3 == 'r3' else '',
            'question3_4_checked': 'bx-option-selected' if question3 == 'r4' else '',

            'lang': request.session['lang'],
            'text': request.session['text'],
            'user': user,
        }, context_instance=RequestContext(request))


    else:
        request.session['question1'] = question1
        request.session['question2'] = question2
        request.session['question3'] = question3

        story = Story.objects.filter(user_id = request.session['user']).filter(type = request.session['story'])[0]

        story.question1 = request.session['question1']
        story.question2 = request.session['question2']
        story.question3 = request.session['question3']
        story.date_ended = timezone.now()
        story.save()

        return redirect('user.final_joc')

#### 10. Final Session
@csrf_exempt
def final_joc(request, **kwargs):
    if 'user' not in request.session or request.session['user'] is None:
        return redirect('index')

    try:
        # Update the user information of the session
        user = User.objects.get(pk=request.session['user'].id)
        user.current_game = None
        user.status = 'End'
        user.save()
        request.session['user'] = user
    except Exception as e:
        return redirect('user.nickname')

    del request.session['user']
    return render_to_response('final_joc.html', {'lang': request.session['lang'],
                                                 'text': request.session['text'],

                                                 },
                              context_instance=RequestContext(request))

#### Logout
@csrf_exempt
def logout(request, **kwargs):
    if 'user' in request.session and request.session['user'] is not None:
        user = User.objects.get(pk=request.session['user'].id)
        user.current_game = None
        user.status = 'Logout'
        user.save()
        del request.session['user']
    return redirect('index')

