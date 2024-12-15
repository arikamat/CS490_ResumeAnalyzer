import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../../assets/global.css';
import './Dashboard.css';
import { generatePDF } from '../../util/generatePDF';
function Dashboard() {
  const [fitScore, setFitScore] = useState(0);
  const [matchedKeywords, setMatchedKeywords] = useState({});
  const [missingKeywords, setMissingKeywords] = useState({});
  const [improvementSuggestions, setImprovementSuggestions] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const jwtToken = localStorage.getItem('token');

  useEffect(() => {
    const fetchAnalysis = async () => {
      setLoading(true);
      setError('');

      try {
        const url = 'http://127.0.0.1:8000/api/analyze';
        const config = {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${jwtToken}`,
          },
        };

        const response = await axios.post(url, {}, config);

        if (response.status === 200) {
          const data = response.data;
          setFitScore(data.fit_score);
          setMatchedKeywords(data.matched_keywords || {});
          setMissingKeywords(data.feedback?.missing_keywords || {});
          setImprovementSuggestions(data.feedback?.suggestions || {});
        } else {
          setError('An error occurred while fetching resume analysis.');
        }
      } catch (err) {
        setError(
          err.response && err.response.data && err.response.data.detail
            ? err.response.data.detail
            : 'An error occurred during submission. Please reupload resume and job description.'
        );
      }

      setLoading(false);
    };

    fetchAnalysis();
  }, [jwtToken]);

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  const renderFilteredKeywords = (keywords) => {
    if (selectedCategory === 'all') return keywords;

    return {
      [selectedCategory]: keywords[selectedCategory] || [],
    };
  };

  const getTooltipText = (category) => {
    switch (category) {
      case 'skills':
        return 'Skills Suggestion: You need to develop your skills!';
      case 'education':
        return 'Education Suggestion: You need to undergo more education!';
      case 'experience':
        return 'Experience Suggestion: You need to gain more experience!';
      default:
        return '';
    }
  };

  return (
    <div className="dashboardContainer">
      <div className="dashboardTitle">Resume Analysis Dashboard</div>

      <div className="categoryFilter">
        <label htmlFor="filterSelect">Filter by:</label>
        <select id="filterSelect" onChange={handleCategoryChange} value={selectedCategory}>
          <option value="all">All</option>
          <option value="skills">Skills</option>
          <option value="experience">Experience</option>
          <option value="education">Education</option>
        </select>
      </div>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">{error}</div>}
      <button onClick={() => generatePDF(fitScore, matchedKeywords, missingKeywords, improvementSuggestions)}>
    Generate PDF
      </button>
      <div className="panelsContainer">
        <div className="panel">
          <h3>Fit Score</h3>
          <p>Your resume matches {fitScore.toFixed(2)}% of the job description.</p>
          <div className="progressBar">
            <div
              className="progressFill"
              style={{ width: `${fitScore}%` }}
            ></div>
          </div>
        </div>

        <div className="panel">
          <h3>Missing Keywords</h3>
          {Object.keys(renderFilteredKeywords(missingKeywords)).length > 0 ? (
            <ul>
              {Object.keys(renderFilteredKeywords(missingKeywords)).map((category) => (
                <li key={category}>
                  <strong>{category.charAt(0).toUpperCase() + category.slice(1)}: </strong>
                  {renderFilteredKeywords(missingKeywords)[category].join(', ')}
                </li>
              ))}
            </ul>
          ) : (
            <p>No missing keywords.</p>
          )}
        </div>

        <div className="panel">
          <h3>Matched Keywords</h3>
          {Object.keys(renderFilteredKeywords(matchedKeywords)).length > 0 ? (
            <ul>
              {Object.keys(renderFilteredKeywords(matchedKeywords)).map((category) => (
                <li key={category}>
                  <strong>{category.charAt(0).toUpperCase() + category.slice(1)}: </strong>
                  {renderFilteredKeywords(matchedKeywords)[category].join(', ')}
                </li>
              ))}
            </ul>
          ) : (
            <p>No matched keywords.</p>
          )}
        </div>

        <div className="panel">
          <h3>Improvement Suggestions</h3>
          {Object.keys(renderFilteredKeywords(improvementSuggestions)).length > 0 ? (
            Object.keys(renderFilteredKeywords(improvementSuggestions)).map((category) => (
              <div key={category}>
                <h4>{category.charAt(0).toUpperCase() + category.slice(1)}</h4>
                <ul>
                  {Object.keys(improvementSuggestions[category]).map((keyword, index) => (
                    <li
                      key={index}
                      title={getTooltipText(category)}
                    >
                      <strong>{keyword}: </strong>
                      {improvementSuggestions[category][keyword]}
                    </li>
                  ))}
                </ul>
              </div>
            ))
          ) : (
            <p>No suggestions available.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
