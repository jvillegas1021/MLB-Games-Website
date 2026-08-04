import "./DiamondsEdgeResults.css";

export default function DiamondsEdgeResults({ mlb_games_prediction_results }) {

    const prediction_results = mlb_games_prediction_results?.[0];

    if (!prediction_results) {
        return <div>Loading...</div>;
    }

    return (
        <div>

            {/* Top Metrics */}
            <div className="stats-grid">

                <div className="stat-card">
                    <div className="stat-title">Overall Accuracy</div>
                    <div 
                        className="stat-value"
                        style={{color:
                            prediction_results.overall_accuracy < 50
                            ? "red"
                            : "green"
                        }}
                        >
                        {prediction_results.overall_accuracy} %
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">Betting Accuracy</div>
                    <div className="stat-value"
                        style={{color:
                            prediction_results.betting_accuracy < 50
                            ? "red"
                            : "green"
                        }}
                        >
                        {prediction_results.betting_accuracy}%
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-title">Underdog Accuracy</div>
                    <div className="stat-value"
                        style={{color:
                            prediction_results.underdog_accuracy < 50
                            ? "red"
                            : "green"
                        }}
                        >
                        {prediction_results.underdog_accuracy}%
                    </div>
                </div>

            </div>

        </div>
    );
}
