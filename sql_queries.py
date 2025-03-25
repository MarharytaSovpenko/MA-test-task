# Select the number of created leads per week grouped by course type
query_1 = """
    --SET DATEFIRST 1 --This will count Monday as the first day of the week; by default - Sunday
    SELECT
        COUNT(*) AS number_of_leads,
        DATEPART(week, created_at) AS week,
        type AS course_type
    FROM
        leads
        LEFT JOIN courses ON  leads.course_id = courses.id
    GROUP BY  DATEPART(week, created_at), type
    ORDER BY number_of_leads, week, course_type
"""

# Select the number of WON flex leads per country created from 01.01.2024
query_2 = """
    SELECT
        COUNT(*) AS number_of_leads,
        country_name
    FROM
        leads
        LEFT JOIN courses ON  leads.course_id = courses.id
        LEFT JOIN users  ON leads.user_id = users.id
        LEFT JOIN domains ON users.domain_id = domains.id
    WHERE 1=1
        AND status = 'WON'
        AND type = 'FLEX'
        AND leads.created_at >= '2024-01-01'
    GROUP BY country_name
    ORDER BY number_of_leads
"""

# Select the email, lead id and lost reason for users who have lost flex leads from 01.07.2024
query_3 = """
    SELECT
        email,
        leads.id,
        lost_reason
    FROM
        leads
        LEFT JOIN courses ON  leads.course_id = courses.id
        LEFT JOIN users  ON leads.user_id = users.id
    WHERE 1=1
        AND status = 'LOST'
        AND type = 'FLEX'
        AND updated_at >= '2024-07-01'
    ORDER BY email
"""
