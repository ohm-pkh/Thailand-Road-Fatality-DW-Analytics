CREATE TABLE IF NOT EXISTS warehouse.dim_nationality(
    id INT,
    nationality_name VARCHAR(50),
    nationality_adjectival TEXT[],
    nationality_2_alpha CHAR(2),
    nationality_3_alpha CHAR(3)
);