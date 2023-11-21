
-- How many animals of each type have outcomes?

SELECT animal_type, COUNT(*) AS ct
	FROM outcomes_fct JOIN animals_dim USING(animal_id)
	GROUP BY animal_type; 
	

-- How many animals are there with more than 1 outcome?

SELECT animal_id, COUNT(*) as animal_ct
FROM outcomes_fct
GROUP BY animal_id
HAVING COUNT(*) > 1;
	
-- What are the top 5 months for outcomes? 

SELECT month, COUNT(*) as outcome_ct
FROM outcomes_fct JOIN date_dim USING(date_id)
GROUP BY month
ORDER by outcome_ct DESC
LIMIT 5;

-- What is the total number of kittens, adults, and seniors, whose outcome is "Adopted"?

SELECT
	CASE
		WHEN cast(age as decimal) < 1 THEN 'Kitten'
		when cast(age as decimal) between 1 and 10 then 'Adult'	
		ELSE 'Senior'
	END AS cat_age,
	count(*) as animal_ct
FROM outcomes_fct
	JOIN animals_dim USING(animal_id)
	JOIN outcome_type_dim USING(outcome_type_id)
WHERE outcome_type = 'Adoption' and animal_type = 'Cat'
GROUP BY cat_age;

-- Conversely, among all the cats who were "Adopted", what is the total number of kittens, adults, and seniors?
-- I believe this is the same question as above.


-- For each date, what is the cumulative total of outcomes up to and including this date?

select 
	distinct date_id,
	count(*) over (order by date_id asc) as outcome_ct
from outcomes_fct;
