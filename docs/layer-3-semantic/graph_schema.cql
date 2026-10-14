CREATE CONSTRAINT unique_system_id IF NOT EXISTS FOR (n:SystemNode) REQUIRE n.id IS UNIQUE;
MERGE (n:SystemNode {id: 'ENT-MEDAI-NODE-01'}) ON CREATE SET n.name = 'Medical AI Edge Diagnostics 3T';
MERGE (h:HardwarePlatform {id: 'HW-RK3588'}) ON CREATE SET h.name = 'Rockchip RK3588 NPU';
MATCH (n:SystemNode {id: 'ENT-MEDAI-NODE-01'}), (h:HardwarePlatform {id: 'HW-RK3588'}) MERGE (n)-[:RUNS_ON]->(h);