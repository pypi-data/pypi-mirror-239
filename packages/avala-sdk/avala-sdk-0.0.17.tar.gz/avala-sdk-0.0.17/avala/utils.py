import json
import os
import configparser

class ConfigValidator:
    def __init__(self):
        try:
            curdir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(curdir, 'config.json')
            with open(config_file, "r") as json_file:
                self.config = json.load(json_file)
        except FileNotFoundError:
            self.config = None
        except json.JSONDecodeError:
            self.config = None

    def validate_api_section(self):
        if 'API' not in self.config:
            return False
        required_fields = ['api_key', 'api_url']
        for field in required_fields:
            if field not in self.config['API']:
                return False
        return True

    def validate_provider_config(self):
        if 'ProviderConfig' not in self.config:
            return False
        pc = self.config['ProviderConfig']['provider_config']
        if pc['provider'] == 'aws_s3':
            required_fields = ['s3_bucket_name', 's3_bucket_region', 's3_bucket_prefix', 's3_access_key_id', 's3_secret_access_key']
        elif pc['provider'] == 'gcs':
            required_fields = ['gc_storage_bucket_name', 'gc_storage_prefix', 'gc_storage_auth_json_content']
        else:
            return False
        for field in required_fields:
            if field not in pc:
                return False
        return True

    def validate_config(self):
        if self.config is None:
            return False
        if not self.validate_api_section():
            return False
        if not self.validate_provider_config():
            return False
        return True

    def get_config(self):
        return self.config
