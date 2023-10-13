import mysql.connector
import json
from datetime import datetime

class DockerDataProcessor:
    def __init__(self, json_file, db_host, db_user, db_password, db_name):
        self.json_file = json_file
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def is_valid_json(self, data):
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    def load_json_data(self):
        with open(self.json_file, 'r') as file:
            data = file.read()
        return data

    def process_data(self):
        data = self.load_json_data()

        print(data)
        if self.is_valid_json(data):
            data = json.loads(data)

            connection = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            cursor = connection.cursor()

            delete_images_sql = "DELETE FROM images"
            cursor.execute(delete_images_sql)

            delete_containers_sql = "DELETE FROM containers"
            cursor.execute(delete_containers_sql)

            reset_auto_increment_sql = "ALTER TABLE images AUTO_INCREMENT = 1;"
            cursor.execute(reset_auto_increment_sql)

            reset_containers_sql = "ALTER TABLE containers AUTO_INCREMENT = 1;"
            cursor.execute(reset_containers_sql)

            connection.commit()

            for image in data["Docker Images"]:
                sql = "INSERT INTO images (ID_image, Repository, Tag, Size) VALUES (%s, %s, %s, %s)"
                values = (image["ID_image"], image["Repository"], image["Tag"], image["Size"])
                cursor.execute(sql, values)
                connection.commit()

            for container in data["Docker Containers"]:
                created_date = datetime.strptime(container["Created"], "%Y-%m-%d %H:%M:%S %z %Z")
                created_date_str = created_date.strftime("%Y-%m-%d %H:%M:%S")

                sql = "INSERT INTO containers (ID_container, ID_img, Created, Status) VALUES (%s, %s, %s, %s)"
                values = (container["ID_container"], container["ID_img"], created_date_str, container["Status"])

                cursor.execute(sql, values)
                connection.commit()

            connection.close()
        else:
            print("File docker_info.json is incorrect")

#def remove_extra_commas(json_str):
#    json_str = json_str.replace(",]", "]")
#    json_str = json_str.replace(",}", "}")
#    return json_str

# Użycie klasy DockerDataProcessor
processor = DockerDataProcessor(
    json_file='docker_info.json',
    db_host='localhost',
    db_user='root',
    db_password='SilneHaslo123',
    db_name='docker_info'
)
processor.process_data()
