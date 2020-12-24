import requests;
import json;
import os;
import sys;

'''Clase rest api '''
class Service(object):
	def get(self, url, args={}):
		response = requests.get(url, params=args)
		if response.status_code == 200:
			return json.loads(response.text)
		return False

class Solucion(Service):
	url =  'https://pokeapi.co/api/v2/';

	def primero(self):
		args = {'limit' : 1118}
		response_json = self.get(self.url + 'pokemon', args)
		if response_json != False:
			pokemons = response_json['results']
			valor = 0;
			for pokemon in pokemons:
				name = pokemon['name'];
				if(name.count('a') == 2):
					if(name.count('at') > 0):
						valor = valor + 1
			return valor
		return 'error'

	def segundo(self):
		res_egg_ground = self.get(self.url + 'egg-group/5')
		res_egg_fairy = self.get(self.url + 'egg-group/6')

		if res_egg_fairy != False and res_egg_ground != False:
			''' Recorrer el listado de especies del egg-group: fairy y ground, se agrega las especies no repetidas '''
			''' para posteriormente usar len para obtener el numero de especies con las que puede procrear raichu'''
			
			list_species = []
			for specie in res_egg_ground['pokemon_species']:
				if specie['name'] not in list_species:
					list_species.append(specie['name'])

			for specie in res_egg_fairy['pokemon_species']:
				if specie['name'] not in list_species:
					list_species.append(specie['name'])
			
			return len(list_species)
		return 'error' 

	def tercero(self):
		response_generation = self.get(self.url + 'generation/1')
		response_type = self.get(self.url + 'type/2')

		if response_generation != False and response_type != False:
			'''Obtiene el listado de pokemos por generation primera y type fighting  '''
			pokemon_generation = response_generation['pokemon_species']
			pokemon_type = response_type['pokemon']

			'* Recorrer el listado de type y generation para obtener el id mediante la url*'
			'* agrega a ids en listado type y generation*'
			list_type = []
			for pokemon in pokemon_type:
				aux = pokemon['pokemon']['url'].split('/')
				poke_ids = int(aux[len(aux) - 2])
				if poke_ids <= 151:
					list_type.append(poke_ids)
			
			list_generation = []
			for pokemon in pokemon_generation:
				aux = pokemon['url'].split('/')
				poke_id = int(aux[len(aux)-2])
				if poke_id <= 151:
					list_generation.append(poke_id)
			
			'* Verifica id que coincidan en listado de generation y type, si encuentra coincidencia obtiene el pokemon*'
			'* con solucitad a la api, agrega a una lista el peso y finalmente obtiene el dato mayor y menor de la lista*'
			list_resp = []
			for value in list_type:
				if value in list_generation:
					pokemons = self.get(self.url + 'pokemon/' + str(value))
					if pokemons != False:
						list_resp.append(pokemons['weight'])
			return [max(list_resp), min(list_resp)]
		return 'error'

def menu():
	solucion = Solucion();

	os.system('cls')
	print('************ Solucion Poke-Preguntas ************\n')
	print('1- Obtén cuantos pokemones poseen en sus nombres “at” y tienen 2 “a” en su nombre, incluyendo la primera del “at”')
	print('2- ¿Con cuántas especies de pokémon puede procrear raichu?')
	print('3- Entrega el máximo y mínimo peso de los pokémon de tipo fighting de primera generación')
	print('4- Salir')
	option = input('\nSelecciona una poke-pregunta: ')
	if option == "1":
		print('Respuesta 1: ', solucion.primero(), ' pokemons')
		input('\n\nPresiona enter para continuar')
		menu()
	elif option == "2":
		print('Respuesta 2: ', solucion.segundo(), ' especies')
		input('\n\nPresiona enter para continuar')
		menu()
	elif option == "3":
		print('Respuesta 3: ', solucion.tercero())
		input('\n\nPresiona enter para continuar')
		menu()
	elif option == "4":
		print('Adios')
		sys.exit();
	else:
		print('Opcion incorrecta	')
		input('\n\nPresiona enter para continuar')
		menu()

if __name__ == '__main__':
	menu()
