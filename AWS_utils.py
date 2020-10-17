import boto3

class StorageWizard():
    def __init__(self):
        #
        self.s3_resource = boto3.resource('s3')
        self.s3_client = boto3.client("s3")
        self.bucket = self.s3_resource.Bucket('select-equity-crawled-resources')
    def print_all_files(self):
        objects = self.s3_client.list_objects(Bucket=self.bucket.name)["Contents"]
        for object in objects:
            print(object["Key"])
    def store(self, folder_destination, file_name, override_protection=True):
        # usage example:
        # StorageWizard.store("CNN news/", "test_file22.txt") will store local file test_file22.txt to the CNN news folder on S3
        # overriding pretection
        if override_protection:
            objects = self.s3_client.list_objects(Bucket=self.bucket.name)["Contents"]
            print(objects)
            for o in objects:
                if o["Key"] == file_name:
                    print("This file already exist, if you wish to override it, set the token to False then run again")
                    return -1
        file = open(file_name, "rb")
        self.bucket.put_object(Key=folder_destination + file_name, Body=file)
        return 0
    def load(self, file_key, file_destination):
        # usage example:
        # StorageWizard.load("CNN news/test_file22.txt", "./test2.txt") will store local file test_file22.txt to the CNN news folder on S3
        with open(file_destination, 'wb') as data:
            self.bucket.download_fileobj(file_key, data)

if __name__ == "__main__":
    wiz = StorageWizard()
    wiz.store("/", "APIs/data/covid_new_keyword.csv")
