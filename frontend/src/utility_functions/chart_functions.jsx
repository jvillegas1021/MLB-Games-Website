export function MirrorBar({ awayValue, homeValue, awayColor, homeColor, category }) {
  // Category‑specific scaling factors
  const scaleFactor = {
    Team_Total_Score: 2,
    Pitcher_Score: 10,
    Lineup_Score: 5,
    Bullpen_Score: 50,
    Batting_Split_Score: 100,
    Pitcher_vs_Lineup_Score: 100,
    Power_Score: 10,
    Team_Record_Score: 10,
    Home_Field_Score: 20,
  };

  // Apply scaling + minimum width threshold
  const awayWidth = Math.max(awayValue * (scaleFactor[category] || 10), 10);
  const homeWidth = Math.max(homeValue * (scaleFactor[category] || 10), 10);

  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%", marginTop: "10px" }}>
      {/* AWAY BAR */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-end", width: "45%" }}>
        <div style={{ height: "20px", width: `${awayWidth}px`, backgroundColor: awayColor, borderRadius: "4px" }}></div>
        <span style={{ marginLeft: "10px", fontSize: "18px", fontWeight: 600 }}>{awayValue}</span>
      </div>

      <div style={{ width: "10%", textAlign: "center", fontSize: "18px" }}>   vs   </div>

      {/* HOME BAR */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-start", width: "45%" }}>
        <span style={{ marginRight: "10px", fontSize: "18px", fontWeight: 600 }}>{homeValue}</span>
        <div style={{ height: "20px", width: `${homeWidth}px`, backgroundColor: homeColor, borderRadius: "4px" }}></div>
      </div>
    </div>
  );
}


export function ScoreBar({ homeValue, awayValue, homeColor, awayColor }) {

  const total = homeValue + awayValue;

  // Avoid division by zero
  const fillX = total === 0 ? 0.5 : awayValue / total;

  return (
    <div style={{
      width: "100%",
      height: "20px",
      position: "relative",
      border: "1px solid gray40",
      borderRadius: "4px",
      overflow: "hidden",
      marginTop: "10px"
    }}>
      {/* HOME SIDE */}
      <div style={{
        position: "absolute",
        left: 0,
        top: 0,
        bottom: 0,
        width: `${fillX * 100}%`,
        backgroundColor: awayColor
      }} />

      {/* AWAY SIDE */}
      <div style={{
        position: "absolute",
        left: `${fillX * 100}%`,
        top: 0,
        bottom: 0,
        width: `${(1 - fillX) * 100}%`,
        backgroundColor: homeColor
      }} />

      {/* Divider */}
      <div style={{
        position: "absolute",
        left: `${fillX * 100}%`,
        top: 0,
        bottom: 0,
        width: "2px",
        backgroundColor: "white"
      }} />
    </div>
  );
}
