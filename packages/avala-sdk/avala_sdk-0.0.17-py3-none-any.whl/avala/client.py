import requests
import json

class APIClient:
    def __init__(self, valid_config):
        self.config = valid_config
        self.api_url = valid_config['API']['api_url']
        self.api_key = valid_config['API']['api_key']
        self.provider_config = valid_config['ProviderConfig']['provider_config']
        self.organization_config = valid_config['Organization']['organization_config']

        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-AVALA-API-KEY': self.api_key,
        }


    def is_valid_id(self, input_id, json_data):
        """
        Validate if the input_id is a valid "id" within the given JSON data.
        """
        if not isinstance(input_id, int):
            return False

        for item in json_data.get('results', []):
            if item.get('id') == input_id:
                return True

        return False

    def make_get_request(self, api_url):
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200 or response.status_code == 201:
            return response.json()

        return None


    def import_dataset(self, args):
        api_url = self.api_url + '/datasets/'
        dataset_info = {
            'name': args.name,
            'slug': args.slug,
            'visibility': args.visibility,
            'industry': args.industry,
            'license': args.license,
            'citation': args.citation,
            'creator': args.creator,
            'description': args.description
        }

        dataset_info.update({'provider_config': self.provider_config})
        print(dataset_info)

        response = requests.post(api_url, headers=self.headers,
                                 data=json.dumps(dataset_info))

        if response.status_code == 201:
            print("Successfully created dataset")
        else:
            print(f"Failed to create dataset. Status code: {response.status_code}")
            return None

    def import_annotations(self, args):
        owner_name = args.owner
        slug = args.slug

        api_url = self.api_url + f'/datasets/{owner_name}/{slug}/upload-existing-annotations'

        json_file = args.annotations_file
        try:
            with open(json_file, 'r') as file:
                annotations_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: '{json_file}' file not found")
            return
        except json.JSONDecodeError:
            print(f"Error: '{json_file}' does not contain valid JSON data")
            return

        # Note: At this time, only 'Coco' format is supported for ingesting
        # annotations.

        annotations = {
            'dataset_uid': args.dataset_uid,
            'annotation_source_format': 'Coco',
            'project_name': args.project_name,
            'annotations_data': annotations_data,
            'keep_annotations': args.keep_annotations,
        }

        response = requests.post(api_url, headers=self.headers,
                                 data=json.dumps(annotations))

        if response.status_code == 202:
            print("Successfully accepted addition of annotations to new project linked to dataset")
        else:
            print(f"Failed to accept addition of annotations for new project linked to dataset. Status code: {response.status_code}")
            return None

    def get_exports(self):
        api_url = self.api_url + '/exports/'
        data = self.make_get_request(api_url)
        return json.dumps(data, indent=4)

    def get_industries(self):
        api_url = self.api_url + '/project-config/industries/'
        return self.make_get_request(api_url)

    def get_licenses(self):
        api_url = self.api_url + '/licenses/'
        return self.make_get_request(api_url)

    def get_projects(self):
        api_url = self.api_url + '/users/me/projects/'
        return self.make_get_request(api_url)

    def get_datasets(self):
        api_url = self.api_url + '/datasets/'
        return self.make_get_request(api_url)

    def show(self, response):
        if response is None or ('results' not in response) or len(response['results']) == 0:
            print("{}")
            return

        test_element = response['results'][0]
        if 'id' in test_element:
            field = 'id'
        elif 'uid' in test_element:
            field = 'uid'
        else:
            field = None

        state = 0

        if field is None:
            output = response['results']
        else:
            output = sorted(response['results'], key=lambda z: z[field])

        for idx, item in enumerate(output):
            if state == 0:
                print("{")
                state = 1
            if idx == len(response['results'])-1:
                print('  "%s": "%s"' % (item[field], item['name']))
            else:
                print('  "%s": "%s",' % (item[field], item['name']))

        if state == 1:
            print("}")




