DROP DATABASE IF EXISTS dis;
CREATE DATABASE dis;

CREATE SCHEMA IF NOT EXISTS my_extensions;
ALTER DATABASE dis SET search_path='$user', public, my_extensions;
CREATE EXTENSION IF NOT EXISTS pg_trgm SCHEMA my_extensions ;

\c dis;
CREATE TABLE public."person"(
  person_name text NOT NULL,
  person_age smallint NOT NULL
);

ALTER TABLE public."person" OWNER TO postgres;