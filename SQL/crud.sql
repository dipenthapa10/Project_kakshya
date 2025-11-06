-- Dipen Thapa and Bishal Regmi 
-- Project 1

-- CRUD Instructor 

INSERT INTO Instructor (instructor_ID, first_name, middle_name, last_name, email, dept_ID)
SELECT 101, 'Grace', NULL, 'Hopper', 'grace@kent.edu', d.dept_ID
FROM Department d
WHERE d.name = 'Computer';

SELECT i.instructor_ID, i.first_name, i.last_name, i.email, d.name AS department
FROM Instructor i
JOIN Department d ON d.dept_ID = i.dept_ID;

UPDATE Instructor
SET email = 'grace.hopper@kent.edu'
WHERE email = 'grace@kent.edu';

DELETE FROM Instructor
WHERE email = 'grace.hopper@kent.edu';

-- CRUD Student

INSERT INTO Student (student_ID, first_name, middle_name, last_name, email, dept_ID)
SELECT 201, 'Omar', NULL, 'Diaz', 'od@kent.edu', d.dept_ID
FROM Department d
WHERE d.name = 'Computer';

SELECT s.student_ID, s.first_name, s.last_name, s.email, d.name AS department
FROM Student s
JOIN Department d ON d.dept_ID = s.dept_ID;

UPDATE Student
SET email = 'od_updated@kent.edu'
WHERE email = 'od@kent.edu';

DELETE FROM Student
WHERE email = 'od_updated@kent.edu';

-- CRUD Section

INSERT INTO Section (section_ID, course_ID, section_no, semester, instructor_ID, building, room_number, timeslot_ID)
VALUES (
  301,
  (SELECT course_ID FROM Course WHERE course_no = 'COMP101'),
  '003',
  'Spring 2026',
  (SELECT instructor_ID FROM Instructor WHERE email = 'gvillalobos@kent.edu'),
  'SCI',
  '110',
  (SELECT timeslot_ID FROM Timeslot WHERE weekday = 'Tuesday' AND start_time = '10:30:00' AND end_time = '11:45:00')
);

SELECT s.section_ID, s.section_no, s.semester, c.course_no, c.title, i.first_name AS instructor
FROM Section s
JOIN Course c ON c.course_ID = s.course_ID
LEFT JOIN Instructor i ON i.instructor_ID = s.instructor_ID;

UPDATE Section
SET semester = 'Summer 2026'
WHERE section_ID = 301;

DELETE FROM Section
WHERE section_ID = 301;

-- CRUD Course

INSERT INTO Course (course_ID, dept_ID, course_no, title, credits)
SELECT 6, d.dept_ID, 'COMP201', 'Advanced Computing', 4
 FROM Department d 
WHERE d.name = 'Computer';

SELECT course_ID, course_no, title, credits, dept_ID 
FROM Course;

UPDATE Course 
SET title = 'Advanced Computing Systems' 
WHERE course_no = 'COMP201';

DELETE FROM Course
WHERE course_no = 'COMP201';
