from sqlmodel import SQLModel, Field


class CompanyPeer(SQLModel, table=True):
    """Company Peers - /stock/peers"""
    __tablename__ = "company_peers"

    symbol: str = Field(primary_key=True, index=True)
    peer_symbol: str = Field(primary_key=True, alias="peerSymbol")
