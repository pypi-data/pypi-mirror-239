from syndb_constants.table import SYNDB_TABLE_NAME_TO_ENUM, SyndbTable

from syndb_cassandra.models import brain_unit_models

CS_CONNECTION_NAME = "scylla"
SYNDB_NEURO_DATA_KEYSPACE = "syndb"

WITH_LEVELED_COMPACTION = "WITH COMPACTION = {'class': 'LeveledCompactionStrategy'}"

syndb_table_to_valid_fields: dict[SyndbTable, frozenset[str]] = {
    SYNDB_TABLE_NAME_TO_ENUM[model.__table_name__.upper()]: frozenset(
        [e for e in vars(model) if "__" not in e and not e.startswith("_")][:-3]
    )
    for model in brain_unit_models
}
