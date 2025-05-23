"""
API client for accessing centralized booking system data.
"""

import requests
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pandas as pd

from ..config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

class MarketingAPIClient:
    """Client for accessing the centralized API server"""
    
    def __init__(self):
        """Initialize the API client"""
        self.base_url = settings.api_base_url
        self.session = requests.Session()
        self.timeout = 30  # 30 seconds timeout
        
        # Set up session headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Marketing-Dashboard/1.0'
        })
    
    def _make_request(self, method: str, endpoint: str, 
                     params: Optional[Dict[str, Any]] = None,
                     data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make an API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            # Return JSON response
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"API request timed out: {endpoint}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"API connection error: {endpoint}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"API HTTP error: {e}")
            return None
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def get_booking_stats(self, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """Get booking statistics for a date range"""
        try:
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            result = self._make_request('GET', 'system/booking-stats', params=params)
            
            if result:
                # Process and return booking stats
                return {
                    'total_bookings': result.get('total_bookings', 0),
                    'confirmed_bookings': result.get('confirmed_bookings', 0),
                    'pending_bookings': result.get('pending_bookings', 0),
                    'cancelled_bookings': result.get('cancelled_bookings', 0),
                    'conversion_rate': result.get('conversion_rate', 0),
                    'average_booking_value': result.get('average_booking_value', 0)
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting booking stats: {e}")
            return None
    
    def get_revenue_data(self, period: str = "30d") -> Optional[Dict[str, Any]]:
        """Get revenue statistics for a period"""
        try:
            params = {'period': period}
            
            result = self._make_request('GET', 'system/revenue-stats', params=params)
            
            if result:
                return {
                    'total_revenue': result.get('total_revenue', 0),
                    'revenue_by_day': result.get('revenue_by_day', []),
                    'revenue_by_vehicle': result.get('revenue_by_vehicle', {}),
                    'avg_booking_value': result.get('avg_booking_value', 0),
                    'top_routes': result.get('top_routes', [])
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting revenue data: {e}")
            return None
    
    def get_vehicle_stats(self) -> Optional[List[Dict[str, Any]]]:
        """Get vehicle performance statistics"""
        try:
            result = self._make_request('GET', 'vehicles')
            
            if result and isinstance(result, list):
                # Process vehicle data
                vehicle_stats = []
                for vehicle in result:
                    vehicle_stats.append({
                        'vehicle_type': vehicle.get('name', 'Unknown'),
                        'capacity': vehicle.get('capacity', 0),
                        'price_per_km': vehicle.get('price_per_km', 0),
                        'bookings_count': vehicle.get('bookings_count', 0),
                        'revenue': vehicle.get('total_revenue', 0)
                    })
                return vehicle_stats
            return None
            
        except Exception as e:
            logger.error(f"Error getting vehicle stats: {e}")
            return None
    
    def get_quote_stats(self, days_back: int = 30) -> Optional[Dict[str, Any]]:
        """Get quote generation statistics"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            params = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            
            result = self._make_request('GET', 'quotes/stats', params=params)
            
            if result:
                return {
                    'total_quotes': result.get('total_quotes', 0),
                    'quotes_converted': result.get('quotes_converted', 0),
                    'conversion_rate': result.get('conversion_rate', 0),
                    'average_quote_value': result.get('average_quote_value', 0),
                    'quotes_by_day': result.get('quotes_by_day', [])
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting quote stats: {e}")
            return None
    
    def get_customer_stats(self) -> Optional[Dict[str, Any]]:
        """Get customer statistics"""
        try:
            result = self._make_request('GET', 'system/customer-stats')
            
            if result:
                return {
                    'total_customers': result.get('total_customers', 0),
                    'new_customers': result.get('new_customers', 0),
                    'repeat_customers': result.get('repeat_customers', 0),
                    'customer_retention_rate': result.get('retention_rate', 0),
                    'average_customer_value': result.get('average_customer_value', 0)
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting customer stats: {e}")
            return None
    
    def get_route_performance(self, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """Get top performing routes"""
        try:
            params = {'limit': limit}
            
            result = self._make_request('GET', 'system/route-performance', params=params)
            
            if result and isinstance(result, list):
                return result
            return None
            
        except Exception as e:
            logger.error(f"Error getting route performance: {e}")
            return None
    
    def get_payment_stats(self, days_back: int = 30) -> Optional[Dict[str, Any]]:
        """Get payment method statistics"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            params = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            
            result = self._make_request('GET', 'payments/stats', params=params)
            
            if result:
                return {
                    'payment_methods': result.get('payment_methods', {}),
                    'success_rate': result.get('success_rate', 0),
                    'failed_payments': result.get('failed_payments', 0),
                    'average_transaction': result.get('average_transaction', 0)
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting payment stats: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            result = self._make_request('GET', 'system/health')
            return result is not None and result.get('status') == 'ok'
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False

# Helper functions for data conversion
def booking_stats_to_dataframe(stats: Dict[str, Any]) -> pd.DataFrame:
    """Convert booking stats to DataFrame"""
    if not stats:
        return pd.DataFrame()
    
    data = {
        'Metric': ['Total Bookings', 'Confirmed', 'Pending', 'Cancelled', 'Conversion Rate', 'Avg Value'],
        'Value': [
            stats.get('total_bookings', 0),
            stats.get('confirmed_bookings', 0),
            stats.get('pending_bookings', 0),
            stats.get('cancelled_bookings', 0),
            f"{stats.get('conversion_rate', 0):.2f}%",
            f"${stats.get('average_booking_value', 0):.2f}"
        ]
    }
    
    return pd.DataFrame(data)

def revenue_timeline_to_dataframe(revenue_data: Dict[str, Any]) -> pd.DataFrame:
    """Convert revenue timeline data to DataFrame"""
    if not revenue_data or 'revenue_by_day' not in revenue_data:
        return pd.DataFrame()
    
    timeline_data = revenue_data['revenue_by_day']
    if not timeline_data:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(timeline_data)
    
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df