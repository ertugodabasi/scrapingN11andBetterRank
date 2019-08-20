SELECT
    CASE
    WHEN POSITION('badge badgeSuccess' in iq3."BranchBadges" ) >0
        THEN 1
        ELSE 0
    END AS SuccessFullBranch,
    CASE
    WHEN POSITION('badge badgeFast' in iq3."BranchBadges" ) >0
        THEN 1
        ELSE 0
    END AS FastBranch,
       iq3."AvgRating",iq3."ReviewCount",* FROM
(
SELECT ROUND(CAST(iq2.BayesianRating AS NUMERIC),2) "RoundedBayesianRating",*
FROM (
         SELECT ((m-std) * (c) + iq1."ReviewCount" * iq1."AvgRating") / (iq1.c + iq1."ReviewCount") BayesianRating
              , *
         FROM (
                  SELECT AVG("AvgRating") OVER (PARTITION BY 1)   m,
                         AVG("ReviewCount") OVER (PARTITION BY 1) c,
                         STDDEV_SAMP("AvgRating") OVER (PARTITION BY 1) std,
                         *

                  FROM public.n11 as n
                  WHERE n."AvgRating" notnull
              ) iq1) iq2 )iq3
order by iq3."RoundedBayesianRating" DESC,iq3."BranchPoint" DESC ,iq3."Price" ;
