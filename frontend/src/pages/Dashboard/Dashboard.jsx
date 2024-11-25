import React from 'react';
import '../../assets/global.css'; 
import './Dashboard.css';


//Generates dashboard based on fitscore, keywords, and suggestions
function Dashboard () {

  const fitScore = 50;
  const matchedKeywords = ["Strafing", "Aim", "Game sense"];

  const improvementSuggestions = [
    "Work on your util usage.",
    "Stop instalocking Reyna.",
    "Hit Aimlabs.",
    "Grind deathmatch."
  ];

  //Format of the page
  return (
    <div className="dashboardContainer">
      <div className="dashboardTitle">Resume Analysis Dashboard</div>

      <div className="panelsContainer">
        <div className="panel leftPanel">
          <div className="card">
            <h3 className="cardTitle">Resume Fit Score</h3>
            <div className="scoreText">
              <p>Your resume matches {fitScore}% of the job description.</p>
            </div>
            <div className="progressBar">
              <div className="progressFill" style={{ width: `${fitScore}%` }}></div>
            </div>
          </div>
          
          <div className="card">
            <h3 className="cardTitle">Skills and Keywords Matched</h3>
            <ul className="skillsList">
              {matchedKeywords.map((keyword, index) => (
                <li key={index}>{keyword}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="panel rightPanel">
          <div className="card">
            <h3 className="cardTitle">Improvement Suggestions</h3>
            <ul className="improvementsList">
              {improvementSuggestions.map((suggestion, index) => (
                <li key={index}>{suggestion}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
