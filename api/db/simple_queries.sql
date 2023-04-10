-- name: add_person!
-- Adds a new person into the database
INSERT INTO "person" (person_name, person_age) VALUES (:person_name, :person_age) RETURNING person_age;

-- name: get_person
-- Gets a person from the database
SELECT * FROM "person" WHERE person_name = :person_name;

-- name: get_all_persons
-- Gets all persons from the database
SELECT * FROM "person";