import React from 'react';
import { HomePage } from './pages/HomePage';

export const App: React.FC = () => {
  return (
    <div className="app-container" style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <header>
        <nav>
          <h2>Real Estate AI</h2>
        </nav>
      </header>
      <main>
        <HomePage />
      </main>
    </div>
  );
};

export default App;
