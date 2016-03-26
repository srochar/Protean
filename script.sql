CREATE TABLE languages (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE letters (
	id SERIAL PRIMARY KEY,
	character CHAR NOT NULL UNIQUE
);

CREATE TABLE frequencys(
	id SERIAL PRIMARY KEY,
	min FLOAT NOT NULL DEFAULT 1,
	max FLOAT NOT NULL DEFAULT 0,
	language_id INTEGER NOT NULL REFERENCES languages(id) ON UPDATE CASCADE ON DELETE CASCADE,
	letter_id INTEGER NOT NULL REFERENCES letters (id) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE FUNCTION insertFrequencysLetter() RETURNS trigger AS
$BODY$
BEGIN
  IF tg_op = 'INSERT' THEN
     INSERT INTO frequencys(language_id,letter_id) (SELECT languages.id,NEW.id FROM languages);
     RETURN NEW;
  END IF;
END
$BODY$ LANGUAGE plpgsql;


CREATE TRIGGER letter_ins AFTER INSERT
        ON letters FOR each ROW
        EXECUTE PROCEDURE insertFrequencysLetter();


CREATE FUNCTION insertFrequencysLanguage() RETURNS trigger AS
$BODY$
BEGIN
  IF tg_op = 'INSERT' THEN
     INSERT INTO frequencys(language_id,letter_id) (SELECT NEW.id,letters.id FROM letters );
     RETURN NEW;
  END IF;
END
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER language_ins AFTER INSERT
        ON languages FOR each ROW
        EXECUTE PROCEDURE insertFrequencysLanguage();