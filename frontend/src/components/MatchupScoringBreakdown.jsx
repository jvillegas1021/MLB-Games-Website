import { compare_stat_low_color, compare_stat_high_color, compare_stat_general_color } from "../utility_functions/color_functions.js";
import { safe_fixed, safe_percent } from "../utility_functions/safe_functions.js";
import { mlb_team_colors } from "../mlb_colors.js";
import { MirrorBar, ScoreBar } from "../utility_functions/chart_functions.jsx";


export default function MatchupScoringBreakdown({ matchup }) {

  const home_team_color = mlb_team_colors[matchup.Home_Team];
  const away_team_color = mlb_team_colors[matchup.Away_Team];

  return (
  <div className="matchup-scoring-details-card" 
       style={{ display: "flex", justifyContent: "center" }}>

    <div style={{ width: "70%", margin: "0 auto" }}>

        {/* 1 — Team Total Score */}
        <h3 style={{ marginTop: "25px" }}>Team Total Score</h3>
        <ScoreBar 
            awayValue={matchup.Away_Team_Total_Score}
            homeValue={matchup.Home_Team_Total_Score}
            awayColor={away_team_color}
            homeColor={home_team_color}
            dividerIcon='🥇'
        />

        {/* 2 — Pitcher Score */}
        <h3 style={{ marginTop: "25px" }}>Pitcher Score</h3>
        <ScoreBar 
            awayValue={matchup.Away_Pitcher_Score}
            homeValue={matchup.Home_Pitcher_Score}
            awayColor={away_team_color}
            homeColor={home_team_color}
            dividerIcon='⚾'
        />

        {/* 3 — Lineup Score */}
        <h3 style={{ marginTop: "25px" }}>Lineup Score</h3>
        <ScoreBar 
            awayValue={matchup.Away_Batting_Score}
            homeValue={matchup.Home_Batting_Score}
            awayColor={away_team_color}
            homeColor={home_team_color}
            dividerIcon='🏏'
        />

        {/* 4 — Bullpen Score */}
        <h3 style={{ marginTop: "25px" }}>Bullpen Score</h3>
        <ScoreBar 
            awayValue={matchup.Away_Pitching_Score}
            homeValue={matchup.Home_Pitching_Score}
            awayColor={away_team_color}
            homeColor={home_team_color}
            dividerIcon='🎯'
        />

        {/* 5 — Batting Split Score */}
        <h3 style={{ marginTop: "25px" }}>Batting Split Score</h3>
        <ScoreBar 
            awayValue={matchup.Away_Team_Split_Score}
            homeValue={matchup.Home_Team_Split_Score}
            awayColor={away_team_color}
            homeColor={home_team_color}
            dividerIcon='⚖️'
        />

        {/* 6 — Pitcher vs Lineup Score */}
        <h3 style={{ marginTop: "25px" }}>Pitcher vs Lineup Score</h3>
        <ScoreBar 
            awayValue={matchup.Away_Pitcher_vs_Home_Batting_Score}
            homeValue={matchup.Home_Pitcher_vs_Away_Batting_Score}
            awayColor={away_team_color}
            homeColor={home_team_color}
            dividerIcon='⚔️'
        />

        {/* 7 — Team Record Score */}
        <h3 style={{ marginTop: "25px" }}>Team Record Score</h3>
        <ScoreBar 
            awayValue={matchup.Away_Team_Record_Score}
            homeValue={matchup.Home_Team_Record_Score}
            awayColor={away_team_color}
            homeColor={home_team_color}
            dividerIcon='📈'
        />
        </div>
  </div>
);

}
