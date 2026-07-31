export function bet_icon(odds_a, odds_b) {
    if (!odds_a || !odds_b) return "";

    if (odds_a === 'Game Started' || odds_b === 'Game Started') return "";

    if (odds_a > odds_b) return "🐶";
    return "🏆"
  }

export function money_icon(team, predicted_winner, place_bet) {

    if (team === predicted_winner && place_bet === true) return "💵";

    return ""
  }
