export default function DiamondsEdgeResults({ mlb_games_prediction_results }) {

    const prediction_results = mlb_games_prediction_results?.[0];
    
    if (!prediction_results) {

    return <div>Loading...</div>;
    }

    return (
        <div>
            <div> Total Picks Made : {prediction_results.overall_picks} </div>
            <div> Total Correct Picks : {prediction_results.overall_correct_picks} </div>
            <div> Total Pick Accuracy : {prediction_results.overall_accuracy} % </div>
            <div> Total Bets Placed : {prediction_results.bets_placed} </div>
            <div> Total Correct Bets : {prediction_results.correct_bets_placed} </div>
            <div> Betting Accuracy : {prediction_results.betting_accuracy} % </div>
            <div> Total Underdog Picks : {prediction_results.underdog_picks} </div>
            <div> Total Correct Underdog Picks : {prediction_results.correct_underdog_picks} </div>
            <div> Underdog Accuracy : {prediction_results.underdog_accuracy} % </div>
            <div> Correct Picks Win Probabilty Under 50 % : {prediction_results.Win_Prob_Under_50} % </div>
            <div> Correct Picks Win Probabilty Between 50 - 55 % : {prediction_results.Win_Prob_50_55} % </div>
            <div> Correct Picks Win Probabilty Between 55 - 60 % : {prediction_results.Win_Prob_55_60} % </div>
            <div> Correct Picks Win Probabilty Between 60 - 65 % : {prediction_results.Win_Prob_60_65} % </div>
            <div> Correct Picks Win Probabilty Above 65 % : {prediction_results["Win_Prob_65+"]} % </div>
        </div>
);
}