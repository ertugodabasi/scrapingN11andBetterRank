-------------------------------------------------
-- Ranks with Bayesian Average
-------------------------------------------------
SELECT "Name",
       ROW_NUMBER() over (ORDER BY "BayesianRating" DESC ) as "newProductPosition",
       "ProductPosition",
       "BayesianRating",
       "ReviewCount",
       "AvgRating",
       "Price",
       "Url"
FROM (
         SELECT (m * c + "ReviewCount" * "AvgRating") /
                (c + "ReviewCount") as "BayesianRating"
              , *
         FROM (
                  SELECT AVG("AvgRating") OVER ()   as m,
                         AVG("ReviewCount") OVER () as c,
                         *

                  FROM public.n11 as n
                  WHERE n."AvgRating" notnull
              ) iq1) iq2


-------------------------------------------------
-- Ranks with Rounded Bayesian Averages and Price
-------------------------------------------------
SELECT "Name",
       ROW_NUMBER() over (ORDER BY "RoundedBayesianRating" DESC, "Price" ASC ) as "newProductPosition",
       "ProductPosition",
       "RoundedBayesianRating",
       "Price",
       "BayesianRating",
       "ReviewCount",
       "AvgRating",
       "Url"
FROM (
         SELECT ROUND(CAST("BayesianRating" AS NUMERIC), 2) "RoundedBayesianRating", *
         FROM (
                  SELECT (m * c + "ReviewCount" * "AvgRating") /
                         (c + "ReviewCount") as "BayesianRating"
                       , *
                  FROM (
                           SELECT AVG("AvgRating") OVER ()   as m,
                                  AVG("ReviewCount") OVER () as c,
                                  *

                           FROM public.n11 as n
                           WHERE n."AvgRating" notnull
                       ) iq1) iq2) iq3
