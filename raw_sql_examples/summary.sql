-- Endpoint 2 raw SQL example
SELECT
    ot.Name AS Observation_Type,
    um.Name AS Unit_Of_Measure,
    COUNT(cd.VALUENUM) AS Num_Admissions,
    MIN(cd.VALUENUM) AS Min_Value,
    MAX(cd.VALUENUM) AS Max_Value,
    SUM(CASE
    WHEN (cd.ERROR IS NULL OR cd.ERROR != 1)
         AND (cd.WARNING IS NULL OR cd.WARNING != 1)
         AND (rs.Name IS NULL OR rs.Name != 'Manual') THEN 1
    ELSE 0
END) AS Valid_Records
FROM
    Chart_Data cd
    LEFT JOIN Observation_Type ot ON cd.Observation_Type_Id = ot.Id
    LEFT JOIN Result_Status rs ON cd.Result_Status_Id = rs.Id
    LEFT JOIN Unit_Of_Measure um ON cd.Unit_Of_Measure_Id = um.Id
GROUP BY
    ot.Name,
    um.Name;