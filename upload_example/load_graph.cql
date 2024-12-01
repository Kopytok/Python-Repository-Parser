-- Remove all nodes and relationships from the database
MATCH (n)-[r]->(m) DELETE n, r, m;
MATCH (n) DELETE n;

-- Load nodes with label 'First'
LOAD CSV WITH HEADERS FROM 'file:///first_nodes.csv' AS row
CREATE (
    p:First {
        id: toInteger(row.index),
        name: row.node
    }
);

-- Load nodes with label 'Second'
LOAD CSV WITH HEADERS FROM 'file:///second_nodes.csv' AS row
CREATE (
    p:Second {
        id: toInteger(row.index),
        name: row.node
    }
);

-- Load edges between all nodes
LOAD CSV WITH HEADERS FROM 'file:///edges.csv' AS row
MATCH (calling {name: row.calling}), (called {name: row.called})
CREATE (calling)-[:CALLS]->(called);
