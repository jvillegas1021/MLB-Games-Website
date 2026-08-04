import "./DiamondsEdgeResults.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";
export default function DiamondsEdgeResults({ mlb_games_prediction_results }) {

    const prediction_results = mlb_games_prediction_results?.[0];

    const winProbData = [
    {
        range: "<50%",
        accuracy: prediction_results.Win_Prob_Under_50
    },
    {
        range: "50-55%",
        accuracy: prediction_results.Win_Prob_50_55
    },
    {
        range: "55-60%",
        accuracy: prediction_results.Win_Prob_55_60
    },
    {
        range: "60-65%",
        accuracy: prediction_results.Win_Prob_60_65
    },
    {
        range: "65%+",
        accuracy: prediction_results["Win_Prob_65+"]
    }
    ];

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

                <div style={{ marginTop: "40px" }}>
                    <h2>Accuracy By Win Probability</h2>

                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={winProbData}>
                        <XAxis dataKey="range" />
                        <YAxis />
                        <Tooltip />
                        <Bar
                            dataKey="accuracy"
                            fill="#16a34a"
                        />
                        </BarChart>
                    </ResponsiveContainer>
                    </div>
                    ``
            </div>

        </div>
    );
}
