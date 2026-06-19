from sqlalchemy import text


class DashboardService:

    @staticmethod
    def breakdown_trend(db, start_date=None, end_date=None):

        sql = """
        SELECT
            report_date,
            COUNT(*) as total_breakdowns
        FROM dbr.breakdown_history
        WHERE report_date IS NOT NULL
        """

        params = {}

        if start_date:
            sql += " AND report_date >= :start_date"
            params["start_date"] = start_date

        if end_date:
            sql += " AND report_date <= :end_date"
            params["end_date"] = end_date

        sql += """
        GROUP BY report_date
        ORDER BY report_date
        """

        result = db.execute(text(sql), params)

        return [
            {
                "date": str(row.report_date),
                "total_breakdowns": row.total_breakdowns
            }
            for row in result
        ]

    @staticmethod
    def top_cn(
        db,
        limit=10,
        start_date=None,
        end_date=None
    ):

        sql = """
        SELECT
            cn,
            COUNT(*) as total_breakdowns
        FROM dbr.breakdown_history
        WHERE cn IS NOT NULL
        """

        params = {"limit": limit}

        if start_date:
            sql += " AND report_date >= :start_date"
            params["start_date"] = start_date

        if end_date:
            sql += " AND report_date <= :end_date"
            params["end_date"] = end_date

        sql += """
        GROUP BY cn
        ORDER BY total_breakdowns DESC
        LIMIT :limit
        """

        result = db.execute(text(sql), params)

        return [
            {
                "cn": row.cn,
                "total_breakdowns": row.total_breakdowns
            }
            for row in result
        ]

    @staticmethod
    def top_breakdown_code(
        db,
        limit=10,
        start_date=None,
        end_date=None
    ):

        sql = """
        SELECT
            breakdown_code,
            COUNT(*) as total
        FROM dbr.breakdown_history
        WHERE breakdown_code IS NOT NULL
        """

        params = {"limit": limit}

        if start_date:
            sql += " AND report_date >= :start_date"
            params["start_date"] = start_date

        if end_date:
            sql += " AND report_date <= :end_date"
            params["end_date"] = end_date

        sql += """
        GROUP BY breakdown_code
        ORDER BY total DESC
        LIMIT :limit
        """

        result = db.execute(text(sql), params)

        return [
            {
                "breakdown_code": row.breakdown_code,
                "total": row.total
            }
            for row in result
        ]

    @staticmethod
    def monthly_summary(
        db,
        start_date=None,
        end_date=None
    ):

        sql = """
        SELECT
            TO_CHAR(report_date, 'YYYY-MM') as month,
            COUNT(*) as total_breakdowns
        FROM dbr.breakdown_history
        WHERE report_date IS NOT NULL
        """

        params = {}

        if start_date:
            sql += " AND report_date >= :start_date"
            params["start_date"] = start_date

        if end_date:
            sql += " AND report_date <= :end_date"
            params["end_date"] = end_date

        sql += """
        GROUP BY month
        ORDER BY month
        """

        result = db.execute(text(sql), params)

        return [
            {
                "month": row.month,
                "total_breakdowns": row.total_breakdowns
            }
            for row in result
        ]
