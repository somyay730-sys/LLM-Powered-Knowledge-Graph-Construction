class GraphQueries:

    def __init__(self, db):
        self.db = db

    def get_ceos(self):
        query = """
        MATCH (person)-[:CEO_OF]->(company)
        RETURN person.name AS CEO,
               company.name AS Company
        """

        with self.db.driver.session() as session:
            result = session.run(query)

            return [
                record.data()
                for record in result
            ]

    def get_products_by_company(self, company_name):
        query = """
        MATCH (company)-[:DEVELOPED]->(product)
        WHERE company.name = $company_name
        RETURN product.name AS Product
        """

        with self.db.driver.session() as session:
            result = session.run(
                query,
                company_name=company_name
            )

            return [
                record.data()
                for record in result
            ]

    def get_company_for_product(self, product_name):
        query = """
        MATCH (company)-[:DEVELOPED]->(product)
        WHERE product.name = $product_name
        RETURN company.name AS Company
        """

        with self.db.driver.session() as session:
            result = session.run(
                query,
                product_name=product_name
            )

            return [
                record.data()
                for record in result
            ]