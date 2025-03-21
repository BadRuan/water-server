from pydantic import BaseModel


class CountModel(BaseModel):
    total_count: int
    this_year_count: int
    visit_count: int
    download_count: int