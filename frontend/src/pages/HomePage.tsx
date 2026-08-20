import React, { useState } from 'react';
import { PredictionForm } from '../components/PredictionForm';
import { getPricePrediction } from '../api/predictionClient';
import { PredictionRequest, PredictionResponse } from '../types/prediction';

export const HomePage: React.FC = () => {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async (data: PredictionRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getPricePrediction(data);
      setResult(response);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      <h1>House Price Prediction</h1>
      <p>Estimate the market value of your property</p>
      
      <PredictionForm onSubmit={handlePredict} isLoading={loading} />

      {error && <div className="error-message" style={{ color: 'red' }}>{error}</div>}

      {result && (
        <div className="prediction-result" style={{ marginTop: '20px', padding: '15px', border: '1px solid #ccc' }}>
          <h2>Estimated Price</h2>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            {result.predicted_price} {result.currency}
          </p>
        </div>
      )}
    </div>
  );
};
