import asyncio
import json
from playwright.async_api import async_playwright

BASE_URL = "https://www.sofascore.com"

async def init_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)

    context = await browser.new_context(
        user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
    )

    return browser, context


async def get(page, url, retries=2):
    if retries == 0:
        return None
    try:
        response = await page.goto(url, wait_until="networkidle", timeout=10000)

        if not response:
            return await get(page, url, retries - 1)

        if response.status == 200:
            return await response.json()

        if response.status == 403:
            await asyncio.sleep(1)
            return await get(page, url, retries - 1)

        raise Exception(f"Failed to fetch {url}: {response.status}")

    except Exception as e:
        print(f"Error performing request: {e}")
        await asyncio.sleep(1)
        return await get(page, url, retries - 1)

competitions = [
    8,
    17,
    23,
    35,
    34,
    238,
    37,
    52,
    38,
    172,
    325,
    18,
    7,
    679,
    17015,
    384,
    1,
    16,
    133
]

no_xg_tournaments = [
    329,
    21,
    19,
    11,
    270,
    357,
    295,
    155,
    480,
    36,
    335,
    328,
    217,
    27,
    10783,
    373,
    463,
]

async def process_tournament(context, tournament_id):
    year_cutoff = 19

    page = await context.new_page()
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    await asyncio.sleep(1)

    expected_fields = ['home_fouledFinalThird_period1', 'away_fouledFinalThird_period1', 'home_fouledFinalThird_period1', 'away_fouledFinalThird_period1', 'home_bigChanceMissed_period1', 'away_bigChanceMissed_period1', 'home_bigChanceMissed_period1', 'away_bigChanceMissed_period1', 'home_bigChanceScored_period1', 'away_bigChanceScored_period1', 'home_bigChanceScored_period1', 'away_bigChanceScored_period1', 'home_expectedGoals_period1', 'away_expectedGoals_period1', 'home_expectedGoals_period1', 'away_expectedGoals_period1', 'home_redCards_period1', 'away_redCards_period1', 'home_redCards_period1', 'away_redCards_period1', 'home_yellowCards_period1', 'away_yellowCards_period1', 'home_yellowCards_period1', 'away_yellowCards_period1', 'home_ballPossession_period1', 'away_ballPossession_period1', 'home_ballPossession_period1', 'away_ballPossession_period1', 'home_bigChanceCreated_period1', 'away_bigChanceCreated_period1', 'home_bigChanceCreated_period1', 'away_bigChanceCreated_period1', 'home_totalShotsOnGoal_period1', 'away_totalShotsOnGoal_period1', 'home_totalShotsOnGoal_period1', 'away_totalShotsOnGoal_period1', 'home_goalkeeperSaves_period1', 'away_goalkeeperSaves_period1', 'home_goalkeeperSaves_period1', 'away_goalkeeperSaves_period1', 'home_cornerKicks_period1', 'away_cornerKicks_period1', 'home_cornerKicks_period1', 'away_cornerKicks_period1', 'home_passes_period1', 'away_passes_period1', 'home_passes_period1', 'away_passes_period1', 'home_totalTackle_period1', 'away_totalTackle_period1', 'home_totalTackle_period1', 'away_totalTackle_period1', 'home_freeKicks_period1', 'away_freeKicks_period1', 'home_freeKicks_period1', 'away_freeKicks_period1', 'home_shotsOnGoal_period1', 'away_shotsOnGoal_period1', 'home_shotsOnGoal_period1', 'away_shotsOnGoal_period1', 'home_hitWoodwork_period1', 'away_hitWoodwork_period1', 'home_hitWoodwork_period1', 'away_hitWoodwork_period1', 'home_shotsOffGoal_period1', 'away_shotsOffGoal_period1', 'home_shotsOffGoal_period1', 'away_shotsOffGoal_period1', 'home_blockedScoringAttempt_period1', 'away_blockedScoringAttempt_period1', 'home_blockedScoringAttempt_period1', 'away_blockedScoringAttempt_period1', 'home_totalShotsInsideBox_period1', 'away_totalShotsInsideBox_period1', 'home_totalShotsInsideBox_period1', 'away_totalShotsInsideBox_period1', 'home_totalShotsOutsideBox_period1', 'away_totalShotsOutsideBox_period1', 'home_totalShotsOutsideBox_period1', 'away_totalShotsOutsideBox_period1', 'home_offsides_period1', 'away_offsides_period1', 'home_offsides_period1', 'away_offsides_period1', 'home_accuratePasses_period1', 'away_accuratePasses_period1', 'home_accuratePasses_period1', 'away_accuratePasses_period1', 'home_throwIns_period1', 'away_throwIns_period1', 'home_throwIns_period1', 'away_throwIns_period1', 'home_finalThirdEntries_period1', 'away_finalThirdEntries_period1', 'home_finalThirdEntries_period1', 'away_finalThirdEntries_period1', 'home_accurateLongBalls_period1', 'away_accurateLongBalls_period1', 'home_accurateLongBalls_period1', 'away_accurateLongBalls_period1', 'home_accurateCross_period1', 'away_accurateCross_period1', 'home_accurateCross_period1', 'away_accurateCross_period1', 'home_duelWonPercent_period1', 'away_duelWonPercent_period1', 'home_duelWonPercent_period1', 'away_duelWonPercent_period1', 'home_dispossessed_period1', 'away_dispossessed_period1', 'home_dispossessed_period1', 'away_dispossessed_period1', 'home_groundDuelsPercentage_period1', 'away_groundDuelsPercentage_period1', 'home_groundDuelsPercentage_period1', 'away_groundDuelsPercentage_period1', 'home_aerialDuelsPercentage_period1', 'away_aerialDuelsPercentage_period1', 'home_aerialDuelsPercentage_period1', 'away_aerialDuelsPercentage_period1', 'home_dribblesPercentage_period1', 'away_dribblesPercentage_period1', 'home_dribblesPercentage_period1', 'away_dribblesPercentage_period1', 'home_wonTacklePercent_period1', 'away_wonTacklePercent_period1', 'home_wonTacklePercent_period1', 'away_wonTacklePercent_period1', 'home_interceptionWon_period1', 'away_interceptionWon_period1', 'home_interceptionWon_period1', 'away_interceptionWon_period1', 'home_totalClearance_period1', 'away_totalClearance_period1', 'home_totalClearance_period1', 'away_totalClearance_period1', 'home_goalKicks_period1', 'away_goalKicks_period1', 'home_goalKicks_period1', 'away_goalKicks_period1']
    
    tournament_response = await get(page, f'https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}')
    tournament_name = tournament_response['uniqueTournament']['slug']

    seasons_response = await get(page, f'https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/seasons')
    seasons = seasons_response['seasons']

    events = []

    for season in seasons:
        try:
            season_id = season['id']
            year = season['year'].split('/')[0]
            year = int(year[-2:])
            if year < year_cutoff:
                continue
            
            counter = 0
            has_next_page = True
            while has_next_page:
                events_list_response = await get(page, f'https://www.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/events/last/{counter}')
                events_list = events_list_response['events']
                events_list.reverse()
                events.extend(events_list)
                has_next_page = events_list_response['hasNextPage']
                counter += 1

        except Exception as e:
            print(e)
            continue

    processed_events = []
    count = 0
    for event in events:
        count += 1
        print(f'{tournament_name}: {round(count / len(events), 1)}%')
        try:
            # if not event.get('hasXg', False):
            #     continue
            id = event['id']
            winner_code = event.get('winnerCode', None)
            if not winner_code:
                continue
            home_goals_period1 = event['homeScore']['period1']
            away_goals_period1 = event['awayScore']['period1']
            
            matchstring = f'{id},{winner_code - 1},{home_goals_period1},{away_goals_period1}'

            statistics_response = await get(page, f'{BASE_URL}/api/v1/event/{id}/statistics')
            if not statistics_response:
                continue
            statistics = statistics_response.get('statistics')
            if len(statistics) < 3:
                continue
            fields = {}
            for period in statistics:
                period_string = 'period1'
                if period['period'] == '2ND':
                    period_string = 'period2'
                elif period['period'] == 'ET1':
                    period_string = 'extra1'
                elif period['period'] == 'ET2':
                    period_string = 'extra2'
                elif period['period'] == 'ALL':
                    period_string = 'total'
                for group in period['groups']:
                    for item in group['statisticsItems']:
                        key = item['key']
                        full_name = f'{key}_{period_string}'
                        fields[f'home_{full_name}'] = item['homeValue']
                        fields[f'away_{full_name}'] = item['awayValue']

            # if not (fields.get('home_expectedGoals_period1') and fields.get('away_expectedGoals_period1')):
            #     continue

            missing = list(set(expected_fields).difference(set(fields.keys())))
            for field in missing:
                fields[field] = 0
            
            for field in expected_fields:
                matchstring += f',{fields[field]}'
            matchstring += '\n'
            processed_events.append(matchstring)
        
        except Exception as e:
            print(e)
            continue
        
        
    with open(f'datasets_no_xg/{tournament_name}.csv', 'w') as file:
        header = 'id,result,home_goals_period1,away_goals_period1'
        for field in expected_fields:
            header += f',{field}'
        header += '\n'
        file.write(header)
        for line in processed_events:
            file.write(line)


async def main():
    browser, context = await init_browser()

    tasks = [
        process_tournament(context, tid)
        for tid in (competitions + no_xg_tournaments)
    ]

    await asyncio.gather(*tasks)

    await browser.close()

    
    
asyncio.run(main())