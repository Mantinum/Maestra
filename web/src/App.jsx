import { useState } from "react";
import Contribute from "./Contribute.jsx";

const MODES = [
  { value: "talk", label: "Discuter en corse" },
  { value: "translate", label: "Traduire" },
  { value: "correct", label: "Corriger le corse" },
  { value: "explain", label: "Expliquer une règle" }
];

const VIEWS = {
  CHAT: "chat",
  CONTRIBUTE: "contribute"
};

export default function App() {
  const [currentView, setCurrentView] = useState(VIEWS.CHAT);
  const [mode, setMode] = useState(MODES[0].value);
  const [inputText, setInputText] = useState("");
  const [answer, setAnswer] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError("");
    setAnswer("");

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ mode, input_text: inputText })
      });

      if (!response.ok) {
        throw new Error("La requête a échoué");
      }

      const data = await response.json();
      setAnswer(data.answer ?? "Réponse vide");
    } catch (err) {
      setError("Impossible de récupérer la réponse. Vérifiez l'API.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>A Maestra</h1>
        <p>Appli de démonstration pour discuter avec l'IA corse (simulée).</p>
        <nav className="nav-tabs">
          <button
            type="button"
            className={`tab-button${currentView === VIEWS.CHAT ? " active" : ""}`}
            onClick={() => setCurrentView(VIEWS.CHAT)}
          >
            Discuter
          </button>
          <button
            type="button"
            className={`tab-button${currentView === VIEWS.CONTRIBUTE ? " active" : ""}`}
            onClick={() => setCurrentView(VIEWS.CONTRIBUTE)}
          >
            Contribuer
          </button>
        </nav>
      </header>
      <main>
        {currentView === VIEWS.CHAT ? (
          <div className="card">
            <form onSubmit={handleSubmit} className="form">
              <label className="form-label" htmlFor="mode">
                Mode d'interaction
              </label>
              <select
                id="mode"
                className="form-select"
                value={mode}
                onChange={(event) => setMode(event.target.value)}
              >
                {MODES.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              <label className="form-label" htmlFor="input-text">
                Votre texte
              </label>
              <textarea
                id="input-text"
                className="form-textarea"
                placeholder="Saisissez votre texte ici..."
                value={inputText}
                onChange={(event) => setInputText(event.target.value)}
                rows={6}
                required
              />

              <button className="submit-button" type="submit" disabled={isLoading}>
                {isLoading ? "Génération en cours..." : "Envoyer"}
              </button>
            </form>

            <section className="response-section">
              <h2>Réponse</h2>
              {error && <p className="error-text">{error}</p>}
              {!error && answer && <p className="answer-text">{answer}</p>}
              {!error && !answer && !isLoading && (
                <p className="placeholder-text">Aucune réponse pour l'instant.</p>
              )}
            </section>
          </div>
        ) : (
          <Contribute />
        )}
      </main>
    </div>
  );
}
