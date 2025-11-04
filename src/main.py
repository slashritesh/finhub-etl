# from dotenv import load_dotenv
# import finnhub
# import os
# import json
# import asyncio
# from datetime import datetime
# from sqlmodel import select

# from src.database import engine, AsyncSession
# from src.models import FinancialReport

# # Load environment variables from .env file
# load_dotenv()


# async def save_financial_report(report_data: dict, symbol: str):
#     """Save a financial report to the database."""
#     async with AsyncSession(engine) as session:
#         # Parse dates
#         start_date = datetime.strptime(report_data['startDate'], "%Y-%m-%d %H:%M:%S")
#         end_date = datetime.strptime(report_data['endDate'], "%Y-%m-%d %H:%M:%S")
#         filed_date = datetime.strptime(report_data['filedDate'], "%Y-%m-%d %H:%M:%S")
#         accepted_date = datetime.strptime(report_data['acceptedDate'], "%Y-%m-%d %H:%M:%S")

#         # Check if report already exists
#         statement = select(FinancialReport).where(
#             FinancialReport.access_number == report_data['accessNumber']
#         )
#         result = await session.exec(statement)
#         existing_report = result.all()

#         if existing_report:
#             print(f"⚠️  Report {report_data['accessNumber']} already exists, updating...")
#             existing_report.report_data = report_data['report']
#             existing_report.updated_at = datetime.utcnow()
#         else:
#             # Create new report
#             financial_report = FinancialReport(
#                 access_number=report_data['accessNumber'],
#                 symbol=symbol,
#                 cik=report_data['cik'],
#                 year=report_data['year'],
#                 quarter=report_data['quarter'],
#                 form=report_data['form'],
#                 start_date=start_date,
#                 end_date=end_date,
#                 filed_date=filed_date,
#                 accepted_date=accepted_date,
#                 report_data=report_data['report']
#             )
#             session.add(financial_report)

#         await session.commit()
#         return existing_report or financial_report


# async def main():
#     """Main ETL function to fetch and store financial data."""
#     # Get the API key safely
#     api_key = os.getenv("FINHUB_API_KEY")

#     # Check if key exists
#     if not api_key:
#         raise ValueError("❌ FINHUB_API_KEY not found in environment variables!")

#     # Initialize client
#     finnhub_client = finnhub.Client(api_key=api_key)

#     # Fetch financial reports for Apple
#     symbol = 'AAPL'
#     print(f"📊 Fetching financial reports for {symbol}...")
#     response = finnhub_client.financials_reported(symbol=symbol, freq='annual')

#     # Save to JSON file for backup
#     output_file = "data/financials.json"
#     os.makedirs("data", exist_ok=True)
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(response, f, indent=4)
#     print(f"💾 Backup saved to {output_file}")

#     # Store each report in the database
#     reports_saved = 0
#     for report in response.get('data', []):
#         await save_financial_report(report, symbol)
#         reports_saved += 1
#         print(f"✅ Saved report for {symbol} - {report['year']} Q{report['quarter']} ({report['form']})")

#     print(f"\n🎉 Successfully saved {reports_saved} financial reports to database!")


# if __name__ == "__main__":
#     asyncio.run(main())


