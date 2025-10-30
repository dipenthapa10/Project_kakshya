

-- DEPARTMENT TABLE

CREATE TABLE Department (
    dept_ID INT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    building VARCHAR(50)
);

-- INSTRUCTOR TABLE

CREATE TABLE Instructor (
    instructor_ID INT PRIMARY KEY,
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    dept_ID INT,
    FOREIGN KEY (dept_ID) REFERENCES Department(dept_ID)
);

-- STUDENT TABLE

CREATE TABLE Student (
    student_ID INT PRIMARY KEY,
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    dept_ID INT,
    FOREIGN KEY (dept_ID) REFERENCES Department(dept_ID),
    FOREIGN KEY (advisor_ID) REFERENCES Instructor(instructor_ID)
);


-- COURSE TABLE

CREATE TABLE Course (
    course_ID INT PRIMARY KEY,
    dept_ID INT,
    course_no VARCHAR(10),
    title VARCHAR(100),
    credits INT,
    FOREIGN KEY (dept_ID) REFERENCES Department(dept_ID)
);


-- PRE-REQUISITE TABLE

CREATE TABLE Pre_Requisite (
    course_ID INT,
    prereq_course_ID INT,
    PRIMARY KEY (course_ID, prereq_course_ID),
    FOREIGN KEY (course_ID) REFERENCES Course(course_ID),
    FOREIGN KEY (prereq_course_ID) REFERENCES Course(course_ID)
);

-- CLASSROOM TABLE
CREATE TABLE Classroom (
    building VARCHAR(50),
    room_number VARCHAR(10),
    capacity INT,
    PRIMARY KEY (building, room_number)
);



-- TIMESLOT TABLE
CREATE TABLE Timeslot (
    timeslot_ID INT PRIMARY KEY,
    weekday VARCHAR(10),
    start_time TIME,
    end_time TIME
);

-- SECTION TABLE
CREATE TABLE Section (
    section_ID INT PRIMARY KEY,
    course_ID INT,
    section_no VARCHAR(10),
    semester VARCHAR(20),
    instructor_ID INT,
    building VARCHAR(50),
    room_number VARCHAR(10),
    timeslot_ID INT,
    FOREIGN KEY (course_ID) REFERENCES Course(course_ID),
    FOREIGN KEY (instructor_ID) REFERENCES Instructor(instructor_ID),
    FOREIGN KEY (building, room_number) REFERENCES Classroom(building, room_number),
    FOREIGN KEY (timeslot_ID) REFERENCES Timeslot(timeslot_ID)
);


-- ENROLLMENT TABLE
CREATE TABLE Enrollment (
    student_ID INT,
    section_ID INT,
    enroll_date DATE,
    grade CHAR(2),
    PRIMARY KEY (student_ID, section_ID),
    FOREIGN KEY (student_ID) REFERENCES Student(student_ID),
    FOREIGN KEY (section_ID) REFERENCES Section(section_ID)
);

