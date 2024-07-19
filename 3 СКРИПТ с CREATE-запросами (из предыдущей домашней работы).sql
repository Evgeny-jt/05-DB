CREATE TABLE IF NOT EXISTS МузыкальныеЖанры (
	жанр_id SERIAL PRIMARY KEY,
	жанр VARCHAR(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS Исполнители (
	исполнитель_id SERIAL PRIMARY KEY,
	исполнитель VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS ЖанрыИсполнители (
	жанры INTEGER REFERENCES МузыкальныеЖанры(жанр_id),
	исполнители INTEGER REFERENCES Исполнители(исполнитель_id),
	CONSTRAINT жанрисп PRIMARY KEY (жанры, исполнители)
);


CREATE TABLE IF NOT EXISTS Альбомы (
	альбом_id SERIAL PRIMARY KEY,
	альбом VARCHAR(50) NOT null,
	год INTEGER NOT null
);


CREATE TABLE IF NOT EXISTS ИсполнительАльбом (
	исполнители INTEGER REFERENCES Исполнители(исполнитель_id),
	альбомы INTEGER REFERENCES Альбомы(альбом_id),
	CONSTRAINT СвязьИсполнителейАльбомов PRIMARY KEY (исполнители, альбомы)
);


CREATE TABLE IF NOT EXISTS Треки (
	трек_id SERIAL PRIMARY KEY,
    альбом_id INTEGER REFERENCES Альбомы(альбом_id),
	трек VARCHAR(50) NOT null,
	продолжительность  INTEGER NOT null
);


CREATE TABLE IF NOT EXISTS Сборники (
	сборник_id SERIAL PRIMARY KEY,
	сборник VARCHAR(40) NOT null,
	год INTEGER NOT null
);


CREATE TABLE IF NOT EXISTS СборникиТреков (
	сборники INTEGER REFERENCES Сборники(сборник_id),
	треки INTEGER REFERENCES Треки(трек_id),
	CONSTRAINT pk PRIMARY KEY (сборники, треки)
);