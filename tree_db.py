import os
import sqlalchemy as db

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
class LeafNode(Node):
    def __init__(self, id, name):
        super().__init__(id, name)

class ParentNode(Node):
    def __init__(self, id, name, childs=None):
        super().__init__(id, name)
        self.childs = [] if childs is None else childs
    


class TreeDb:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'db','folders_tree.db')
        self.engine = db.create_engine(f'sqlite:///{self.db_path}')
        self.metadata = db.MetaData()
        self.nodes_tables = db.Table('nodes', self.metadata, autoload=True, autoload_with=self.engine)
        self.edges_table = db.Table('edges', self.metadata, autoload=True, autoload_with=self.engine)
    
    def get_subtree(self, parent_node_id):
        # Set an alias to the nodes table because we will use it multiple time in the select qurey
        nodes_tables_alias = self.nodes_tables.alias('dummy')
        # Run a left join on nodes -> edges -> nodes to get for the given parent node its childs and for each child its name
        query = db.select([self.nodes_tables.c.node_id, self.nodes_tables.c.node_name, self.edges_table.c.child_id, nodes_tables_alias.c.node_name]).select_from(self.nodes_tables.outerjoin(self.edges_table, self.nodes_tables.c.node_id == self.edges_table.c.parent_id).outerjoin(nodes_tables_alias, nodes_tables_alias.c.node_id == self.edges_table.c.child_id)).where(self.nodes_tables.columns.node_id == parent_node_id)
        connection = self._get_connection()
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchall()
        # If the result set is empty - return None
        if len(ResultSet) == 0:
            return None
        # Extract the parent information and first child
        id, name , child_id , child_name = ResultSet[0]
        childs = []
        child_exists = child_id is not None
        if child_exists:
            for child in ResultSet:
                _, _, child_id, child_name = child
                childs.append(LeafNode(child_id, child_name))
        return ParentNode(id, name, childs)
    
    def _get_connection(self):
        # TODO: connection pool if needed 
        return self.engine.connect()





