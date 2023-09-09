import os
from typing import Optional

from dotenv import load_dotenv
from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.sk_pydantic import PydanticField
from semantic_kernel.skill_definition import sk_function
import snowflake.connector as sf

load_dotenv()

sf_user = os.getenv("sf_user")
sf_pass = os.getenv("sf_pass")
sf_account = os.getenv("sf_account")


class SnowflakeOperations(PydanticField):
    def get_connection(self):
        connection = sf.connect(user=sf_user, password=sf_pass, account=sf_account)
        return connection

    @sk_function(description="Executes a SQL Query", name="execute_query")
    def execute_query(self, context: SKContext) -> str:
        input = context["input"]
        connection = self.get_connection()

        print(input)
        try:
            cursor = connection.cursor()
            cursor.execute('use {dbname}'.format(dbname="CUSTOMER_DB"))
            cursor.execute('use schema {schemaname}'.format(schemaname="CUSTOMER_SCHEMA"))
            results = cursor.execute(input)
            queryid = cursor.sfqid

            return str(results.fetchall())
        except Exception as e:
            print(e)
            print('failed')
