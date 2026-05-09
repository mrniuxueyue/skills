---
name: stock-market-monitoring
description: 'Monitor Chinese stock market index fluctuations in real-time. Use for tracking Shanghai (SSE) and Shenzhen (SZSE) indices, analyzing price movements, identifying trends, and setting up market alerts. Supports multiple data sources: APIs, CSV files, web scraping, and manual input.'
argument-hint: 'Specify index (SSE/SZSE), timeframe, and data source'
user-invocable: true
---

# Stock Market Monitoring

Monitor Chinese stock market index fluctuations with real-time data acquisition, trend analysis, and alert notifications.

## When to Use

- Track daily SSE (Shanghai Composite Index) and SZSE (Shenzhen Component Index) movements
- Monitor market volatility and identify significant price changes (±2%, ±5%, etc.)
- Analyze intraday trends and support/resistance levels
- Detect market anomalies or unusual trading patterns
- Generate alerts when indices hit predefined thresholds
- Archive historical data for trend analysis

## Supported Data Sources

### 1. Financial APIs (Real-time)
- **Tencent Securities** - Free, low latency
- **Sina Finance** - Historical + real-time data
- **NetEase Finance** - Comprehensive market data
- **Alpha Vantage** - Global + China indices
- **TUSHARE** (Python library) - Professional-grade data

### 2. CSV/Local Files
- Historical data repositories (CSV format)
- User-maintained spreadsheets
- Exported reports from brokers

### 3. Web Scraping
- Financial websites (eastmoney.com, finance.sina.com.cn, etc.)
- Market news and analysis aggregation

### 4. Manual Input
- Quick manual price tracking
- Snapshot verification against real-time sources

## Quick Start Checklist

### Step 1: Choose Your Data Source
- [ ] **API**: Select preferred API (Tencent/Sina/NetEase)
  - Obtain API key if required
  - Test connection with sample request
- [ ] **CSV**: Locate data file
  - Verify format: Date, Open, High, Low, Close, Volume
  - Check time range covers your needs
- [ ] **Web Scraping**: Identify target website
  - Confirm HTML structure hasn't changed
  - Set up request headers to avoid blocking
- [ ] **Manual Input**: Prepare tracking spreadsheet
  - Columns: Timestamp, Index, Price, % Change, Notes

### Step 2: Set Up Monitoring Parameters
- [ ] Define indices to monitor
  - `000001.SH` = Shanghai Composite (SSE)
  - `399001.SZ` = Shenzhen Component (SZSE)
  - Optional: Industry indices (Finance, Tech, etc.)
- [ ] Set time interval
  - Real-time: Every 1-5 minutes (market hours)
  - Daily: Once at market close
  - Weekly/Monthly: Periodic snapshots
- [ ] Define alert thresholds
  - Price change ±2% (minor movement)
  - Price change ±5% (significant movement)
  - Volume spike: >150% daily average
  - Custom: User-defined conditions

### Step 3: Implement Monitoring Script
- [ ] Select implementation language
  - Python: pandas + requests (easiest for data analysis)
  - Node.js: axios + cheerio (web scraping)
  - PowerShell: native Windows integration
- [ ] Create core functions
  - `fetchMarketData()` - Retrieve current index price
  - `calculateChange()` - Compute % and point changes
  - `checkThresholds()` - Evaluate alert conditions
  - `recordData()` - Store to local DB/CSV
  - `sendAlert()` - Notify via email/Slack/WeChat

### Step 4: Configure Storage
- [ ] **Local CSV**: Create `market-data.csv`
  - Headers: Timestamp, Index, Price, Daily%, 5D%, Monthly%, Notes
- [ ] **JSON Lines**: One JSON object per line (easy append)
  - `{"time":"2026-05-09T14:30:00","index":"000001.SH","price":3250.45,"change":-1.23}`
- [ ] **SQLite Database**: For large historical datasets
  - Enables efficient querying and aggregation
- [ ] **Cloud Storage**: Optional (Azure Blob, AWS S3)
  - For cross-device access and backup

### Step 5: Set Up Notifications
- [ ] **Email Alerts**
  - SMTP configuration (Gmail, Outlook, corporate)
  - Template: Index, Current Price, Change %, Threshold Triggered
- [ ] **Slack/Teams Messages**
  - Webhook URL configuration
  - Message formatting with trend indicators
- [ ] **WeChat Official Account** (China-specific)
  - API access token
  - Push to mobile device
- [ ] **Log Files**
  - Alert history in `alerts.log`
  - Timestamps and triggering conditions

### Step 6: Test & Validate
- [ ] Fetch data from each configured source
  - Verify data accuracy against official sources
  - Check for API rate limits or access issues
- [ ] Trigger test alerts
  - Manual threshold override to test notification delivery
  - Verify message content and formatting
- [ ] Monitor for 2-3 trading days
  - Check CPU/memory usage
  - Verify data consistency
  - Validate alert timing and accuracy

### Step 7: Schedule & Automate
- [ ] **Windows Task Scheduler**
  - Run Python script on schedule
  - Set up dependencies and working directory
- [ ] **Cron (Linux/Mac)**
  - Configure monitoring during market hours
  - Example: `*/5 9-15 * * 1-5 python monitor.py`
- [ ] **Docker Container** (Optional)
  - Package with dependencies
  - Run reliably across environments
- [ ] **Logging & Monitoring**
  - Enable debug logs to diagnose issues
  - Track success/failure metrics

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API rate limit exceeded | Reduce request frequency or upgrade API plan |
| Stale data from web scraping | Add automatic website change detection, switch source |
| Missing market hours data | Verify trading session times (9:30-11:30, 13:00-15:00 CST) |
| False alerts | Adjust thresholds, add moving average filters |
| Database grows too large | Archive old data, implement retention policy |
| Notification delivery fails | Test SMTP/webhook settings, check firewall/proxy |

## Example Use Cases

1. **Daily Market Summary**
   - Fetch closing prices at 15:05 (after market close)
   - Calculate daily % change
   - Email summary to yourself

2. **Volatile Day Detection**
   - Monitor intraday swings >3%
   - Send Slack alert when triggered
   - Maintain alert log for pattern analysis

3. **Support/Resistance Tracking**
   - Record price whenever it touches key levels
   - Analyze bounces and breaks
   - Identify reversal patterns

4. **Weekly Trend Analysis**
   - Export 5 weeks of daily close prices to CSV
   - Calculate 5-day/20-day moving averages
   - Generate trend visualization

## Reference Resources

- [Tencent Securities API Docs](http://vip.stock.qq.com/q?c=real_sz000001)
- [NetEase Finance API](http://quotes.money.163.com/)
- [TUSHARE Python Library](https://tushare.pro/)
- [China Stock Market Trading Hours](https://www.ssec.org.cn/)
- Common Indices Reference
  - 000001.SH: Shanghai Composite Index
  - 399001.SZ: Shenzhen Component Index
  - 000300.SH: CSI 300 Index
  - 000905.SH: CSI 500 Index
