CREATE TABLE outcomes (
    animal_id VARCHAR,
    animal_name VARCHAR,
    ts TIMESTAMP,
    dob DATE,
    outcome_type VARCHAR,
    outcome_subtype VARCHAR,
    animal_type VARCHAR,
    sex_outcome VARCHAR,
    age VARCHAR,
    breed VARCHAR,
    color VARCHAR,
    month VARCHAR,
    year INT
);

CREATE TABLE animals_dim (
    animal_id VARCHAR PRIMARY KEY,
    animal_name VARCHAR,
    animal_type VARCHAR,
    breed VARCHAR,
    color VARCHAR,
    dob DATE,
    sex_outcome VARCHAR,
    age VARCHAR
);

CREATE TABLE outcome_type_dim (
    outcome_type_id INT PRIMARY KEY,
    outcome_type VARCHAR
);

CREATE TABLE outcome_subtype_dim (
    outcome_subtype_id INT PRIMARY KEY,
    outcome_subtype VARCHAR
);

CREATE TABLE date_dim (
    date_id INT PRIMARY KEY,
    year INT,
    month VARCHAR,
    day INT,
    dow INT
);

CREATE TABLE outcomes_fct (
    outcome_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    animal_id VARCHAR,
    outcome_type_id INT,
    outcome_subtype_id INT,
    date_id INT,
    FOREIGN KEY (animal_id) REFERENCES animals_dim(animal_id),
    FOREIGN KEY (outcome_type_id) REFERENCES outcome_type_dim(outcome_type_id),
    FOREIGN KEY (outcome_subtype_id) REFERENCES outcome_subtype_dim(outcome_subtype_id),
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id)
);
