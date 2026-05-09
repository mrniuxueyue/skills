# Stock Market Monitoring Skill

A comprehensive skill for monitoring Chinese stock market indices (Shanghai SSE & Shenzhen SZSE) with real-time data acquisition, trend analysis, and intelligent alerting.

## Quick Start

### 1. Run the Basic Monitor
```powershell
python scripts/monitor.py
```

This will:
- Fetch current prices for SSE (Shanghai Composite) and SZSE (Shenzhen Component)
- Check against predefined thresholds
- Log alerts if significant movements detected
- Save all data to `market_data.csv`

### 2. Supported Indices
- **000001.SH** - Shanghai Composite Index (SSE)
- **399001.SZ** - Shenzhen Component Index (SZSE)
- **000300.SH** - CSI 300 Index
- **000905.SH** - CSI 500 Index

### 3. Data Sources
Choose one or combine multiple:
- **Tencent Securities** (default) - Free real-time quotes
- **Sina Finance** - Alternative real-time source
- **CSV Files** - For historical data analysis
- **Manual Input** - Quick threshold testing

### 4. Configure Alerts
Edit thresholds in `monitor.py`:
```python
self.thresholds = {
    'minor': 2.0,           # Alert if ±2% change
    'significant': 5.0,     # Critical alert if ±5% change
    'volume_spike': 1.5     # Alert if volume 1.5x average
}
```

### 5. Output Files
- **market_data.csv** - All recorded prices and changes
- **alerts.log** - Alert history with timestamps
- **console output** - Real-time monitoring feedback

## Example Workflows

### Monitor Market During Trading Hours
```powershell
# Run every 5 minutes during 9:30-15:00
While($true) {
    python scripts/monitor.py
    Start-Sleep -Seconds 300
}
```

### Generate Daily Report
```powershell
# Run at 15:05 (after market close)
$trigger = New-ScheduledTaskTrigger -Daily -At "15:05"
Register-ScheduledTask -TaskName "StockMonitor" -Trigger $trigger -Action (New-ScheduledTaskAction -Program "python" -Arguments "scripts/monitor.py")
```

### Analyze Historical Data
```powershell
# Open market_data.csv in Excel or import to Python
import pandas as pd
df = pd.read_csv('market_data.csv')
print(df.groupby('index').agg({'daily_change_pct': ['min', 'max', 'mean']}))
```

## Integration Examples

### Email Alerts
Modify `send_notification()` to use SMTP:
```python
import smtplib
# Configure Gmail or Outlook SMTP
sender = "your-email@gmail.com"
# Send when alert triggered
```

### Slack Notifications
```python
import requests
webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
requests.post(webhook_url, json={"text": alert['message']})
```

### WeChat Official Account (China)
```python
# Use WeChat Enterprise API
# POST to https://api.weixin.qq.com/cgi-bin/message/send
```

## Dependencies

```
requests>=2.28.0    # HTTP library for API calls
pandas>=1.3.0       # Optional: for data analysis
```

Install with:
```bash
pip install requests pandas
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't fetch from Tencent | Check internet, try Sina alternative |
| Stale data | Verify market is open (9:30-11:30, 13:00-15:00 CST) |
| Script blocked by firewall | Use VPN or configure proxy |
| CSV encoding issues | Re-save as UTF-8 in Excel |

## Market Information

- **Shanghai Stock Exchange (SSE)**: 9:30-11:30, 13:00-15:00 CST
- **Shenzhen Stock Exchange (SZSE)**: Same as SSE
- **Weekend/Holidays**: No trading
- **Data refresh**: Real-time during trading hours, closed outside hours

## References

- [SSEC Official Site](https://www.ssec.org.cn/)
- [SZSE Official Site](https://www.szse.cn/)
- [TUSHARE Professional Data](https://tushare.pro/)
