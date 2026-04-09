SELECT 
airline_code,
ROUND(SAFE_DIVIDE(SUM(departure_delay), 60), 3) AS total_departure_delay_hours,
ROUND(SAFE_DIVIDE(SUM(arrival_delay), 60), 3) AS total_arrival_delay_hours,
ROUND(SAFE_DIVIDE(AVG(departure_delay), 60), 3) AS avg_departure_delay_hours,
ROUND(SAFE_DIVIDE(AVG(arrival_delay), 60), 3) AS avg_arrival_delay_hours,
COUNT(*) AS total_flights,
COUNTIF(departure_delay > 15 OR arrival_delay > 15) AS delayed_flights,
ROUND(SAFE_DIVIDE(
COUNTIF(departure_delay > 15 OR arrival_delay > 15),
COUNT(*)),3) AS delay_rate
FROM {{ref('enriched_flights')}}
WHERE is_cancelled IS FALSE 
AND is_diverted IS FALSE
GROUP BY airline_code
ORDER BY delay_rate DESC