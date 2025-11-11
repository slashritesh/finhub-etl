from sqlmodel import JSON, Column, SQLModel, Field


class CompanyPeer(SQLModel, table=True):
    """Company Peers - /stock/peers"""
    __tablename__ = "company_peers"

    symbol: str = Field(primary_key=True, index=True)
    peers: list[str] = Field(default_factory=list, sa_column=Column(JSON))
