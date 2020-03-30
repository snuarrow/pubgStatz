SELECT
        id
FROM
        matches
WHERE
        DATA -> 'data' -> 'attributes' ->> 'mapName' = '{mapName}'
        AND DATA -> 'data' -> 'attributes' ->> 'gameMode' = '{gameMode}'

