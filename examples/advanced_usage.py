"""
Advanced usage examples for The Odds API Python SDK.

This script demonstrates advanced features like filtering, player props,
and data analysis capabilities.
"""

from datetime import datetime, timedelta
from typing import Dict, List
from the_odds_api_sdk import OddsAPIClient, OddsAPIError, Event, Bookmaker


def find_best_odds(events: List[Event]) -> Dict[str, Dict[str, float]]:
    """
    Analyze events to find the best odds for each team across all bookmakers.
    
    Returns:
        Dictionary mapping game -> team -> best_odds
    """
    best_odds = {}
    
    for event in events:
        game_key = f"{event.away_team} @ {event.home_team}"
        best_odds[game_key] = {}
        
        # Track best odds for each team
        team_odds = {}
        
        for bookmaker in event.bookmakers:
            for market in bookmaker.markets:
                if market.key == "h2h":  # Moneyline odds
                    for outcome in market.outcomes:
                        team = outcome.name
                        price = outcome.price
                        
                        if team not in team_odds:
                            team_odds[team] = []
                        team_odds[team].append((price, bookmaker.title))
        
        # Find best odds for each team
        for team, odds_list in team_odds.items():
            if odds_list:
                # For American odds, higher positive or less negative is better
                best_price, best_bookmaker = max(odds_list, key=lambda x: x[0])
                best_odds[game_key][team] = {
                    'price': best_price,
                    'bookmaker': best_bookmaker
                }
    
    return best_odds


def analyze_market_coverage(events: List[Event]) -> Dict[str, int]:
    """Analyze which markets are most commonly available."""
    market_counts = {}
    
    for event in events:
        event_markets = set()
        for bookmaker in event.bookmakers:
            for market in bookmaker.markets:
                event_markets.add(market.key)
        
        for market in event_markets:
            market_counts[market] = market_counts.get(market, 0) + 1
    
    return market_counts


def main():
    """Run advanced usage examples."""
    
    try:
        client = OddsAPIClient()
    except OddsAPIError as e:
        print(f"Error: {e}")
        print("Please set your API key using the ODDS_API_KEY environment variable")
        return
    
    print("🔥 The Odds API Python SDK - Advanced Usage Examples\n")
    
    # Example 1: Filter events by date range
    print("1. Getting events for next 3 days...")
    try:
        now = datetime.utcnow()
        three_days_later = now + timedelta(days=3)
        
        filtered_events = client.get_odds(
            sport="upcoming",
            regions=["us"],
            markets=["h2h", "spreads"],
            commence_time_from=now,
            commence_time_to=three_days_later,
            odds_format="american"
        )
        
        print(f"Found {len(filtered_events)} events in next 3 days")
        
        # Analyze best odds
        best_odds = find_best_odds(filtered_events)
        
        print("\n📊 Best Odds Analysis:")
        for game, odds in list(best_odds.items())[:3]:  # Show first 3
            print(f"  {game}:")
            for team, team_odds in odds.items():
                price = team_odds['price']
                bookmaker = team_odds['bookmaker']
                print(f"    {team}: {price:+d} ({bookmaker})")
            print()
            
    except OddsAPIError as e:
        print(f"Error: {e}")
    
    # Example 2: Get specific events by ID
    print("2. Getting specific events by ID...")
    try:
        # First get some events to extract IDs
        all_events = client.get_odds("upcoming", regions=["us"], markets=["h2h"])
        
        if all_events:
            # Get first event's detailed odds
            first_event_id = all_events[0].id
            sport_key = all_events[0].sport_key
            
            specific_event = client.get_event_odds(
                sport=sport_key,
                event_id=first_event_id,
                regions=["us"],
                markets=["h2h", "spreads", "totals"]
            )
            
            print(f"Detailed odds for: {specific_event.away_team} @ {specific_event.home_team}")
            print(f"Event ID: {specific_event.id}")
            print(f"Sport: {specific_event.sport_key}")
            print(f"Bookmakers available: {len(specific_event.bookmakers)}")
            
            # Show market coverage
            if specific_event.bookmakers:
                markets = set()
                for bookmaker in specific_event.bookmakers:
                    for market in bookmaker.markets:
                        markets.add(market.key)
                print(f"Markets available: {', '.join(sorted(markets))}")
        
    except OddsAPIError as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 3: Market coverage analysis
    print("3. Analyzing market coverage across events...")
    try:
        events = client.get_odds(
            sport="upcoming",
            regions=["us", "uk"],
            markets=["h2h", "spreads", "totals"]
        )
        
        market_coverage = analyze_market_coverage(events)
        
        print("Market coverage analysis:")
        for market, count in sorted(market_coverage.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(events)) * 100 if events else 0
            print(f"  {market}: {count}/{len(events)} events ({percentage:.1f}%)")
        
    except OddsAPIError as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 4: Multiple bookmaker comparison
    print("4. Comparing odds across multiple bookmakers...")
    try:
        # Get odds from specific bookmakers
        events = client.get_odds(
            sport="americanfootball_nfl",
            bookmakers=["fanduel", "draftkings", "betmgm"],
            markets=["h2h"],
            odds_format="american"
        )
        
        if events:
            event = events[0]
            print(f"Comparing odds for: {event.away_team} @ {event.home_team}")
            
            bookmaker_odds = {}
            for bookmaker in event.bookmakers:
                bookmaker_odds[bookmaker.title] = {}
                for market in bookmaker.markets:
                    if market.key == "h2h":
                        for outcome in market.outcomes:
                            bookmaker_odds[bookmaker.title][outcome.name] = outcome.price
            
            # Display comparison table
            teams = list(bookmaker_odds[list(bookmaker_odds.keys())[0]].keys()) if bookmaker_odds else []
            
            print(f"{'Bookmaker':<15} {teams[0] if teams else 'Team1':<20} {teams[1] if len(teams) > 1 else 'Team2':<20}")
            print("-" * 60)
            
            for bookmaker, odds in bookmaker_odds.items():
                team1_odds = odds.get(teams[0], "N/A") if teams else "N/A"
                team2_odds = odds.get(teams[1], "N/A") if len(teams) > 1 else "N/A"
                print(f"{bookmaker:<15} {str(team1_odds):<20} {str(team2_odds):<20}")
        
    except OddsAPIError as e:
        print(f"Error: {e}")
    
    print()
    
    # Example 5: Historical event lookup (using commence time filtering)
    print("5. Looking up recent events...")
    try:
        # Look for events from the past week
        week_ago = datetime.utcnow() - timedelta(days=7)
        now = datetime.utcnow()
        
        recent_events = client.get_odds(
            sport="americanfootball_nfl",
            regions=["us"],
            commence_time_from=week_ago,
            commence_time_to=now
        )
        
        print(f"Found {len(recent_events)} recent NFL events")
        for event in recent_events[:3]:
            days_ago = (now - event.commence_time).days
            print(f"  {event.away_team} @ {event.home_team} ({days_ago} days ago)")
        
    except OddsAPIError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 