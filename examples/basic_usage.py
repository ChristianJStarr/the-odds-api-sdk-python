"""
Basic usage examples for The Odds API Python SDK.

This script demonstrates the main features of the SDK with practical examples.
"""

import os
from datetime import datetime, timedelta
from the_odds_api_sdk import OddsAPIClient, OddsAPIError


def main():
    """Run basic usage examples."""
    
    # Initialize the client
    # Option 1: Pass API key directly
    # client = OddsAPIClient(api_key="your-api-key-here")
    
    # Option 2: Use environment variable (recommended)
    # Set ODDS_API_KEY=your-api-key in your environment
    try:
        client = OddsAPIClient()
    except OddsAPIError as e:
        print(f"Error: {e}")
        print("Please set your API key using the ODDS_API_KEY environment variable")
        return
    
    print("🏈 The Odds API Python SDK - Basic Usage Examples\n")
    
    # Example 1: Get all available sports
    print("1. Getting all available sports...")
    try:
        sports = client.get_sports()
        print(f"Found {len(sports)} sports:")
        for sport in sports[:5]:  # Show first 5
            status = "✅ Active" if sport.active else "❌ Inactive"
            print(f"  • {sport.title} ({sport.key}) - {status}")
        if len(sports) > 5:
            print(f"  ... and {len(sports) - 5} more")
    except OddsAPIError as e:
        print(f"Error getting sports: {e}")
    
    print()
    
    # Example 2: Get odds for NFL games
    print("2. Getting NFL odds from US bookmakers...")
    try:
        nfl_odds = client.get_odds(
            sport="americanfootball_nfl",
            regions=["us"],
            markets=["h2h"],  # Head-to-head (moneyline)
            odds_format="american"
        )
        
        print(f"Found {len(nfl_odds)} NFL games:")
        for event in nfl_odds[:3]:  # Show first 3 games
            print(f"  🏟️  {event.away_team} @ {event.home_team}")
            print(f"     Starts: {event.commence_time.strftime('%Y-%m-%d %H:%M UTC')}")
            
            # Show odds from first bookmaker
            if event.bookmakers:
                bookmaker = event.bookmakers[0]
                print(f"     {bookmaker.title} odds:")
                
                for market in bookmaker.markets:
                    if market.key == "h2h":
                        for outcome in market.outcomes:
                            print(f"       {outcome.name}: {outcome.price:+d}")
            print()
            
    except OddsAPIError as e:
        print(f"Error getting NFL odds: {e}")
    
    # Example 3: Get upcoming games across all sports
    print("3. Getting upcoming games with spreads and totals...")
    try:
        upcoming_odds = client.get_odds(
            sport="upcoming",
            regions=["us"],
            markets=["spreads", "totals"],
            odds_format="decimal"
        )
        
        print(f"Found {len(upcoming_odds)} upcoming games with spreads/totals:")
        for event in upcoming_odds[:2]:  # Show first 2
            print(f"  🎯 {event.away_team} @ {event.home_team}")
            
            if event.bookmakers:
                bookmaker = event.bookmakers[0]
                for market in bookmaker.markets:
                    print(f"     {market.key.upper()}:")
                    for outcome in market.outcomes:
                        point_info = f" ({outcome.point:+g})" if outcome.point else ""
                        print(f"       {outcome.name}{point_info}: {outcome.price}")
            print()
                        
    except OddsAPIError as e:
        print(f"Error getting upcoming odds: {e}")
    
    # Example 4: Using context manager for automatic cleanup
    print("4. Using context manager...")
    try:
        with OddsAPIClient() as client:
            sports = client.get_sports()
            active_sports = [s for s in sports if s.active]
            print(f"Found {len(active_sports)} active sports using context manager")
    except OddsAPIError as e:
        print(f"Error: {e}")
    
    # Example 5: Error handling
    print("\n5. Demonstrating error handling...")
    try:
        # This will fail with an invalid sport key
        invalid_odds = client.get_odds("invalid_sport_key")
    except OddsAPIError as e:
        print(f"Caught expected error: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Status code: {e.status_code}")


if __name__ == "__main__":
    main() 