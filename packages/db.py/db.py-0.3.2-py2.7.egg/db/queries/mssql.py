queries = {
    "column": {
        "head": "select top %d %s from %s;",
        "all": "select %s from %s;",
        "unique": "select distinct %s from %s;",
        "sample": "select top %d %s from %s order by rand();"
    },
    "table": {
        "select": "select %s from %s;",
        "head": "select top %d * from %s;",
        "all": "select * from %s;",
        "unique": "select distinct %s from %s;",
        "sample": "select top %d * from %s order by rand();"
    },
    "system": {
        "schema_no_system": """
                select
                    table_name
                    , column_name
                    , data_type
                from
                    information_schema.columns
                where
                    table_schema not in ('information_schema', 'sys')
                """,
        "schema_with_system": """
                select
                    table_name
                    , column_name
                    , data_type
                from
                    information_schema.columns;
                """,
        "schema_specified": """
                select
                    table_name
                    , column_name
                    , data_type
                from
                    information_schema.columns
                where table_schema in (%s);
                """,
        "foreign_keys_for_table": """
            SELECT
                parent_col.name AS foreign_key,
                object_name(referenced_object_id) AS referenced_table,
                col.name AS referenced_column
            FROM sys.foreign_key_columns
            INNER JOIN sys.columns col
                ON col.column_id = referenced_column_id
                    AND col.object_id = referenced_object_id
            INNER JOIN sys.columns parent_col
                ON parent_col.column_id = parent_column_id
                   AND parent_col.object_id = parent_object_id
            WHERE parent_object_id = object_id('%s');
        """,
        "foreign_keys_for_column": """
            SELECT
                object_name(constraint_object_id) AS foreign_key,
                object_name(referenced_object_id) AS referenced_table,
                col.name AS referenced_column
            FROM sys.foreign_key_columns
            INNER JOIN sys.columns col
                ON col.column_id = referenced_column_id
                    AND col.object_id = referenced_object_id
            WHERE parent_object_id = object_id('%s')
                AND constraint_object_id = object_id('%s');
        """,
        "ref_keys_for_table": """
            SELECT
                ref_col.name,
                object_name(parent_object_id),
                col.name as column_name
            FROM sys.foreign_key_columns
            INNER JOIN sys.columns col
               ON col.column_id = parent_column_id
                   AND col.object_id = parent_object_id
            INNER JOIN sys.columns ref_col
                ON ref_col.column_id = referenced_column_id
                   AND ref_col.object_id = referenced_object_id
            WHERE referenced_object_id = object_id('%s');
        """
    }
}

