-- create a student table.
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(50) NOT NULL,
    year INTEGER
);

--Insert a student:
INSERT INTO students (name, course, year)
VALUES ('Rahul', 'CSE', 3);

-- Retrieve students:
SELECT * FROM students;


-- Update a student:
UPDATE students
SET course = 'IT'
WHERE id = 1;


-- Delete a student:
DELETE FROM students
WHERE id = 1;