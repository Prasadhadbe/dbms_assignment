from neo4j import GraphDatabase

class Neo4jCRUD:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_person(self, name, age):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_return_person, name, age)
            return result

    @staticmethod
    def _create_and_return_person(tx, name, age):
        query = (
            "CREATE (p:Person {name: $name, age: $age}) "
            "RETURN p"
        )
        result = tx.run(query, name=name, age=age)
        return result.single()[0]

    def get_person(self, name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, name)
            return result

    @staticmethod
    def _find_and_return_person(tx, name):
        query = (
            "MATCH (p:Person {name: $name}) "
            "RETURN p"
        )
        result = tx.run(query, name=name)
        return result.single()[0]

    def update_person(self, name, age):
        with self.driver.session() as session:
            result = session.write_transaction(self._update_and_return_person, name, age)
            return result

    @staticmethod
    def _update_and_return_person(tx, name, age):
        query = (
            "MATCH (p:Person {name: $name}) "
            "SET p.age = $age "
            "RETURN p"
        )
        result = tx.run(query, name=name, age=age)
        return result.single()[0]

    def delete_person(self, name):
        with self.driver.session() as session:
            result = session.write_transaction(self._delete_and_return_person, name)
            return result

    @staticmethod
    def _delete_and_return_person(tx, name):
        query = (
            "MATCH (p:Person {name: $name}) "
            "DELETE p "
            "RETURN 'Person deleted'"
        )
        result = tx.run(query, name=name)
        return result.single()[0]
