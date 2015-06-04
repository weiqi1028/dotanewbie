CREATE TABLE Heroes
(
heroId INT,
heroName VARCHAR(30) NOT NULL,

PRIMARY KEY(heroId)
);

CREATE TABLE Tags
(
tagId INT,
tag VARCHAR(20) NOT NULL,

PRIMARY KEY(tagId)
);

CREATE TABLE Hero_tag_ties
(
id INT AUTO_INCREMENT,
tagId INT NOT NULL,
heroId INT NOT NULL,

PRIMARY KEY(id),
FOREIGN KEY (tagId) REFERENCES Tags(tagId),
FOREIGN KEY (heroId) REFERENCES Heroes(heroId)
);

CREATE TABLE Items
(
id INT,
itemName VARCHAR(30) NOT NULL,

PRIMARY KEY (id)
);

CREATE TABLE Matches
(
matchId INT UNSIGNED,
duration INT,
startTime INT UNSIGNED,
matchSeqNum INT UNSIGNED,
towerStatusRadiant INT,
towerStatusDire INT,
barracksStatusRadiant INT,
barracksStatusDire INT,
cluster INT,
firstBloodTime INT,
lobbyType TINYINT,
gameMode TINYINT,
player1Id INT,
player2Id INT,
player3Id INT,
player4Id INT,
player5Id INT,
player6Id INT,
player7Id INT,
player8Id INT,
player9Id INT,
player10Id INT,

PRIMARY KEY (matchId)
);

CREATE TABLE Hero_item_ties
(
id INT AUTO_INCREMENT,
heroId INT NOT NULL,
matchId INT UNSIGNED NOT NULL,
item1Id INT,
item2Id INT,
item3Id INT,
item4Id INT,
item5Id INT,
item6Id INT,
win TINYINT(1) NOT NULL,

PRIMARY KEY (id),
FOREIGN KEY (heroId) REFERENCES Heroes(heroId),
FOREIGN KEY (matchId) REFERENCES Matches(matchId)
);

CREATE TABLE Players
(
playerId INT,
profileUrl VARCHAR(60),

PRIMARY KEY (playerId)
);

CREATE TABLE Players_match_ties
(
id INT AUTO_INCREMENT,
playerId INT UNSIGNED,
matchId INT UNSIGNED NOT NULL,
playerSlot INT,
radiant TINYINT(1),
win TINYINT(1),
heroId INT,
kills INT,
deaths INT,
assists INT,
leaverStatus INT,
gold INT,
lastHits INT,
denies INT,
gpm INT,
xpm INT,
goldSpent INT,
heroDamage INT,
towerDamage INT,
heroHealing INT,
heroLevel INT,

PRIMARY KEY (id),
FOREIGN KEY (matchId) REFERENCES Matches(matchId)
);