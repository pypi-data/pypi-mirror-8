from errors import BAD_UNIVERSE_NAME, BAD_DEFENSE_ID, NOT_LOGGED
import constants
from bs4 import BeautifulSoup

import requests
import json
import time


class pyogame(object):
    def __init__(self, universe, username, password, domain='ogame.org'):
        self.session = requests.session()
        self.session.headers['User-Agent'] = '''
            Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'''

        self.server_url = universe
        self.username = username
        self.password = password
        self.login()


    def login(self):
        """Get the ogame session token."""
        payload = {'kid': '',
                   'uni': self.server_url,
                   'login': self.username,
                   'pass': self.password}
        res = self.session.post('http://us.ogame.gameforge.com/main/login', data=payload).content
        soup = BeautifulSoup(res)
        self.ogame_session = soup.find('meta', {'name': 'ogame-session'}) \
                                 .get('content')
        if not self.is_logged():
            print( 'didn\'t login' )


    def logout(self):
        self.session.get(self.get_url('logout'))


    def is_logged(self):
        res = self.session.get(self.get_url('overview')).content
        soup = BeautifulSoup(res)
        session = soup.find('meta', {'name': 'ogame-session'})
        return session is not None


    def get_page_content(self, page='overview'):
        """Return the html of a specific page."""
        return self.session.get(self.get_url(page)).content


    def fetch_eventbox(self):
        res = self.session.get(self.get_url('fetchEventbox')).content
        try:
            obj = json.loads(res)
        except ValueError, e:
            raise NOT_LOGGED
        return obj


    def fetch_resources(self, planet_id):
        url = self.get_url('fetchResources', planet_id)
        res = self.session.get(url).content
        try:
            obj = json.loads(res)
        except ValueError, e:
            raise NOT_LOGGED
        return obj


    def get_resources(self, planet_id):
        """Returns the planet resources stats."""
        resources = self.fetch_resources(planet_id)
        metal = resources['metal']['resources']['actual']
        crystal = resources['crystal']['resources']['actual']
        deuterium = resources['deuterium']['resources']['actual']
        energy = resources['energy']['resources']['actual']
        darkmatter = resources['darkmatter']['resources']['actual']
        result = {'metal': metal, 'crystal': crystal, 'deuterium': deuterium,
                  'energy': energy, 'darkmatter': darkmatter}
        return result


    def get_ships(self, planet_id):
        def get_nbr(soup, name):
            div = soup.find('div', {'class': name})
            level = div.find('span', {'class': 'level'})
            for tag in level.findAll(True):
                tag.extract()
            return int(level.text.strip())

        res = self.session.get(self.get_url('shipyard')).content
        soup = BeautifulSoup(res)

        lightFighter = get_nbr(soup, 'military204')
        heavyFighter = get_nbr(soup, 'military205')
        cruiser = get_nbr(soup, 'military206')
        battleship = get_nbr(soup, 'military207')
        battlecruiser = get_nbr(soup, 'military215')
        bomber = get_nbr(soup, 'military211')
        destroyer = get_nbr(soup, 'military213')
        deathstar = get_nbr(soup, 'military214')
        smallCargo = get_nbr(soup, 'civil202')
        largeCargo = get_nbr(soup, 'civil203')
        colonyShip = get_nbr(soup, 'civil208')
        recycler = get_nbr(soup, 'civil209')
        espionageProbe = get_nbr(soup, 'civil210')
        solarSatellite = get_nbr(soup, 'civil212')

        return {'LightFighter': lightFighter,
                'HeavyFighter': heavyFighter,
                'Cruiser': cruiser,
                'Battleship': battleship,
                'Battlecruiser': battlecruiser,
                'Bomber': bomber,
                'Destroyer': destroyer,
                'Deathstar': deathstar,
                'SmallCargo': smallCargo,
                'LargeCargo': largeCargo,
                'ColonyShip': colonyShip,
                'Recycler': recycler,
                'EspionageProbe': espionageProbe,
                'SolarSatellite': solarSatellite}


    def is_under_attack(self):
        json = self.fetch_eventbox()
        return not json.get('hostile', 0) == 0


    def get_planet_ids(self):
        """Get the ids of your planets."""
        res = self.session.get(self.get_url('overview')).content
        soup = BeautifulSoup(res)
        planets = soup.findAll('div', {'class': 'smallplanet'})
        ids = [planet['id'].replace('planet-', '') for planet in planets]
        return ids


    def get_planet_by_name(self, planet_name):
        """Returns the first planet id with the specified name."""
        res = self.session.get(self.get_url('overview')).content
        soup = BeautifulSoup(res)
        planets = soup.findAll('div', {'class': 'smallplanet'})
        for planet in planets:
            name = planet.find('span', {'class': 'planet-name'}).string
            if name == planet_name:
                return planet.get('id').replace('planet-', '')
        return None


    def build_defense(self, planet_id, defense_id, nbr):
        """Build a defense unit."""
        if defense_id not in constants.Defense.values():
            raise BAD_DEFENSE_ID

        url = self.get_url('defense', planet_id)

        res = self.session.get(url).content
        soup = BeautifulSoup(res)
        form = soup.find('form')
        token = form.find('input', {'name': 'token'}).get('value')

        payload = {'menge': nbr,
                   'modus': 1,
                   'token': token,
                   'type': defense_id}
        self.session.post(url, data=payload)


    def build_ships(self, planet_id, ship_id, nbr):
        """Build a ship unit."""
        if ship_id not in constants.Ships.values():
            raise BAD_SHIP_ID

        url = self.get_url('shipyard', planet_id)

        res = self.session.get(url).content
        soup = BeautifulSoup(res)
        form = soup.find('form')
        token = form.find('input', {'name': 'token'}).get('value')

        payload = {'menge': nbr,
                   'modus': 1,
                   'token': token,
                   'type': ship_id}
        self.session.post(url, data=payload)


    def build_building(self, planet_id, building_id):
        """Build a ship unit."""
        if building_id not in constants.Buildings.values():
            raise BAD_BUILDING_ID

        url = self.get_url('resources', planet_id)

        res = self.session.get(url).content
        soup = BeautifulSoup(res)
        form = soup.find('form')
        token = form.find('input', {'name': 'token'}).get('value')

        payload = {'modus': 1,
                   'token': token,
                   'type': building_id}
        self.session.post(url, data=payload)


    def build_technology(self, planet_id, technology_id):
        if technology_id not in constants.Research.values():
            raise BAD_RESEARCH_ID

        url = self.get_url('research', planet_id)

        payload = {'modus': 1,
                   'type': technology_id}
        self.session.post(url, data=payload)


    def _build(self, planet_id, object_id, nbr=None):
        if object_id in constants.Buildings.values():
            self.build_building(planet_id, object_id)
        elif object_id in constants.Research.values():
            self.build_technology(planet_id, object_id)
        elif object_id in constants.Ships.values():
            self.build_ships(planet_id, object_id, nbr)
        elif object_id in constants.Defense.values():
            self.build_defense(planet_id, object_id, nbr)
        else:
            print( 'bad id' )


    def build(self, planet_id, arg):
        planet_id = self.id_check( planet_id )

        if isinstance(arg, list):
            for el in arg:
                self.build(planet_id, el)
        elif isinstance(arg, tuple):
            elem_id, nbr = arg
            self._build(planet_id, elem_id, nbr)
        else:
            elem_id = arg
            self._build(planet_id, elem_id)


    def send_fleet(self, planet_id, ships, speed, where, mission, resources):

        def get_hidden_fields(html):
            soup = BeautifulSoup(html)
            inputs = soup.findAll('input', {'type': 'hidden'})
            fields = {}
            for input in inputs:
                name = input.get('name')
                value = input.get('value')
                fields[name] = value
            return fields

        url = self.get_url('fleet1', planet_id)

        res = self.session.get(url).content
        payload= {}
        payload.update(get_hidden_fields(res))
        for name, value in ships:
            payload['am%s' % name] = value
        res = self.session.post(self.get_url('fleet2'), data=payload).content

        payload= {}
        payload.update(get_hidden_fields(res))
        payload.update({'speed': speed,
                        'galaxy': where.get('galaxy'),
                        'system': where.get('system'),
                        'position': where.get('position')})
        res = self.session.post(self.get_url('fleet3'), data=payload).content

        payload= {}
        payload.update(get_hidden_fields(res))
        payload.update({'crystal': resources.get('crystal'),
                        'deuterium': resources.get('deuterium'),
                        'metal': resources.get('metal'),
                        'mission': mission})
        res = self.session.post(self.get_url('movement'), data=payload).content
        # TODO: Should return the fleet ID.


    def cancel_fleet(self, fleet_id):
        self.session.get(self.get_url('movement') + '&return=%s' % fleet_id)


    def get_fleet_ids(self):
        """Return the reversable fleet ids."""
        res = self.session.get(self.get_url('movement')).content
        soup = BeautifulSoup(res)
        spans = soup.findAll('span', {'class': 'reversal'})
        fleet_ids = [span.get('ref') for span in spans]
        return fleet_ids


    def get_url(self, page, planet_id=None):
        if page == 'login':
            return 'http://%s/game/reg/login2.php' % self.server_url
        else:
            url = 'http://%s/game/index.php?page=%s' % (self.server_url, page)
            if planet_id:
                url += '&cp=%s' % planet_id
            return url


    def get_servers(self, domain):
        res = self.session.get('http://%s' % domain).content
        soup = BeautifulSoup(res)
        select = soup.find('select', {'id': 'serverLogin'})
        servers = {}
        for opt in select.findAll('option'):
            url = opt.get('value')
            name = opt.string.strip().lower()
            servers[name] = url
        return servers


    def get_universe_url(self, universe, servers):
        """Get a universe name and return the server url."""
        universe = universe.lower()
        if universe not in servers:
            raise BAD_UNIVERSE_NAME
        return servers[universe]

    def id_check( self, id ):
        if id not in self.get_planet_ids():
            return self.get_planet_by_name( id )
        return id

    def view_system( self, planet_id, system ):
        planet_id = self.id_check( planet_id )
        payload = {
            'galaxy': system['galaxy'],
            'system': system['system']
        }

        url = self.get_url('galaxy') + 'Content&ajax=1'
        return self.session.post( url, payload ).content

    def view_messages( self, page ):
        payload = {
            'displayCategory': '10',
            'displayPage': page,
            'siteType': '101',
            'ajax': '1'
        }

        res = self.session.post( self.get_url('messages'), data=payload ).content
        soup = BeautifulSoup(res)
        res = self.session.get(soup.find('a').get('href'    )).content
        soup = BeautifulSoup(res)
        tag = soup.find('div', {'class':'note'})
        return tag.get_text().strip()






