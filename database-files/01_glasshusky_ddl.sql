CREATE DATABASE IF NOT EXISTS glasshusky;
USE glasshusky;

# CREATE TABLES
DROP TABLE IF EXISTS company;
CREATE TABLE IF NOT EXISTS company (
    name    VARCHAR(50) NOT NULL,
    size    INT,
    companyID   INT AUTO_INCREMENT PRIMARY KEY,
    days_on_site    INT
);

DROP TABLE IF EXISTS `position`;
CREATE TABLE `position`(
    positionID INT AUTO_INCREMENT NOT NULL,
    companyID INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    industry VARCHAR(100) NOT NULL,
    remote BOOLEAN NOT NULL,
    PRIMARY KEY (positionID),
    UNIQUE KEY (companyID, positionID),
    CONSTRAINT companyID
        FOREIGN KEY (companyID) REFERENCES company(companyID)
        ON UPDATE cascade ON DELETE cascade
);


DROP TABLE IF EXISTS location;
CREATE TABLE IF NOT EXISTS location (
   street  VARCHAR(50),
   city    VARCHAR(50),
   state   CHAR(2), # 2 letter abbreviation
   country CHAR(3) NOT NULL, # 3 letter abbreviation
   postcode    INT,
   locID   INT AUTO_INCREMENT PRIMARY KEY
);

DROP TABLE IF EXISTS reviewer;
CREATE TABLE IF NOT EXISTS reviewer (
    reviewerID   INT AUTO_INCREMENT NOT NULL,
    major        VARCHAR(50),
    name         VARCHAR(50),
    `num_co-ops` INT,
    year         INT,
    bio          VARCHAR(2500),
    active      BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (reviewerID)
);

DROP TABLE IF EXISTS reviews;
CREATE TABLE IF NOT EXISTS reviews (
    reviewID    INT AUTO_INCREMENT NOT NULL,
    positionID INT NOT NULL,
    companyID   INT NOT NULL,
    authorID    INT,
    title        VARCHAR(50),
    `num_co-op` INT,
    rating       INT,
    recommend    BOOL,
    pay_type     VARCHAR(50),
    pay          FLOAT,
    job_type     VARCHAR(50),
    date_time    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    verified    BOOLEAN DEFAULT FALSE,
    text        TEXT,
    PRIMARY KEY (reviewID),
    UNIQUE KEY (positionID, reviewID),
    CONSTRAINT authorID_fk
        FOREIGN KEY (authorID) REFERENCES reviewer(reviewerID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT positionID_fk
        FOREIGN KEY (positionID) REFERENCES `position`(positionID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT companyID_fk
        FOREIGN KEY (companyID) REFERENCES company(companyID)
        ON UPDATE cascade ON DELETE cascade
);


DROP TABLE IF EXISTS companylocation;
CREATE TABLE IF NOT EXISTS companylocation (
   companyID INT,
   locID   INT,
   PRIMARY KEY (companyID, locID),
   FOREIGN KEY (companyID)
       REFERENCES company(companyID)
       ON UPDATE CASCADE ON DELETE RESTRICT,
   FOREIGN KEY (locID)
       REFERENCES location(locID)
       ON UPDATE CASCADE ON DELETE RESTRICT
);


DROP TABLE IF EXISTS `college`;
CREATE TABLE IF NOT EXISTS `college` (
  collegeID INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(50),
  PRIMARY KEY (collegeID)
);

DROP TABLE IF EXISTS `positionTargetCollege`;
CREATE TABLE IF NOT EXISTS `positionTargetCollege` (
  collegeID INT NOT NULL,
  positionID INT NOT NULL,
  PRIMARY KEY (collegeID, positionID),
  CONSTRAINT fk_college_ptc FOREIGN KEY (collegeID)
      REFERENCES `college`(collegeID) ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk_position_ptc FOREIGN KEY (positionID) REFERENCES
      `position`(positionID) ON UPDATE cascade ON DELETE restrict
);


DROP TABLE IF EXISTS `industry`;
CREATE TABLE IF NOT EXISTS `industry` (
  industryID INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(50),
  PRIMARY KEY(industryID)
);

DROP TABLE IF EXISTS `companyIndustry`;
CREATE TABLE IF NOT EXISTS `companyIndustry` (
  industryID INT NOT NULL,
  companyID INT NOT NULL,
  PRIMARY KEY(industryID, companyID),
  CONSTRAINT fk_industry_ci FOREIGN KEY (industryID)
      REFERENCES `industry`(industryID) ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk_company_ci FOREIGN KEY (companyID)
      REFERENCES `company`(companyID) ON UPDATE cascade ON DELETE restrict
);


DROP TABLE IF EXISTS analyst;
CREATE TABLE IF NOT EXISTS analyst (
   analystID int AUTO_INCREMENT NOT NULL,
   name VARCHAR(50) NOT NULL,
   PRIMARY KEY (analystID)
);

DROP TABLE IF EXISTS admin;
CREATE TABLE IF NOT EXISTS admin (
   adminID int AUTO_INCREMENT NOT NULL,
   name VARCHAR(50) NOT NULL,
   PRIMARY KEY (adminID)
);

DROP TABLE IF EXISTS questions;
CREATE TABLE IF NOT EXISTS questions (
   questionId int AUTO_INCREMENT NOT NULL,
   postId int NOT NULL,
   author VARCHAR(50),
   text VARCHAR(255) NOT NULL,
   PRIMARY KEY (questionId),
   CONSTRAINT questPostId_fk FOREIGN KEY (postId) REFERENCES reviews (reviewID)
   ON UPDATE CASCADE
   ON DELETE CASCADE
);

DROP TABLE IF EXISTS answers;
CREATE TABLE IF NOT EXISTS answers (
   answerId int AUTO_INCREMENT NOT NULL,
   postId int NOT NULL,
   questionId int NOT NULL,
   author VARCHAR(50),
   text VARCHAR(255) NOT NULL,
   PRIMARY KEY (answerId),
   CONSTRAINT answPostId_fk FOREIGN KEY (postId) REFERENCES reviews (reviewID),
   CONSTRAINT answQuestionId_fk FOREIGN KEY (questionId) REFERENCES questions (questionId)
   ON UPDATE CASCADE
   ON DELETE CASCADE
);

