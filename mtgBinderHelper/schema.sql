DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS collection;
DROP TABLE IF EXISTS cardInfo;
DROP TABLE IF EXISTS priceHistory;
DROP TABLE IF EXISTS setInfo;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL,
  createdAt TIMESTAMP DEFAULT (now()),
  accountType TEXT DEFAULT "user"
);

CREATE TABLE collection (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER,
  cardId INTEGER,
  setCode TEXT,
  setNumber INTEGER,
  isFoil boolean,
  isTradeable boolean,
  promo boolean,
  treatment TEXT,
  dateAcquired DATETIME,
  dateAdded TIMESTAMP,
  dateUpdated TIMESTAMP
);

CREATE TABLE priceHistory (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  price float NOT NULL,
  isFoil boolean,
  isPromo boolean,
  cardId INTEGER,
  createdAt TIMESTAMP DEFAULT (now()),
  updatedAt TIMESTAMP
);

CREATE TABLE cardInfo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  setCode TEXT,
  setNumber INTEGER,
  name TEXT,
  borderColor TEXT,
  rarity TEXT,
  artist TEXT,
  hasFoil boolean,
  hasNonFoil boolean,
  frameVersion TEXT,
  finishes TEXT,
  layout TEXT,
  manaCost TEXT,
  convertedManaCost INTEGER,
--  legalities TEXT,
  oracle longtext,
  scryfallId TEXT,
  type TEXT
);

CREATE TABLE setInfo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  setCode TEXT UNIQUE,
  name TEXT,
  block TEXT,
  releaseDate DATETIME,
  baseSetSize INTEGER,
  totalSetSize INTEGER,
  type TEXT
);

-- ALTER TABLE collection ADD FOREIGN KEY (price_id) REFERENCES priceHistory (id);

-- ALTER TABLE collection ADD FOREIGN KEY (user_id) REFERENCES user (id);

-- ALTER TABLE collection ADD FOREIGN KEY (card_id) REFERENCES cardInfo (id);

-- ALTER TABLE priceHistory ADD FOREIGN KEY (card_id) REFERENCES cardInfo (id);

-- ALTER TABLE cardInfo ADD FOREIGN KEY (set_id) REFERENCES setInfo (set_id);