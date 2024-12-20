import os
import sys
import logging
from azure.data.tables import TableServiceClient, TableEntity

table_name = "people"

class TableActions:

    def __init__(self):
        #Make sure the connection string is available
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if self.connection_string is None:
            logging.error("Missing envarionment variable AZURE_STORAGE_CONNECTION_STRING.")
            sys.exit(1)

        self.table_client = self.create_table_client()
    #Table creation (not necessary)
    def create_table_client(self):
        table_service_client = TableServiceClient.from_connection_string(conn_str=self.connection_string)
        table_client = table_service_client.get_table_client(table_name)
        try:
            table_client.create_table()
        except Exception as e:
            logging.info(f"Table '{table_name}' is already exists. {str(e)}")
        return table_client

    def insert_person(self, person_data):
        # Verify if the keys are valid
        allowed_keys = ['id', 'name', 'lastname', 'mail', 'password', 'age','gender', 'phone', 'photo_data']
        invalid_keys = [key for key in person_data if key not in allowed_keys]
        if invalid_keys:
            raise ValueError("Invalid parameters")
        # Verify if the required keys are present
        if "mail" not in person_data:
            raise ValueError("mail must be provided")
        if "password" not in person_data:
            raise ValueError("password must be provided")
        
        entity = TableEntity()
        entity["PartitionKey"] = "peoplePartition"
        entity["RowKey"] = str(person_data["mail"])  # Use the email as the RowKey
        entity.update(person_data)  # Add the rest of the data to the entity
        self.table_client.create_entity(entity=entity) # Insert the entity into the table
        return {"success": "Person inserted"}

    def get_person_by_id(self, person_mail):
        try:
            entity = self.table_client.get_entity(partition_key="peoplePartition", row_key=str(person_mail))
            return {"password":entity["password"]}
        except Exception as e:
            logging.error(f"No se pudo recuperar la entidad con id {person_mail}: {str(e)}")
            return None
import os
import sys
import logging
from azure.data.tables import TableServiceClient, TableEntity

table_name = "people"

class TableActions:

    def __init__(self):
        # Make sure the connection string is available
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if self.connection_string is None:
            logging.error("Missing environment variable AZURE_STORAGE_CONNECTION_STRING.")
            sys.exit(1)

        self.table_client = self.create_table_client()

    # Table creation (not necessary)
    def create_table_client(self):
        table_service_client = TableServiceClient.from_connection_string(conn_str=self.connection_string)
        table_client = table_service_client.get_table_client(table_name)
        try:
            table_client.create_table()
        except Exception as e:
            logging.info(f"Table '{table_name}' already exists. {str(e)}")
        return table_client

    def insert_person(self, person_data):
        # Verify if the keys are valid
        allowed_keys = ['id', 'name', 'lastname', 'mail', 'password', 'age', 'gender', 'phone', 'photo_data']
        invalid_keys = [key for key in person_data if key not in allowed_keys]
        if invalid_keys:
            raise ValueError("Invalid parameters")
        # Verify if the required keys are present
        if "mail" not in person_data:
            raise ValueError("mail must be provided")
        if "password" not in person_data:
            raise ValueError("password must be provided")
        
        entity = TableEntity()
        entity["PartitionKey"] = "peoplePartition"
        entity["RowKey"] = str(person_data["mail"])  # Use the email as the RowKey
        entity.update(person_data)  # Add the rest of the data to the entity
        self.table_client.create_entity(entity=entity)  # Insert the entity into the table
        return {"success": "Person inserted"}

    def get_person_by_id(self, person_mail):
        try:
            entity = self.table_client.get_entity(partition_key="peoplePartition", row_key=str(person_mail))
            return {"password": entity["password"]}
        except Exception as e:
            logging.error(f"No se pudo recuperar la entidad con id {person_mail}: {str(e)}")
            return None

    def change_password(self, person_mail, new_password):
        try:
            # Get the entity with the provided mail
            entity = self.table_client.get_entity(partition_key="peoplePartition", row_key=str(person_mail))
            
            # Update the password
            entity["password"] = new_password
            
            # Replace the entity in the table
            self.table_client.update_entity(entity=entity)
            
            return {"success": "Password updated successfully"}
        
        except Exception as e:
            logging.error(f"No se pudo actualizar la contraseña para {person_mail}: {str(e)}")
            return None

