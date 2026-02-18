Return the result in a json format.
If a schema/table/file name is found, return it as a key value pair in the json. 
response should be in the following json format
{
   "table": "table/schema/file",
   "query": "query",
   "points": [
     " information about query"
   ],
   "explanation": "This query extracts name information from the people table. It specifically targets the column containing identity data for all records."
 } 
Keep the response to the point and short. Give bullet points. Explanation should not exceed 50 words.