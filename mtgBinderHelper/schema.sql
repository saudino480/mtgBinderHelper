DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS collection;
DROP TABLE IF EXISTS cardInfo;
DROP TABLE IF EXISTS priceHistory;
DROP TABLE IF EXISTS setInfo;

CREATE TABLE `user` (
  `id` int PRIMARY KEY,
  `username` varchar(255) UNIQUE NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT (now()),
  `accountType` varchar(255) DEFAULT "user"
);

CREATE TABLE `collection` (
  `id` int PRIMARY KEY,
  `user_id` int,
  `card_id` int,
  `price_id` int,
  `set_id` varchar(255),
  `set_number` int,
  `isFoil` boolean,
  `isTradeable` boolean,
  `promo` boolean,
  `treatment` varchar(255),
  `dateAcquired` datetime,
  `dateAdded` datetime,
  `dateUpdated` datetime
);

CREATE TABLE `priceHistory` (
  `id` int PRIMARY KEY,
  `price` float NOT NULL,
  `isFoil` boolean,
  `isPromo` boolean,
  `date` datetime,
  `card_id` int,
  `created_at` TIMESTAMP DEFAULT (now()),
  `updated_at` TIMESTAMP
);

CREATE TABLE `cardInfo` (
  `id` int PRIMARY KEY,
  `set_id` varchar(255),
  `set_number` int,
  `name` varchar(255),
  `rarity` varchar(255),
  `artist` varchar(255),
  `hasFoil` boolean,
  `hasNonFoil` boolean,
  `frameVersion` varchar(255),
  `layout` varchar(255),
  `convertedManaCost` int,
  `legalIn` varchar,
  `oracle` longtext,
  `scryfallId` varchar(255),
  `type` varchar(255)
);

CREATE TABLE `setInfo` (
  `id` int PRIMARY KEY,
  `set_id` varchar(255) UNIQUE,
  `block` varchar(255),
  `releaseDate` datetime,
  `baseSetSize` int,
  `totalSetSize` int,
  `type` varchar(255)
);

ALTER TABLE `collection` ADD FOREIGN KEY (`price_id`) REFERENCES `priceHistory` (`id`);

ALTER TABLE `collection` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `collection` ADD FOREIGN KEY (`card_id`) REFERENCES `cardInfo` (`id`);

ALTER TABLE `priceHistory` ADD FOREIGN KEY (`card_id`) REFERENCES `cardInfo` (`id`);

ALTER TABLE `cardInfo` ADD FOREIGN KEY (`set_id`) REFERENCES `setInfo` (`set_id`);