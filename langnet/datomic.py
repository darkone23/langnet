import datomic_py
import sys


def main():

    connection = datomic_py.connect(
        "datomic:sql://my-datomic-database?jdbc:postgresql://localhost:5432/my-datomic-storage?user=datomic-user&password=unsafe"
    )

    db = datomic_py.db(connection)

    results = datomic_py.q(
        """
      [:find ?id ?type ?gender
       :in $ ?name
       :where
         [?e :artist/name ?name]
         [?e :artist/gid ?id]
         [?e :artist/type ?teid]
         [?teid :db/ident ?type]
         [?e :artist/gender ?geid]
         [?geid :db/ident ?gender]] 
    """,
        db,
        "Jimi Hendrix",
    )

    for result in results:
        [_id, _type, _gender] = result
        print(_id, _type, _gender)

    print("Goodbye!")
    sys.exit(0)
