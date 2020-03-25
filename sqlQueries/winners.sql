SELECT
    id as matchId,
    included -> 'attributes' -> 'stats' ->> 'playerId' as playerId
FROM (
        SELECT
            id,
            json_array_elements(data -> 'included') AS included
        FROM
            matches
        WHERE
            DATA -> 'data' -> 'attributes' ->> 'mapName' = 'Summerland_Main'
            AND DATA -> 'data' -> 'attributes' ->> 'gameMode' = 'squad-fpp'
) as X
WHERE
    included ->> 'type' = 'participant'
    AND included -> 'attributes' -> 'stats' ->> 'winPlace' = '1'
