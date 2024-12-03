CREATE DATABASE IF NOT EXISTS glasshusky;
USE glasshusky;
flush privileges;

DROP TABLE IF EXISTS `company`;
CREATE TABLE IF NOT EXISTS `company` (
    `name`    VARCHAR(50) NOT NULL,
    `size`    INT,
    companyID   INT AUTO_INCREMENT PRIMARY KEY
);

DROP TABLE IF EXISTS `position`;
CREATE TABLE `position`(
    positionID INT AUTO_INCREMENT NOT NULL,
    companyID INT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `remote` BOOLEAN NOT NULL,
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
   `state`   CHAR(2), # 2 letter abbreviation
   country CHAR(3) NOT NULL, # 3 letter abbreviation
   postcode    INT,
   locID   INT AUTO_INCREMENT PRIMARY KEY
);

DROP TABLE IF EXISTS reviewer;
CREATE TABLE IF NOT EXISTS reviewer (
    reviewerID   INT AUTO_INCREMENT NOT NULL,
    major        VARCHAR(50),
    `name`         VARCHAR(50),
    `num_co-ops` INT,
    `year`        INT,
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
    `text`        TEXT,
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
   `name` VARCHAR(50) NOT NULL,
   PRIMARY KEY (adminID)
);

DROP TABLE IF EXISTS questions;
CREATE TABLE IF NOT EXISTS questions (
   questionId int AUTO_INCREMENT NOT NULL,
   postId int NOT NULL,
   author VARCHAR(50),
   `text` VARCHAR(255) NOT NULL,
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
   `text` VARCHAR(255) NOT NULL,
   PRIMARY KEY (answerId),
   CONSTRAINT answPostId_fk FOREIGN KEY (postId) REFERENCES reviews (reviewID),
   CONSTRAINT answQuestionId_fk FOREIGN KEY (questionId) REFERENCES questions (questionId)
   ON UPDATE CASCADE
   ON DELETE CASCADE
);

INSERT INTO `college` (`name`) VALUES
('Khoury College of Computer Sciences'),
("D'amore Mckim"),
('Bouve College of Health Sciences'),
('College of Arts, Media and Design'),
('College of Professional Studies'),
('College of Science'),
('College of Social Sciences and Humanities'),
('Northeastern University School of Law');



INSERT INTO `industry` (`name`) VALUES
('Technology'),
('Healthcare'),
('Finance'),
('Education'),
('Manufacturing'),
('Retail'),
('Hospitality'),
('Telecommunications'),
('Energy'),
('Automotive'),
('Aerospace'),
('Agriculture'),
('Construction'),
('Entertainment'),
('Media'),
('Pharmaceuticals'),
('Real Estate'),
('Transportation'),
('Logistics'),
('Food and Beverage'),
('Biotechnology'),
('Environmental Services'),
('Consulting'),
('Marketing'),
('Legal Services'),
('Insurance'),
('Tourism'),
('Fitness and Wellness'),
('E-commerce'),
('Cybersecurity');



INSERT INTO company (`name`, `size`) VALUES
('TechNova Solutions', 5000),
('GreenLeaf Innovations', 1200),
('Quantum Dynamics', 8000),
('SilverStream Systems', 3500),
('RedRock Analytics', 2000),
('BlueWave Technologies', 6000),
('GoldenGate Software', 4500),
('PurpleMountain Data', 1800),
('OrangeSky Networks', 7000),
('BlackDiamond Systems', 2500),
('WhitePearl Solutions', 3000),
('EmeraldCity Tech', 5500),
('RubyRed Innovations', 1500),
('SapphireBlue Analytics', 4000),
('AmberGlow Software', 2800),
('JadeGreen Networks', 6500),
('TopazYellow Systems', 3200),
('OpalWhite Technologies', 7500),
('OnixBlack Solutions', 1900),
('AquamarineBlue Data', 4200),
('CoralPink Innovations', 2300),
('TurquoiseGreen Software', 5800),
('LavenderPurple Systems', 3700),
('MaroonRed Networks', 6200),
('NavyBlue Analytics', 2700),
('SlateGray Technologies', 4800),
('IvoryWhite Solutions', 1600),
('CrimsonRed Software', 5200),
('IndigoBlue Systems', 3900),
('OliveGreen Networks', 7200);


INSERT INTO `position` (companyID, `name`, `description`, `remote`) VALUES
(1, 'Software Engineer', 'Develop and maintain software applications', TRUE),
(2, 'Data Analyst', 'Analyze and interpret complex data sets', FALSE),
(3, 'Product Manager', 'Lead product development and strategy', TRUE),
(4, 'UX Designer', 'Create user-centered designs for digital products', FALSE),
(5, 'Sales Representative', 'Generate leads and close sales deals', TRUE),
(6, 'Marketing Specialist', 'Develop and execute marketing campaigns', FALSE),
(7, 'DevOps Engineer', 'Manage and optimize IT infrastructure', TRUE),
(8, 'Financial Analyst', 'Perform financial planning and analysis', FALSE),
(9, 'HR Coordinator', 'Support human resources operations', TRUE),
(10, 'Customer Support Specialist', 'Provide excellent customer service', FALSE),
(11, 'Business Development Manager', 'Identify and pursue new business opportunities', TRUE),
(12, 'Content Writer', 'Create engaging content for various platforms', FALSE),
(13, 'Quality Assurance Tester', 'Ensure software quality through testing', TRUE),
(14, 'Project Coordinator', 'Assist in project planning and execution', FALSE),
(15, 'Systems Administrator', 'Maintain and troubleshoot IT systems', TRUE),
(16, 'Graphic Designer', 'Create visual concepts using computer software', FALSE),
(17, 'Account Manager', 'Manage client relationships and accounts', TRUE),
(18, 'Data Scientist', 'Apply advanced analytics to solve business problems', FALSE),
(19, 'Network Engineer', 'Design and implement computer networks', TRUE),
(20, 'Social Media Manager', 'Manage social media presence and strategy', FALSE),
(21, 'Frontend Developer', 'Build user interfaces for web applications', TRUE),
(22, 'Business Analyst', 'Analyze business processes and recommend improvements', FALSE),
(23, 'Technical Writer', 'Create technical documentation and user guides', TRUE),
(24, 'Database Administrator', 'Manage and maintain database systems', FALSE),
(25, 'UI Designer', 'Design user interfaces for digital products', TRUE),
(26, 'Operations Manager', 'Oversee daily business operations', FALSE),
(27, 'SEO Specialist', 'Optimize websites for search engines', TRUE),
(28, 'Mobile App Developer', 'Develop applications for mobile devices', FALSE),
(29, 'Customer Success Manager', 'Ensure customer satisfaction and retention', TRUE),
(30, 'Product Designer', 'Design and prototype new products', FALSE),
(1, 'Cloud Architect', 'Design and implement cloud computing strategies', TRUE),
(2, 'Machine Learning Engineer', 'Develop machine learning models and algorithms', FALSE),
(3, 'Scrum Master', 'Facilitate agile development processes', TRUE),
(4, 'Cybersecurity Analyst', 'Protect computer networks from threats', FALSE),
(5, 'Supply Chain Analyst', 'Analyze and optimize supply chain operations', TRUE),
(6, 'Brand Manager', 'Develop and maintain brand strategy', FALSE),
(7, 'Full Stack Developer', 'Develop both client and server software', TRUE),
(8, 'Risk Analyst', 'Identify and assess business risks', FALSE),
(9, 'Talent Acquisition Specialist', 'Recruit and hire new employees', TRUE),
(10, 'Technical Support Engineer', 'Provide technical assistance to customers', FALSE),
(11, 'Digital Marketing Manager', 'Lead digital marketing initiatives', TRUE),
(12, 'Data Engineer', 'Design and maintain data systems', FALSE),
(13, 'UX Researcher', 'Conduct user research to inform product design', TRUE),
(14, 'Compliance Officer', 'Ensure company compliance with regulations', FALSE),
(15, 'IT Project Manager', 'Manage IT projects from inception to completion', TRUE),
(16, 'Blockchain Developer', 'Develop blockchain-based applications', FALSE),
(17, 'Growth Hacker', 'Drive rapid company growth through innovative strategies', TRUE),
(18, 'AR/VR Developer', 'Create augmented and virtual reality experiences', FALSE),
(19, 'Sustainability Consultant', 'Advise on sustainable business practices', TRUE),
(20, 'AI Ethics Researcher', 'Study ethical implications of AI technologies', FALSE);


INSERT INTO location (street, city, `state`, country, postcode) VALUES
('123 Main St', 'New York', 'NY', 'USA', 10001),
('456 Elm St', 'Los Angeles', 'CA', 'USA', 90001),
('789 Oak Ave', 'Chicago', 'IL', 'USA', 60601),
('321 Pine Rd', 'Houston', 'TX', 'USA', 77001),
('654 Maple Dr', 'Phoenix', 'AZ', 'USA', 85001),
('987 Cedar Ln', 'Philadelphia', 'PA', 'USA', 19101),
('147 Birch Blvd', 'San Antonio', 'TX', 'USA', 78201),
('258 Spruce St', 'San Diego', 'CA', 'USA', 92101),
('369 Willow Way', 'Dallas', 'TX', 'USA', 75201),
('159 Sycamore Ave', 'San Jose', 'CA', 'USA', 95101),
('753 Ash St', 'Austin', 'TX', 'USA', 73301),
('951 Poplar Rd', 'Jacksonville', 'FL', 'USA', 32201),
('357 Chestnut Ln', 'San Francisco', 'CA', 'USA', 94101),
('852 Walnut Dr', 'Indianapolis', 'IN', 'USA', 46201),
('426 Elm St', 'Columbus', 'OH', 'USA', 43201),
('739 Oak Ave', 'Fort Worth', 'TX', 'USA', 76101),
('314 Pine Rd', 'Charlotte', 'NC', 'USA', 28201),
('628 Maple Dr', 'Seattle', 'WA', 'USA', 98101),
('942 Cedar Ln', 'Denver', 'CO', 'USA', 80201),
('135 Birch Blvd', 'El Paso', 'TX', 'USA', 79901),
('246 Spruce St', 'Detroit', 'MI', 'USA', 48201),
('357 Willow Way', 'Washington', 'DC', 'USA', 20001),
('468 Sycamore Ave', 'Boston', 'MA', 'USA', 02101),
('579 Ash St', 'Memphis', 'TN', 'USA', 38101),
('680 Poplar Rd', 'Nashville', 'TN', 'USA', 37201),
('791 Chestnut Ln', 'Portland', 'OR', 'USA', 97201),
('802 Walnut Dr', 'Oklahoma City', 'OK', 'USA', 73101),
('913 Elm St', 'Las Vegas', 'NV', 'USA', 89101),
('124 Oak Ave', 'Louisville', 'KY', 'USA', 40201),
('235 Pine Rd', 'Baltimore', 'MD', 'USA', 21201),
('346 Maple Dr', 'Milwaukee', 'WI', 'USA', 53201),
('457 Cedar Ln', 'Albuquerque', 'NM', 'USA', 87101),
('568 Birch Blvd', 'Tucson', 'AZ', 'USA', 85701),
('679 Spruce St', 'Fresno', 'CA', 'USA', 93701),
('780 Willow Way', 'Sacramento', 'CA', 'USA', 95801),
('891 Sycamore Ave', 'Long Beach', 'CA', 'USA', 90801),
('902 Ash St', 'Kansas City', 'MO', 'USA', 64101),
('113 Poplar Rd', 'Mesa', 'AZ', 'USA', 85201),
('224 Chestnut Ln', 'Atlanta', 'GA', 'USA', 30301),
('335 Walnut Dr', 'Colorado Springs', 'CO', 'USA', 80901);


INSERT INTO reviewer (major, `name`, `num_co-ops`, `year`, bio, active) VALUES
('Computer Science', 'Alice Johnson', 2, 3, 'Passionate about AI and machine learning', TRUE),
('Mechanical Engineering', 'Bob Williams', 1, 2, 'Love designing and building robots', FALSE),
('Business Administration', 'Carol Brown', 3, 4, 'Aspiring entrepreneur with a focus on sustainable business', TRUE),
('Electrical Engineering', 'David Lee', 2, 3, 'Interested in renewable energy systems', TRUE),
('Psychology', 'Emma Davis', 1, 2, 'Fascinated by cognitive neuroscience', FALSE),
('Biology', 'Frank Miller', 2, 3, 'Researching gene therapy applications', TRUE),
('Economics', 'Grace Wilson', 3, 4, 'Passionate about behavioral economics', TRUE),
('Chemistry', 'Henry Taylor', 1, 2, 'Exploring new materials for energy storage', FALSE),
('Political Science', 'Isabella Martinez', 2, 3, 'Interested in international relations', TRUE),
('Physics', 'Jack Anderson', 3, 4, 'Studying quantum computing', TRUE),
('Marketing', 'Karen Thomas', 1, 2, 'Creative mind with a passion for digital marketing', FALSE),
('Environmental Science', 'Liam White', 2, 3, 'Committed to fighting climate change', TRUE),
('Graphic Design', 'Mia Garcia', 3, 4, 'Skilled in UX/UI design', TRUE),
('Mathematics', 'Noah Robinson', 1, 2, 'Fascinated by number theory', FALSE),
('Nursing', 'Olivia Clark', 2, 3, 'Dedicated to improving patient care', TRUE),
('Computer Engineering', 'Peter King', 3, 4, 'Developing cutting-edge IoT devices', TRUE),
('Finance', 'Quinn Adams', 1, 2, 'Interested in blockchain and cryptocurrency', FALSE),
('Aerospace Engineering', 'Rachel Scott', 2, 3, 'Dreaming of space exploration', TRUE),
('Sociology', 'Samuel Baker', 3, 4, 'Studying the impact of social media on society', TRUE),
('Biomedical Engineering', 'Tara Nelson', 1, 2, 'Working on advanced prosthetics', FALSE),
('Architecture', 'Ulysses Hall', 2, 3, 'Passionate about sustainable urban design', TRUE),
('Data Science', 'Victoria Young', 3, 4, 'Applying machine learning to solve real-world problems', TRUE),
('English Literature', 'William Turner', 1, 2, 'Aspiring novelist and literary critic', FALSE),
('Chemical Engineering', 'Xena Rodriguez', 2, 3, 'Developing eco-friendly plastics', TRUE),
('Anthropology', 'Yannick Dubois', 3, 4, 'Studying cultural evolution in the digital age', TRUE),
('Music Production', 'Zoe Phillips', 1, 2, 'Creating innovative electronic music', FALSE),
('Cybersecurity', 'Adam Foster', 2, 3, 'Protecting digital assets from cyber threats', TRUE),
('Neuroscience', 'Bella Chen', 3, 4, 'Researching brain-computer interfaces', TRUE),
('Civil Engineering', "Connor O\'Brien", 1, 2, 'Designing sustainable infrastructure', FALSE),
('Linguistics', 'Diana Kim', 2, 3, 'Fascinated by language acquisition and AI', TRUE),
('Astronomy', 'Ethan Wright', 3, 4, 'Searching for exoplanets', TRUE),
('Biotechnology', 'Fiona Campbell', 1, 2, 'Developing new gene editing techniques', FALSE),
('Information Systems', 'George Patel', 2, 3, 'Optimizing business processes through technology', TRUE),
('Journalism', 'Hannah Stewart', 3, 4, 'Investigating the future of digital media', TRUE),
('Robotics', 'Ian Nguyen', 1, 2, 'Building autonomous robots for search and rescue', FALSE),
('Public Health', 'Julia Fernandez', 2, 3, 'Promoting global health equity', TRUE),
('Materials Science', 'Kevin Chang', 3, 4, 'Developing smart materials for wearable tech', TRUE),
('Philosophy', 'Leah Morgan', 1, 2, 'Exploring ethics in artificial intelligence', FALSE),
('Marine Biology', 'Michael Collins', 2, 3, 'Studying the impact of climate change on coral reefs', TRUE),
('Game Design', 'Natalie Wood', 3, 4, 'Creating immersive VR experiences', TRUE);


INSERT INTO reviews (positionID, companyID, authorID, title, `num_co-op`, rating, recommend, pay_type, pay, job_type, `text`, verified, date_time) VALUES
(1, 1, 1, 'Great learning experience', 1, 4, TRUE, 'hourly', 25.50, 'Internship', 'I learned a lot during my time here. The team was supportive and the projects were challenging.', TRUE, '2020-05-01 08:30:00'),
(2, 2, 2, 'Challenging but rewarding', 2, 5, TRUE, 'salary', 75000.00, 'Full-time', 'The work was demanding but I grew professionally. Great company culture.', TRUE, '2021-07-12 09:45:00'),
(3, 3, 1, 'Excellent mentorship', 1, 5, TRUE, 'hourly', 30.00, 'Co-op', 'The mentors were fantastic. I gained valuable industry insights.', FALSE, '2020-11-23 10:15:00'),
(4, 4, 2, 'Fast-paced environment', 3, 4, TRUE, 'salary', 85000.00, 'Full-time', 'Always busy but in a good way. Lots of opportunities to take initiative.', TRUE, '2022-02-10 13:30:00'),
(5, 5, 1, 'Good work-life balance', 2, 4, TRUE, 'hourly', 22.00, 'Part-time', 'Flexible hours and understanding management. Great for students.', FALSE, '2023-01-09 14:45:00'),
(6, 6, 2, 'Innovative projects', 1, 5, TRUE, 'salary', 90000.00, 'Full-time', 'Worked on cutting-edge technology. Very exciting and fulfilling.', TRUE, '2022-05-19 11:00:00'),
(7, 7, 1, 'Supportive team', 1, 4, TRUE, 'hourly', 28.00, 'Internship', 'Everyone was willing to help. Great collaborative atmosphere.', FALSE, '2020-08-25 16:15:00'),
(8, 8, 2, 'Room for growth', 2, 4, TRUE, 'salary', 80000.00, 'Full-time', 'Many opportunities for professional development and advancement.', TRUE, '2021-04-02 12:00:00'),
(9, 9, 1, 'Valuable industry experience', 1, 5, TRUE, 'hourly', 26.50, 'Co-op', 'Gained practical skills that are highly relevant in the job market.', FALSE, '2022-11-30 17:00:00'),
(10, 10, 2, 'Competitive compensation', 3, 5, TRUE, 'salary', 95000.00, 'Full-time', 'Excellent pay and benefits package. Felt valued as an employee.', TRUE, '2023-06-15 09:00:00'),
(11, 11, 1, 'Interesting challenges', 2, 4, TRUE, 'hourly', 24.00, 'Part-time', 'Each day brought new and exciting problems to solve.', FALSE, '2020-03-05 08:45:00'),
(12, 12, 2, 'Great company culture', 1, 5, TRUE, 'salary', 82000.00, 'Full-time', 'Fun work environment with regular team-building activities.', TRUE, '2021-09-21 14:00:00'),
(13, 13, 1, 'Flexible work arrangements', 1, 4, TRUE, 'hourly', 27.00, 'Internship', 'Appreciated the option to work remotely when needed.', FALSE, '2021-12-11 10:30:00'),
(14, 14, 2, 'Strong leadership', 2, 5, TRUE, 'salary', 88000.00, 'Full-time', 'Management was transparent and provided clear direction.', TRUE, '2022-08-14 15:00:00'),
(15, 15, 1, 'Hands-on experience', 1, 4, TRUE, 'hourly', 23.50, 'Co-op', 'Got to work on real projects that impacted the business.', FALSE, '2020-10-22 13:30:00'),
(16, 16, 2, 'Collaborative environment', 3, 4, TRUE, 'salary', 78000.00, 'Full-time', 'Great teamwork and open communication across departments.', TRUE, '2023-02-17 11:15:00'),
(17, 17, 1, 'Learning opportunities', 2, 5, TRUE, 'hourly', 25.00, 'Part-time', 'Constant chances to learn new skills and technologies.', FALSE, '2020-09-18 12:30:00'),
(18, 18, 2, 'Impactful work', 1, 5, TRUE, 'salary', 92000.00, 'Full-time', 'Felt like my work was making a difference in the industry.', TRUE, '2024-01-05 08:00:00'),
(19, 19, 1, 'Supportive management', 1, 4, TRUE, 'hourly', 29.00, 'Internship', 'Managers were always available and willing to provide guidance.', FALSE, '2021-03-14 17:30:00'),
(20, 20, 2, 'Career growth', 2, 5, TRUE, 'salary', 86000.00, 'Full-time', 'Clear path for advancement within the company.', TRUE, '2023-05-11 14:45:00'),
(21, 21, 1, 'Diverse project exposure', 1, 4, TRUE, 'hourly', 26.00, 'Co-op', 'Worked on a variety of projects across different domains.', FALSE, '2021-08-27 16:30:00'),
(22, 22, 2, 'Innovative company', 3, 5, TRUE, 'salary', 98000.00, 'Full-time', "Always pushing the boundaries of what\'s possible in the industry.", TRUE, '2023-11-19 10:00:00'),
(23, 23, 1, 'Friendly colleagues', 2, 4, TRUE, 'hourly', 24.50, 'Part-time', 'Great people to work with, made coming to work enjoyable.', FALSE, '2021-10-03 09:30:00'),
(24, 24, 2, 'Professional development', 1, 5, TRUE, 'salary', 84000.00, 'Full-time', 'Company invested in employee growth through training and conferences.', TRUE, '2020-07-14 15:00:00'),
(25, 25, 1, 'Challenging projects', 1, 4, TRUE, 'hourly', 28.50, 'Internship', 'Assigned to complex projects that pushed me to grow.', FALSE, '2022-04-21 11:30:00'),
(26, 26, 2, 'Work-life balance', 2, 4, TRUE, 'salary', 79000.00, 'Full-time', 'Reasonable hours and respect for personal time.', TRUE, '2023-03-03 12:15:00'),
(27, 27, 1, 'Innovative technology', 1, 5, TRUE, 'hourly', 27.50, 'Co-op', 'Exposure to cutting-edge tools and technologies.', FALSE, '2022-09-06 14:45:00'),
(28, 28, 2, 'Inclusive workplace', 3, 5, TRUE, 'salary', 91000.00, 'Full-time', 'Diverse and welcoming environment for all employees.', TRUE, '2021-06-18 13:00:00'),
(29, 29, 1, 'Mentorship program', 2, 4, TRUE, 'hourly', 25.50, 'Part-time', 'Paired with experienced professionals for guidance.', FALSE, '2020-02-14 16:00:00'),
(30, 30, 2, 'Competitive industry position', 1, 5, TRUE, 'salary', 89000.00, 'Full-time', 'Company is a leader in the field with a strong market presence.', TRUE, '2024-03-07 09:00:00'),
(1, 1, 2, 'Room for improvement', 1, 3, FALSE, 'hourly', 22.00, 'Internship', 'Some processes could be more efficient. Communication was lacking at times.', TRUE, '2023-08-01 12:00:00'),
(2, 2, 1, 'High pressure environment', 2, 3, FALSE, 'salary', 72000.00, 'Full-time', 'Very demanding workload with tight deadlines. Not for everyone.', TRUE, '2024-03-07 09:00:00'),
(3, 3, 2, 'Limited resources', 1, 3, FALSE, 'hourly', 26.00, 'Co-op', 'Often had to make do with outdated tools and technology.', FALSE, '2024-03-07 09:00:00'),
(4, 4, 1, 'Bureaucratic processes', 3, 2, FALSE, 'salary', 76000.00, 'Full-time', 'Too much red tape. Simple tasks took forever to complete.', TRUE, '2024-03-07 09:00:00'),
(5, 5, 2, 'Lack of direction', 2, 2, FALSE, 'hourly', 20.00, 'Part-time', 'Objectives were often unclear. Felt lost at times.', FALSE, '2024-03-07 09:00:00');


INSERT INTO questions (postId, author, `text`) VALUES
(1, 'Emily Chen', 'What skills did you find most valuable during your internship?'),
(1, 'Michael Johnson', 'How was the work-life balance during your time at the company?'),
(2, 'Sarah Lee', 'Did you have opportunities for professional development?'),
(2, 'David Brown', 'How would you describe the company culture?'),
(3, 'Rachel Kim', 'Were there any challenges you faced during your co-op?'),
(3, 'Alex Turner', 'Did the job align with your career goals?'),
(1, 'Olivia Martinez', 'How was the onboarding process?'),
(2, 'Ethan Wilson', 'Did you receive regular feedback from your supervisor?'),
(3, 'Sophia Nguyen', 'Were there opportunities for networking within the company?'),
(1, 'Daniel Park', 'How diverse and inclusive was the workplace?'),
(2, 'Emma Davis', 'Did you feel supported by your team members?'),
(3, 'Ryan Thompson', 'What was the most valuable lesson you learned during your time there?'),
(1, 'Isabella Rodriguez', 'How did this experience compare to your expectations?'),
(2, 'William Chang', 'Were there opportunities for remote work or flexible hours?'),
(3, 'Ava Patel', 'Did you feel your contributions were valued by the company?'),
(1, 'Noah Garcia', "How would you rate the company\'s technology and tools?"),
(2, 'Mia Lewis', 'Were there any social or team-building activities?'),
(3, 'Liam Wright', 'Did you receive adequate training for your role?'),
(1, 'Charlotte Kim', 'How approachable were the senior management?'),
(2, 'Jacob Anderson', 'Did you have a mentor during your time at the company?'),
(3, 'Amelia Taylor', 'Were there opportunities for cross-departmental collaboration?'),
(1, 'Benjamin Lee', 'How would you describe the pace of work?'),
(2, 'Harper Wilson', 'Did you feel the compensation was fair for your role?'),
(3, 'Lucas Martinez', 'Were there any aspects of the job that surprised you?'),
(1, 'Evelyn Chen', "How eco-friendly were the company\'s practices?"),
(2, 'Mason Brown', 'Did you feel there were growth opportunities within the company?'),
(3, 'Abigail Johnson', 'How would you rate the overall employee satisfaction?'),
(1, 'Elijah Davis', 'Were there any employee resource groups or diversity initiatives?'),
(2, 'Elizabeth Thompson', 'How did the company handle work-related stress?'),
(3, 'James Rodriguez', 'Did you feel the company values aligned with your own?'),
(1, 'Sofia Garcia', 'How accessible was management for questions or concerns?'),
(2, 'Alexander Nguyen', 'Were there opportunities to work on challenging projects?'),
(3, 'Grace Lee', "How would you describe the company\'s approach to innovation?"),
(1, 'Christopher Park', 'Did you feel the company invested in your professional growth?'),
(2, 'Chloe Turner', "How would you rate the company\'s commitment to work-life balance?"),
(3, 'Andrew Kim', 'Were there opportunities for leadership development?'),
(1, 'Zoe Wilson', 'How transparent was the company about its goals and performance?'),
(2, 'Samuel Martinez', 'Did you feel your ideas were heard and considered?'),
(3, 'Lily Chang', "How would you describe the company\'s approach to customer service?"),
(1, 'Joseph Taylor', 'Were there any unique perks or benefits offered by the company?');



INSERT INTO answers (postId, questionId, author, `text`) VALUES
(1, 1, 'John Smith', 'The most valuable skills I gained were in project management and data analysis.'),
(1, 2, 'Emma Watson', 'The work-life balance was excellent, with flexible hours and respect for personal time.'),
(2, 3, 'Chris Evans', 'Yes, there were numerous workshops and training sessions available.'),
(2, 4, 'Natalie Portman', 'The company culture was collaborative and innovative, with a focus on teamwork.'),
(3, 5, 'Tom Holland', 'The main challenge was adapting to the fast-paced environment, but it was a great learning experience.'),
(3, 6, 'Zendaya', 'Absolutely, this co-op aligned perfectly with my career goals in software development.'),
(1, 7, 'Robert Downey Jr.', 'The onboarding process was thorough and well-organized, making it easy to integrate into the team.'),
(2, 8, 'Scarlett Johansson', 'Yes, I had weekly check-ins with my supervisor for feedback and guidance.'),
(3, 9, 'Chris Hemsworth', 'There were many networking events and opportunities to connect with colleagues across departments.'),
(1, 10, 'Elizabeth Olsen', 'The workplace was very diverse and inclusive, with a strong emphasis on equality.'),
(2, 11, 'Mark Ruffalo', 'My team was incredibly supportive, always ready to help and share knowledge.'),
(3, 12, 'Jeremy Renner', 'The most valuable lesson was the importance of clear communication in a professional setting.'),
(1, 13, 'Paul Rudd', 'The experience exceeded my expectations in terms of responsibility and learning opportunities.'),
(2, 14, 'Karen Gillan', 'Yes, the company offered flexible work arrangements, including remote work options.'),
(3, 15, 'Benedict Cumberbatch', 'Definitely, my ideas were often implemented and I felt my work made a real impact.'),
(1, 16, 'Brie Larson', 'The company used cutting-edge technology and tools, which was impressive.'),
(2, 17, 'Don Cheadle', 'There were regular team-building activities and social events to foster camaraderie.'),
(3, 18, 'Chadwick Boseman', 'The training was comprehensive and ongoing, ensuring we were always up-to-date with industry trends.'),
(1, 19, 'Anthony Mackie', 'Senior management was very approachable and open to ideas from all levels.'),
(2, 20, 'Sebastian Stan', 'Yes, I was assigned a mentor who provided invaluable guidance throughout my time there.'),
(3, 21, 'Tom Hiddleston', 'Cross-departmental collaboration was encouraged, leading to innovative solutions.'),
(1, 22, 'Chris Pratt', 'The pace of work was fast but manageable, with a good balance of challenging and routine tasks.'),
(2, 23, 'Zoe Saldana', 'The compensation was competitive and fair, with good benefits included.'),
(3, 24, 'Dave Bautista', 'I was surprised by the level of responsibility given to interns and co-op students.'),
(1, 25, 'Vin Diesel', 'The company had strong eco-friendly initiatives and encouraged sustainable practices.'),
(2, 26, 'Bradley Cooper', 'There were clear paths for growth within the company, including mentorship programs.'),
(3, 27, 'Gwyneth Paltrow', 'Overall employee satisfaction seemed high, with low turnover rates.'),
(1, 28, 'Jon Favreau', 'There were several employee resource groups and active diversity initiatives.'),
(2, 29, 'Samuel L. Jackson', 'The company provided resources for stress management and mental health support.'),
(3, 30, 'Cobie Smulders', "The company\'s values of innovation and integrity aligned well with my own."),
(1, 31, 'Clark Gregg', 'Management was easily accessible and responsive to questions and concerns.'),
(2, 32, 'Hayley Atwell', 'I had the opportunity to work on several challenging and impactful projects.'),
(3, 33, 'James Spader', 'The company fostered a culture of innovation, encouraging new ideas at all levels.'),
(1, 34, 'Emily VanCamp', 'The company invested in our growth through training programs and conference attendance.'),
(2, 35, 'Frank Grillo', 'Work-life balance was a priority, with policies supporting personal time and mental health.'),
(3, 36, 'Linda Cardellini', 'There were leadership workshops and opportunities to lead small teams on projects.'),
(1, 37, 'Aaron Taylor-Johnson', 'The company was very transparent about its goals and regularly shared performance updates.'),
(2, 38, 'Elizabeth Debicki', 'My ideas were always welcomed and often implemented, making me feel valued.'),
(3, 39, 'Pom Klementieff', 'Customer service was a top priority, with a focus on exceeding client expectations.'),
(1, 40, 'Letitia Wright', 'The company offered unique perks like on-site fitness classes and catered lunches.');


INSERT INTO companylocation (companyID, locID) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
(3, 11), (3, 12), (3, 13), (3, 14), (3, 15),
(4, 16), (4, 17), (4, 18), (4, 19), (4, 20),
(5, 21), (5, 22), (5, 23), (5, 24), (5, 25),
(6, 26), (6, 27), (6, 28), (6, 29), (6, 30),
(7, 31), (7, 32), (7, 33), (7, 34), (7, 35),
(8, 36), (8, 37), (8, 38), (8, 39), (8, 40),
(9, 1), (9, 6), (9, 11), (9, 16), (9, 21),
(10, 2), (10, 7), (10, 12), (10, 17), (10, 22),
(11, 3), (11, 8), (11, 13), (11, 18), (11, 23),
(12, 4), (12, 9), (12, 14), (12, 19), (12, 24),
(13, 5), (13, 10), (13, 15), (13, 20), (13, 25),
(14, 26), (14, 31), (14, 36), (14, 1), (14, 6),
(15, 27), (15, 32), (15, 37), (15, 2), (15, 7),
(16, 28), (16, 33), (16, 38), (16, 3), (16, 8),
(17, 29), (17, 34), (17, 39), (17, 4), (17, 9),
(18, 30), (18, 35), (18, 40), (18, 5), (18, 10),
(19, 1), (19, 11), (19, 21), (19, 31), (19, 40),
(20, 2), (20, 12), (20, 22), (20, 32), (20, 39);


INSERT INTO `companyIndustry` (industryID, companyID) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
(3, 11), (3, 12), (3, 13), (3, 14), (3, 15),
(4, 16), (4, 17), (4, 18), (4, 19), (4, 20),
(5, 1), (5, 6), (5, 11), (5, 16), (5, 20),
(6, 2), (6, 7), (6, 12), (6, 17), (6, 19),
(7, 3), (7, 8), (7, 13), (7, 18),
(8, 4), (8, 9), (8, 14), (8, 19),
(9, 5), (9, 10), (9, 15), (9, 20), (9, 16),
(10, 1), (10, 7), (10, 13), (10, 19), (10, 15),
(11, 2), (11, 8), (11, 14), (11, 20),
(12, 3), (12, 9), (12, 15), (12, 1), (12, 13),
(13, 4), (13, 10), (13, 16), (13, 2),
(14, 5), (14, 11), (14, 17), (14, 3),
(15, 6), (15, 12), (15, 18), (15, 4),
(16, 7), (16, 13), (16, 19), (16, 5), (16, 9),
(17, 8), (17, 14), (17, 20), (17, 6),
(18, 9), (18, 15), (18, 1), (18, 7),
(19, 10), (19, 16), (19, 2), (19, 8),
(20, 11), (20, 17), (20, 3), (20, 9), (20, 5);

INSERT INTO `positionTargetCollege` (collegeID, positionID) VALUES
-- Khoury College of Computer Sciences (ID: 1)
(1, 1), (1, 2), (1, 3), (1, 7), (1, 11), (1, 13), (1, 15), (1, 18), (1, 19), (1, 21),
(1, 23), (1, 24), (1, 27), (1, 28),

-- D'Amore-McKim School of Business (ID: 2)
(2, 3), (2, 4), (2, 5), (2, 6), (2, 11), (2, 12), (2, 17), (2, 20), (2, 22), (2, 26), 
(2, 28), (2, 29),

-- Bouvé College of Health Sciences (ID: 3)
(3, 5), (3, 8), (3, 9), (3, 13), (3, 14), (3, 19), (3, 21), (3, 29),

-- College of Arts, Media and Design (ID: 4)
(4, 4), (4, 6), (4, 14), (4, 16), (4, 20), (4, 22), (4, 25), (4, 30),

-- College of Professional Studies (ID: 5)
(5, 7), (5, 12), (5, 15), (5, 22), (5, 23), (5, 26),

-- College of Science (ID: 6)
(6, 1), (6, 8), (6, 16), (6, 18), (6, 19), (6, 20), (6, 24),

-- College of Social Sciences and Humanities (ID: 7)
(7, 6), (7, 9), (7, 11), (7, 14), (7, 17), (7, 22), (7, 25),

-- Northeastern University School of Law (ID: 8)
(8, 10), (8, 14), (8, 18), (8, 22), (8, 26),
