#!/usr/bin/env python3
"""
Comprehensive usage example demonstrating full API coverage.

This example shows how to use all endpoints and features of The Odds API SDK,
including the newly added endpoints for complete API coverage.
"""

import os
from datetime import datetime, timedelta
from the_odds_api_sdk import OddsAPIClient


def main():
    """Demonstrate comprehensive usage of The Odds API SDK."""
    
    # Initialize client
    client = OddsAPIClient()
    
    print("=== Comprehensive Odds API SDK Usage ===\n")
    
    # 1. Get sports (with new 'all' parameter)
    print("1. Getting in-season sports...")
    sports = client.get_sports()
    print(f"Found {len(sports)} in-season sports")
    
    print("\n1b. Getting ALL sports (including inactive)...")
    all_sports = client.get_sports(all_sports=True)
    print(f"Found {len(all_sports)} total sports")
    
    # Find NFL for examples
    nfl = next((s for s in sports if s.key == "americanfootball_nfl"), None)
    if not nfl:
        print("NFL not found in active sports, using first available sport")
        nfl = sports[0] if sports else None
    
    if not nfl:
        print("No sports available")
        return
    
    print(f"Using sport: {nfl.title} ({nfl.key})")
    
    # 2. Get events without odds (free endpoint)
    print(f"\n2. Getting events for {nfl.title} (free endpoint)...")
    try:
        events = client.get_events(nfl.key)
        print(f"Found {len(events)} events")
        if events:
            event = events[0]
            print(f"First event: {event.away_team} @ {event.home_team}")
            print(f"Event ID: {event.id}")
            
    except Exception as e:
        print(f"Error getting events: {e}")
        events = []
    
    # 3. Get participants (teams/players)
    print(f"\n3. Getting participants for {nfl.title}...")
    try:
        participants = client.get_participants(nfl.key)
        print(f"Found {len(participants)} participants")
        if participants:
            print(f"First participant: {participants[0].full_name}")
            
    except Exception as e:
        print(f"Error getting participants: {e}")
    
    # 4. Get odds with new parameters
    print(f"\n4. Getting odds with enhanced features...")
    try:
        odds = client.get_odds(
            nfl.key,
            regions=["us"],
            markets=["h2h", "spreads"],
            include_links=True,
            include_sids=True,
            include_bet_limits=True
        )
        print(f"Found {len(odds)} events with odds")
        
        if odds and odds[0].bookmakers:
            bookmaker = odds[0].bookmakers[0]
            print(f"First bookmaker: {bookmaker.title}")
            print(f"Bookmaker link: {bookmaker.link}")
            print(f"Bookmaker SID: {bookmaker.sid}")
            
            if bookmaker.markets:
                market = bookmaker.markets[0]
                print(f"Market: {market.key}")
                print(f"Market link: {market.link}")
                print(f"Market SID: {market.sid}")
                
                if market.outcomes:
                    outcome = market.outcomes[0]
                    print(f"Outcome: {outcome.name} - {outcome.price}")
                    print(f"Outcome link: {outcome.link}")
                    print(f"Outcome SID: {outcome.sid}")
                    print(f"Bet limit: {outcome.bet_limit}")
                    
    except Exception as e:
        print(f"Error getting odds: {e}")
    
    # 5. Get event-specific odds with enhanced features
    if events:
        print(f"\n5. Getting specific event odds with all markets...")
        try:
            event_odds = client.get_event_odds(
                nfl.key,
                events[0].id,
                regions=["us"],
                markets=["h2h", "spreads", "totals"],  # Could include player props too
                include_links=True,
                include_sids=True,
                include_bet_limits=True
            )
            print(f"Event: {event_odds.away_team} @ {event_odds.home_team}")
            print(f"Number of bookmakers: {len(event_odds.bookmakers)}")
            
        except Exception as e:
            print(f"Error getting event odds: {e}")
    
    # 6. Get scores
    print(f"\n6. Getting scores...")
    try:
        # Live and upcoming only
        scores = client.get_scores(nfl.key)
        print(f"Found {len(scores)} live/upcoming games")
        
        # Include completed games from last 3 days
        scores_with_history = client.get_scores(nfl.key, days_from=3)
        print(f"Found {len(scores_with_history)} games including completed")
        
        completed_games = [s for s in scores_with_history if s.completed]
        print(f"Completed games: {len(completed_games)}")
        
        if completed_games:
            game = completed_games[0]
            print(f"Sample completed game: {game.away_team} @ {game.home_team}")
            if game.scores:
                for score in game.scores:
                    print(f"  {score.name}: {score.score}")
                    
    except Exception as e:
        print(f"Error getting scores: {e}")
    
    # 7. Historical data (if available)
    print(f"\n7. Demonstrating historical data endpoints...")
    
    # Use a date from a few days ago
    historical_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT12:00:00Z")
    
    try:
        print(f"Getting historical odds for {historical_date}...")
        historical_odds = client.get_historical_odds(
            nfl.key,
            historical_date,
            regions=["us"],
            markets=["h2h"]
        )
        print(f"Historical snapshot timestamp: {historical_odds.timestamp}")
        print(f"Previous snapshot: {historical_odds.previous_timestamp}")
        print(f"Next snapshot: {historical_odds.next_timestamp}")
        
        if isinstance(historical_odds.data, list):
            print(f"Found {len(historical_odds.data)} historical events")
        
    except Exception as e:
        print(f"Error getting historical odds: {e}")
    
    try:
        print(f"Getting historical events for {historical_date}...")
        historical_events = client.get_historical_events(
            nfl.key,
            historical_date
        )
        print(f"Historical events snapshot timestamp: {historical_events.timestamp}")
        
        if isinstance(historical_events.data, list):
            print(f"Found {len(historical_events.data)} historical events")
        
    except Exception as e:
        print(f"Error getting historical events: {e}")
    
    # Historical event-specific odds (if we have an event)
    if events:
        try:
            print(f"Getting historical event odds for {historical_date}...")
            historical_event_odds = client.get_historical_event_odds(
                nfl.key,
                events[0].id,
                historical_date,
                regions=["us"],
                markets=["h2h"]
            )
            print(f"Historical event odds timestamp: {historical_event_odds.timestamp}")
            
        except Exception as e:
            print(f"Error getting historical event odds: {e}")
    
    print("\n=== Comprehensive usage demonstration complete! ===")


if __name__ == "__main__":
    main() 