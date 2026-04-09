SELECT 
origin_airport_id,
ROUND(SAFE_DIVIDE(SUM(departure_delay), 60), 3) AS total_departure_delay_hours,
ROUND(SAFE_DIVIDE(AVG(departure_delay), 60), 3) AS avg_departure_delay_hours,
COUNT(*) AS total_flights,
COUNTIF(departure_delay > 15) AS delayed_flights,
ROUND(SAFE_DIVIDE(
  COUNTIF(departure_delay > 15),
  COUNT(*)
),3) AS delay_rate,
--composite score
ROUND(
  SAFE_DIVIDE(COUNTIF(departure_delay > 15), COUNT(*))
  + SAFE_DIVIDE(AVG(departure_delay), 60),
3) AS score
FROM {{ref('enriched_flights')}}
WHERE is_cancelled IS FALSE 
AND is_diverted IS FALSE
GROUP BY origin_airport_id
HAVING COUNT(*) > 100
ORDER BY score DESC