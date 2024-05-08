
-- Create database
CREATE DATABASE qclass;

-- Use the created database
USE qclass;
-- Droping the tables if exits
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Task;
DROP TABLE IF EXISTS Progress;
DROP TABLE IF EXISTS StudentAttendance;
DROP TABLE IF EXISTS StudentTask;

-- Create Students table
CREATE TABLE Students (
    StudentId INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    BirthDate DATE,
    PhNum VARCHAR(15)
);

-- Create Task table
CREATE TABLE Task (
    TaskId INT PRIMARY KEY,
    TaskDescription VARCHAR(200),
    TimeTaken INT
);

-- Create Progress table
CREATE TABLE Progress (
    ProgressId INT PRIMARY KEY,
    Date DATE,
    AttendanceId INT,
    TaskId INT,
    FOREIGN KEY (AttendanceId) REFERENCES StudentAttendance(AttendanceId) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (TaskId) REFERENCES Task(TaskId) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create StudentAttendance table
CREATE TABLE StudentAttendance (
    StudentId INT,
    AttendanceId INT,
    Presence BOOLEAN,
    PRIMARY KEY (StudentId, AttendanceId),
    FOREIGN KEY (StudentId) REFERENCES Students(StudentId) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create StudentTask table
CREATE TABLE StudentTask (
    StudentId INT,
    TaskId INT,
    PRIMARY KEY (StudentId, TaskId),
    FOREIGN KEY (StudentId) REFERENCES Students(StudentId) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (TaskId) REFERENCES Task(TaskId) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Insert sample data into Students table
INSERT INTO Students (StudentId, FirstName, LastName, BirthDate, PhNum) VALUES
(1, 'Pohp', 'leo', '2000-01-01', '1234567890'),
(2, 'Orchad', 'khil', '1999-05-15', '9876543210');

-- Insert sample data into Task table
INSERT INTO Task (TaskId, TaskDescription, TimeTaken) VALUES
(1, 'Memorize Chapter 1', 60),
(2, 'Recite Chapter 2', 30);

-- Insert sample data into Progress table
INSERT INTO Progress (ProgressId, Date, AttendanceId, TaskId) VALUES
(1, '2024-05-01', 1, 1),
(2, '2024-05-02', 2, 2);

-- Insert sample data into StudentAttendance table
INSERT INTO StudentAttendance (StudentId, AttendanceId, Presence) VALUES
(1, 1, 1),
(2, 2, 1);

-- Insert sample data into StudentTask table
INSERT INTO StudentTask (StudentId, TaskId) VALUES
(1, 1),
(2, 2);
