export function MirrorBar({ awayValue, homeValue, awayColor, homeColor }) {
  return (
    <div 
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        width: "100%",
        marginTop: "10px"
      }}
    >

      {/* AWAY BAR — extends left */}
      <div 
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-end",
          width: "45%"
        }}
      >
        <div 
          style={{
            height: "20px",
            width: `${awayValue * 2}px`,
            backgroundColor: awayColor,
            borderRadius: "4px"
          }}
        ></div>

        <span style={{ marginLeft: "10px", fontSize: "18px", fontWeight: 600 }}>
          {awayValue}
        </span>
      </div>

      {/* CENTER DIVIDER */}
      <div style={{ width: "10%", textAlign: "center", fontSize: "18px" }}>
        VS
      </div>

      {/* HOME BAR — extends right */}
      <div 
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-start",
          width: "45%"
        }}
      >
        <span style={{ marginRight: "10px", fontSize: "18px", fontWeight: 600 }}>
          {homeValue}
        </span>

        <div 
          style={{
            height: "20px",
            width: `${homeValue * 2}px`,
            backgroundColor: homeColor,
            borderRadius: "4px"
          }}
        ></div>
      </div>

    </div>
  );
}
