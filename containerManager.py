import mysql.connector
import docker

class ContainerManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.docker_client = docker.from_env()

    def create_container_from_db(self):
        try:
            db_connection = mysql.connector.connect(**self.db_config)
            cursor = db_connection.cursor()

            # Query the database to get image_name and image_version
            cursor.execute("SELECT image_name, image_version FROM pull")
            results = cursor.fetchall()

            for result in results:
                image_name, image_version = result
                full_image_name = f"{image_name}:{image_version}"
                log_message = None

                try:
                    self.docker_client.images.pull(full_image_name)
                    container = self.docker_client.containers.run(full_image_name, detach=True)
                    container_id = container.id
                    log_message = f"Container created from image: {full_image_name}, Container ID: {container_id}"

                except Exception as error:
                    log_message = f"Error while creating a container from image: {full_image_name}, {str(error)}"

                self._save_log(log_message)

        except mysql.connector.Error as error:
            print(f"Database connection error: {error}")
        finally:
            cursor.close()
            db_connection.close()

    def _save_log(self, log_message):
        try:
            db_connection = mysql.connector.connect(**self.db_config)
            cursor = db_connection.cursor()

            cursor.execute("INSERT INTO create_logs (log) VALUES (%s)", (log_message,))
            db_connection.commit()
        except mysql.connector.Error as error:
            print(f"Database connection error: {error}")
        finally:
            cursor.close()
            db_connection.close()

if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "SilneHaslo123",
        "database": "docker_info"
    }

    manager = ContainerManager(db_config)
    manager.create_container_from_db()

