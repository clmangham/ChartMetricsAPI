-- Endpoint 1 raw SQL example
SELECT
	cd.Id, cd.ChartTime, cd.VALUENUM, cd.ERROR, cd.WARNING, cd.Stopped,
	ot.Name,
	um.Name
FROM Chart_Data cd
LEFT JOIN Observation_Type ot ON ot.Id = cd.Observation_Type_Id
LEFT JOIN Result_Status rs ON rs.Id = cd.Result_Status_Id
LEFT JOIN Unit_Of_Measure um ON um.Id = cd.Unit_Of_Measure_Id
WHERE cd.Id in (1, 2, 3);