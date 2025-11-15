import { useState } from "react";

export default function Contribute() {
  const [direction, setDirection] = useState("co->fr");
  const [sourceText, setSourceText] = useState("");
  const [targetText, setTargetText] = useState("");
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitting(true);
    setError("");
    setSuccessMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/contribute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          direction,
          source_text: sourceText,
          target_text: targetText,
          notes: notes || null
        })
      });

      if (!response.ok) {
        throw new Error("La contribution a échoué");
      }

      await response.json();
      setSuccessMessage("Merci pour ta contribution ❤️");
      setSourceText("");
      setTargetText("");
      setNotes("");
    } catch (err) {
      console.error(err);
      setError("Envoi impossible, réessaie plus tard.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card">
      <h2>Contribuer à Maestra</h2>
      <p>
        Propose une phrase en corse ou en français, sa traduction, ou une correction. Tes
        contributions aident à entraîner l'IA.
      </p>
      <form className="form" onSubmit={handleSubmit}>
        <label className="form-label" htmlFor="direction">
          Direction
        </label>
        <select
          id="direction"
          className="form-select"
          value={direction}
          onChange={(event) => setDirection(event.target.value)}
        >
          <option value="co->fr">Corse → Français</option>
          <option value="fr->co">Français → Corse</option>
        </select>

        <label className="form-label" htmlFor="source-text">
          Texte original
        </label>
        <textarea
          id="source-text"
          className="form-textarea"
          placeholder="Texte original"
          value={sourceText}
          onChange={(event) => setSourceText(event.target.value)}
          rows={4}
          required
        />

        <label className="form-label" htmlFor="target-text">
          Traduction / Correction / Explication
        </label>
        <textarea
          id="target-text"
          className="form-textarea"
          placeholder="Traduction / Correction / Explication"
          value={targetText}
          onChange={(event) => setTargetText(event.target.value)}
          rows={4}
          required
        />

        <label className="form-label" htmlFor="notes">
          Contexte culturel, registre, région (optionnel)
        </label>
        <textarea
          id="notes"
          className="form-textarea"
          placeholder="Contexte culturel, registre (familier, poli...), région (Nord/Sud)..."
          value={notes}
          onChange={(event) => setNotes(event.target.value)}
          rows={3}
        />

        <button className="submit-button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Envoi en cours..." : "Envoyer"}
        </button>
      </form>
      {successMessage && <p className="answer-text">{successMessage}</p>}
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}
