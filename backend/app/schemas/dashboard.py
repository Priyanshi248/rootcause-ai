from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_incidents: int

    open_incidents: int
    resolved_incidents: int

    critical_incidents: int
    high_incidents: int
    medium_incidents: int
    low_incidents: int

    production_incidents: int
    staging_incidents: int
    development_incidents: int