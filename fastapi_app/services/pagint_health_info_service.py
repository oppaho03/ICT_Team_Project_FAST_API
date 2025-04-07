import cx_Oracle

dsn = cx_Oracle.makedsn("localhost", 1521, service_name="xepdb1")
conn = cx_Oracle.connect(user="TESTAPP", password="TESTAPP", dsn=dsn)
cursor = conn.cursor()

def fetch_disease_info(page: int, size: int, category: str = None):
    start_row = (page - 1) * size + 1
    end_row = page * size

    try:
        if category:
            query = """
                SELECT * FROM (
                    SELECT d.*, ROWNUM rn
                    FROM (
                        SELECT * FROM disease_information WHERE category = :category ORDER BY id
                    ) d
                    WHERE ROWNUM <= :end_row
                )
                WHERE rn >= :start_row
            """
            cursor.execute(query, {"category": category, "start_row": start_row, "end_row": end_row})
        else:
            query = """
                SELECT * FROM (
                    SELECT d.*, ROWNUM rn
                    FROM (
                        SELECT * FROM disease_information ORDER BY id
                    ) d
                    WHERE ROWNUM <= :end_row
                )
                WHERE rn >= :start_row
            """
            cursor.execute(query, {"start_row": start_row, "end_row": end_row})

        rows = cursor.fetchall()
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        return {"error": str(e)}
