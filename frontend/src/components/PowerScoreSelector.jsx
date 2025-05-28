// Frontend (React) - PowerScoreSelector.jsx
import React, { useState } from 'react';

const defaultWeights = {
  Points_avg: 27,
  xG_diff: 18,
  form_score: 13,
  dominance_ratio: 10,
  SoS_factor: 12,
  momentum: 10,
  efficiency_vs_opponent_tier: 10,
};

const componentLabels = {
  Points_avg: 'Średnia xPTS z 5 meczów',
  xG_diff: 'Różnica xG - xGA',
  form_score: 'Punkty z ostatnich 5 meczów',
  dominance_ratio: 'Procent zwycięstw 3+ bramkami',
  SoS_factor: 'Średnia siła przeciwników',
  momentum: 'Momentum (czy xPTS rośnie)',
  efficiency_vs_opponent_tier: 'Efektywność vs siła przeciwnika',
};

export default function PowerScoreSelector() {
  const [selected, setSelected] = useState(Object.keys(defaultWeights));
  const [weights, setWeights] = useState(defaultWeights);
  const [savedWeights, setSavedWeights] = useState(defaultWeights);
  const [warning, setWarning] = useState('');
  const [teamData, setTeamData] = useState(null);
  const [league, setLeague] = useState('premier_league');
  const [team, setTeam] = useState('');
  const [side, setSide] = useState('Home');
  const [round, setRound] = useState(15);
  const [resultData, setResultData] = useState(null);

  const getTotalWeight = () => {
    return selected.reduce((sum, key) => sum + (weights[key] || 0), 0);
  };

 const toggleComponent = (key) => {
  setSelected((prev) => {
    const updated = prev.includes(key)
      ? prev.filter((k) => k !== key)
      : [...prev, key];

    if (!prev.includes(key)) {
      // ✅ Checkbox ZAZNACZONY – przywróć poprzednią wagę jeśli możliwe
      const valueToRestore = savedWeights[key] || 0;
      setWeights((w) => {
        const totalWithout = selected.reduce((sum, k) => {
          if (k === key) return sum;
          return sum + (w[k] || 0);
        }, 0);

        const available = 100 - totalWithout;
        return {
          ...w,
          [key]: Math.min(valueToRestore, available),
        };
      });
    } else {
      // ✅ Checkbox ODHACZONY – zapisz wagę, ustaw 0
      setSavedWeights((sw) => ({ ...sw, [key]: weights[key] }));
      setWeights((w) => ({ ...w, [key]: 0 }));
    }

    return updated;
  });
};


  const handleWeightChange = (key, value) => {
    const newWeight = parseFloat(value);
    if (isNaN(newWeight) || newWeight < 0) return;

    const totalWithoutCurrent = getTotalWeight() - (weights[key] || 0);
    if (totalWithoutCurrent + newWeight > 100) {
      setWarning(
        `Nie możesz przypisać ${newWeight.toFixed(1)}%. Dostępna pula: ${(
          100 - totalWithoutCurrent
        ).toFixed(1)}%`
      );
      return;
    }

    setWarning('');
    setWeights((prev) => ({ ...prev, [key]: newWeight }));
  };

  const loadTeamData = async () => {
  // 🔁 Resetuj checkboxy i wagi do wartości domyślnych
  setSelected(Object.keys(defaultWeights));
  setWeights(defaultWeights);
  setSavedWeights(defaultWeights);
  setResultData(null); // Czyścimy poprzedni wynik

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/team_stats/${league}/${team}/${side}/${round}`
    );
    const data = await response.json();
    console.log('📡 Odpowiedź backendu:', data);
    setTeamData(data);
  } catch (error) {
    alert('Błąd pobierania danych drużyny.');
    console.error(error);
  }
};


  const handleSubmit = async () => {
    console.log('📦 Dane drużyny:', teamData);
    if (!teamData) {
      alert('Najpierw załaduj dane drużyny.');
      return;
    }

    const selectedWeights = {};
    selected.forEach((key) => {
      selectedWeights[key] = (weights[key] || 0) / 100;
    });

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/calculate_power_score',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            team_data: teamData,
            user_weights: selectedWeights,
          }),
        }
      );

      const result = await response.json();
      console.log('🎯 Wynik:', result);
      setResultData(result);
    } catch (error) {
      console.error('❌ Błąd połączenia z backendem:', error);
      alert('Nie udało się połączyć z backendem');
    }
  };

const redistributeRemainingWeight = () => {
  const total = getTotalWeight();
  const missing = 100 - total;
  if (missing <= 0) return;

  const selectedKeys = selected.filter((key) => weights[key] > 0);
  if (selectedKeys.length === 0) return;

  const updatedWeights = { ...weights };
  const sumCurrent = selectedKeys.reduce((sum, key) => sum + updatedWeights[key], 0);

  selectedKeys.forEach((key) => {
    const share = updatedWeights[key] / sumCurrent;
    updatedWeights[key] += share * missing;
  });

  setWeights(updatedWeights);
};





  return (
    <div className="p-4 rounded-xl bg-gray-900 text-white">
      <h2 className="text-xl mb-4">1️⃣ Wybierz drużynę i kolejkę</h2>
      <div className="mb-4 space-y-2">
        <select
          value={league}
          onChange={(e) => setLeague(e.target.value)}
          className="text-black px-2 py-1"
        >
          <option value="premier_league">Premier League</option>
          <option value="la_liga">La Liga</option>
          <option value="serie_a">Serie A</option>
          <option value="bundesliga">Bundesliga</option>
          <option value="ligue1">Ligue 1</option>
        </select>
        <input
          placeholder="Drużyna (np. Arsenal)"
          value={team}
          onChange={(e) => setTeam(e.target.value)}
          className="text-black px-2 py-1"
        />
        <select
          value={side}
          onChange={(e) => setSide(e.target.value)}
          className="text-black px-2 py-1"
        >
          <option value="Home">Home</option>
          <option value="Away">Away</option>
        </select>
        <input
          type="number"
          value={round}
          onChange={(e) => setRound(Number(e.target.value))}
          className="text-black px-2 py-1"
        />
        <button
          onClick={loadTeamData}
          className="bg-blue-500 px-3 py-1 rounded"
        >
          Załaduj dane
        </button>
      </div>

      <h2 className="text-xl mb-4">
        2️⃣ Wybierz składniki Power Score (łącznie 100%)
      </h2>
      {Object.keys(defaultWeights).map((key) => (
        <div key={key} className="mb-2 flex items-center">
          <input
            type="checkbox"
            checked={selected.includes(key)}
            onChange={() => toggleComponent(key)}
            className="mr-2"
          />
          <label className="w-64">{componentLabels[key]}</label>
          <input
            type="number"
            value={weights[key]}
            onChange={(e) => handleWeightChange(key, e.target.value)}
            step="1"
            min="0"
            max="100"
            className="ml-2 w-24 text-black"
          />
          <span className="ml-1">%</span>
        </div>
      ))}

      <p className="text-sm mt-2">
        💡 Dostępna pula wag:{' '}
        <strong>{(100 - getTotalWeight()).toFixed(1)}%</strong>
      </p>
      {warning && <p className="text-red-400 text-sm mt-1">{warning}</p>}

      <button
        onClick={redistributeRemainingWeight}
        className="mt-2 px-4 py-2 bg-yellow-600 rounded-xl"
      >
        🔁 Rozłóż wolną wagę automatycznie
      </button>


      <button
        onClick={handleSubmit}
        className="mt-4 px-4 py-2 bg-green-600 rounded-xl disabled:opacity-50"
        disabled={getTotalWeight() !== 100}
      >
        Oblicz Power Score
      </button>

      {resultData && (
        <div className="mt-6 p-4 rounded-xl bg-gray-800 text-white border border-green-400">
          <h3 className="text-lg font-bold mb-2">🔋 Wynik Power Score:</h3>
          <p className="text-xl mb-2">
            Wartość: <strong>{resultData.score}</strong>
          </p>
          <p className="mb-1">Rozkład wag:</p>
          <ul className="text-sm list-disc pl-5">
            {Object.entries(resultData.components).map(([key, val]) => (
              <li key={key}>
                {componentLabels[key] || key}: {val}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
