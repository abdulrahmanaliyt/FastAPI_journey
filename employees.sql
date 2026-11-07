-- Drop the table if it already exists (optional, to start fresh)
DROP TABLE IF EXISTS employees;

-- Create the table with a UNIQUE constraint
CREATE TABLE employees(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    CONSTRAINT unique_employee UNIQUE (name, department)
);

-- Now this INSERT will successfully ignore duplicates on rerun!
INSERT INTO employees (name, department, salary)
VALUES
    ('Rahul', 'IT', 35000),
    ('Aman', 'HR', 30000),
    ('Priya', 'IT', 40000),
	('Abdul Rahman Ali','CSE',50000),
	('Yadav','CSE',50000)
ON CONFLICT (name, department) DO NOTHING;

UPDATE employees
SET salary = 45000
WHERE name = 'Rahul';
SELECT * FROM employees WHERE name = 'Rahul'; 

-- SELECT * FROM employees 
-- WHERE department = 'IT';

-- DELETE FROM employees
-- WHERE name = 'Aman';
SELECT * FROM employees

-- SELECT COUNT(*) FROM employees;