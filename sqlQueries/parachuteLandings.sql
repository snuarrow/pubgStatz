SELECT
    id,
    _t
FROM (
    SELECT
        id,
        _t
    FROM (
        SELECT
            id,
            _T
        FROM (
            SELECT
                id,
                json_array_elements(DATA) AS _T
            FROM
                telemetries
            WHERE
                id IN (
                    SELECT
                        id
                    FROM
                        matches
                    WHERE
                        DATA -> 'data' -> 'attributes' ->> 'mapName' = '{mapName}'
                        AND DATA -> 'data' -> 'attributes' ->> 'gameMode' = 'squad-fpp')) AS x) AS y
        WHERE
            _t ->> '_T' = 'LogParachuteLanding') AS z;
