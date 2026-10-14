# Влезни фактури

Local book for incoming electricity invoices. Macedonian interface, one login, SQLite.

- Partners, with measurement places when the partner has them
- Articles per partner, each with its own tax rate
- Invoice lines: quantity, price, amount without tax
- Tax and amount with tax are calculated
- Place report: totals by measurement place, all-time or by date
- Partner report: pick a partner and see quantity, amount, and tax by article
- Excel export

`bills.db` is part of the repository. Cloning the repo includes the partners, places, articles, and tax rates already entered.

## Run

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:5050.

Windows: double-click `start.bat`.

First login: `admin` / `admin123`. Change the password after login.

## Already entered

- Електродистрибуција ДООЕЛ Скопје, with the 7 measurement places
- ЕСМ Продажба ДООЕЛ Скопје, with no places
- Articles for both, with a tax rate on each
- Tax rates: Без данок, 5%, 10%, 15%, 18%

Do not enter ДДВ as its own line. The rate comes from the article. Leave Израмнување empty to round the payable total to a whole denar.

## Push

```powershell
.\push.ps1 "commit message"
```

## License

MIT. See [LICENSE](LICENSE).
