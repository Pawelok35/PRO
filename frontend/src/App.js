import React from 'react';
import PowerScoreSelector from './components/PowerScoreSelector';

function App() {
  return (
    <div className="App" style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '1rem' }}>
        In Stats We Trust – Power Score
      </h1>
      <PowerScoreSelector />
    </div>
  );
}

export default App;
