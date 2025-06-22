"""
Example: Using the scores endpoint to get live and completed game scores.

This example demonstrates how to use the get_scores() method to retrieve:
- Live game scores
- Completed game scores
- Upcoming games (without scores)
"""

import os
from datetime import datetime, timedelta
from the_odds_api_sdk import OddsAPIClient


def main():
    # Initialize the client
    api_key = os.getenv("ODDS_API_KEY")
    client = OddsAPIClient(api_key)
    
    print("🏈 The Odds API - Scores Examples")
    print("=" * 50)
    
    # Example 1: Get live and upcoming games only (quota cost: 1)
    print("\n1. Getting live and upcoming NFL games...")
    try:
        live_scores = client.get_scores("americanfootball_nfl")
        print(f"   Found {len(live_scores)} games")
        
        # Show some examples
        for i, game in enumerate(live_scores[:3]):
            print(f"\n   Game {i+1}:")
            print(f"   • {game.away_team} @ {game.home_team}")
            print(f"   • Start: {game.commence_time}")
            print(f"   • Status: {'✅ Completed' if game.completed else '🔴 Live/Upcoming'}")
            
            if game.scores:
                print(f"   • Scores:")
                for score in game.scores:
                    print(f"     - {score.name}: {score.score}")
            else:
                print(f"   • No scores yet (upcoming game)")
                
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Get games from last 3 days including completed (quota cost: 2)
    print("\n\n2. Getting NFL games from last 3 days (including completed)...")
    try:
        recent_scores = client.get_scores("americanfootball_nfl", days_from=3)
        print(f"   Found {len(recent_scores)} games")
        
        # Count completed vs live/upcoming
        completed_count = sum(1 for game in recent_scores if game.completed)
        live_upcoming_count = len(recent_scores) - completed_count
        
        print(f"   • Completed games: {completed_count}")
        print(f"   • Live/Upcoming games: {live_upcoming_count}")
        
        # Show completed games with scores
        completed_games = [game for game in recent_scores if game.completed and game.scores]
        if completed_games:
            print(f"\n   Recent completed games with scores:")
            for game in completed_games[:2]:
                print(f"\n   • {game.away_team} @ {game.home_team}")
                print(f"   • Completed: {game.commence_time}")
                if game.scores:
                    for score in game.scores:
                        print(f"     - {score.name}: {score.score}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Try different sports
    print("\n\n3. Getting NBA scores...")
    try:
        nba_scores = client.get_scores("basketball_nba")
        print(f"   Found {len(nba_scores)} NBA games")
        
        if nba_scores:
            game = nba_scores[0]
            print(f"\n   Example NBA game:")
            print(f"   • {game.away_team} @ {game.home_team}")
            print(f"   • Sport: {game.sport_title}")
            print(f"   • Status: {'✅ Completed' if game.completed else '🔴 Live/Upcoming'}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    
    # Example 4: Analyze live vs completed games
    print("\n\n4. Analyzing game statuses across sports...")
    sports_to_check = ["americanfootball_nfl", "basketball_nba", "icehockey_nhl"]
    
    for sport in sports_to_check:
        try:
            scores = client.get_scores(sport)
            if scores:
                completed = sum(1 for game in scores if game.completed)
                with_scores = sum(1 for game in scores if game.scores)
                
                print(f"\n   {scores[0].sport_title}:")
                print(f"   • Total games: {len(scores)}")
                print(f"   • Completed: {completed}")
                print(f"   • With scores: {with_scores}")
                
        except Exception as e:
            print(f"   Error with {sport}: {e}")


if __name__ == "__main__":
    main() 