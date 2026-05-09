#!/usr/bin/env python3
"""
Stock Market Monitoring Script
Monitors Chinese stock indices (SSE/SZSE) with alert capabilities.
"""

import requests
import json
import csv
from datetime import datetime
from pathlib import Path


class StockMonitor:
    """Monitor Chinese stock market indices."""
    
    # Common Chinese stock indices
    INDICES = {
        'SSE': '000001.SH',      # Shanghai Composite
        'SZSE': '399001.SZ',     # Shenzhen Component
        'CSI300': '000300.SH',   # CSI 300
        'CSI500': '000905.SH',   # CSI 500
    }
    
    def __init__(self, data_file='market_data.csv', alert_file='alerts.log'):
        """Initialize monitor with storage paths."""
        self.data_file = Path(data_file)
        self.alert_file = Path(alert_file)
        self.thresholds = {
            'minor': 2.0,      # ±2%
            'significant': 5.0, # ±5%
            'volume_spike': 1.5 # 1.5x average volume
        }
        self._init_storage()
    
    def _init_storage(self):
        """Initialize data storage files."""
        if not self.data_file.exists():
            self.data_file.write_text(
                'timestamp,index,code,price,daily_change_pct,volume,notes\n'
            )
        if not self.alert_file.exists():
            self.alert_file.touch()
    
    def fetch_from_tencent(self, index_code):
        """
        Fetch real-time data from Tencent Securities API.
        Returns: dict with price, change%, volume
        """
        try:
            # Tencent API endpoint for real-time quotes
            url = f'http://qt.gtimg.cn/q=sh{index_code.split(".")[0]}'
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                # Parse Tencent format: v_sh000001="...,price,change_pct,..."
                data = response.text
                parts = data.split('"')[1].split(',')
                
                return {
                    'price': float(parts[3]),
                    'change_pct': float(parts[4]),
                    'volume': int(parts[8]) if len(parts) > 8 else 0,
                    'source': 'tencent',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error fetching from Tencent: {e}")
        return None
    
    def fetch_from_sina(self, index_code):
        """
        Fetch from Sina Finance API.
        Returns: dict with price, change%, volume
        """
        try:
            code = index_code.replace('.', '').lower()
            url = f'https://hq.sinajs.cn/?list={code}'
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                # Sina format: var hq_str_sh000001="..., price, change_point, change_pct, ..."
                data = response.text
                parts = data.split('"')[1].split(',')
                
                return {
                    'price': float(parts[1]),
                    'change_point': float(parts[2]),
                    'change_pct': float(parts[3]),
                    'volume': int(parts[8]) if len(parts) > 8 else 0,
                    'source': 'sina',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error fetching from Sina: {e}")
        return None
    
    def fetch_manual_input(self, index_name, price, change_pct, volume=0):
        """Accept manual price input."""
        return {
            'price': float(price),
            'change_pct': float(change_pct),
            'volume': int(volume),
            'source': 'manual',
            'timestamp': datetime.now().isoformat()
        }
    
    def check_thresholds(self, index_name, data):
        """Check if data triggers any alerts."""
        alerts = []
        change_pct = abs(data['change_pct'])
        
        if change_pct >= self.thresholds['significant']:
            alerts.append({
                'level': 'CRITICAL',
                'message': f"{index_name}: Significant movement {data['change_pct']:+.2f}%",
                'trigger': 'significant_change'
            })
        elif change_pct >= self.thresholds['minor']:
            alerts.append({
                'level': 'WARNING',
                'message': f"{index_name}: Notable movement {data['change_pct']:+.2f}%",
                'trigger': 'minor_change'
            })
        
        return alerts
    
    def record_data(self, index_name, index_code, data):
        """Save market data to CSV."""
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['timestamp'],
                index_name,
                index_code,
                data['price'],
                data['change_pct'],
                data.get('volume', 0),
                data.get('source', 'unknown')
            ])
        print(f"[{data['timestamp']}] Recorded {index_name}: {data['price']} ({data['change_pct']:+.2f}%)")
    
    def log_alert(self, alert):
        """Log alert to file."""
        with open(self.alert_file, 'a') as f:
            alert['timestamp'] = datetime.now().isoformat()
            f.write(json.dumps(alert) + '\n')
        print(f"[ALERT] {alert['level']}: {alert['message']}")
    
    def send_notification(self, alert, method='console'):
        """Send notification via specified method."""
        if method == 'console':
            print(f"\n{'='*60}")
            print(f"ALERT: {alert['level']}")
            print(f"Time: {alert['timestamp']}")
            print(f"Message: {alert['message']}")
            print(f"{'='*60}\n")
        elif method == 'email':
            print(f"[EMAIL] Would send: {alert['message']}")
            # TODO: Implement SMTP
        elif method == 'slack':
            print(f"[SLACK] Would send: {alert['message']}")
            # TODO: Implement Slack webhook
    
    def monitor_index(self, index_name, index_code, source='tencent'):
        """Monitor a single index."""
        print(f"\nMonitoring {index_name} ({index_code}) from {source}...")
        
        # Fetch data
        if source == 'tencent':
            data = self.fetch_from_tencent(index_code)
        elif source == 'sina':
            data = self.fetch_from_sina(index_code)
        else:
            print(f"Unknown source: {source}")
            return
        
        if not data:
            print(f"Failed to fetch data for {index_name}")
            return
        
        # Record data
        self.record_data(index_name, index_code, data)
        
        # Check thresholds
        alerts = self.check_thresholds(index_name, data)
        for alert in alerts:
            self.log_alert(alert)
            self.send_notification(alert, method='console')
    
    def display_summary(self):
        """Display recent market summary."""
        if not self.data_file.exists():
            print("No data recorded yet.")
            return
        
        with open(self.data_file, 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                print("\n" + "="*80)
                print("Recent Market Data (Last 5 records)")
                print("="*80)
                # Show header
                print(lines[0].strip())
                # Show last 5 records
                for line in lines[-5:]:
                    print(line.strip())
                print("="*80)


def main():
    """Example usage."""
    monitor = StockMonitor()
    
    # Monitor multiple indices
    indices_to_monitor = [
        ('Shanghai Composite', '000001.SH'),
        ('Shenzhen Component', '399001.SZ'),
    ]
    
    print("="*60)
    print("Chinese Stock Market Monitor")
    print("="*60)
    
    for index_name, index_code in indices_to_monitor:
        try:
            monitor.monitor_index(index_name, index_code, source='tencent')
        except Exception as e:
            print(f"Error monitoring {index_name}: {e}")
            # Try alternative source
            try:
                monitor.monitor_index(index_name, index_code, source='sina')
            except Exception as e2:
                print(f"Also failed with Sina: {e2}")
    
    # Example: Manual input for testing
    # monitor.record_data('Test Index', 'TEST.XX', monitor.fetch_manual_input(
    #     'Test', price=3250.45, change_pct=-2.5, volume=1000000000
    # ))
    
    monitor.display_summary()


if __name__ == '__main__':
    main()
