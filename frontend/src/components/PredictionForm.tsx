import React, { useState } from 'react';
import { PredictionRequest } from '../types/prediction';

interface PredictionFormProps {
  onSubmit: (data: PredictionRequest) => void;
  isLoading?: boolean;
}

export const PredictionForm: React.FC<PredictionFormProps> = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState<PredictionRequest>({
    location: 'Whitefield',
    total_sqft: 1200,
    bath: 2,
    bhk: 2,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'location' ? value : Number(value),
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="prediction-form">
      <div>
        <label htmlFor="location">Location:</label>
        <input
          id="location"
          name="location"
          type="text"
          value={formData.location}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="total_sqft">Total Square Feet:</label>
        <input
          id="total_sqft"
          name="total_sqft"
          type="number"
          min="100"
          value={formData.total_sqft}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="bhk">BHK (Bedrooms):</label>
        <input
          id="bhk"
          name="bhk"
          type="number"
          min="1"
          max="20"
          value={formData.bhk}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label htmlFor="bath">Bathrooms:</label>
        <input
          id="bath"
          name="bath"
          type="number"
          min="1"
          max="20"
          value={formData.bath}
          onChange={handleChange}
          required
        />
      </div>

      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Estimating...' : 'Predict Price'}
      </button>
    </form>
  );
};
