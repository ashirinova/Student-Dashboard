-- ========================================================
-- LAYİHƏ: Student Performance Dashboard (Database Schema)
-- CLEAN CODE PRİNSİPLƏRİ İLƏ HAZIRLANMIŞ MƏLUMAT BAZASI
-- ========================================================

-- 1. Verilənlər Bazasının Yaradılması
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'UniversityDB')
BEGIN
    CREATE DATABASE UniversityDB;
END;
GO

USE UniversityDB;
GO

-- 2. Tələbələr Cədvəlinin Yaradılması
IF OBJECT_ID('dbo.Students', 'U') IS NOT NULL
    DROP TABLE dbo.Students;
GO

CREATE TABLE Students (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Score FLOAT NOT NULL CONSTRAINT CHK_Student_Score CHECK (Score >= 0 AND Score <= 100),
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- Performance Optimization: Axtarış və Çeşidləmə üçün İndekslər
CREATE INDEX IX_Students_Score ON Students(Score DESC);
CREATE INDEX IX_Students_Name ON Students(Name);
GO

-- Nümunə Məlumatların Daxil Edilməsi
INSERT INTO Students (Name, Score) VALUES 
('Ali', 85.0),
('Leyla', 72.0),
('Murad', 48.0),
('Aysel', 91.0),
('Kamran', 63.0),
('Nigar', 95.0),
('Elvin', 55.0);
GO

-- ========================================================
-- TASK 1: MAIN STORED PROCEDURE (Müəllimin Tələb Etdiyi)
-- Tələbə Nəticələrini və Qiymətini (Grade) Hesablayan Prosedur
-- ========================================================
IF OBJECT_ID('dbo.GetStudentResult', 'P') IS NOT NULL
    DROP PROCEDURE dbo.GetStudentResult;
GO

CREATE PROCEDURE GetStudentResult
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        Id,
        Name,
        Score,
        CASE 
            WHEN Score >= 90 THEN 'A'
            WHEN Score >= 80 THEN 'B'
            WHEN Score >= 70 THEN 'C'
            WHEN Score >= 60 THEN 'D'
            ELSE 'F'
        END AS Grade
    FROM Students
    ORDER BY Score DESC;
END;
GO

-- ========================================================
-- BONUS STORED PROCEDURES (Maksimum Qiymət Üçün)
-- ========================================================

-- Bonus 1: Statistikaları SQL Server Səviyyəsində Hesablayan Prosedur
IF OBJECT_ID('dbo.GetStudentStatistics', 'P') IS NOT NULL
    DROP PROCEDURE dbo.GetStudentStatistics;
GO

CREATE PROCEDURE GetStudentStatistics
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        COUNT(*) AS TotalStudents,
        ROUND(AVG(Score), 1) AS AverageScore,
        MAX(Score) AS HighestScore,
        MIN(Score) AS LowestScore
    FROM Students;
END;
GO

-- Bonus 2: Tələbə Əlavə Edən Təhlükəsiz Stored Procedure
IF OBJECT_ID('dbo.AddStudent', 'P') IS NOT NULL
    DROP PROCEDURE dbo.AddStudent;
GO

CREATE PROCEDURE AddStudent
    @StudentName NVARCHAR(100),
    @StudentScore FLOAT
AS
BEGIN
    SET NOCOUNT ON;

    IF @StudentName IS NULL OR LEN(TRIM(@StudentName)) = 0
    BEGIN
        RAISERROR('Tələbə adı boş ola bilməz!', 16, 1);
        RETURN;
    END

    INSERT INTO Students (Name, Score) 
    VALUES (TRIM(@StudentName), @StudentScore);
END;
GO