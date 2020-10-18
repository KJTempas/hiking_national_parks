import osimport requestsimport loggingfrom dotenv import load_dotenvimport reload_dotenv('application/.env')NTL_PARK_KEY = os.environ.get('NATLPARKS_KEY')API_URL = 'https://developer.nps.gov/api/v1/parks'# Loggerlogging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%y %H:%M:%S')log = logging.getLogger('root')def get_response(state):    try:        query = {'stateCode': state, 'api_key': NTL_PARK_KEY}        response = requests.get(API_URL, params=query)        response.raise_for_status()  # will raise an exception for 400(client) or 500(server) errors        data = response.json()        park_list = get_info(data)        return park_list    except Exception as ex:        log.exception(ex)        raise exdef get_info(data):    try:        park_list = list()        list_of_parks = data['data']        for park in list_of_parks:            park_list_w_info = dict()            if park['fullName'] and park['latitude'] and park['longitude'] and park['designation']:                modified_name = " ".join(re.findall("[a-zA-Z]+", park['fullName']))                park_list_w_info['name'] = modified_name                park_list_w_info['lat'] = park['latitude']                park_list_w_info['lon'] = park['longitude']                park_list_w_info['designation']= park['designation']                park_list.append(park_list_w_info)        return park_list    except Exception as e:        log.exception(e)        raise e