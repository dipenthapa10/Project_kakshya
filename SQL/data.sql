-- Dipen Thapa and Bishal Regmi 
-- Project 1

-- DEPARTMENT 
INSERT INTO Department (dept_ID, name, building) VALUES
(1,'Math','MSB'),
(2,'Computer','SCI'),
(3,'Physics','ENG'),
(4,'Chemistry','LAB'),
(5,'Exercise','REC');

-- INSTRUCTOR TABLE
INSERT INTO Instructor (instructor_ID, first_name, middle_name, last_name, email, dept_ID) VALUES
(1,'Giovanni',NULL,'Villa','gvillalobos@kent.edu',2),
(2,'Maletic',NULL,'Athletic','mathletic@kent.edu',1),
(3,'Mikhael',NULL,'Nest','mnesterenko@kent.edu',3),
(4,'Gokarna',NULL,'Sharma','gsharma@kent.edu',4),
(5,'Dippz',NULL,'Newton','aakbar@kent.edu',5);

-- STUDENT TABLE
INSERT INTO Student (student_ID, first_name, middle_name, last_name, email, dept_ID) VALUES
(1,'Bishal',NULL,'Regmi','bregmi17@kent.edu',2),
(2,'Dipen',NULL,'Thapa','dthapa24@kent.edu',1),
(3,'Anuj',NULL,'Manandhar','amanandhar31@kent.edu',3),
(4,'Suyog',NULL,'Karki','skarki42@kent.edu',4),
(5,'Aarav',NULL,'Dhungana','adhungana55@kent.edu',5);

-- COURSE TABLE
INSERT INTO Course (course_ID, dept_ID, course_no, title, credits) VALUES
(1,1,'MATH101','Calculus I',4),
(2,2,'COMP101','Intro to Computing',3),
(3,3,'PHYS101','General Physics I',4),
(4,4,'CHEM101','General Chemistry I',4),
(5,5,'SPORT101','Sports Science Basics',3);

-- PRE-REQUISITE TABLE
INSERT INTO Pre_Requisite (course_ID, prereq_course_ID, prereq_title) VALUES
(2, 1, 'Calculus I'),
(3, 1, 'Calculus I'),
(4, 2, 'Intro to Computing'),
(5, 3, 'General Physics I'),
(5, 1, 'Calculus I');

-- CLASSROOM TABLE
INSERT INTO Classroom (building, room_number, capacity) VALUES
('MSB','201',40),
('SCI','110',35),
('ENG','101',30),
('LAB','210',25),
('GYM','001',60);

-- TIMESLOT TABLE
INSERT INTO Timeslot (timeslot_ID, weekday, start_time, end_time) VALUES
(1,'Monday','09:00:00','10:15:00'),
(2,'Tuesday','10:30:00','11:45:00'),
(3,'Wednesday','12:00:00','13:15:00'),
(4,'Thursday','13:30:00','14:45:00'),
(5,'Friday','15:00:00','16:15:00');

-- SECTION TABLE
INSERT INTO Section (section_ID, course_ID, section_no, semester, instructor_ID, building, room_number, timeslot_ID) VALUES
(1,1,'001','Fall 2025',2,'MSB','201',1),
(2,2,'001','Fall 2025',1,'SCI','110',2),
(3,3,'001','Fall 2025',3,'ENG','101',3),
(4,4,'001','Fall 2025',4,'LAB','210',4),
(5,5,'001','Fall 2025',5,'GYM','001',5);

-- ENROLLMENT TABLE 
INSERT INTO Enrollment (student_ID, section_ID, enroll_semester, enroll_year, grade)
VALUES (
    (SELECT student_ID FROM Student WHERE email = 'bregmi17@kent.edu'),
    (SELECT s.section_ID 
     FROM Section s 
     JOIN Course c ON s.course_ID = c.course_ID
     WHERE c.course_no = 'COMP101' AND s.section_no = '001'),
    'Fall',
    2025,
    'A'
);
