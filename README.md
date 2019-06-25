# README #

## CitizenSocialLab: consCIENCIES ##

Experiment designed and implemented to be performed in [Biennal Ciutat i Ciència](https://www.biennalciutaticiencia.barcelona/en/awareness-market-place) and the citizen science festival [Calidoscopi](https://ajuntament.barcelona.cat/santandreu/es/conozca-el-distrito/calidoscopi-cultural/noticias/consciencies-a-la-placa-et-necessita-pel-seu-experiment_799233).

This participatory experiment consist on a set of dilemmas that study how we behave in front of a situation of gender-based violence in public spaces. Natalia, Alex, Raquel and Sandra tell us situations lived in public spaces and participants have to decide to what extent do they intervene to alleviate the situation.

This experiment is performed in groups of 6 participants. 

## Data ##
**Not available**  

## Derived Scientific Publications ##
**Not available**  

## Configuration ##
Steps are necessary to get consCIENCIES install, up and running in local network.

### Creation of the project ###

__Database MySQL__  
Create MySQL database: name\_db  
Create user database: user\_db  
Create password database: pass\_db

Introduce this information about the database in: `/consCIENCIES/settings.py`

__Environment__   
```mkvirtualenv consciencies ```  

__Requirements__  
```pip install -r requirements.txt```

__MongoDB__  
```mongod --dbpath /.../consCIENCIES/ddbb```

__Load text__   
File with text and translations:  `/.../consCIENCIES/game/i18n/translations.xlsx`  
   
```python excel_to_mongodb.py```

__Run Server__  
```python manage.py runserver localhost:port```

__Migrations__  
```python manage.py makemigrations```  
```python manage.py migrate```  

### Run project in Local ###

__Step 1: Run MySQL server__  
Run MySQL: `mysql.server start`

__Step 2: Open terminal tabs and work on the environment__  

in Tab 1: MongoDB  
in Tab 2: MySQL  
in Tab 3: Run Application  

Work on environment (in each terminal tab): `workon consciencies`

__Step 3: Run MongoDB (Tab 1)__  
Run mongodb: `mongod --dbpath /.../consCIENCIES/ddbb`

__Step 4: MySQL actions (Tab 2)__

Directory: `cd /.../consCIENCIES/`   
Database: `mysql -u user_db -p (pass_db)`

Drop database: `drop database name\_db;`  
Create database: `create database name\_db;`  
Exit: `exit;`

Modificate fields of database: `python manage.py makemigrations`  
Refresh database:
`python manage.py migrate` 

__Step 5: Load texts (Tab 2)__    
Load translations: `python excel_to_mongodb.py`

__Step 6: Run Server (Tab 3)__  
Directory: `cd /.../consCIENCIES/ `   
Runserver: `python manage.py runserver localhost:port`

### Access client ###
Client application:  
**http://localhost:port/**  
 
Control and Administration:  
**http://localhost:port/admin**
## Versions ##
Version 1.0

## License ##
CitizenSocialLab | consCIENCIES (c) by Julian Vicens

CitizenSocialLab | consCIENCIES is licensed under a
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

You should have received a copy of the license along with this work. If not, see [CC BY-NC-SA license](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Contributors ##

[Julián Vicens](https://github.com/jvicens)

## Contact ##

Julian Vicens: **julianvicens@gmail.com**
