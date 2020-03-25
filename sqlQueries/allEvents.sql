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
                        DATA -> 'data' -> 'attributes' ->> 'mapName' = 'Summerland_Main'
                        AND DATA -> 'data' -> 'attributes' ->> 'gameMode' = 'squad-fpp')) AS x) AS y
        ) AS z;
