import React from 'react';
import { PredictionResponse } from '../types/prediction';

interface ResultPageProps {
  result?: PredictionResponse;
  onReset?: () => void;
}

export const ResultPage: React.FC<ResultPageProps> = ({ result, onReset }) => {
  if (!result) {
    return (
      <div className="result-page">
        <h2>No prediction results found.</h2>
        {onReset && <button onClick={onReset}>Go Back</button>}
      </div>
    );
  }

  return (
    <div className="result-page">
      <h2>Prediction Result Details</h2>
      <p><strong>Predicted Price:</strong> {result.predicted_price} {result.currency}</p>
      <div>
        <h3>Input Summary:</h3>
        <ul>
          <li>Location: {result.features_used.location}</li>
          <li>Total Sqft: {result.features_used.total_sqft}</li>
          <li>BHK: {result.features_used.bhk}</li>
          <li>Bathrooms: {result.features_used.bath}</li>
        </ul>
      </div>
      {onReset && <button onClick={onReset}>Make Another Prediction</button>}
    </div>
  );
};
