--WITH today AS (
--    SELECT toStartOfDay(now()) AS day_start
--)

WITH today AS (
    SELECT toDateTime('2025-01-01 00:00:00') AS day_start
)
SELECT
    phrase,
    groupArray((hour, views_diff)) AS views_by_hour
FROM (
    SELECT
        phrase,
        toHour(dt) AS hour,
        max(views) - any(views) AS views_diff
    FROM test.phrases_views, today
    WHERE dt >= day_start
      AND campaign_id = 1111111
    GROUP BY phrase, hour
    ORDER BY phrase, hour DESC
)
GROUP BY phrase;
